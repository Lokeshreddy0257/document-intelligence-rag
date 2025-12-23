# Quick Start Guide - Document Intelligence RAG System

## 🚀 Getting Started

### Step 1: Navigate to Project Directory
```bash
cd /Users/lokeshreddykona/Desktop/document-intelligence-rag
```

### Step 2: Set Up Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure API Key
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 4: Run the Application

**Option A: Streamlit UI (Recommended for Demo)**
```bash
streamlit run app.py
```
Then open http://localhost:8501 in your browser

**Option B: FastAPI Backend**
```bash
uvicorn api:app --reload
```
API available at http://localhost:8000

## 📤 Push to GitHub

### Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `document-intelligence-rag`
3. Description: "Production-ready RAG system for intelligent document querying"
4. Keep it Public (to showcase on portfolio)
5. Don't initialize with README (we already have one)
6. Click "Create repository"

### Step 2: Push Your Code
```bash
# Add remote origin (replace 'yourusername' with your GitHub username)
git remote add origin https://github.com/yourusername/document-intelligence-rag.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Update Portfolio Link
After pushing to GitHub, update the link in your portfolio:
- Open `/Users/lokeshreddykona/Desktop/portfolio-ai/index.html`
- Find line with: `href="https://github.com/lokeshreddy/document-intelligence-rag"`
- Replace `lokeshreddy` with your actual GitHub username

## 🎯 Testing the System

### Quick Test
1. Start the Streamlit app: `streamlit run app.py`
2. Upload a sample PDF (any PDF document)
3. Ask questions like:
   - "What is this document about?"
   - "Summarize the main points"
   - "What are the key findings?"

### Sample Test Documents
You can test with:
- Research papers
- Technical documentation
- Financial reports
- Any PDF with text content

## 📝 Next Steps

1. **Add Screenshots**: Take screenshots of the UI and add to README
2. **Create Demo Video**: Record a quick demo showing the system in action
3. **Add Tests**: Write unit tests in a `tests/` directory
4. **Deploy**: Consider deploying to Streamlit Cloud or AWS

## 🔧 Troubleshooting

**Issue: OpenAI API Error**
- Make sure your API key is correctly set in `.env`
- Check you have credits in your OpenAI account

**Issue: ChromaDB Error**
- Delete the `chroma_db/` folder and restart
- Make sure you have write permissions

**Issue: Import Errors**
- Make sure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

## 📊 Project Structure
```
document-intelligence-rag/
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── config.py             # Configuration settings
├── document_processor.py # PDF processing
├── vector_store.py       # ChromaDB integration
├── rag_chain.py          # RAG chain logic
├── rag_system.py         # Main orchestrator
├── api.py                # FastAPI backend
├── app.py                # Streamlit UI
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
└── LICENSE               # MIT License
```

## 🎓 Key Features to Highlight

When discussing this project in interviews:
1. **Production-Ready**: FastAPI backend, error handling, validation
2. **Scalable Architecture**: Modular design, vector database
3. **Modern Stack**: LangChain, GPT-4, ChromaDB
4. **Full-Stack**: Both API and UI implementations
5. **Best Practices**: Type hints, documentation, git workflow

---

Good luck with your project! 🚀
