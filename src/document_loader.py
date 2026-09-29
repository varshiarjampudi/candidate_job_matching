from pathlib import Path

from llama_index.core import SimpleDirectoryReader


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def resolve_project_path(path_value):
    """Resolve a project-relative path against the app root."""
    path = Path(path_value)

    if path.is_absolute():
        return path

    return (PROJECT_ROOT / path).resolve()


def load_documents(folder_path):
    """
    Load all supported documents from the given folder.
    """
    folder = resolve_project_path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(
            f"Directory '{folder}' does not exist. "
            f"Project root: {PROJECT_ROOT}"
        )

    documents = SimpleDirectoryReader(str(folder)).load_data()

    return documents