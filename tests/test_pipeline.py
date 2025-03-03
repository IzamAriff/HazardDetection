import unittest
from src.integration.pipeline import run_pipeline

class TestPipeline(unittest.TestCase):
    def test_pipeline_runs(self):
        # Test that the end-to-end pipeline runs without throwing an exception.
        try:
            run_pipeline()
        except Exception as e:
            self.fail(f"Pipeline raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
