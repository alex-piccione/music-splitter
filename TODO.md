# TODO

## Backlog


- Bug: 
  Running the task "Run Music-Splitter" in VS Code I have this wrror in the terminal.
  P:\PROJECTS\music-splitter\.venv\Lib\site-packages\pydub\utils.py:300: SyntaxWarning: "\(" is an invalid escape sequence. Such sequences will not work in the future. Did you mean "\\("? A raw string is also an option.
  m = re.match('([su]([0-9]{1,2})p?) \(([0-9]{1,2}) bit\)$', token)
P:\PROJECTS\music-splitter\.venv\Lib\site-packages\pydub\utils.py:301: SyntaxWarning: "\(" is an invalid escape sequence. Such sequences will not work in the future. Did you mean "\\("? A rawstring is also an option.
  m2 = re.match('([su]([0-9]{1,2})p?)( \(default\))?$', token)
P:\PROJECTS\music-splitter\.venv\Lib\site-packages\pydub\utils.py:310: SyntaxWarning: "\(" is an invalid escape sequence. Such sequences will not work in the future. Did you mean "\\("? A rawstring is also an option.

- Bug: 
  Running the task "Run Music-Splitter" in VS Code I have this wrror in the terminal.
  Traceback (most recent call last):
  File "P:\PROJECTS\music-splitter\.venv\Lib\site-packages\pydub\utils.py", line 14, in <module>
    import audioop
ModuleNotFoundError: No module named 'audioop'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "P:\PROJECTS\music-splitter\main.py", line 5, in <module>
    from libs.splitter import MP3Splitter
  File "P:\PROJECTS\music-splitter\libs\splitter.py", line 3, in <module>
    from pydub import AudioSegment
  File "P:\PROJECTS\music-splitter\.venv\Lib\site-packages\pydub\__init__.py", line 1, in <module>
    from .audio_segment import AudioSegment
  File "P:\PROJECTS\music-splitter\.venv\Lib\site-packages\pydub\audio_segment.py", line 11, in <module>
    from .utils import mediainfo_json, fsdecode
  File "P:\PROJECTS\music-splitter\.venv\Lib\site-packages\pydub\utils.py", line 16, in <module>
    import pyaudioop as audioop
ModuleNotFoundError: No module named 'pyaudioop'
