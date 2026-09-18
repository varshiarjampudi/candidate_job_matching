from llama_index.core import SimpleDirectoryReader


def load_documents(folder_path):
    """
    Load all supported documents from the given folder.
    """

    documents = SimpleDirectoryReader(folder_path).load_data()

    return documents