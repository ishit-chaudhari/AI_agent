from google.adk.agents import Agent
import pypdf
import os

# Hardcoded paths as requested
PDF_PATHS = [
    "FILE_ACTUAL_LOCATION"
]

def load_pdfs():
    """Loads text from the hardcoded PDF paths."""
    data = {}
    for path in PDF_PATHS:
        if os.path.exists(path):
            try:
                reader = pypdf.PdfReader(path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                data[os.path.basename(path)] = text
            except Exception as e:
                print(f"Error reading {path}: {e}")
        else:
            print(f"Warning: File not found: {path}")
    return data

# Load data once when module is imported
PDF_DATA = load_pdfs()

def search_knowledge_base(query: str):
    """
    Searches the internal PDF knowledge base for the query.
    Returns relevant snippets from the documents.
    """
    results = []
    query_lower = query.lower()
    
    for filename, text in PDF_DATA.items():
        if query_lower in text.lower():
            text_lower = text.lower()
            start_idx = 0
            # Limit to first few matches per file to avoid context overflow
            count = 0
            while count < 3:
                idx = text_lower.find(query_lower, start_idx)
                if idx == -1:
                    break
                
                # Extract context (300 chars before and after)
                context_start = max(0, idx - 300)
                context_end = min(len(text), idx + len(query) + 300)
                snippet = text[context_start:context_end].replace('\n', ' ')
                results.append(f"Source: {filename}\nContext: ...{snippet}...\n")
                
                start_idx = idx + len(query)
                count += 1
                
    if not results:
        return "No relevant information found in the provided documents."
        
    return "\n".join(results)

root_agent = Agent(
    name="pdf_knowledge_agent",
    model="gemini-2.0-flash",
    description="Answers questions based strictly on specific PDF documents.",
    instruction="You are a helpful assistant. You answer questions and summarize ONLY using the information found in the provided PDF documents. Use the 'search_knowledge_base' tool to find information. If the information is not in the context, say you don't know.",
    tools=[search_knowledge_base],
)
