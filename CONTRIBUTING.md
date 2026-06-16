# Contributing to k6-ts-docker

Thanks for wanting to contribute. Follow these lightweight rules to keep changes reviewable.

## Getting started

1. Install Docker and Python 3 (>=3.10). No Node or k6 is required on the host.
2. Run `./bin/punch doctor` to confirm your environment.
3. Use a feature branch named `ai-ready/*` or `feature/*`.

## Branch and PR rules

- Target the default branch (`main`) via a pull request from a feature branch.
- Keep PRs small and focused. Each PR should include a verification step in the description.
- Use the provided issue and PR templates.

## Running and testing locally

```bash
./bin/punch run all --collect-logs  # Build and run the full suite
./bin/punch run smoke               # Run a single test
./bin/punch clean                   # Tear down containers and volumes
```

## What to include in PRs

- Short description and how to validate locally
- Which reports or artifacts changed
- Reference any docs or AGENTS.md updates

## Contact

For questions about the AI lifecycle or prompts, see [`docs/ai/operating-model.md`](docs/ai/operating-model.md), [`docs/ai/workflow.md`](docs/ai/workflow.md), and the prompts under [`.github/prompts/`](.github/prompts).
