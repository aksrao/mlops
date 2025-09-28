import os
from dotenv import load_dotenv
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import Document

load_dotenv()
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_KEY:
    raise ValueError("Set GEMINI_API_KEY in .env")

PDF_DIR = Path("12th_Class_chemistry")
PERSIST_DIR = "chroma_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
COLLECTION_NAME = "chemistry_12th"

def load_pdfs(pdf_dir: Path):
    docs = []
    pdfs = sorted(pdf_dir.glob("*.pdf"))
    if not pdfs:
        return docs
    pdf = pdfs[0]  
    loader = PyPDFLoader(str(pdf))
    pages = loader.load_and_split()
    for i, d in enumerate(pages):
        d.metadata["source"] = str(pdf.name)
        d.metadata["page"] = i + 1
    docs.extend(pages)
    return docs
def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    texts = []
    metadatas = []
    for d in docs:
        chunks = splitter.split_text(d.page_content)
        for c in chunks:
            texts.append(c)
            metadatas.append(d.metadata)
    return texts, metadatas
def build_vectorstore(texts, metadatas):
    os.environ["GOOGLE_API_KEY"] = GEMINI_KEY  
    embed = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectordb = Chroma.from_texts(texts, embedding=embed, metadatas=metadatas,
                                collection_name=COLLECTION_NAME, persist_directory=PERSIST_DIR)
    vectordb.persist()
    return vectordb
def make_qa_chain(vectordb):
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    chat = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    qa = RetrievalQA.from_chain_type(llm=chat, chain_type="stuff", retriever=retriever, return_source_documents=True)
    return qa

def main():
    print("Loading PDFs...")
    docs = load_pdfs(PDF_DIR)
    print(f"Loaded {len(docs)} doc pages.")
    texts, metadatas = chunk_documents(docs)
    print(f"Created {len(texts)} chunks.")
    print("Building vector store (this can take a few minutes)…")
    vectordb = build_vectorstore(texts, metadatas)
    print("Vector store built and persisted.")
    qa = make_qa_chain(vectordb)

    print("\nAsk questions about the chemistry material. Type 'exit' to quit.")
    while True:
        q = input("\nQ: ")
        if q.strip().lower() in ("exit", "quit"):
            break
        res = qa.invoke(q)
        print("\n--- ANSWER ---")
        print(res["result"])
        print("\n--- SOURCES ---")
        for src in res.get("source_documents", []):
            print(f"{src.metadata.get('source')} - page {src.metadata.get('page')}")
    print("bye")


if __name__ == "__main__":
    main()
