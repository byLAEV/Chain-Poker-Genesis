import io
import unittest
from unittest.mock import patch

from Installer import install as installer


class CliInteractionTests(unittest.TestCase):
    def test_menu_install_option_starts_installation(self):
        with patch("Installer.install.install") as mocked_install:
            with patch("builtins.input", side_effect=["1", "n"]):
                with patch("sys.stdout", new_callable=io.StringIO) as output:
                    installer.run_interactive_menu()

            mocked_install.assert_not_called()
            self.assertIn("Install Node Core", output.getvalue())

    def test_menu_exit_option(self):
        with patch("builtins.input", side_effect=["2"]):
            with patch("sys.stdout", new_callable=io.StringIO) as output:
                installer.run_interactive_menu()

        self.assertIn("Exit", output.getvalue())


if __name__ == "__main__":
    unittest.main()
