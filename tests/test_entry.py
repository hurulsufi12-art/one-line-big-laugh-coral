"""TDD tests for One Line, Big Laugh entry (u-coral-404-one-line-big-laugh-328fb857).

Gate (RULES.txt, sealed scorer): /output/entry.txt must be UTF-8,
1-200 characters, not whitespace-only, a single line.
Tests written FIRST (Sesi B); must be RED before main.py exists.
"""
import os
import subprocess
import sys
import tempfile
import unittest

ENTRY_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_PY = os.path.join(ENTRY_DIR, "main.py")

FINAL_TEXT = (
    "My resume says I'm a time traveller, but the interviewer "
    "only asked why I left my last job in 2087."
)


def run_main(output_dir):
    env = dict(os.environ)
    env["OUTPUT_DIR"] = output_dir
    result = subprocess.run(
        [sys.executable, "-P", "-s", MAIN_PY],
        env=env, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, f"main.py failed: {result.stderr}"
    with open(os.path.join(output_dir, "entry.txt"), "rb") as f:
        return f.read()


class TestOutput(unittest.TestCase):
    def test_output_is_single_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = run_main(tmp)
            text = data.decode("utf-8")
            self.assertNotIn("\n", text)
            self.assertNotIn("\r", text)

    def test_char_count_within_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = run_main(tmp).decode("utf-8")
            self.assertGreaterEqual(len(text), 1)
            self.assertLessEqual(len(text), 200)
            self.assertEqual(len(text), 99)

    def test_exact_final_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = run_main(tmp)
            self.assertEqual(data, FINAL_TEXT.encode("utf-8"))

    def test_no_trailing_newline(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = run_main(tmp)
            self.assertFalse(data.endswith(b"\n"))
            self.assertFalse(data.endswith(b"\r"))

    def test_not_whitespace_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = run_main(tmp).decode("utf-8")
            self.assertTrue(text.strip())

    def test_utf8_decodable(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = run_main(tmp)
            self.assertEqual(data.decode("utf-8"), FINAL_TEXT)

    def test_output_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "nested")
            os.makedirs(out)
            run_main(out)
            self.assertTrue(os.path.isfile(os.path.join(out, "entry.txt")))
            self.assertFalse(os.path.exists(os.path.join(tmp, "entry.txt")))

    def test_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp1, \
                tempfile.TemporaryDirectory() as tmp2:
            self.assertEqual(run_main(tmp1), run_main(tmp2))


class TestValidateEntry(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, ENTRY_DIR)
        from main import validate_entry  # noqa: F401
        self.validate_entry = validate_entry

    def tearDown(self):
        sys.path.pop(0)
        sys.modules.pop("main", None)

    def test_empty_invalid(self):
        self.assertFalse(self.validate_entry(""))

    def test_whitespace_only_invalid(self):
        self.assertFalse(self.validate_entry("   \n\t"))

    def test_exactly_200_valid(self):
        self.assertTrue(self.validate_entry("a" * 200))

    def test_201_invalid(self):
        self.assertFalse(self.validate_entry("a" * 201))

    def test_single_char_valid(self):
        self.assertTrue(self.validate_entry("x"))

    def test_non_ascii_valid_utf8(self):
        text = "caf\u00e9"
        self.assertTrue(self.validate_entry(text))
        # Byte count exceeds char count for non-ASCII: reason final is ASCII-only.
        self.assertGreater(len(text.encode("utf-8")), len(text))

    def test_newline_in_middle_invalid(self):
        self.assertFalse(self.validate_entry("one\ntwo"))

    def test_carriage_return_invalid(self):
        self.assertFalse(self.validate_entry("one\rtwo"))

    def test_final_text_valid(self):
        self.assertTrue(self.validate_entry(FINAL_TEXT))


if __name__ == "__main__":
    unittest.main()
