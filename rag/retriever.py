def retrieve_chunks(vector_store, query):

    results=vector_store.similarity_search(
        query,
        k=4
    )

    return results