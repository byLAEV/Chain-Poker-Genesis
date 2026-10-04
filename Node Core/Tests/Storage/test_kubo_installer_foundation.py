#!/usr/bin/env python3
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

BASE = Path(__file__).resolve().parents[2] / "Storage" / "Kubo"
sys.path.insert(0, str(BASE))

from kubo_release_resolver import KuboReleaseError, KuboReleaseResolver
from kubo_paths import KuboPathError, KuboPathManager
from kubo_provider_state import KuboProviderState, KuboStateError


RELEASES = [
    {
        "version": "v0.43.1", "os": "linux", "architecture": "amd64",
        "filename": "kubo_v0.43.1_linux-amd64.tar.gz",
        "source_url": "https://dist.ipfs.tech/kubo/v0.43.1/",
        "expected_integrity": "sha256:example-43", "channel": "stable", "official": True,
    },
    {
        "version": "v0.42.0", "os": "linux", "architecture": "amd64",
        "filename": "kubo_v0.42.0_linux-amd64.tar.gz",
        "source_url": "https://dist.ipfs.tech/kubo/v0.42.0/",
        "expected_integrity": "sha256:example-42", "channel": "stable", "official": True,
    },
]


def test_latest_linux_release():
    release = KuboReleaseResolver(platform_os="linux", architecture="x86_64").resolve(RELEASES)
    assert release.version == "v0.43.1"
    assert release.architecture == "amd64"


def test_exact_version():
    release = KuboReleaseResolver(platform_os="linux", architecture="amd64").resolve(
        RELEASES, policy="EXACT_VERSION", exact_version="v0.42.0"
    )
    assert release.version == "v0.42.0"


def test_unsupported_architecture():
    try:
        KuboReleaseResolver(platform_os="linux", architecture="mips64")
        raise AssertionError("unsupported architecture accepted")
    except KuboReleaseError:
        pass


def test_path_derivation():
    with TemporaryDirectory() as root:
        paths = KuboPathManager(Path(root)).paths("v0.43.1")
        assert paths.repository == Path(root).resolve() / "node-storage/providers/kubo/repository"
        assert paths.ipfs_path.is_absolute()
        assert KuboPathManager(root).environment(paths)["IPFS_PATH"] == str(paths.repository)


def test_path_escape_rejected():
    with TemporaryDirectory() as root:
        manager = KuboPathManager(root)
        paths = manager.paths("v0.43.1")
        escaped = paths.__class__(
            paths.node_root, Path("/tmp/escape"), paths.active_root, paths.repository,
            paths.runtime, paths.logs, paths.state, paths.synchronization
        )
        try:
            manager.validate(escaped)
            raise AssertionError("escaped path accepted")
        except KuboPathError:
            pass


def _record(root):
    repository = Path(root) / "node-storage/providers/kubo/repository"
    return {
        "provider_id": "kubo",
        "provider": "Kubo",
        "state_version": "1.0.0",
        "installation_id": "install-001",
        "lifecycle_state": "HEALTHY",
        "health_state": "HEALTHY",
        "synchronization_state": "PENDING",
        "kubo_version": "v0.43.1",
        "platform": "linux",
        "architecture": "amd64",
        "release_source": "official",
        "release_metadata_source": "official",
        "expected_integrity": "sha256:expected",
        "observed_integrity": "sha256:expected",
        "executable_path": str(Path(root) / "External Providers/Kubo/v0.43.1/bin/ipfs"),
        "repository_path": str(repository),
        "ipfs_path": str(repository.resolve()),
        "installed_at": "2026-10-03T00:00:00+00:00",
        "last_transition_at": "2026-10-03T00:00:00+00:00",
        "last_health_check_at": "2026-10-03T00:00:00+00:00",
    }


def test_atomic_state():
    with TemporaryDirectory() as root:
        path = Path(root) / "node-storage/providers/kubo/state/provider-state.json"
        state = KuboProviderState(path)
        record = _record(root)
        state.write(record)
        assert state.read()["installation_id"] == "install-001"


def test_ready_requires_sync():
    with TemporaryDirectory() as root:
        path = Path(root) / "state.json"
        state = KuboProviderState(path)
        record = _record(root)
        record["lifecycle_state"] = "READY"
        try:
            state.write(record)
            raise AssertionError("READY without synchronization accepted")
        except KuboStateError:
            pass
        record["synchronization_state"] = "SYNCHRONIZED"
        state.write(record)
        assert state.read()["lifecycle_state"] == "READY"


if __name__ == "__main__":
    test_latest_linux_release()
    test_exact_version()
    test_unsupported_architecture()
    test_path_derivation()
    test_path_escape_rejected()
    test_atomic_state()
    test_ready_requires_sync()
    print("Kubo Installer foundation tests: PASS")
