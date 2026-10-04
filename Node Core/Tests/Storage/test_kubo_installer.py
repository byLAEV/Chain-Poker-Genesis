from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib, os, tarfile, io, sys

BASE = Path(__file__).resolve().parents[2] / "Storage" / "Kubo"
sys.path.insert(0, str(BASE))
from kubo_installer import KuboPackageInstaller, KuboInstallationError
from kubo_paths import KuboPathManager

def make_package(root, malicious=False):
    payload = Path(root) / "payload"
    dist = payload / "kubo"
    (dist / "bin").mkdir(parents=True)
    exe = dist / "ipfs"
    exe.write_text("#!/bin/sh\necho kubo version 0.43.1\n")
    os.chmod(exe, 0o755)
    package = Path(root) / "kubo_v0.43.1_linux-amd64.tar.gz"
    with tarfile.open(package, "w:gz") as archive:
        archive.add(dist, arcname="kubo")
        if malicious:
            info = tarfile.TarInfo("../../escape")
            data = b"bad"
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
    return package

def test_install_verified_package():
    with TemporaryDirectory() as root:
        package = make_package(root)
        digest = hashlib.sha512(package.read_bytes()).hexdigest()
        paths = KuboPathManager(root).paths("v0.43.1")
        installed = KuboPackageInstaller().install(
            package, paths=paths, version="v0.43.1",
            expected_sha512=digest
        )
        assert (installed / "ipfs").is_file()
        assert (installed / "INSTALLATION-MANIFEST.json").is_file()

def test_changed_package_rejected():
    with TemporaryDirectory() as root:
        package = make_package(root)
        digest = "0" * 128
        paths = KuboPathManager(root).paths("v0.43.1")
        try:
            KuboPackageInstaller().install(package, paths=paths, version="v0.43.1", expected_sha512=digest)
        except KuboInstallationError:
            pass
        else:
            raise AssertionError("changed package accepted")

def test_archive_traversal_rejected():
    with TemporaryDirectory() as root:
        package = make_package(root, malicious=True)
        digest = hashlib.sha512(package.read_bytes()).hexdigest()
        paths = KuboPathManager(root).paths("v0.43.1")
        try:
            KuboPackageInstaller().install(package, paths=paths, version="v0.43.1", expected_sha512=digest)
        except KuboInstallationError:
            pass
        else:
            raise AssertionError("unsafe archive accepted")

if __name__ == "__main__":
    test_install_verified_package()
    test_changed_package_rejected()
    test_archive_traversal_rejected()
    print("Kubo installer tests: PASS")
