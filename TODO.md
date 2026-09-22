# TODO

## Backlog

- Bug 1: test "test_default_output_folder" doesn't take in account difefrent OS path separator
  ```
  AssertionError: 'P:\\music\\DJ Session' != '/music/DJ Session'
    - P:\music\DJ Session
    ? ^^^     ^
    + /music/DJ Session
    ? ^     ^
  ```

- Feature 10: add TEST.md file in the root. Empty.
  This file is just to test teh /feature command.
  Don't overthink... is a simple 1 minute task (don't forget branch + PR).

- Feature 7: The internal log will be replaced by a log file, plus a button that shows it when an operation fails.

- Feature 6: Add an installer for Windows (should it comprehend a ffmpeg too? maybe used only if not already present in the system?)
