import unittest
import os
import shutil
import tempfile
from pathlib import Path
import yaml as _yaml
from libs.splitter import (
    MP3Splitter,
    DEFAULT_PROVENANCE,
    UI_TEXT_FILE,
    load_provenance,
)
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, COMM, TRK

class TestMP3Splitter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture_path = 'tests/fixtures/sample.mp3'
        cls.output_dir = 'tests/output_test'
        cls.splitter = MP3Splitter()

    def setUp(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)

    def tearDown(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test_split_success(self):
        """Verify splitting works and creates correct filenames."""
        # sample.mp3 is ~12 seconds. Split into 5 second segments -> 3 parts.
        # We pass duration in minutes. 5 seconds = 5/60 minutes.
        parts = self.splitter.split(self.fixture_path, self.output_dir, 5/60)
        
        self.assertEqual(len(parts), 3)
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, "part_01.mp3")))
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, "part_02.mp3")))
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, "part_03.mp3")))

    def test_invalid_extension(self):
        """Ensure non-mp3 files trigger ValueError."""
        bad_file = 'tests/fixtures/not_an_audio.txt'
        with open(bad_file, 'w') as f:
            f.write("Not audio")
        
        try:
            with self.assertRaises(ValueError) as cm:
                self.splitter.split(bad_file, self.output_dir, 1.0)
            self.assertEqual(str(cm.exception), "Only MP3 files are supported.")
        finally:
            if os.path.exists(bad_file):
                os.remove(bad_file)

    def test_invalid_duration(self):
        """Ensure non-positive durations raise ValueError."""
        bad_duration = 0
        with self.assertRaises(ValueError) as cm:
            self.splitter.split(self.fixture_path, self.output_dir, bad_duration)
        self.assertEqual(str(cm.exception), "Segment duration must be greater than zero.")

    def test_file_not_found(self):
        """Ensure FileNotFoundError is raised for missing files."""
        with self.assertRaises(FileNotFoundError):
            self.splitter.split("non_existent.mp3", self.output_dir, 1.0)

    def test_default_output_folder(self):
        """The default output folder is named after the source file (no extension)."""
        self.assertEqual(
            MP3Splitter.default_output_folder("/music/DJ Session.mp3"),
            "/music/DJ Session",
        )

    def test_split_into_source_named_folder(self):
        """Segments land inside a folder created next to the source file."""
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "My Mix.mp3")
            shutil.copyfile('tests/fixtures/sample.mp3', src)
            out_dir = MP3Splitter.default_output_folder(src)
            try:
                parts = self.splitter.split(src, out_dir, 5/60)
                self.assertEqual(len(parts), 3)
                self.assertTrue(os.path.isdir(out_dir))
                for p in parts:
                    self.assertEqual(os.path.dirname(p), out_dir)
            finally:
                if os.path.exists(out_dir):
                    shutil.rmtree(out_dir)

    def test_split_file_plus_numbers_naming(self):
        """With naming='file+numbers' segments are prefixed with the source stem."""
        parts = self.splitter.split(
            self.fixture_path, self.output_dir, 5/60,
            naming=MP3Splitter.NAMING_FILE_PLUS_NUMBERS,
        )
        self.assertEqual(len(parts), 3)
        expected = [f"sample_part_{i}.mp3" for i in ("01", "02", "03")]
        self.assertEqual([os.path.basename(p) for p in parts], expected)

    def test_split_invalid_naming(self):
        """Unknown naming formats raise ValueError."""
        with self.assertRaises(ValueError) as cm:
            self.splitter.split(self.fixture_path, self.output_dir, 5/60, naming="bogus")
        self.assertIn("Unknown filename format", str(cm.exception))

    def test_metadata_preservation(self):
        """Verify metadata is copied correctly."""
        parts = self.splitter.split(self.fixture_path, self.output_dir, 5/60)
        first_part = parts[0]
        
        audio = MP3(first_part)
        self.assertIn('TIT2', audio)
        self.assertEqual(str(audio['TIT2'][0]), 'Test Title')
        self.assertIn('TPE1', audio)
        self.assertEqual(str(audio['TPE1'][0]), 'Test Artist')
        self.assertIn('TALB', audio)
        self.assertEqual(str(audio['TALB'][0]), 'Test Album')

    def test_trk_added_when_source_has_none(self):
        """Source without TRK: each part gets TRK '{part}/{total}'."""
        parts = self.splitter.split(self.fixture_path, self.output_dir, 5/60)
        for i, part in enumerate(parts, start=1):
            audio = MP3(part)
            self.assertIn('TRCK', audio)
            self.assertEqual(str(audio['TRCK'][0]), f"{i}/3")

    def test_trk_preserved_when_source_has_one(self):
        """Source with TRK: it is copied verbatim, never overridden."""
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "with_trk.mp3")
            shutil.copyfile(self.fixture_path, src)
            audio = MP3(src)
            audio.tags.add(TRK(encoding=3, text="7/18"))
            audio.save()
            out_dir = os.path.join(tmp, "out")
            try:
                parts = self.splitter.split(src, out_dir, 5/60)
                for part in parts:
                    seg = MP3(part)
                    self.assertIn('TRCK', seg)
                    self.assertEqual(str(seg['TRCK'][0]), "7/18")
            finally:
                if os.path.exists(out_dir):
                    shutil.rmtree(out_dir)

    def _provenance_frames(self, path, prov=None):
        prov = prov or self.splitter.provenance
        audio = MP3(path)
        return [f for f in audio.tags.getall('COMM')
                if f.lang == prov["lang"] and f.desc == prov["description"]]

    def test_provenance_config_matches_repo_yaml(self):
        """load_provenance parses english.yml; values must match the raw file (no drift)."""
        raw = _yaml.safe_load(UI_TEXT_FILE.read_text(encoding="utf-8"))
        comm = raw["comm"]
        loaded = load_provenance()
        self.assertEqual(loaded["lang"], str(comm["language"]))
        self.assertEqual(loaded["description"], str(comm["description"]))
        self.assertEqual(loaded["text"], str(comm["text"]).strip())

    def test_provenance_comm_added_to_every_part(self):
        """Every part carries exactly one provenance COMM frame with the configured values."""
        prov = self.splitter.provenance
        parts = self.splitter.split(self.fixture_path, self.output_dir, 5/60)
        for part in parts:
            frames = self._provenance_frames(part)
            self.assertEqual(len(frames), 1)
            self.assertEqual(list(frames[0].text), [prov["text"]])

    def test_provenance_not_duplicated_when_source_has_same_identity_frame(self):
        """A source COMM frame with the same lang+description is kept as-is, not duplicated.

        A matching frame with different text is preserved verbatim: identity is
        language + description, not the text content.
        """
        prov = self.splitter.provenance
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "with_comm.mp3")
            shutil.copyfile(self.fixture_path, src)
            audio = MP3(src)
            audio.tags.add(COMM(encoding=3, lang=prov["lang"], desc=prov["description"],
                                text=["original author's note"]))
            audio.save()
            out_dir = os.path.join(tmp, "out")
            try:
                parts = self.splitter.split(src, out_dir, 5/60)
                for part in parts:
                    frames = self._provenance_frames(part)
                    self.assertEqual(len(frames), 1)
                    self.assertEqual(list(frames[0].text), ["original author's note"])
            finally:
                if os.path.exists(out_dir):
                    shutil.rmtree(out_dir)

    def test_load_provenance_reads_distinct_temp_yaml(self):
        """Loading a valid YAML file returns its actual values (not the fallback)."""
        custom = {"language": "ita", "description": "Origine",
                  "text": "File originale suddiviso con Music Splitter."}
        with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as f:
            _yaml.safe_dump({"comm": custom}, f, allow_unicode=True)
            path = Path(f.name)
        try:
            loaded = load_provenance(path)
            self.assertEqual(loaded["lang"], custom["language"])
            self.assertEqual(loaded["description"], custom["description"])
            self.assertEqual(loaded["text"], custom["text"])
        finally:
            path.unlink()

    def test_load_provenance_fallbacks(self):
        """Missing files, invalid YAML and missing 'comm' section fall back to defaults."""
        self.assertEqual(load_provenance(Path("does/not/exist.yml")), DEFAULT_PROVENANCE)
        with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as f:
            f.write("main description: |>\n  broken scalar header\n")
            bad = Path(f.name)
        with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as f:
            _yaml.safe_dump({"unrelated": True}, f)
            no_comm = Path(f.name)
        try:
            self.assertEqual(load_provenance(bad), DEFAULT_PROVENANCE)
            self.assertEqual(load_provenance(no_comm), DEFAULT_PROVENANCE)
        finally:
            bad.unlink()
            no_comm.unlink()

    def test_custom_provenance_injection(self):
        """An explicit provenance mapping overrides the configured one."""
        prov = {"lang": "fra", "description": "Provenance",
                "text": "Fichier original decoupe avec Music Splitter."}
        splitter = MP3Splitter(provenance=prov)
        parts = splitter.split(self.fixture_path, self.output_dir, 5/60)
        for part in parts:
            frames = self._provenance_frames(part, prov)
            self.assertEqual(len(frames), 1)
            self.assertEqual(list(frames[0].text), [prov["text"]])

if __name__ == '__main__':
    unittest.main()
