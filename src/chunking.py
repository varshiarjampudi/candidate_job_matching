from llama_index.core.node_parser import SentenceSplitter


def chunk_documents(documents):
    splitter = SentenceSplitter(
        chunk_size=512,
        chunk_overlap=64
    )

    nodes = splitter.get_nodes_from_documents(documents)

    return nodes