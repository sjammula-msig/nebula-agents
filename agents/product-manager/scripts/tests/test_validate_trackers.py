from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[4]
VALIDATOR = REPO_ROOT / "agents" / "product-manager" / "scripts" / "validate-trackers.py"
RUN_ID = "2026-06-30-dbc93ab5"


def load_validator():
    module_name = "validate_trackers_under_test"
    spec = importlib.util.spec_from_file_location(module_name, VALIDATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def write_tracker_product(product_root: Path) -> None:
    features = product_root / "planning-mds" / "features"
    feature_dir = features / "F0038-scoped"
    feature_dir.mkdir(parents=True, exist_ok=True)

    (features / "REGISTRY.md").write_text(
        """# Feature Registry

## Active Features

| Feature ID | Name | Status | Phase | Folder |
|------------|------|--------|-------|--------|
| F0038 | Scoped Evidence | In Progress | MVP | `F0038-scoped/` |

## Planned (Reserved IDs)

| Feature ID | Name | Status | Phase | Folder |
|------------|------|--------|-------|--------|

## Archived Features

| Feature ID | Name | Archived Date | Evidence Reentry Date | Folder |
|------------|------|---------------|-----------------------|--------|
""",
        encoding="utf-8",
    )
    (features / "ROADMAP.md").write_text(
        """# Roadmap

## Now

| Feature | Status | Target |
|---------|--------|--------|
| [F0038 Scoped Evidence](./F0038-scoped/) | In Progress | Current |

## Next

| Feature | Status | Target |
|---------|--------|--------|

## Later

| Feature | Status | Target |
|---------|--------|--------|

## Completed

| Feature | Status | Target |
|---------|--------|--------|
""",
        encoding="utf-8",
    )
    (features / "STORY-INDEX.md").write_text("# Story Index\n\n**Total Stories:** 0\n", encoding="utf-8")
    (feature_dir / "STATUS.md").write_text("# Status\n\n**Overall Status:** In Progress\n", encoding="utf-8")
    (product_root / "planning-mds" / "BLUEPRINT.md").write_text("# Blueprint\n", encoding="utf-8")


def run_main(module, monkeypatch: pytest.MonkeyPatch, product_root: Path, *args: str) -> int:
    monkeypatch.setattr(
        sys,
        "argv",
        [str(VALIDATOR), "--product-root", str(product_root), *args],
    )
    return module.main()


def test_skip_feature_evidence_validates_trackers_only(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    product = tmp_path / "product"
    write_tracker_product(product)
    module = load_validator()
    calls: list[tuple[Path, str | None, str | None, bool]] = []

    def fake_invoke(
        product_root: Path,
        feature: str | None,
        run_id: str | None,
        *,
        all_feature_evidence: bool = False,
    ) -> int:
        calls.append((product_root, feature, run_id, all_feature_evidence))
        return 1

    monkeypatch.setattr(module, "_invoke_feature_evidence_validator", fake_invoke)

    assert run_main(module, monkeypatch, product, "--skip-feature-evidence") == 0
    assert calls == []


def test_default_validates_trackers_only_without_feature_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    product = tmp_path / "product"
    write_tracker_product(product)
    module = load_validator()
    calls: list[tuple[Path, str | None, str | None, bool]] = []

    def fake_invoke(
        product_root: Path,
        feature: str | None,
        run_id: str | None,
        *,
        all_feature_evidence: bool = False,
    ) -> int:
        calls.append((product_root, feature, run_id, all_feature_evidence))
        return 1

    monkeypatch.setattr(module, "_invoke_feature_evidence_validator", fake_invoke)

    assert run_main(module, monkeypatch, product) == 0
    assert calls == []


def test_feature_and_run_id_invokes_scoped_feature_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    product = tmp_path / "product"
    write_tracker_product(product)
    module = load_validator()
    calls: list[tuple[Path, str | None, str | None, bool]] = []

    def fake_invoke(
        product_root: Path,
        feature: str | None,
        run_id: str | None,
        *,
        all_feature_evidence: bool = False,
    ) -> int:
        calls.append((product_root, feature, run_id, all_feature_evidence))
        return 0

    monkeypatch.setattr(module, "_invoke_feature_evidence_validator", fake_invoke)

    assert run_main(module, monkeypatch, product, "--feature", "F0038", "--run-id", RUN_ID) == 0
    assert calls == [(product.resolve(), "F0038", RUN_ID, False)]


def test_feature_without_run_id_invokes_scoped_latest_run_validation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    product = tmp_path / "product"
    write_tracker_product(product)
    module = load_validator()
    calls: list[tuple[Path, str | None, str | None, bool]] = []

    def fake_invoke(
        product_root: Path,
        feature: str | None,
        run_id: str | None,
        *,
        all_feature_evidence: bool = False,
    ) -> int:
        calls.append((product_root, feature, run_id, all_feature_evidence))
        return 0

    monkeypatch.setattr(module, "_invoke_feature_evidence_validator", fake_invoke)

    assert run_main(module, monkeypatch, product, "--feature", "F0038") == 0
    assert calls == [(product.resolve(), "F0038", None, False)]


def test_run_id_without_feature_is_usage_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    product = tmp_path / "product"
    write_tracker_product(product)
    module = load_validator()

    with pytest.raises(SystemExit) as excinfo:
        run_main(module, monkeypatch, product, "--run-id", RUN_ID)

    assert excinfo.value.code == 2
    assert "--run-id requires --feature" in capsys.readouterr().err


def test_all_feature_evidence_invokes_repo_wide_validation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    product = tmp_path / "product"
    write_tracker_product(product)
    module = load_validator()
    calls: list[tuple[Path, str | None, str | None, bool]] = []

    def fake_invoke(
        product_root: Path,
        feature: str | None,
        run_id: str | None,
        *,
        all_feature_evidence: bool = False,
    ) -> int:
        calls.append((product_root, feature, run_id, all_feature_evidence))
        return 0

    monkeypatch.setattr(module, "_invoke_feature_evidence_validator", fake_invoke)

    assert run_main(module, monkeypatch, product, "--all-feature-evidence") == 0
    assert calls == [(product.resolve(), None, None, True)]


def test_feature_evidence_failure_propagates_after_tracker_pass(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    product = tmp_path / "product"
    write_tracker_product(product)
    module = load_validator()

    def fake_invoke(
        product_root: Path,
        feature: str | None,
        run_id: str | None,
        *,
        all_feature_evidence: bool = False,
    ) -> int:
        return 1

    monkeypatch.setattr(module, "_invoke_feature_evidence_validator", fake_invoke)

    assert run_main(module, monkeypatch, product, "--feature", "F0038", "--run-id", RUN_ID) == 1
