#!/usr/bin/env python3
"""Bounded, read-only metadata inventory. No source-content parsing."""
import argparse
from collections import Counter
import fnmatch
import json
import os
from pathlib import Path
import subprocess
import time

EXCLUDED_DIRS = {".git", ".weaver", "node_modules", "vendor", ".venv", "venv",
                 "__pycache__", "dist", "build", "target", ".next", ".cache"}
EXCLUDED_FILES = {".DS_Store"}
SECRET_PATTERNS = (".env", ".env.*", "*.pem", "*.key", "auth.json", "credentials", "credentials.*")
BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".zip", ".gz",
                   ".jar", ".class", ".pyc", ".so", ".dylib", ".dll", ".exe", ".woff", ".woff2"}
MANIFESTS = {"package.json", "pom.xml", "Cargo.toml", "pyproject.toml", "go.mod",
             "build.gradle", "build.gradle.kts", "settings.gradle", "pnpm-workspace.yaml",
             "Makefile", "CMakeLists.txt", "plugin.json", "marketplace.json"}
ENTRIES = {"main.py", "app.py", "cli.py", "main.rs", "lib.rs", "main.go", "Main.java",
           "server.js", "server.ts", "index.ts", "index.js", "Program.cs"}
LANGUAGES = {".py":"Python", ".java":"Java", ".rs":"Rust", ".go":"Go", ".ts":"TypeScript",
             ".tsx":"TypeScript", ".js":"JavaScript", ".jsx":"JavaScript", ".cs":"C#",
             ".cpp":"C++", ".c":"C", ".rb":"Ruby", ".swift":"Swift", ".kt":"Kotlin",
             ".sql":"SQL", ".yaml":"YAML", ".yml":"YAML", ".json":"JSON", ".md":"Markdown",
             ".tf":"Terraform", ".sh":"Shell"}

def git_metadata(repo):
    result = {"revision": None, "git_root": None, "worktree_status": "not-collected"}
    for key, args in [("revision", ["rev-parse", "HEAD"]),
                      ("git_root", ["rev-parse", "--show-toplevel"])]:
        try:
            p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                               text=True, timeout=3)
            if p.returncode == 0:
                result[key] = p.stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            pass
    return result

def inventory(repo, max_files, max_dirs, seconds):
    deadline = time.monotonic() + seconds
    files, stops, errors = [], [], []
    excluded = Counter()
    stack, visited = [repo], 0
    while stack and not stops:
        if time.monotonic() >= deadline:
            stops.append("time_limit"); break
        if visited >= max_dirs:
            stops.append("directory_limit"); break
        directory = stack.pop()
        visited += 1
        try:
            with os.scandir(directory) as entries:
                for entry in entries:
                    if time.monotonic() >= deadline:
                        stops.append("time_limit"); break
                    if entry.is_symlink():
                        excluded["symlink"] += 1; continue
                    if entry.is_dir(follow_symlinks=False):
                        if entry.name in EXCLUDED_DIRS:
                            excluded["directory"] += 1
                        else:
                            stack.append(Path(entry.path))
                        continue
                    if not entry.is_file(follow_symlinks=False):
                        excluded["non_regular"] += 1; continue
                    name = entry.name
                    path = Path(entry.path)
                    if (name in EXCLUDED_FILES or
                        any(fnmatch.fnmatch(name.lower(), pat) for pat in SECRET_PATTERNS) or
                        path.suffix.lower() in BINARY_SUFFIXES):
                        excluded["file"] += 1; continue
                    if len(files) >= max_files:
                        stops.append("file_limit"); break
                    rel = path.relative_to(repo).as_posix()
                    parts = Path(rel).parts
                    module = "/".join(parts[:2]) if len(parts) > 2 and parts[0] in {
                        "services", "apps", "packages", "plugins", "modules"} else (
                        parts[0] if len(parts) > 1 else "(root)")
                    files.append({"path": rel, "bytes": entry.stat(follow_symlinks=False).st_size,
                                  "module_candidate": module,
                                  "language_hint": LANGUAGES.get(path.suffix.lower(), "other"),
                                  "manifest_hint": name in MANIFESTS,
                                  "entrypoint_hint": name in ENTRIES})
        except OSError as exc:
            errors.append({"path": str(directory.relative_to(repo)), "error": type(exc).__name__})
    complete = not stops and not errors
    files.sort(key=lambda f: f["path"])
    return {
        "ok": True, "schema_version": 1, "repository": {"path": str(repo), **git_metadata(repo)},
        "inventory_complete": complete, "semantic_coverage_verified": False,
        "scope": "Filesystem candidates after built-in exclusions; Git ignore rules are not evaluated.",
        "eligible_file_count": len(files) if complete else None,
        "returned_file_count": len(files), "directories_visited": visited,
        "stop_reasons": stops, "read_errors": errors, "excluded_counts": dict(excluded),
        "module_candidates": dict(Counter(f["module_candidate"] for f in files)),
        "language_hints": dict(Counter(f["language_hint"] for f in files)),
        "manifest_candidates": [f["path"] for f in files if f["manifest_hint"]],
        "entrypoint_candidates": [f["path"] for f in files if f["entrypoint_hint"]],
        "files": files
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--max-files", type=int, default=10000)
    parser.add_argument("--max-dirs", type=int, default=5000)
    parser.add_argument("--seconds", type=float, default=20)
    args = parser.parse_args()
    repo = args.repo.resolve()
    if not repo.is_dir() or min(args.max_files, args.max_dirs, args.seconds) <= 0:
        print(json.dumps({"ok": False, "error": "A repository directory and positive limits are required."}))
        return 2
    result = inventory(repo, args.max_files, args.max_dirs, args.seconds)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
