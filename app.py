import os
import json
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# -----------------------------------------------------------------------------
# Configuration & Theme
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="🤖 UHV AI Tutor Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling (Glassmorphism & Dark Slate Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Global scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(15, 18, 25, 0.5);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    /* Main Layout */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #121620 0%, #090c13 100%);
        color: #e6edf3;
    }
    
    /* Header Banner */
    .banner {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px 30px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    .title-text {
        background: linear-gradient(90deg, #ff7e5f 0%, #feb47b 30%, #86e3ce 70%, #d0e1fd 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 6s linear infinite;
        font-weight: 700;
        font-size: 2.6rem;
        margin-bottom: 5px;
    }
    
    @keyframes shine {
        to { background-position: 200% center; }
    }
    
    .subtitle-text {
        color: #98a2b3;
        font-size: 1.1rem;
        font-weight: 300;
        margin-top: 5px;
    }
    
    /* Headings */
    h1, h2, h3, h4 {
        color: #f0f6fc !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar glassmorphic container */
    [data-testid="stSidebar"] {
        background-color: #0b0e14 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Sidebar Titles styling */
    .sidebar-section-title {
        font-size: 0.9rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 10px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 5px;
    }
    
    /* Status Badge Container */
    .status-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 15px;
    }
    
    .badge {
        padding: 5px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.3px;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    
    .badge-connected {
        background: rgba(46, 204, 113, 0.1);
        color: #2ecc71;
        border: 1px solid rgba(46, 204, 113, 0.25);
    }
    
    .badge-fallback {
        background: rgba(241, 196, 15, 0.1);
        color: #f1c40f;
        border: 1px solid rgba(241, 196, 15, 0.25);
    }
    
    .badge-info {
        background: rgba(52, 152, 219, 0.1);
        color: #3498db;
        border: 1px solid rgba(52, 152, 219, 0.25);
    }
    
    /* Glassmorphic boxes & Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.2);
    }
    
    .syllabus-unit-title {
        color: #feb47b;
        font-weight: 600;
        margin-top: 10px;
        margin-bottom: 5px;
        font-size: 0.95rem;
    }
    
    /* Streamlit overrides for inputs & buttons */
    .stButton>button {
        border-radius: 8px !important;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%) !important;
        color: #f0f6fc !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        border-color: #ff7e5f !important;
        background: linear-gradient(135deg, rgba(255, 126, 95, 0.1) 0%, rgba(254, 180, 123, 0.05) 100%) !important;
        box-shadow: 0 0 15px rgba(255, 126, 95, 0.2) !important;
    }
    
    /* Reference block styling */
    .ref-box {
        background: rgba(255, 255, 255, 0.01) !important;
        border-left: 3px solid #86e3ce !important;
        padding: 12px;
        border-radius: 4px;
        font-size: 0.9rem;
        margin-bottom: 10px;
    }
    
    /* Customize native streamlit chat messages for premium feel */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-radius: 12px !important;
        margin-bottom: 12px !important;
        padding: 15px !important;
    }
    
    [data-testid="stChatMessage"][data-user="user"] {
        background-color: rgba(255, 126, 95, 0.05) !important;
        border: 1px solid rgba(255, 126, 95, 0.12) !important;
    }
    
    [data-testid="stChatMessage"][data-user="assistant"] {
        background-color: rgba(134, 227, 206, 0.03) !important;
        border: 1px solid rgba(134, 227, 206, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Static Structured Syllabus Data
# -----------------------------------------------------------------------------
UHV_COURSES = {
    "Semester III: Human Psychology": {
        "code": "BSH23MD19",
        "description": "Human Psychology: Realising Human Potential introduces students to core psychological processes aimed at understanding consciousness, motivation, and achieving complete human potential.",
        "objectives": [
            "Introduce basic concepts of psychology with an emphasis on realizing full human potential.",
            "Initiate and strengthen the process of self-exploration to build self and social awareness.",
            "Generate commitment to make effort to realize human potential and become responsible global citizens."
        ],
        "outcomes": [
            "Explain the basic concepts of psychology and historical efforts.",
            "Develop an understanding of the role of 'sanskar' in human conduct.",
            "Examine human psychology when governed by right understanding.",
            "Appraise proposed theories in psychology and formulate a path forward."
        ],
        "units": {
            "Unit I: Introduction to Human Psychology": [
                "Process of Inquiry into Human Psychology - Self-Exploration",
                "Human Being as an Existential Reality",
                "Role of Psychology in Day-to-Day Life"
            ],
            "Unit II: Understanding Consciousness (Self)": [
                "Bases of Human Behavior, Work, and Participation",
                "Sources of Motivation in the Self",
                "Role of Sanskar (Acceptance, Likes, Dislikes)",
                "Higher activities of the Self"
            ],
            "Unit III: Full Human Potential": [
                "State of Imagination & Possible Sources",
                "Consequences of Imagination",
                "Ensuring Harmony in the Self by way of Self-Exploration"
            ],
            "Unit IV: Concepts in Psychology": [
                "Theories in Psychology & Comparative Study of Concepts",
                "Personality Structure Theory by Sigmund Freud"
            ]
        },
        "prompts": [
            "What is the process of self-exploration in human psychology?",
            "Explain the role of Sanskar in human conduct.",
            "What are the higher activities of the Self?",
            "How does UHV compare with Freud's personality structure theory?"
        ]
    },
    "Semester IV: Madhyasth Darshan": {
        "code": "BSH24MD20",
        "description": "Human Values in Madhyasth Darshan explores the basic principles of existential realities, coexistence, human values, and the participation of human beings in nature.",
        "objectives": [
            "Understand the basic principles of Madhyasth Darshan.",
            "Understand existential realities, including human existence, through Madhyasth Darshan.",
            "See the participation of human beings in nature and leading an ethical life."
        ],
        "outcomes": [
            "Explain the basic concepts of Madhyasth Darshan.",
            "Understand human beings as inseparable components of the natural world.",
            "Interpret the human goal of realization in Madhyasth Darshan context.",
            "Apply virtues and values to real-life situations."
        ],
        "units": {
            "Unit I: Introduction & Basics": [
                "Need to study Madhyasth Darshan; Basic formulations",
                "Submergence of Nature in Space; Classification of Nature (Material/Consciousness)",
                "The Four Orders of Nature (Form, Property, Natural Characteristics, Self-Organisation)",
                "Process of Evolution in Nature or Existence"
            ],
            "Unit II: Human as a Component of Nature": [
                "Understanding humans as integral components of the natural world",
                "Classification of human beings; Integration of Self and Body",
                "Goals of realization and prosperity; Behavior and work for goal attainment"
            ],
            "Unit III: Goal of Realization": [
                "Realization as the ultimate aim of human existence",
                "Principles: Natural, Social, and Psychological principles",
                "Conducive society, social order, community, and self-study"
            ],
            "Unit IV: Human Conduct": [
                "Characteristics of realized self (Inner Peace, Harmony, Contentment)",
                "Continuity of happiness, peace, and satisfaction",
                "Ethical conduct, service mindset, and addressing present-day global problems"
            ]
        },
        "prompts": [
            "What are the four orders of nature in Madhyasth Darshan?",
            "Explain the concept of submergence of nature in space.",
            "What are the characteristics of a Realized Self?",
            "How can we solve environmental degradation using Madhyasth Darshan?"
        ]
    },
    "Semester V: Vision for Humane Society": {
        "code": "BSH25MD21",
        "description": "Vision for Humane Society focuses on relationships, feelings, and the transition toward an undivided society and universal human order.",
        "objectives": [
            "Understand values ensuring justice in human-human relationships.",
            "Develop the competence to analyze undivided society and universal human order.",
            "Examine the transition from current systems to a humane society."
        ],
        "outcomes": [
            "Construct conceptual framework for humane society based on relationship and harmony.",
            "Develop competence to work in teams based on relationship dimensions.",
            "Analyze feelings ensuring justice in human-human relationships.",
            "Formulate steps for establishing a universal human order."
        ],
        "units": {
            "Unit I: Introduction & Comprehensive Goal": [
                "Basic aspiration and comprehensive human goal",
                "Need for family and relationships; Human-rest of nature relationship",
                "Universal Human Order and appraisal of history and current state"
            ],
            "Unit II: Human-Human Relationships": [
                "Recognition of relationships and feelings (Trust, Respect, Gratitude, Love)",
                "Established vs Expressed Values; Mutual evaluation",
                "Justice in relationship leading to culture, civilization, and human conduct"
            ],
            "Unit III: Justice & Universal Order": [
                "Family order and continuity of culture/civilization",
                "Universal order on the basis of undivided society",
                "Expanse of order: family to world family"
            ],
            "Unit IV: Program for Universal Order": [
                "Education-Sanskar, Health-Self-regulation, Production-Work",
                "Exchange-Storage, Justice-Preservation"
            ],
            "Unit V: Human Tradition": [
                "Scope and steps of Universal Human Order",
                "Transitioning steps from the current state; Student participation"
            ]
        },
        "prompts": [
            "What is the difference between established values and expressed values?",
            "Explain justice in human-human relationships.",
            "What are the five dimensions of Universal Human Order?",
            "How can students participate in transitioning to a world family order?"
        ]
    },
    "Semester V Lab: Humane Society Lab": {
        "code": "BSH25MD22",
        "description": "Humane Society Lab translates UHV principles into practical skills through community building, roleplays, mindfulness, and workshops.",
        "objectives": [
            "Understand significance of UHV in promoting harmony and mutual respect.",
            "Cultivate self-awareness, emotional regulation, and mindfulness."
        ],
        "outcomes": [
            "Demonstrate self-awareness and accountability.",
            "Implement sustainable living practices for environmental harmony.",
            "Apply strategies for promoting inclusivity and equity."
        ],
        "units": {
            "Selected Lab Activities": [
                "Simulated interpersonal interactions & conflict resolution",
                "Group discussions on ethical dilemmas & Reflective journaling",
                "Nature immersion activities (conservation, tree planting)",
                "Workshops: gardening, composting, energy conservation",
                "Mindfulness sessions for self-regulation and stress management"
            ]
        },
        "prompts": [
            "What are the key activities in the Humane Society Lab?",
            "How does reflective journaling build self-awareness?",
            "What are the benefits of mindfulness meditation in UHV?"
        ]
    },
    "Semester VI: Human Economics": {
        "code": "BSH26MD23",
        "description": "Human Economics covers economic prosperity, sustainable generation/sharing of wealth, and an appraisal of modern capitalism/management systems.",
        "objectives": [
            "Introduce economic prosperity concepts for family and citizenship.",
            "Develop sensitivity to national economic issues and resolve contradictions.",
            "Equip with basic economic measures, tools, and analytical systems."
        ],
        "outcomes": [
            "Explain basic concepts of human economics.",
            "Choose sustainable and mutually fulfilling production systems.",
            "Analyze the role of economics in societal development."
        ],
        "units": {
            "Unit I: Introduction to Human Economics": [
                "Human Economics and its role in Universal Human Order",
                "Human Needs and their fulfillment; Three types of economics",
                "Role of economics in day-to-day life"
            ],
            "Unit II: Wealth Generation & Sharing": [
                "Meaning of Wealth vs Feeling of Prosperity",
                "Sustainable production, preservation, and right utilization of wealth",
                "Tools and techniques for production and management"
            ],
            "Unit III: Societal Development": [
                "Interdependence of societal orders; Contribution of wealth"
            ],
            "Unit IV: Economic Appraisal & Way Forward": [
                "Evaluation of modern notions (Needs, Resources, Wealth)",
                "Inherent contradictions and dilemmas in modern capitalism and management"
            ]
        },
        "prompts": [
            "What is the difference between Wealth and Prosperity?",
            "Explain the concept of cyclical, sustainable production in Human Economics.",
            "What are the three types of economics?",
            "What are the contradictions in modern management systems?"
        ]
    },
    "Semester VII: Holistic Vision of Life": {
        "code": "BSH27MD24",
        "description": "Holistic Vision of Life involves self-awareness project work, intercultural competence, global awareness, and environmental responsibility.",
        "objectives": [
            "Cultivate self-awareness by exploring beliefs, strengths, and values.",
            "Cultivate global awareness and intercultural competence.",
            "Instill environmental responsibility and sustainability."
        ],
        "outcomes": [
            "Demonstrate communication, active listening, and empathy.",
            "Understand connection between holistic well-being and overall living."
        ],
        "units": {
            "Core Project Focus": [
                "Exploring beliefs, values, strengths, weaknesses, and aspirations",
                "Intercultural competence & Global worldview analysis",
                "Interconnectedness of human society and nature (Sustainability projects)"
            ]
        },
        "prompts": [
            "What does a 'Holistic Vision of Life' represent?",
            "How does global awareness link to local values?",
            "Explain active listening and empathy as defined in this course."
        ]
    }
}

# Fallback quizzes in case the API Key/LLM JSON generation fails or key is missing
FALLBACK_QUIZZES = {
    "Semester III: Human Psychology": [
        {
            "question": "What is the primary method of inquiry into Human Psychology in the UHV course?",
            "options": ["A) Laboratory animal testing", "B) Self-Exploration on the basis of Natural Acceptance", "C) External psychiatric observation", "D) Rote memorization of terms"],
            "correct_answer": "B"
        },
        {
            "question": "What role does 'Sanskar' play in human conduct?",
            "options": ["A) It plays no active role in behavior", "B) It defines temporary sensory likes and dislikes only", "C) It represents the values, acceptances, and habits that govern conduct", "D) It is an external physical force"],
            "correct_answer": "C"
        },
        {
            "question": "Which of the following is considered an existential reality of a human being in UHV?",
            "options": ["A) The body is the only reality", "B) Human being is a co-existence of Self (I) and Body", "C) Self (I) is only an illusion of the brain", "D) The body is a tool owned by society"],
            "correct_answer": "B"
        }
    ],
    "Semester IV: Madhyasth Darshan": [
        {
            "question": "What are the four orders of nature in Madhyasth Darshan?",
            "options": ["A) Fire, Water, Air, Space", "B) Material, Plant, Animal, Human (Physical, Bio, Animal, Human)", "C) Solid, Liquid, Gas, Plasma", "D) Solar, Planetary, Ecological, Atmospheric"],
            "correct_answer": "B"
        },
        {
            "question": "What is 'submergence of nature in space' referring to?",
            "options": ["A) Natural resources are sinking into the ocean", "B) All units of nature are co-existing in space, which is all-pervading and self-organized", "C) Space is void and empty of value", "D) Space is pulling gravity from the Earth"],
            "correct_answer": "B"
        },
        {
            "question": "What characterizes the conduct of a realized human being in Madhyasth Darshan?",
            "options": ["A) Accumulation of maximum material assets", "B) Ethical conduct, inner peace, and service-oriented mindset", "C) Reclusiveness from the family", "D) Dominating other species"],
            "correct_answer": "B"
        }
    ],
    "Semester V: Vision for Humane Society": [
        {
            "question": "What is the ultimate expanse of Universal Human Order in UHV?",
            "options": ["A) From national sovereignty to global commerce alliances", "B) From family order to world family order", "C) From school classrooms to state boards", "D) Local self-governance structures only"],
            "correct_answer": "B"
        },
        {
            "question": "What does 'Justice' in human-human relationships mean?",
            "options": ["A) Strictly legal action inside a courtroom", "B) Recognition, fulfillment, and evaluation of feelings leading to mutual happiness", "C) Equalling of salaries across all jobs", "D) Forgiving all crimes instantly"],
            "correct_answer": "B"
        },
        {
            "question": "Which of the following represents a program for ensuring an Undivided Society?",
            "options": ["A) Increased border walls and surveillance", "B) Education-Sanskar, Health-Self-regulation, Production-Work", "C) Higher defense budgets", "D) Encouraging separate community laws"],
            "correct_answer": "B"
        }
    ],
    "Semester V Lab: Humane Society Lab": [
        {
            "question": "What is the primary objective of reflective journaling in the VFHS Lab?",
            "options": ["A) Practicing handwriting and calligraphy", "B) Reflecting on one's own behavior and its effects on relationships", "C) Correcting other students' answers", "D) Creating study summaries"],
            "correct_answer": "B"
        },
        {
            "question": "How do outdoor nature immersion activities contribute to course outcomes?",
            "options": ["A) Learning military marching coordinates", "B) Connecting with nature and understanding ecological harmony", "C) Learning land appraisal", "D) Developing basic outdoor survival skills"],
            "correct_answer": "B"
        }
    ],
    "Semester VI: Human Economics": [
        {
            "question": "What is the key difference between 'Prosperity' and 'Wealth' in UHV Human Economics?",
            "options": ["A) Wealth is feeling of having enough, prosperity is physical accumulation", "B) Wealth is physical assets; Prosperity is the feeling of having more than required physical facilities", "C) They are identical terms", "D) Wealth is public assets, prosperity is private savings"],
            "correct_answer": "B"
        },
        {
            "question": "Which system of production is advocated in Human Economics?",
            "options": ["A) Linear production with maximum output and high waste", "B) Eco-friendly, cyclical, and mutually fulfilling production systems", "C) Purely manual handcrafting without tools", "D) Exploitation of resources for national export dominance"],
            "correct_answer": "B"
        }
    ],
    "Semester VII: Holistic Vision of Life": [
        {
            "question": "What constitutes a 'Holistic Vision of Life'?",
            "options": ["A) Focusing solely on financial career gains", "B) Understanding the interconnectedness of self, family, society, and nature", "C) Complete denial of modern scientific practices", "D) Exercising daily to run marathons"],
            "correct_answer": "B"
        }
    ]
}

# -----------------------------------------------------------------------------
# Secrets & API Keys
# -----------------------------------------------------------------------------
groq_api_key_env = os.getenv("GROQ_API_KEY", "")
mongo_uri_env = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

# Sidebar Settings
st.sidebar.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=70)
st.sidebar.title("UHV Tutor Dashboard")

# App Mode Selector
st.sidebar.subheader("Navigation")
app_mode = st.sidebar.selectbox(
    "Choose Mode",
    ["💬 Study Chatbot", "✍️ Practice Quiz", "📚 Syllabus Overview"]
)

# API Keys Settings
st.sidebar.subheader("API Configuration")
groq_api_key = st.sidebar.text_input(
    "Groq API Key", 
    value=groq_api_key_env, 
    type="password", 
    help="Get a free API key from console.groq.com"
)

mongo_uri = st.sidebar.text_input(
    "MongoDB URI",
    value=mongo_uri_env,
    help="Connection string for your chat database"
)
session_id = st.sidebar.text_input("Session ID", value="uhv_default_session")

# Custom PDF Upload
st.sidebar.markdown("<p class='sidebar-section-title'>Custom Study Material</p>", unsafe_allow_html=True)
uploaded_pdf = st.sidebar.file_uploader("Upload custom PDF study guide:", type=["pdf"])

pdf_source = "Syllabus-Universal-Human-Values (1).pdf"
if uploaded_pdf is not None:
    pdf_source = "uploaded_study_material.pdf"
    try:
        with open(pdf_source, "wb") as f:
            f.write(uploaded_pdf.getbuffer())
        st.sidebar.success("Custom PDF loaded!")
    except Exception as e:
        st.sidebar.error(f"Failed to save custom PDF: {e}")

# Rebuild DB Cache Button
st.sidebar.markdown("<p class='sidebar-section-title'>System Maintenance</p>", unsafe_allow_html=True)
rebuild_db = st.sidebar.button("Rebuild Vector Store Cache", use_container_width=True)

# Connection & Validation variables
mongo_connected = False
mongo_history = None

# Connect to MongoDB
if mongo_uri:
    try:
        from pymongo import MongoClient
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=800)
        client.server_info()  # triggers exception if cannot connect
        
        from langchain_mongodb import MongoDBChatMessageHistory
        mongo_history = MongoDBChatMessageHistory(
            connection_string=mongo_uri,
            session_id=session_id,
            database_name="uhv_chat",
            collection_name="history"
        )
        mongo_connected = True
    except Exception:
        pass

# -----------------------------------------------------------------------------
# Vector Store (Knowledge Base) Setup
# -----------------------------------------------------------------------------
DB_PATH = "faiss_index"

@st.cache_resource
def load_or_create_vector_db(pdf_path, force_rebuild=False):
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Cache path: separate folder if it's the custom uploaded file to protect main syllabus
    db_cache_path = "faiss_index_custom" if "uploaded" in pdf_path else "faiss_index"
    
    if os.path.exists(db_cache_path) and not force_rebuild:
        try:
            return FAISS.load_local(db_cache_path, embeddings, allow_dangerous_deserialization=True)
        except Exception as e:
            st.warning(f"Failed to load existing index on disk: {e}. Rebuilding...")

    # Build DB
    if not os.path.exists(pdf_path):
        st.error(f"Target PDF file `{pdf_path}` was not found.")
        return None
        
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=120,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(docs)
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(DB_PATH)
    return db

# Trigger Vector DB Ingestion
if rebuild_db:
    st.cache_resource.clear()
    with st.spinner("Rebuilding Vector Store index from PDF. Please wait..."):
        db_temp = load_or_create_vector_db(pdf_source, force_rebuild=True)
        if db_temp:
            st.sidebar.success("Vector Store Rebuilt Successfully!")

# -----------------------------------------------------------------------------
# Session State Local Memory Initializer
# -----------------------------------------------------------------------------
if "local_history" not in st.session_state:
    st.session_state["local_history"] = []

if "chat_references" not in st.session_state:
    st.session_state["chat_references"] = {}  # Index mappings for sources

if "clicked_prompt" not in st.session_state:
    st.session_state["clicked_prompt"] = None

# Active course selected in interactive syllabus
if "selected_course" not in st.session_state:
    st.session_state["selected_course"] = "Semester III: Human Psychology"

# Session state for Quiz Mode
if "quiz_questions" not in st.session_state:
    st.session_state["quiz_questions"] = []
if "quiz_active" not in st.session_state:
    st.session_state["quiz_active"] = False
if "quiz_submitted" not in st.session_state:
    st.session_state["quiz_submitted"] = False
if "quiz_user_answers" not in st.session_state:
    st.session_state["quiz_user_answers"] = {}
if "quiz_evaluation" not in st.session_state:
    st.session_state["quiz_evaluation"] = ""
if "quiz_course_name" not in st.session_state:
    st.session_state["quiz_course_name"] = "Semester III: Human Psychology"

def get_chat_history():
    """Retrieve chat history based on the configured connection."""
    if mongo_connected and mongo_history:
        history = []
        for msg in mongo_history.messages:
            role = "user" if msg.type == "human" else "assistant"
            history.append({"role": role, "content": msg.content})
        return history
    else:
        return st.session_state["local_history"]

def save_chat_message(role, content, references=None):
    """Save message to the active history backend."""
    if mongo_connected and mongo_history:
        if role == "user":
            mongo_history.add_user_message(content)
        else:
            mongo_history.add_ai_message(content)
    else:
        st.session_state["local_history"].append({"role": role, "content": content})
    
    # Save references cache locally mapped to history indices
    if references:
        msg_idx = len(get_chat_history()) - 1
        st.session_state["chat_references"][msg_idx] = references

def clear_chat_history():
    """Clears history depending on memory backend."""
    if mongo_connected and mongo_history:
        mongo_history.clear()
    else:
        st.session_state["local_history"] = []
    st.session_state["chat_references"] = {}
    st.session_state["clicked_prompt"] = None

# Clear & Export Controls in Sidebar
st.sidebar.markdown("<p class='sidebar-section-title'>Session Controls</p>", unsafe_allow_html=True)
if st.sidebar.button("Clear Chat History", use_container_width=True):
    clear_chat_history()
    st.sidebar.success("Chat history cleared!")
    time.sleep(0.5)
    st.rerun()

# -----------------------------------------------------------------------------
# Export Transcript Utility
# -----------------------------------------------------------------------------
def get_markdown_transcript():
    messages = get_chat_history()
    if not messages:
        return "No chat history recorded yet."
    
    transcript = "# Universal Human Values (UHV) Study Chat Log\n"
    transcript += f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n"
    
    for idx, msg in enumerate(messages):
        role_label = "Student" if msg["role"] == "user" else "AI Tutor"
        transcript += f"### **{role_label}**:\n{msg['content']}\n\n"
        
        # Add references if available
        if msg["role"] == "assistant" and idx in st.session_state["chat_references"]:
            refs = st.session_state["chat_references"][idx]
            if refs:
                transcript += "> **Verified Syllabus Sources Cited:**\n"
                for r in refs:
                    transcript += f"> - *Page {r['page']}*: {r['content'].replace(chr(10), ' ')}\n"
                transcript += "\n"
        transcript += "---\n\n"
    return transcript

transcript_data = get_markdown_transcript()
st.sidebar.download_button(
    label="📥 Download Study Log",
    data=transcript_data,
    file_name=f"uhv_study_log_{session_id}.md",
    mime="text/markdown",
    use_container_width=True
)

# -----------------------------------------------------------------------------
# Main Header
# -----------------------------------------------------------------------------
st.markdown("""
<div class="banner">
    <div class="title-text">🤖 Universal Human Values AI Tutor</div>
    <div class="subtitle-text">Your intelligent RAG agent for course content, self-exploration, harmony, and professional ethics.</div>
</div>
""", unsafe_allow_html=True)

# Connection Badge display
status_html = '<div class="status-container">'
if mongo_connected:
    status_html += '<span class="badge badge-connected">● MongoDB Connected</span>'
else:
    status_html += '<span class="badge badge-fallback">▲ Local Memory (MongoDB Offline)</span>'

if groq_api_key:
    status_html += '<span class="badge badge-connected">● Groq API Active</span>'
else:
    status_html += '<span class="badge badge-fallback">▲ API Key Missing</span>'

status_html += f'<span class="badge badge-info">🎓 Mode: {app_mode}</span>'
status_html += '</div>'
st.markdown(status_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# VIEW 1: Study Chatbot
# -----------------------------------------------------------------------------
if app_mode == "💬 Study Chatbot":
    # Columns for Chat and dynamic Quick Suggestions
    chat_col, sidebar_col = st.columns([3, 1.2])
    
    with sidebar_col:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📚 Quick Guide")
        st.write("Browse a course topic in the dropdown below to show starter questions. Click a prompt card to send it instantly to your tutor!")
        
        # Course selector for suggestion cards
        selected_card_course = st.selectbox(
            "Select Course Area:",
            list(UHV_COURSES.keys()),
            index=list(UHV_COURSES.keys()).index(st.session_state["selected_course"])
        )
        st.session_state["selected_course"] = selected_card_course
        
        # Render suggestion questions as cards
        st.markdown("<p style='font-size: 0.95rem; font-weight: 600; color: #feb47b; margin-top: 15px;'>Starter Suggestions:</p>", unsafe_allow_html=True)
        course_prompts = UHV_COURSES[selected_card_course]["prompts"]
        
        for idx, prompt in enumerate(course_prompts):
            if st.button(prompt, key=f"sug_{idx}", use_container_width=True):
                st.session_state["clicked_prompt"] = prompt
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with chat_col:
        # Display Messages from History
        messages = get_chat_history()
        for idx, msg in enumerate(messages):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
                # Render verified RAG references if saved in state
                if msg["role"] == "assistant" and idx in st.session_state["chat_references"]:
                    refs = st.session_state["chat_references"][idx]
                    if refs:
                        with st.expander("📚 Verified References from Course Syllabus"):
                            for ref in refs:
                                st.markdown(f"<div class='ref-box'><strong>Source: Page {ref['page']}</strong><br/>{ref['content']}</div>", unsafe_allow_html=True)

        # Handle user query inputs
        query = st.chat_input("Ask about harmony, self-exploration, syllabus details...")
        user_query = None
        
        if st.session_state["clicked_prompt"]:
            user_query = st.session_state["clicked_prompt"]
            st.session_state["clicked_prompt"] = None  # reset
        elif query:
            user_query = query
            
        if user_query:
            # Display user message
            with st.chat_message("user"):
                st.markdown(user_query)
            save_chat_message("user", user_query)
            
            # API validations
            if not groq_api_key:
                with st.chat_message("assistant"):
                    st.markdown("⚠️ **API Key Missing**: Please enter your Groq API Key in the sidebar to generate responses.")
                st.stop()
                
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                
                # Retrieve relative context
                with st.spinner("Searching syllabus database..."):
                    db_instance = load_or_create_vector_db(pdf_source)
                    if db_instance is None:
                        st.markdown("❌ **Error**: The knowledge base is not loaded properly. Rebuild it from the sidebar.")
                        st.stop()
                    retrieved_docs = db_instance.similarity_search(user_query, k=4)
                    context_list = []
                    references_to_save = []
                    for doc in retrieved_docs:
                        page = doc.metadata.get('page', 'Unknown')
                        context_list.append(f"[Source: Page {page}] {doc.page_content}")
                        references_to_save.append({"page": page, "content": doc.page_content})
                        
                    context = "\n\n".join(context_list)
                
                # Formulate Chat History with token window limit
                msg_context = []
                system_prompt = f"""You are a helpful, professional, and empathetic AI Academic Assistant specializing in the "Universal Human Values" (UHV) course.
Your goal is to guide students in understanding harmony, self-exploration, ethics, and values based on the syllabus.

Instructions:
1. Answer the student's question based strictly on the retrieved syllabus context below.
2. If the answer cannot be found in the context, politely state that the syllabus does not mention this and offer to help with other UHV topics.
3. Keep your tone encouraging, clear, and educational.

Syllabus Context:
{context}"""
                
                msg_context.append(("system", system_prompt))
                
                # Limit history context to the last 6 messages
                for msg in messages[-6:]:
                    role = "human" if msg["role"] == "user" else "ai"
                    msg_context.append((role, msg["content"]))
                    
                msg_context.append(("human", user_query))
                
                try:
                    llm = ChatGroq(
                        model="llama-3.1-8b-instant",
                        temperature=0.3,
                        groq_api_key=groq_api_key
                    )
                    
                    chat_prompt = ChatPromptTemplate.from_messages(msg_context)
                    chain = chat_prompt | llm
                    
                    response_chunks = []
                    for chunk in chain.stream({}):
                        response_chunks.append(chunk.content)
                        response_placeholder.markdown("".join(response_chunks) + "▌")
                    
                    final_response = "".join(response_chunks)
                    response_placeholder.markdown(final_response)
                    
                    # Display references expander under response
                    if references_to_save:
                        with st.expander("📚 Verified References from Course Syllabus"):
                            for ref in references_to_save:
                                st.markdown(f"<div class='ref-box'><strong>Source: Page {ref['page']}</strong><br/>{ref['content']}</div>", unsafe_allow_html=True)
                    
                    # Save assistant response along with its references
                    save_chat_message("assistant", final_response, references=references_to_save)
                    
                except Exception as e:
                    st.error(f"Error during response generation: {e}")

# -----------------------------------------------------------------------------
# VIEW 2: Practice Quiz Mode
# -----------------------------------------------------------------------------
elif app_mode == "✍️ Practice Quiz":
    st.markdown("## ✍️ Interactive Practice Quiz")
    st.write("Test your knowledge of the UHV syllabus. Switch between courses to practice different modules.")
    
    # Quiz Settings Card
    if not st.session_state["quiz_active"]:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### Prepare Your Assessment")
        quiz_course = st.selectbox(
            "Select Course for Practice Quiz:",
            list(UHV_COURSES.keys()),
            index=list(UHV_COURSES.keys()).index(st.session_state["quiz_course_name"])
        )
        st.session_state["quiz_course_name"] = quiz_course
        
        generate_btn = st.button("🚀 Start Quiz Session", use_container_width=True)
        
        if generate_btn:
            st.session_state["quiz_questions"] = []
            st.session_state["quiz_user_answers"] = {}
            st.session_state["quiz_submitted"] = False
            st.session_state["quiz_evaluation"] = ""
            
            # Request Groq to generate challenging questions
            if groq_api_key:
                with st.spinner("Analyzing syllabus and generating custom questions..."):
                    course_info = UHV_COURSES[quiz_course]
                    syllabus_summary = f"Course: {quiz_course} ({course_info['code']})\n"
                    syllabus_summary += "Objectives:\n" + "\n".join([f"- {obj}" for obj in course_info["objectives"]]) + "\n"
                    syllabus_summary += "Units:\n"
                    for unit_name, topics in course_info["units"].items():
                        syllabus_summary += f"- {unit_name}:\n"
                        syllabus_summary += "\n".join([f"  * {topic}" for topic in topics]) + "\n"
                        
                    prompt = f"""You are a professor teaching the "Universal Human Values" (UHV) course.
Generate exactly 3 challenging multiple-choice questions testing key concepts of the course: {quiz_course}.
Base the questions on this syllabus context:
{syllabus_summary}

Format your response STRICTLY as a JSON array of objects. Do not write any markdown code blocks, intro, or explanations. Just output clean JSON.
Each object must have exactly these keys:
- "question": (string) The question text
- "options": (array of 4 strings) The options, starting with "A) ", "B) ", "C) ", "D) "
- "correct_answer": (string) Either "A", "B", "C", or "D"

Example JSON output format:
[
  {{
    "question": "What is the primary method of inquiry in UHV?",
    "options": ["A) Theoretical rules", "B) Self-exploration on basis of natural acceptance", "C) Scientific laboratory testing", "D) Social regulations"],
    "correct_answer": "B"
  }}
]"""
                    try:
                        llm = ChatGroq(
                            model="llama-3.1-8b-instant",
                            temperature=0.7,
                            groq_api_key=groq_api_key
                        )
                        response = llm.invoke(prompt)
                        content = response.content.strip()
                        
                        # Clean JSON codeblock wrapper if present
                        if content.startswith("```"):
                            lines = content.split("\n")
                            if lines[0].startswith("```"):
                                lines = lines[1:]
                            if lines[-1].startswith("```"):
                                lines = lines[:-1]
                            content = "\n".join(lines).strip()
                            
                        st.session_state["quiz_questions"] = json.loads(content)
                        st.session_state["quiz_active"] = True
                        st.toast("Quiz loaded successfully from LLM!", icon="✅")
                    except Exception as e:
                        # Fallback to local quizzes
                        st.session_state["quiz_questions"] = FALLBACK_QUIZZES.get(quiz_course, FALLBACK_QUIZZES["Semester III: Human Psychology"])
                        st.session_state["quiz_active"] = True
                        st.toast("Using local pre-compiled syllabus quiz (LLM connection offline)", icon="ℹ️")
            else:
                # Load fallback quiz
                st.session_state["quiz_questions"] = FALLBACK_QUIZZES.get(quiz_course, FALLBACK_QUIZZES["Semester III: Human Psychology"])
                st.session_state["quiz_active"] = True
                st.toast("Using local pre-compiled syllabus quiz (No Groq API Key entered)", icon="ℹ️")
            
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        st.markdown(f"### 📑 {st.session_state['quiz_course_name']} Quiz")
        st.write("Answer the questions below to evaluate your understanding of UHV guidelines.")
        
        # Display each question
        user_answers = {}
        for idx, q in enumerate(st.session_state["quiz_questions"]):
            st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown(f"**Q{idx+1}:** {q['question']}")
            
            # Map choice index
            current_choice = q["options"][0]
            if st.session_state["quiz_submitted"]:
                saved_ans = st.session_state["quiz_user_answers"].get(idx, "A")
                # find option index matching saved choice character
                op_index = 0
                for o_idx, opt in enumerate(q["options"]):
                    if opt.startswith(saved_ans):
                        op_index = o_idx
                        break
                selected_option = st.radio(
                    f"Select answer for Q{idx+1}:",
                    q["options"],
                    index=op_index,
                    key=f"quiz_radio_{idx}",
                    disabled=True
                )
            else:
                selected_option = st.radio(
                    f"Select answer for Q{idx+1}:",
                    q["options"],
                    index=0,
                    key=f"quiz_radio_{idx}"
                )
                # Store selection (character)
                user_answers[idx] = selected_option[0] if selected_option else "A"
            st.markdown("</div>", unsafe_allow_html=True)

        if not st.session_state["quiz_submitted"]:
            if st.button("Submit My Answers", use_container_width=True):
                st.session_state["quiz_user_answers"] = user_answers
                st.session_state["quiz_submitted"] = True
                
                # Ask LLM for a report card explanation if key is available
                if groq_api_key:
                    with st.spinner("Generating custom explanation report card..."):
                        report_prompt = f"""You are an encouraging academic tutor evaluating a student's answers for a 3-question quiz in: {st.session_state['quiz_course_name']}.
Here is the quiz JSON:
{json.dumps(st.session_state['quiz_questions'])}

The student's submitted answers are:
{json.dumps(user_answers)} (Keys represent question index 0, 1, 2. Value represents student answer option character A, B, C, or D).

Write a short, highly encouraging, and empathetic evaluation report card (max 200 words).
1. Compare each answer to the correct answer.
2. Provide a single-sentence explanation of why the correct answer is right and what the student should study next.
Keep the style supportive, aligned with the values of harmony, respect, and self-exploration in UHV."""
                        try:
                            llm = ChatGroq(
                                model="llama-3.1-8b-instant",
                                temperature=0.5,
                                groq_api_key=groq_api_key
                            )
                            response = llm.invoke(report_prompt)
                            st.session_state["quiz_evaluation"] = response.content
                        except Exception:
                            st.session_state["quiz_evaluation"] = "Unable to generate dynamic evaluation report card. Refer to details below."
                st.rerun()
        else:
            # Score card & explanations
            correct_count = 0
            for idx, q in enumerate(st.session_state["quiz_questions"]):
                user_ans = st.session_state["quiz_user_answers"].get(idx, "A")
                if user_ans == q["correct_answer"]:
                    correct_count += 1
            
            # Show score
            score_color = "#2ecc71" if correct_count == len(st.session_state["quiz_questions"]) else "#f1c40f" if correct_count > 0 else "#e74c3c"
            st.markdown(f"""
            <div class='glass-card' style='text-align: center; border-color: {score_color};'>
                <h3 style='margin: 0;'>Your Score: <span style='color: {score_color}; font-size: 2.2rem;'>{correct_count} / {len(st.session_state['quiz_questions'])}</span></h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Show LLM evaluation if available
            if st.session_state["quiz_evaluation"]:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 🎓 Tutor Evaluation & Tips")
                st.write(st.session_state["quiz_evaluation"])
                st.markdown("</div>", unsafe_allow_html=True)
                
            # Detail display
            for idx, q in enumerate(st.session_state["quiz_questions"]):
                user_ans = st.session_state["quiz_user_answers"].get(idx, "A")
                corr_ans = q["correct_answer"]
                is_correct = user_ans == corr_ans
                
                with st.expander(f"Review Question {idx+1}: {'✅ Correct' if is_correct else '❌ Incorrect'}"):
                    st.markdown(f"**Question:** {q['question']}")
                    st.write(f"Your answer: **{user_ans}**")
                    st.write(f"Correct answer: **{corr_ans}**")
                    
                    # Find correct option string
                    opt_str = ""
                    for opt in q["options"]:
                        if opt.startswith(corr_ans):
                            opt_str = opt
                            break
                    st.info(f"Correct Option Detail: {opt_str}")
                    
            if st.button("🔄 Try Another Quiz", use_container_width=True):
                st.session_state["quiz_active"] = False
                st.session_state["quiz_submitted"] = False
                st.session_state["quiz_questions"] = []
                st.session_state["quiz_user_answers"] = {}
                st.session_state["quiz_evaluation"] = ""
                st.rerun()

# -----------------------------------------------------------------------------
# VIEW 3: Syllabus Overview
# -----------------------------------------------------------------------------
elif app_mode == "📚 Syllabus Overview":
    st.markdown("## 📚 Course Curriculum & Modules")
    st.write("Browse details of the Universal Human Values (UHV) Multi-Disciplinary Minor, including units, learning outcomes, and objectives.")
    
    # Render all courses in tabs
    tabs = st.tabs(list(UHV_COURSES.keys()))
    
    for idx, (course_name, data) in enumerate(UHV_COURSES.items()):
        with tabs[idx]:
            st.markdown(f"### {course_name} (`{data['code']}`)")
            st.markdown(f"*{data['description']}*")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### 🎯 Course Objectives")
                for obj in data["objectives"]:
                    st.markdown(f"- {obj}")
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### 🎓 Learning Outcomes")
                for out in data["outcomes"]:
                    st.markdown(f"- {out}")
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col2:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### 📑 Syllabus Units")
                for unit_title, topics in data["units"].items():
                    st.markdown(f"<p class='syllabus-unit-title'>{unit_title}</p>", unsafe_allow_html=True)
                    for topic in topics:
                        st.markdown(f"- {topic}")
                st.markdown("</div>", unsafe_allow_html=True)
