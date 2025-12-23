# 📊 Standalone Visualizations Guide

## Overview

Your RAG system now supports **standalone visualizations** that can be opened independently, without running the Streamlit UI!

## 🎯 Three Ways to View Visualizations

### 1. **Standalone HTML Dashboard** (Recommended)

Generate interactive HTML dashboards that open in your browser:

```python
from rag_system import DocumentRAG
from dashboard_generator import create_dashboard

# Initialize system
rag = DocumentRAG()

# Upload some documents
rag.upload_document("document.pdf")

# Create and auto-open dashboard
dashboard_path = create_dashboard(rag)
```

**Features**:
- ✅ Opens automatically in your default browser
- ✅ Fully interactive Plotly charts
- ✅ No server required - just an HTML file
- ✅ Can be shared with others
- ✅ Saved in `dashboards/` folder

### 2. **Jupyter Notebook** (Interactive)

Run the analytics notebook for interactive exploration:

```bash
# Start Jupyter
jupyter notebook analytics_notebook.ipynb
```

**Features**:
- ✅ Interactive code cells
- ✅ Live visualizations
- ✅ Experiment with queries
- ✅ Custom analysis
- ✅ Export charts as images

### 3. **Simple Metrics Page**

Generate a clean metrics overview:

```python
from dashboard_generator import DashboardGenerator
from rag_system import DocumentRAG

rag = DocumentRAG()
generator = DashboardGenerator(rag)

# Create metrics card
metrics_path = generator.generate_metrics_card()
print(f"Metrics page: {metrics_path}")
```

## 🚀 Quick Start

### Option A: Python Script

Create a file `generate_dashboard.py`:

```python
from rag_system import DocumentRAG
from dashboard_generator import create_dashboard

# Initialize
rag = DocumentRAG()

# Upload your documents
rag.upload_document("doc1.pdf")
rag.upload_document("doc2.pdf")

# Ask some questions (optional)
chat_history = []
result = rag.query("What is this about?")
if result['status'] == 'success':
    chat_history.append({
        'question': result['question'],
        'answer': result['answer'],
        'sources': result['sources'],
        'time': 1.5
    })

# Generate dashboard
dashboard_path = create_dashboard(rag, chat_history)
print(f"Dashboard opened: {dashboard_path}")
```

Run it:
```bash
python generate_dashboard.py
```

### Option B: Jupyter Notebook

```bash
# Install Jupyter (if not already installed)
pip install jupyter notebook

# Start notebook
jupyter notebook analytics_notebook.ipynb

# Run the cells to generate visualizations
```

## 📁 Output Files

All standalone visualizations are saved in the `dashboards/` folder:

```
document-intelligence-rag/
├── dashboards/
│   ├── rag_dashboard_20231223_140530.html
│   ├── rag_dashboard_20231223_141205.html
│   └── metrics_20231223_140530.html
```

Each file is timestamped and can be:
- Opened in any browser
- Shared via email
- Embedded in presentations
- Archived for later review

## 🎨 Dashboard Features

### Full Dashboard Includes:
1. **Document Distribution** (Pie Chart)
2. **Query Performance** (Bar Chart)
3. **Query Timeline** (Line Chart)
4. **Response Time Distribution** (Histogram)
5. **Source Usage** (Horizontal Bar Chart)
6. **System Metrics** (Gauge)

### Metrics Card Includes:
- Total documents count
- Total chunks indexed
- Average chunks per document
- List of uploaded documents

## 💡 Use Cases

### For Presentations
```python
# Generate dashboard before your demo
dashboard_path = create_dashboard(rag, chat_history)
# Open the HTML file during your presentation
```

### For Reports
```python
# Generate dashboard
dashboard_path = create_dashboard(rag)
# Attach the HTML file to your report
```

### For Analysis
```python
# Use Jupyter notebook for interactive exploration
# jupyter notebook analytics_notebook.ipynb
```

## 🔧 Customization

### Custom Dashboard

```python
from dashboard_generator import DashboardGenerator

generator = DashboardGenerator(rag)

# Generate with custom chat history
custom_history = [
    {
        'question': 'What is AI?',
        'answer': 'Artificial Intelligence...',
        'sources': [...],
        'time': 1.2
    }
]

dashboard_path = generator.generate_full_dashboard(custom_history)
```

### Export Individual Charts

```python
import plotly.express as px

# Create custom chart
docs = rag.get_uploaded_documents()
df = pd.DataFrame(docs)

fig = px.bar(df, x='filename', y='chunks')
fig.write_html('my_custom_chart.html')
```

## 📊 Chart Types Available

- **Pie Charts**: Document distribution
- **Bar Charts**: Performance metrics
- **Line Charts**: Trends over time
- **Histograms**: Distribution analysis
- **Gauges**: Performance indicators
- **Scatter Plots**: Correlation analysis

## 🎯 Benefits of Standalone Dashboards

✅ **No Server Required**: Just open the HTML file  
✅ **Portable**: Share via email or cloud storage  
✅ **Interactive**: Full Plotly interactivity  
✅ **Offline**: Works without internet  
✅ **Archivable**: Keep historical snapshots  
✅ **Embeddable**: Use in presentations or reports  

## 📝 Example Workflow

```bash
# 1. Upload documents
python -c "from rag_system import DocumentRAG; rag = DocumentRAG(); rag.upload_document('doc.pdf')"

# 2. Generate dashboard
python -c "from dashboard_generator import create_dashboard; from rag_system import DocumentRAG; create_dashboard(DocumentRAG())"

# 3. Dashboard opens automatically in browser!
```

## 🚀 Next Steps

1. Try generating a dashboard with your documents
2. Explore the Jupyter notebook for interactive analysis
3. Customize the dashboard generator for your needs
4. Share dashboards with your team

---

**Tip**: Dashboards are perfect for demos, reports, and presentations!
