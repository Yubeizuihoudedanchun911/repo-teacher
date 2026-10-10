#!/usr/bin/env python3
"""Read-only verification of evidence structure, source snapshots and lesson links."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

LEVELS = {"documentation", "source", "test", "runtime", "inference", "unknown"}
MAX_BYTES = 16 * 1024 * 1024

def load_text(path):
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("file exceeds 16 MiB verification limit")
    return path.read_text(encoding="utf-8")

def verify(repo, lesson, evidence):
    errors = []
    def error(code, **context):
        errors.append({"code": code, **context})
    if evidence.get("schema_version") != 1:
        error("unsupported_schema_version")
    revision = evidence.get("repository", {}).get("revision")
    if revision:
        try:
            result = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                                    text=True, capture_output=True, timeout=3)
            if result.returncode != 0 or result.stdout.strip() != revision:
                error("repository_revision_changed")
        except (OSError, subprocess.TimeoutExpired):
            error("repository_revision_unavailable")
    claims = evidence.get("claims")
    if not isinstance(claims, list) or not claims:
        error("missing_claims"); claims = []
    seen, checked = set(), 0
    for claim in claims:
        if not isinstance(claim, dict):
            error("invalid_claim"); continue
        cid = claim.get("id")
        if not isinstance(cid, str) or not cid or cid in seen:
            error("invalid_or_duplicate_claim_id", claim=str(cid))
        if isinstance(cid, str):
            seen.add(cid)
        if not isinstance(claim.get("statement"), str) or not claim["statement"].strip():
            error("missing_statement", claim=cid)
        level = claim.get("level")
        if level not in LEVELS:
            error("invalid_evidence_level", claim=cid)
        sources = claim.get("sources", [])
        if not isinstance(sources, list):
            error("invalid_sources", claim=cid); sources = []
        if level == "unknown":
            if not claim.get("reason"):
                error("missing_unknown_reason", claim=cid)
        elif not sources:
            error("missing_sources", claim=cid)
        if level in {"test", "runtime"}:
            run = claim.get("run", {})
            if not isinstance(run, dict) or not all(
                isinstance(run.get(k), str) and run[k].strip()
                for k in ("id", "timestamp", "environment")):
                error("missing_run_metadata", claim=cid)
            if not any(isinstance(s, dict) and s.get("kind") == "artifact" for s in sources):
                error("missing_execution_record", claim=cid)
        for source in sources:
            if not isinstance(source, dict) or not isinstance(source.get("path"), str):
                error("invalid_source", claim=cid); continue
            kind = source.get("kind", "repository")
            if kind not in {"repository", "artifact"}:
                error("invalid_source_kind", claim=cid); continue
            base = lesson.parent if kind == "artifact" else repo
            raw = Path(source["path"])
            candidate = (base / raw).resolve()
            if raw.is_absolute() or not candidate.is_relative_to(base):
                error("source_outside_repository" if kind == "repository" else
                      "source_outside_artifact_directory", claim=cid, path=source["path"])
                continue
            if not candidate.is_file():
                error("missing_source", claim=cid, path=source["path"]); continue
            try:
                if candidate.stat().st_size > MAX_BYTES:
                    raise ValueError("file exceeds 16 MiB verification limit")
                data = candidate.read_bytes()
                text = data.decode("utf-8")
                digest = hashlib.sha256(data).hexdigest()
            except (OSError, UnicodeError, ValueError) as exc:
                error("unreadable_source", claim=cid, path=source["path"], reason=str(exc))
                continue
            sha = source.get("sha256")
            if not isinstance(sha, str) or not re.fullmatch("[0-9a-fA-F]{64}", sha):
                error("invalid_source_hash", claim=cid, path=source["path"])
            elif sha.lower() != digest:
                error("source_changed", claim=cid, path=source["path"])
            start, end = source.get("line_start"), source.get("line_end")
            if (type(start) is not int or type(end) is not int or
                    not 1 <= start <= end <= len(text.splitlines())):
                error("invalid_line_range", claim=cid, path=source["path"])
            checked += 1
    text = load_text(lesson)
    prose, fence = [], None
    for line in text.splitlines():
        match = re.match(r"^[ ]{0,3}(`{3,}|~{3,})(.*)$", line)
        if match:
            marker, tail = match.groups()
            if fence is None:
                fence = (marker[0], len(marker))
            elif marker[0] == fence[0] and len(marker) >= fence[1] and not tail.strip():
                fence = None
            continue
        if fence is None:
            prose.append(line)
    if fence is not None:
        error("unclosed_code_fence")
    prose = "\n".join(prose)
    links = re.findall(r"!?\[[^\]]*\]\((?:<([^>]+)>|([^\s)]+))(?:\s+\"[^\"]*\")?\)", prose)
    definitions = re.findall(r"(?m)^\s*\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))", prose)
    local_checked = 0
    for angle, bare in links + definitions:
        href = angle or bare
        parsed = urlsplit(href)
        bare_line_link = re.fullmatch(r"[^/:\s]+:\d+", href) is not None
        if (parsed.scheme and not bare_line_link) or parsed.netloc or not parsed.path:
            continue
        local_path = unquote(href if bare_line_link else parsed.path)
        line_suffix = re.fullmatch(r"(.+):(\d+)", local_path)
        link_line = None
        if line_suffix:
            local_path, link_line = line_suffix.group(1), int(line_suffix.group(2))
        candidate = (lesson.parent / local_path).resolve()
        if not candidate.is_relative_to(repo) and not candidate.is_relative_to(lesson.parent):
            error("local_link_outside_allowed_roots", path=href)
        elif not candidate.exists():
            error("missing_local_link", path=href)
        elif link_line is not None:
            try:
                if not candidate.is_file() or not 1 <= link_line <= len(load_text(candidate).splitlines()):
                    error("invalid_link_line", path=href)
            except (OSError, UnicodeError, ValueError):
                error("unreadable_link_target", path=href)
        local_checked += 1
    return {"ok": not errors, "static_validation_only": True, "claims_checked": len(claims),
            "source_references_checked": checked, "local_file_links_checked": local_checked,
            "remote_links_checked": False, "heading_anchors_checked": False,
            "errors": errors}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--lesson", type=Path, required=True)
    parser.add_argument("--evidence", required=True, help="JSON path, or - for stdin")
    args = parser.parse_args()
    repo, lesson = args.repo.resolve(), args.lesson.resolve()
    try:
        if not repo.is_dir() or not lesson.is_file():
            raise ValueError("Repository directory and lesson file must exist.")
        raw = sys.stdin.read(MAX_BYTES + 1) if args.evidence == "-" else load_text(Path(args.evidence))
        if len(raw.encode("utf-8")) > MAX_BYTES:
            raise ValueError("Evidence exceeds 16 MiB verification limit.")
        evidence = json.loads(raw)
        if not isinstance(evidence, dict):
            raise ValueError("Evidence must be an object.")
        result = verify(repo, lesson, evidence)
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        print(json.dumps({"ok": False, "errors": [{"code": "invalid_input", "reason": str(exc)}]}))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
