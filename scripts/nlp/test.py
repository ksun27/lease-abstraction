import json
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import pdfplumber
from tqdm import tqdm

def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + ' '  
    return text

path = 'leases/cleaned/'
pdf_files = ['0.pdf', '1.pdf', '2.pdf', '3.pdf', '4.pdf', '5.pdf', '6.pdf', '7.pdf', '8.pdf', '9.pdf'] 
texts = [extract_text_from_pdf(pdf) for pdf in tqdm(pdf_files)]
print(texts)

model = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_text(text, max_length=500):
    """Chunk text into smaller parts with a maximum length."""
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

# Chunk and embed all documents
all_chunks = []
for text in texts:
    all_chunks.extend(chunk_text(text))

# Generate embeddings for all chunks
embeddings = model.encode(all_chunks, show_progress_bar=True)

client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="db"))
collection = client.get_or_create_collection(name="leases")

for i, chunk in enumerate(all_chunks):
    collection.add(
        documents=[chunk],
        metadatas=[{"source": f"Document {i // len(all_chunks)}"}],
        ids=[str(i)],
        embeddings=[embeddings[i]]
    )

client.persist()

query = "What is the monthly rent and lease term?"
query_embedding = model.encode(query)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5  # Adjust for the number of matches you want
)

for document, metadata in zip(results['documents'][0], results['metadatas'][0]):
    print(f"Text: {document}\nSource: {metadata['source']}\n")
