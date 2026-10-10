# Contributing

Contributions that make repository explanations clearer, source-backed, or more scalable are welcome.

## Local checks

Use Python 3.10 or newer; runtime tools require only the standard library.

```bash
python3 -B -m unittest discover -s tests -v
```

Keep source snapshots, unknown behavior, and runtime evidence distinct. A useful teaching change includes a before/after explanation or a small anonymized repository scenario, plus what a reader should be able to predict afterward. Do not commit credentials, private source, account logs, or local edit records.

## Pull requests

1. Open an issue for substantial workflow changes to explain the reader's problem and scope.
2. Work on a focused branch and preserve existing language/format choices.
3. For a tool change, add a behavior test that fails before the fix, then run the suite.
4. For a skill change, use a realistic forward trial; exact phrase matching is not a teaching-quality test.
5. Update documentation and CHANGELOG.md when user-visible behavior changes.
6. Regenerate PACKAGE-CONTENTS.json if packaged files change; it excludes itself and contains SHA-256 hashes of distributable files.
7. Explain validation, limitations, and any third-party material in the PR.

By submitting original contributions, you agree to license them under this project's MIT License. Separately licensed excerpts must keep their attribution and terms. No CLA is required by this project.

## Releases

The maintainer verifies the intended file set, tests, manifests, package hashes, and third-party notices, then tags a version and attaches its ZIP to a GitHub Release. CI results and limited trials are reported with their actual scope.
