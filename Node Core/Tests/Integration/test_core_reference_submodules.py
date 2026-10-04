import configparser
import json
import pathlib
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
GITMODULES = REPO_ROOT / ".gitmodules"
REFERENCE_MANIFEST = (
    REPO_ROOT
    / "Node Core"
    / "Cryptography"
    / "Core References"
    / "CRYPTO-CORE-REFERENCE-MANIFEST.json"
)


class CoreReferenceSubmoduleTests(unittest.TestCase):
    def test_declared_submodules_match_node_core_crypto_references(self):
        self.assertTrue(GITMODULES.is_file(), ".gitmodules is required for Node Core external references")
        self.assertTrue(
            REFERENCE_MANIFEST.is_file(),
            "Node Core cryptography reference manifest is required",
        )

        config = configparser.ConfigParser()
        config.read(GITMODULES, encoding="utf-8")

        with REFERENCE_MANIFEST.open(encoding="utf-8") as handle:
            manifest = json.load(handle)

        expected = {
            "bitcoin/bitcoin": (
                "Node Core/Cryptography/Core References/bitcoin--bitcoin",
                "https://github.com/bitcoin/bitcoin.git",
            ),
            "bitcoin-core/secp256k1": (
                "Node Core/Cryptography/Core References/bitcoin-core--secp256k1",
                "https://github.com/bitcoin-core/secp256k1.git",
            ),
            "jedisct1/libsodium": (
                "Node Core/Cryptography/Core References/jedisct1--libsodium",
                "https://github.com/jedisct1/libsodium.git",
            ),
            "lightning/bolts": (
                "Node Core/Cryptography/Core References/lightning--bolts",
                "https://github.com/lightning/bolts.git",
            ),
            "lightningnetwork/lnd": (
                "Node Core/Cryptography/Core References/lightningnetwork--lnd",
                "https://github.com/lightningnetwork/lnd.git",
            ),
        }

        external_expected = {
            "gpg/gpgme": (
                "Node Core/Cryptography/External References/gpg--gpgme",
                "https://github.com/gpg/gpgme.git",
            ),
            "gpg/poldi": (
                "Node Core/Cryptography/External References/gpg--poldi",
                "https://github.com/gpg/poldi.git",
            ),
            "openpgpjs/openpgpjs": (
                "Node Core/Cryptography/External References/openpgpjs--openpgpjs",
                "https://github.com/openpgpjs/openpgpjs.git",
            ),
            "pgpainless/pgpainless": (
                "Node Core/Cryptography/External References/pgpainless--pgpainless",
                "https://github.com/pgpainless/pgpainless.git",
            ),
        }

        for repository, (path, url) in external_expected.items():
            section = f'submodule "{path}"'
            self.assertIn(section, config.sections())
            self.assertEqual(config[section]["path"], path)
            self.assertEqual(config[section]["url"], url)

        manifest_repositories = {
            item["repository"]: item for item in manifest["references"]
        }

        self.assertEqual(set(manifest_repositories), set(expected))

        for repository, (path, url) in expected.items():
            section = f'submodule "{path}"'
            self.assertIn(section, config.sections())
            self.assertEqual(config[section]["path"], path)
            self.assertEqual(config[section]["url"], url)
            self.assertEqual(manifest_repositories[repository]["commit"], self._gitlink_commit(repository))

    @staticmethod
    def _gitlink_commit(repository):
        commits = {
            "bitcoin/bitcoin": "66776840beb558f7e84451c2c55457f0e06242f0",
            "bitcoin-core/secp256k1": "22245aedf4000e62b597d40091a23388f2fa533a",
            "jedisct1/libsodium": "75c6d5520a3b99790696d98b554673697c71c5cc",
            "lightning/bolts": "1aadb719b4007c4cea0ba6e36b08c4fb53788dee",
            "lightningnetwork/lnd": "f3a8f4e8ae8237ff2b40e4724de45085170df962",
        }
        return commits[repository]


if __name__ == "__main__":
    unittest.main()
