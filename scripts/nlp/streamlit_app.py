import streamlit as st
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os
import pdfplumber

# Initialize the embedding model and ChromaDB
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection(name="leases")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ''.join(page.extract_text() for page in pdf.pages)
    return text

# Streamlit app
st.title("Lease Semantic Search")
st.sidebar.header("Upload a Lease or Query the Database")

# Tab 1: Upload a new lease
uploaded_file = st.sidebar.file_uploader("Upload a Lease PDF", type="pdf")
if uploaded_file:
    # Extract text
    text = extract_text_from_pdf(uploaded_file)
    
    # Chunk the text
    def chunk_text(text, max_length=500):
        sentences = text.split('. ')
        chunks = []
        chunk = ""
        for sentence in sentences:
            if len(chunk) + len(sentence) < max_length:
                chunk += sentence + ". "
            else:
                chunks.append(chunk.strip())
                chunk = sentence + ". "
        if chunk:
            chunks.append(chunk.strip())
        return chunks

    chunks = chunk_text(text)
    embeddings = model.encode(chunks, show_progress_bar=True)
    
    # Add to ChromaDB
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            metadatas=[{"source": uploaded_file.name}],
            ids=[f"{uploaded_file.name}-{i}"],
            embeddings=[embeddings[i]]
        )
    st.success(f"Lease '{uploaded_file.name}' has been successfully added to the database!")

# Tab 2: Query the database
query = st.text_input("Enter your query:", placeholder="e.g., What is the monthly rent?")
if query:
    query_embedding = model.encode(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5  # Number of results to show
    )
    
    st.header("Search Results")
    if results["documents"]:
        for document, metadata in zip(results["documents"][0], results["metadatas"][0]):
            st.write(f"**Source:** {metadata['source']}")
            st.write(f"**Text:** {document}")
            st.markdown("---")
    else:
        st.write("No results found.")

# add nyc leasing laws and see if any leases are in violation

