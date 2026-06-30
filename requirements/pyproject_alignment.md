# Requirements and pyproject alignment notes

- Keep runtime dependencies in sync between pyproject.toml and requirements/requirements.txt.
- Add new runtime packages to both files when they become required by the backend.
- Keep development-only tools separate from the core runtime dependency list.
- Update this note as the project grows beyond the initial placeholder scaffold.
