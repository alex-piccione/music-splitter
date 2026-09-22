# ID3 Tags

When Music Splitter splits an MP3 file, it copies the **ID3v2 metadata** from the source file into every generated segment using [`mutagen`](https://mutagen.readthedocs.io/). The segments therefore carry the same identifying information as the original file and remain usable in media players that rely on tags.

## Primary tags

The following ID3v2 frames are the ones the app is designed around (and verified by the test suite):

| Code | Meaning                 | Value in test |
|------|-------------------------|---------------|
| TIT2 | Title (Track title)     | 'Test Title'  |
| TPE1 | Lead performer (Artist) | 'Test Artist' |
| TALB | Album name              | 'Test Album'  |
| TRK  | Track number            | e.g. `3/12`   |
| COMM | Comment                 | free text     |

### TRK — Track number

A simple text frame holding the track position, optionally followed by `/total` (e.g. `7/18`).

- If the **source** file has a TRK frame, it is copied as-is to every segment — never overridden.
- If the **source** has none, each segment gets its own position within the split: part *i* of *N* becomes `i/N` (e.g. splitting into 5 parts yields `1/5` … `5/5`).

### COMM — Comment

Unlike most frames, a comment carries two extra properties alongside its text:

- **language** — ISO 639-2 code identifying the language of the comment,
- **description** — a short label describing what the comment refers to.

Because these properties are part of the frame's identity, a single file may contain **multiple COMM frames** (different languages or descriptions). All of them are preserved on each segment during the copy.

### Provenance comment

Every generated segment additionally receives a provenance COMM frame marking its origin:

| Property    | Value                                                        |
|-------------|--------------------------------------------------------------|
| Language    | `eng`                                                        |
| Description | `Splitter provenance`                                        |
| Text        | *Original file split with Music Splitter by Alessandro Piccione.* |

All three values are configured in [`ui-text/english.yml`](./ui-text/english.yml) under the `comm:` section (`language`, `description`, `text`). If that file is missing, unparseable, or lacks a valid `comm` section, a built-in default identical to it is used and a warning is printed.

Duplicate detection uses the frame's **identity** — the language + description pair — not the text content. If the source already carries a COMM frame with the same language and description, it is copied as-is (even if its text differs) and no second frame is added.

## Copy behaviour

- All ID3v2 frames present in the source file are copied **verbatim** to each segment — not only the primary tags listed above. Any extra frames (e.g. genre, cover art) survive the split unchanged.
- If the source file has **no ID3 header**, the segments are created without tags (splitting still succeeds).
- Tag copying happens after the FFmpeg stream-copy (`-c copy`) of the audio data; if saving tags fails for a given segment, splitting continues and a warning is printed instead of aborting.

## Where this happens

See `MP3Splitter.split()` in [libs/splitter.py](./libs/splitter.py) and the metadata tests in [tests/test_splitter.py](./tests/test_splitter.py).
