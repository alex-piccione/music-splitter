# TODO

## In Progress: Split MP3

- **Feature: Split MP3**
  Split large `.mp3` files into equal segments (default: 5 minutes).
  Create a destination folder named after the source file.
  Save parts as `01.mp3`, `02.mp3`, etc.
  Copy metadata from the original file and include "part" info if possible.

  **Implementation Plan:**
  1. [ ] Setup: Initialize `libs/splitter.py` and ensure `pydub` dependency is set.
  2. [ ] Core Engine: Implement `MP3Splitter` class with segmenting and naming logic.
  3. [ ] UI Integration: Connect engine to `main.py` using threading (prevent UI freeze).
  4. [ ] Testing: Implement unit tests for the splitter module.
  5. [ ] Documentation: Update `README.md` with installation and run instructions.

## Backlog

- Feature: Config 
  Add a config.txt file. 
  It has to contain the fields: MP3SPLIT_BINS_FOLDER and SPLIT_FIXED_DURATION_MINUTES.

## Done

- Implement UI elements:
  + Modernize Look & Feel using `tkinter.ttk`.
  + Improve Layout (Header, Selected File Display, Status/Log Area).
  + Integrate File Selection visibility and Split trigger.
  + Enhance Error Handling/Feedback.
