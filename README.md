# Repo Teacher

[简体中文](README.zh-CN.md) · [Teaching principles](PEDAGOGY.md) · [Example lesson](examples/financial-services/GUIDE.md)

A Codex plugin that turns repository evidence into lessons for people who have **not read the source code**.

Start with one concrete scenario: who reads each file, what changes between steps, which program does the work, and where the result goes. Explain unfamiliar concepts before using their technical names. Keep source facts, illustrative examples, tests, and observed runtime behavior distinguishable.

## Install

With a Codex CLI that supports plugins:

```bash
codex plugin marketplace add Yubeizuihoudedanchun911/repo-teacher --ref v0.1.0
codex plugin add repo-teacher@repo-teacher-local
```

Start a new session and invoke `$teach-repo`. Check `codex plugin --help` for your installed version; desktop discovery and refresh depend on the host.

For a local copy, clone this repository or extract the [release ZIP](https://github.com/Yubeizuihoudedanchun911/repo-teacher/releases), keep it in a stable directory, then replace the first command with:

```bash
codex plugin marketplace add /absolute/path/to/repo-teacher
```

These installation commands change your Codex configuration and plugin cache. The package does not install itself. Editing a source copy does not necessarily refresh an already installed copy.

## Use

```text
Use $teach-repo to explain /path/to/repository.
I know general programming but have never read this project.
Walk through one request, then explain the project-specific files.
```

```text
Use $teach-repo to rewrite this confusing architecture explanation.
Show the missing assumptions, the actor at every step,
and a concrete before/after example of each configuration transformation.
```

```text
Use $teach-repo for this large monorepo.
Build a system map, trace the checkout flow and a message failure,
and identify unverified modules and external implementations.
```

The skill supports generating, rewriting, and updating lessons. It uses the conversation language and requested output format. The instructions are currently written in Chinese. Ordinary code edits, isolated diagrams, and quick API lookups do not need this workflow.

## How it works

1. Establish the reader's starting knowledge and learning goal.
2. Inspect repository instructions, module declarations, entry points, and boundaries.
3. Trace a representative behavior through callers, configuration readers, storage, and outputs.
4. Teach that behavior through one concrete example, with intermediate states.
5. Add diagrams where they help; connect each arrow to an explained action.
6. Record evidence and coverage, then check citations and ask a short self-check question.

For large projects, exploration proceeds from a module map to selected end-to-end paths and deeper chapters. File inventory coverage and behavior understanding are recorded separately. Missing repositories, runtime switches, and external services remain explicit unknowns. See [large-repository guidance](skills/teach-repo/references/large-repos.md).

The teaching rules reference [CMU Eberly Center learning principles](https://www.cmu.edu/teaching/principles/learning.html). [PEDAGOGY.md](PEDAGOGY.md) maps those concepts to concrete plugin behavior and distinguishes teaching choices from engineering checks. This project is independent of CMU; learner outcomes have not been measured.

## Local tools

Python 3.10+ and its standard library are sufficient:

```bash
python3 skills/teach-repo/scripts/inspect_repo.py --repo /path/to/repo
python3 skills/teach-repo/scripts/check_lesson.py --repo /path/to/repo --lesson /path/to/GUIDE.md --evidence /path/to/evidence.json
python3 -B -m unittest discover -s tests -v
```

Both scripts read local inputs and write JSON to stdout. They do not start the inspected application, install its dependencies, or upload its source.

- `inspect_repo.py` inventories metadata and entry-point candidates within file, directory, and time budgets. It does not parse all code or prove call relationships. Defaults: 10,000 files, 5,000 directories, 20 seconds. It uses its own exclusion rules, not Git's complete ignore semantics.
- `check_lesson.py` checks local source paths, line ranges, content hashes, revision metadata, and local document links. It cannot establish semantic correctness, production success, diagram rendering, or reader understanding. Remote URLs and heading anchors are not checked.

The AI host may process material through its own services. These local scripts do not make the overall AI workflow offline.

## Diagrams and examples

If Archify is already available, the workflow can use it. Otherwise it falls back to simple Mermaid or text steps. No Archify code, MCP server, account connection, or browser dependency is bundled.

The [Financial Services lesson](examples/financial-services/GUIDE.md) includes [evidence](examples/financial-services/evidence.json) and [coverage](examples/financial-services/coverage.json) tied to one upstream revision. It demonstrates file readers, field transformations, and the difference between creating an agent and running a task. No cloud task was executed.

[VALIDATION.md](VALIDATION.md) describes the 11 behavior tests, scenario trials, and limits. GitHub Actions checks Python 3.10 and 3.13 plus package metadata and hashes.

## Package and contribution

The root `plugin.json` is the portable manifest. `.codex-plugin/plugin.json` provides Codex compatibility; `.agents/plugins/marketplace.json` exposes the local marketplace. Packaging follows the [OpenAI plugin documentation](https://developers.openai.com/plugins/build/plugins).

See [CONTRIBUTING.md](CONTRIBUTING.md), [Code of Conduct](CODE_OF_CONDUCT.md), [security reporting](SECURITY.md), and [CHANGELOG.md](CHANGELOG.md). Feedback about an explanation is welcome: include the unclear sentence, your starting knowledge, and the behavior you wanted to understand. Share only source you are authorized to disclose.

## License

Original plugin code and documentation are [MIT licensed](LICENSE). The attributed upstream YAML excerpt in the Financial Services example remains Apache-2.0; its license is included in [LICENSES/Apache-2.0.txt](LICENSES/Apache-2.0.txt). See [NOTICE](NOTICE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Referenced CMU pages, optional tools, and external projects retain their own licenses.
