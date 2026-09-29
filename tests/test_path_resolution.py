import os
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.document_loader import load_documents


class TestPathResolution(unittest.TestCase):
    def test_resume_folder_is_resolved_from_project_root(self):
        original_cwd = Path.cwd()
        os.chdir(PROJECT_ROOT.parent)

        try:
            documents = load_documents("data/resumes")
            self.assertTrue(len(documents) > 0)
        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    unittest.main()
