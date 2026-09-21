# TODO

## Backlog

- Feature 11: instead of "01.mp3" or "album_01.mp3" it should be "part_01.mp3" and "album_part_01.mp3"

- Feature 5: the user should be able to decide the parts length, default: 10 minutes. The selection should obviously be persisted as a user preference.

- Feature 8: Add TRK tag (don't override it if already exists!)

- Feature 10: Add the COMM tag for this text: "Original file split with Music Splitter by Alessandro Piccione."
  Frame:       COMM
  Language:    eng
  Description: Splitter provenance
  Text:        Original file split with Music Splitter by Alessandro Piccione.

  The text should be stored in ui-text/english.yml


- Feature 7: Replace the log text with a simple Message bar.:
  It will inform the user of hte latest completed actions, errors, etc...
  Do we really need a "log"? we can discuss of this. 
  Maybe it can be a file that can be opened and sent to the repo to feeedback a bug?

- Feature 6: Add an installer for Windows (should it comprehend a ffmpeg too? maybe used only if not already present in the system?)
