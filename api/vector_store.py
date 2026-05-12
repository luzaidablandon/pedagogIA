import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def build_vector_store():
    # Usamos embeddings de Google para coherencia con el modelo Flash
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Carga de documentos del SENA
    data_path = "data/"
    documents = []
    for file in os.listdir(data_path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(data_path, file))
            documents.extend(loader.load())
            
    # Crear la base vectorial y guardarla localmente
    vector_db = FAISS.from_documents(documents, embeddings)
    vector_db.save_local("faiss_sena_index")
    return vector_db
