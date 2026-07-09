import os
import sys
from dotenv import load_dotenv

# Load env variables
load_dotenv()

from deepeval import evaluate
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from deepeval.models import DeepEvalBaseLLM

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Ensure API Key is present
groq_api_key = os.getenv("GROQ_API_KEY", "")
if not groq_api_key:
    print("Error: GROQ_API_KEY not found in environment. Please set it in .env first.")
    sys.exit(1)

# Define Custom LLM for DeepEval using Groq
class GroqDeepEvalLLM(DeepEvalBaseLLM):
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        self.model_name = model_name
        self.client = ChatGroq(
            model=self.model_name,
            temperature=0.0,
            groq_api_key=groq_api_key
        )

    def load_model(self):
        return self.client

    def generate(self, prompt: str) -> str:
        res = self.client.invoke(prompt)
        return res.content

    async def a_generate(self, prompt: str) -> str:
        res = await self.client.ainvoke(prompt)
        return res.content

    def get_model_name(self):
        return self.model_name

# Initialize evaluation model
eval_model = GroqDeepEvalLLM()

# Initialize original RAG pipeline resources
print("Loading vector database...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
if os.path.exists("faiss_index"):
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
else:
    print("FAISS index not found. Building it first...")
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    
    pdf_path = "Syllabus-Universal-Human-Values (1).pdf"
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found.")
        sys.exit(1)
        
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=120)
    chunks = text_splitter.split_documents(docs)
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local("faiss_index")

# Initialize Chat Model for the RAG chatbot
rag_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    groq_api_key=groq_api_key
)

def run_rag_query(query: str):
    """Executes the standard RAG pipeline to generate the response and return retrieval context."""
    retrieved = db.similarity_search(query, k=3)
    context_chunks = [doc.page_content for doc in retrieved]
    context_text = "\n\n".join(context_chunks)
    
    system_prompt = f"""You are a helpful academic AI tutor. Answer the student's question based strictly on the syllabus context below:
    
Syllabus Context:
{context_text}"""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])
    
    chain = prompt | rag_llm
    res = chain.invoke({"question": query})
    return res.content, context_chunks

# Test cases representing syllabus queries
evaluation_data = [
    {
        "query": "What are the course objectives of Universal Human Values?",
        "expected": "The course aims to help students see and value human values, self-exploration, and develop harmony within self, family, society, and nature."
    },
    {
        "query": "What is self-exploration according to the UHV syllabus?",
        "expected": "Self-exploration is a process of dialogue within oneself to find harmony, understand what is value and value-conflict, and verify human conduct."
    },
    {
        "query": "What is professional ethics in the context of the course?",
        "expected": "Professional ethics is the application of human values to engineering or professional practice, leading to harmony and ethical behavior."
    }
]

test_cases = []
for idx, data in enumerate(evaluation_data):
    print(f"\n[{idx+1}/{len(evaluation_data)}] Querying RAG for: '{data['query']}'")
    actual_output, context_chunks = run_rag_query(data["query"])
    
    test_case = LLMTestCase(
        input=data["query"],
        actual_output=actual_output,
        expected_output=data["expected"],
        retrieval_context=context_chunks
    )
    test_cases.append(test_case)

print("\nStarting DeepEval Metric Computations...")
faithfulness_metric = FaithfulnessMetric(threshold=0.6, model=eval_model)
relevancy_metric = AnswerRelevancyMetric(threshold=0.6, model=eval_model)

results = evaluate(
    test_cases=test_cases,
    metrics=[faithfulness_metric, relevancy_metric]
)
print("\nEvaluation Completed!")
for idx, test_case in enumerate(test_cases):
    print(f"\nTest Case {idx+1}:")
    print(f"  Input: {test_case.input}")
    print(f"  Actual Output: {test_case.actual_output}")
    print(f"  Faithfulness Score: {faithfulness_metric.score}")
    print(f"  Relevancy Score: {relevancy_metric.score}")
