# TODO

## Backlog


- Feature 1: When I click "Split file" it has to open the dialog on the last directory I used (apart from first app use obviously)

- Feature 2: When it splits the file it should try to create a folder with the same name of the source file, and put the files there.

- Feature 4: Two option buttons should allow to select the file name format. "File names"  (a) Numbers ("01.mp3")  (b) File+Numbers ("DJ-AAA 2028-12-31 full_session_01.mp3")

- Feature 5: the user should be able to decide the parts length, default: 10 seconds. The selection should obviously be persisted as a user preference.

- Feature 7: Replace teh log text wit ha simple Message bar.:
  It will inform the user of hte latest completed actions, errors, etc...
  Do we really need a "log"? we can discuss of this. 
  Maybe it can be a file that can be opened and sent to the repo to feeedback a bug?

- Feature 6: Add an installer for Windows (should it comprehend a ffmpeg too? maybe used only if not already present in the system?)

- **[docs/01_id3_tag]** Create `ID3_tag.md` documenting the ID3v2 tags written by the app:

  | Code | Meaning                 | Value in test |
  |------|-------------------------|---------------|
  | TIT2 | Title (Track title)     | 'Test Title'  |
  | TPE1 | Lead performer (Artist) | 'Test Artist' |
  | TALB | Album name              | 'Test Album'  |

  Link it from `README.md` so the README stays short.
- **[docs/02_cue_file]** Create `CUE.md` documenting the CUE sheet files produced by the app (structure, fields, how they reference the split segments). Link it from `README.md`.
