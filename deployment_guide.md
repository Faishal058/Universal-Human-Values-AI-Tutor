# UHV AI Tutor Deployment Guide

This guide describes how to deploy the **Universal Human Values AI Tutor** to a free hosting platform. We recommend **Streamlit Community Cloud** or **Hugging Face Spaces**.

---

## Option 1: Streamlit Community Cloud (Recommended)

Streamlit Community Cloud is 100% free, integrates directly with GitHub, and automatically handles package installs from `requirements.txt`.

### Step 1: Upload Your Code to GitHub
1. Log in to your [GitHub account](https://github.com).
2. Create a new repository named `universal-human-values-ai-tutor` (make it Public or Private).
3. Open your terminal in the project directory (`c:\Users\faish\Downloads\Universal-Human-Values-AI-Tutor`) and run these commands to push the project:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of UHV AI Tutor Dashboard"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/universal-human-values-ai-tutor.git
   git push -u origin main
   ```
   *(Note: Replace `YOUR_USERNAME` with your actual GitHub username.)*

### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click the **"New app"** button.
3. Select your repository: `universal-human-values-ai-tutor`.
4. Set the **Main file path** to: `app.py`.
5. Click **"Deploy"**!

### Step 3: Add API Keys (Secrets)
Once the app starts deploying, you will see a settings console:
1. Click **Settings** -> **Secrets**.
2. Paste your environment keys (such as `GROQ_API_KEY`) so that the AI model can run securely:
   ```toml
   GROQ_API_KEY = "your-actual-groq-key"
   MONGO_URI = "mongodb://localhost:27017/"
   ```
3. Save the secrets. The app will automatically reload and be live at a public URL!

---

## Option 2: Hugging Face Spaces (Free)

Hugging Face Spaces is another excellent free hosting platform that supports Streamlit natively.

### Step 1: Create a Space
1. Log in to [Hugging Face](https://huggingface.co/).
2. Go to **Spaces** -> **Create new Space**.
3. Name your space (e.g. `uhv-ai-tutor`).
4. Select SDK: **Streamlit**.
5. Set Space hardware to **CPU Basic** (which is 100% free).
6. Set visibility to **Public** or **Private**.

### Step 2: Push Your Code
Hugging Face Spaces are git repositories. You can add the Hugging Face repository as a git remote and push directly:
```bash
git remote add hf https://huggingface.co/spaces/YOUR_HF_USERNAME/uhv-ai-tutor
git push -u hf main
```

### Step 3: Configure Secrets
1. In your Hugging Face Space page, go to the **Settings** tab.
2. Under **Variables and secrets**, click **New secret**.
3. Name: `GROQ_API_KEY`, Value: `your-actual-groq-key`.
4. The space will rebuild and run your app automatically!
