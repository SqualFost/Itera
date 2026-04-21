import os
from datetime import datetime
import uuid
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

DIR = os.path.dirname(os.path.abspath(__file__))
client = chromadb.PersistentClient(path=os.path.join(DIR, "chroma"))

default_ef = DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="ITERA",
    embedding_function=default_ef,
    metadata={
        "description": "ITERA memory",
        "created": str(datetime.now())
    }
)

def save_memory(text):
    """
    Stores a text entry into the vector memory database (ChromaDB).

    The text is embedded using the default embedding function and saved
    with a unique identifier and a timestamp.

    Args:
        text (str): The textual content to be stored in memory.

    Returns:
        str: A success message if the operation succeeds,
             otherwise an error message.
    """
    try:
        collection.add(
            ids=[str(uuid.uuid4())],
            documents=[text],
            metadatas=[{"ts": datetime.now().isoformat()}]
        )
        return "Memory saved"
    except Exception as e:
        return f"Error: {e}"


def get_memory(query, k=5):
    """
    Retrieves the most relevant entries from the vector memory database.

    Performs a semantic search over the ChromaDB collection and returns
    the closest documents to the given query.

    Args:
        query (str): The input text used for semantic search.
        k (int, optional): Number of results to return. Defaults to 5.

    Returns:
        list[str] | str: A list of matching documents if successful,
                         otherwise an error message.
    """
    try:
        results = collection.query(
            query_texts=[query],
            n_results=k,
        )
        return results["documents"][0]
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("Chroma path:", os.path.abspath("./chroma"))