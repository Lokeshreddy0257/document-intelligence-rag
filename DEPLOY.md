# Deployment Instructions

## Push to GitHub

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in the details:
   - **Repository name**: `document-intelligence-rag`
   - **Description**: "Production-ready RAG system for intelligent document querying using LangChain, ChromaDB, and GPT-4"
   - **Visibility**: Public (recommended for portfolio)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
3. Click **"Create repository"**

### Step 2: Push Your Code

Run these commands in the project directory:

```bash
cd /Users/lokeshreddykona/Desktop/document-intelligence-rag

# Add remote repository
git remote add origin https://github.com/Lokeshreddy0257/document-intelligence-rag.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 3: Verify

After pushing, visit:
https://github.com/Lokeshreddy0257/document-intelligence-rag

You should see all your files including the README!

## Optional: Add Repository Topics

On GitHub, add these topics to make your project more discoverable:
- `rag`
- `langchain`
- `chromadb`
- `gpt-4`
- `fastapi`
- `streamlit`
- `document-intelligence`
- `semantic-search`
- `python`
- `machine-learning`

## Optional: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `Lokeshreddy0257/document-intelligence-rag`
5. Set main file: `app.py`
6. Add secrets (OpenAI API key) in Advanced settings
7. Click "Deploy"

Your app will be live at: `https://your-app-name.streamlit.app`

## Portfolio Link

✅ Your portfolio already has the correct GitHub link:
https://github.com/Lokeshreddy0257/document-intelligence-rag

The link will work once you push the repository to GitHub!
