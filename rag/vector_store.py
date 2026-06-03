from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

def create_vector_store(chunks, embeddings, source_name):

    docs = []

    for i, chunk in enumerate(chunks):
        docs.append(
            Document(
                page_content=chunk,
                metadata={
                    "source": source_name,
                    "chunk_id": i + 1
                }
            )
        )

    vector_store = FAISS.from_documents(docs, embeddings)

    return vector_store
    