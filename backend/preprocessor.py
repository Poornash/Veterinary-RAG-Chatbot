import os
import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader
)
from langchain_community.embeddings import HuggingFaceEmbeddings

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
VECTOR_DIR = os.path.join(BASE_DIR, "vectorstore")


# ---------------------------------------------------------
# LOAD DOCUMENTS FROM /data/
# ---------------------------------------------------------
def load_documents():
    docs = []

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    for file in os.listdir(DATA_DIR):
        fpath = os.path.join(DATA_DIR, file)

        if file.endswith(".pdf"):
            loader = PyPDFLoader(fpath)
            docs.extend(loader.load())

        elif file.endswith(".txt") or file.endswith(".md"):
            loader = TextLoader(fpath, encoding="utf-8")
            docs.extend(loader.load())

        elif file.endswith(".csv"):
            df = pd.read_csv(fpath)
            text = df.to_string()
            docs.append({"page_content": text, "metadata": {"source": file}})

    return docs


# ---------------------------------------------------------
# CHUNKING LOGIC
# ---------------------------------------------------------
def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    return splitter.split_documents(docs)


# ---------------------------------------------------------
# CREATE EMBEDDINGS MODEL (LOCAL)
# ---------------------------------------------------------
def get_embedding_model():
    print("🔍 Loading MiniLM embeddings (local)...")
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


# ---------------------------------------------------------
# BUILD VECTOR STORE (CHROMA)
# ---------------------------------------------------------
def build_vectorstore():
    print("📚 Loading documents...")
    docs = load_documents()

    if len(docs) == 0:
        print("⚠ No documents found in /data/ folder.")
        return None

    print(f"📄 Loaded {len(docs)} documents.")

    print("✂️ Chunking documents...")
    chunks = chunk_documents(docs)

    print(f"🧩 Created {len(chunks)} chunks.")

    embeddings = get_embedding_model()

    print("🧠 Creating Chroma Vector DB...")
    vectordb = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DIR
    )

    vectordb.persist()
    print("✅ Vector DB created & saved!")

    return vectordb


# ---------------------------------------------------------
# LOAD EXISTING VECTOR DB
# ---------------------------------------------------------
def load_vectorstore():
    if not os.path.exists(VECTOR_DIR):
        print("⚠ Vectorstore not found. Building new one...")
        return build_vectorstore()

    print("🔄 Loading existing vector DB...")
    embeddings = get_embedding_model()

    vectordb = Chroma(
        persist_directory=VECTOR_DIR,
        embedding_function=embeddings
    )

    print("✅ Vectorstore loaded!")
    return vectordb
