from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


EXPECTED_IDS = (
    "GEO-P1",
    "GEO-P2",
    "GEO-P3",
    "WAM-P1",
    "WAM-P2",
    "WAM-P3",
    "STR-P1",
    "STR-P2",
    "STR-P3",
    "JEP-P1",
    "JEP-P2",
    "JEP-P3",
)


def files_named(root: Path, name: str) -> list[Path]:
    return sorted(path for path in root.rglob(name) if path.is_file())


def proposal_file_for(root: Path, proposal_id: str, name: str) -> Path | None:
    proposal_root = root / "proposals"
    matches = [
        path
        for path in files_named(proposal_root, name)
        if proposal_id.lower() in str(path).lower()
        or proposal_id.lower() in path.read_text(encoding="utf-8", errors="ignore").lower()
    ]
    return matches[0] if len(matches) == 1 else None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the 12-proposal, 10+-round embodied-robotics research pack."
    )
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent,
    )
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    for required in (
        "proposal_index.md",
        "evaluation_rubric.md",
        "reviewer_literature_audit.md",
        "final_recommendations.md",
        "final_certification.md",
    ):
        path = root / required
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty: {required}")

    proposal_paths: dict[str, Path] = {}
    for proposal_id in EXPECTED_IDS:
        proposal = proposal_file_for(root, proposal_id, "proposal.md")
        log = proposal_file_for(root, proposal_id, "refinement_log.md")
        if proposal is None:
            errors.append(f"missing or ambiguous proposal.md for {proposal_id}")
        else:
            proposal_paths[proposal_id] = proposal
        if log is None:
            errors.append(f"missing or ambiguous refinement_log.md for {proposal_id}")
        elif len(set(re.findall(r"round[_ -]?(\d+)", log.read_text(encoding="utf-8", errors="ignore"), re.I))) < 10:
            errors.append(f"fewer than 10 distinct refinement rounds in {log}")

    review_root = root / "reviews"
    round_dirs = sorted(
        path
        for path in review_root.glob("round_*")
        if path.is_dir() and re.fullmatch(r"round_\d+", path.name, re.I)
    )
    if len(round_dirs) < 10:
        errors.append(f"only {len(round_dirs)} review round directories; need at least 10")
    for round_dir in round_dirs:
        if not (round_dir / "summary.md").is_file():
            errors.append(f"missing summary.md in {round_dir.name}")
        for proposal_id in EXPECTED_IDS:
            candidates = [
                path
                for path in round_dir.glob("*.md")
                if path.name.lower() != "summary.md"
                and proposal_id.lower() in path.name.lower()
            ]
            if len(candidates) != 1:
                errors.append(
                    f"{round_dir.name}: expected exactly one review file for {proposal_id}, got {len(candidates)}"
                )

    certification = root / "final_certification.md"
    if certification.is_file():
        cert_text = certification.read_text(encoding="utf-8", errors="ignore")
        for proposal_id in EXPECTED_IDS:
            if proposal_id not in cert_text:
                errors.append(f"final certification omits {proposal_id}")
        pass_count = len(re.findall(r"\bPASS\b", cert_text, re.I))
        if pass_count < len(EXPECTED_IDS):
            errors.append(
                f"final certification has only {pass_count} PASS markers; need at least {len(EXPECTED_IDS)}"
            )

    literature_files = [
        path
        for path in (root / "literature").rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".csv", ".json", ".bib", ".pdf"}
    ] if (root / "literature").is_dir() else []
    if not literature_files:
        errors.append("literature evidence directory is missing or empty")

    print(f"root={root}")
    print(f"proposals_resolved={len(proposal_paths)}/{len(EXPECTED_IDS)}")
    print(f"review_rounds={len(round_dirs)}")
    print(f"literature_files={len(literature_files)}")
    if errors:
        print("status=FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("status=PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
