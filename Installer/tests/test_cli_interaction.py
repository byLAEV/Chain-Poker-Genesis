import io
import unittest
from unittest.mock import patch

from Installer.install import interactive


class CliInteractionTests(unittest.TestCase):
    def test_menu_exit_option(self):
        with patch("builtins.input", side_effect=["2"]):
            with patch("sys.stdout", new_callable=io.StringIO) as output:
                result = interactive("main", __import__("pathlib").Path("/tmp/cpg-test-target"))

        self.assertEqual(result, 0)
        self.assertIn("1. Install Node Core", output.getvalue())
        self.assertIn("2. Exit", output.getvalue())
        self.assertIn("Exiting.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
