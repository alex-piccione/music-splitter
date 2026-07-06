## Doing

## Backlog

- Feature: Split MP3  
  Split large .mp3 file into smaller files. Given the .mp3 file, create a folder with the same name and add the part_NN.mp3 files created there.  
  File are split in equally long files, where the duration is fixed 5 minutes (will be configurable in th efuture)  
  Files are stored in a new folder called like the original file  
  Files are names 01.mp3, 02.mp3 etc...  
  MP3 metadata are copied from the original MP£, but adding the "part" information... if it is possible.

  Subrtasks:
  + Implement core MP3 splitting engine.
  + implement test of it
  + Implement automated directory organization for split parts (`part_NN.mp3`).
  + Ad the functionality to the UI (complete the feature)
  
- Feature: Config 
  Add a config.txt file. 
  It has to contain the fields: MP3SPLIT_BINS_FOLDER and SPLIT_FIXED_DURATION_MINUTES.

## Done

- Implement UI elements:
  + Modernize Look & Feel using `tkinter.ttk`.
  + Improve Layout (Header, Selected File Display, Status/Log Area).
  + Integrate File Selection visibility and Split trigger.
  + Enhance Error Handling/Feedback.
