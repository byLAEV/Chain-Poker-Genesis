import io
import unittest
from unittest.mock import patch

from Installer.install import interactive


class CliInteractionTests(unittest.TestCase):
    def test_main_menu_branding_and_options(self):
        with patch("builtins.input", side_effect=["0"]):
            with patch("sys.stdout", new_callable=io.StringIO) as output:
                result = interactive("main", __import__("pathlib").Path("/tmp/cpg-test-target"))

        rendered = output.getvalue()
        self.assertEqual(result, 0)
        self.assertIn("Trilema Project Presents", rendered)
        self.assertIn("Node Core Network by LAEV", rendered)
        self.assertIn("& The Chain Poker Genesis Protocol", rendered)
        self.assertIn("[In Memory of Satoshi Nakamoto's Legacy,", rendered)
        self.assertIn(" Trilema.com (MP), Hannah Wiggins (Hanbot),", rendered)
        self.assertIn(" Lerry Alexander (LAEV) & The Bitcoin Network]", rendered)
        self.assertIn("1. Node Core BIOS", rendered)
        self.assertIn("2. Node Core", rendered)
        self.assertIn("3. Protocols", rendered)
        self.assertIn("0. Exit", rendered)
        self.assertIn("Exiting.", rendered)


if __name__ == "__main__":
    unittest.main()
