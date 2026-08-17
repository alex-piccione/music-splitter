# TODO

## In Progress: Split MP3

- **Feature: Split MP3**
  Complete the user-facing MP3 splitting workflow.

  **Remaining Work:**
  1. [ ] UI Integration: Connect `MP3Splitter` to `main.py` using threading to prevent UI freezes.
  2. [ ] Documentation: Update `README.md` with installation and run instructions.

## Backlog

- [ ] **[chore/04_publish_todo_update]** Publish the completed core-splitter TODO reconciliation through a pull request.
  - [ ] Create the branch from the planned main commit.
  - [ ] Push the branch and open a pull request.
  - [ ] Verify the pull request has no unresolved review comments.

- Feature: Config
  Add a `config.txt` file containing:
  - `MP3SPLIT_BINS_FOLDER`
  - `SPLIT_FIXED_DURATION_MINUTES`

## Completed

- **Split MP3 core engine** — Added the `MP3Splitter` implementation, `pydub` setup, metadata handling, naming logic, and unit tests.
