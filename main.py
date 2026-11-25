"""One Line, Big Laugh — make.fun bounty u-coral-404-one-line-big-laugh-328fb857.

Writes a single hilarious line to $OUTPUT_DIR/entry.txt (default /output).
Stdlib only, no network, no external input.
Gate: UTF-8, 1-200 characters, not whitespace-only, single line.
"""
import os

FINAL_TEXT = (
    "My resume says I'm a time traveller, but the interviewer "
    "only asked why I left my last job in 2087."
)


def validate_entry(text):
    """Return True iff text passes the sealed-scorer gate."""
    if not isinstance(text, str):
        return False
    if not 1 <= len(text) <= 200:
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    return True


def main():
    # Gate guard: never write an entry that would score Valid 0.
    if not validate_entry(FINAL_TEXT):
        raise SystemExit("FINAL_TEXT fails the 1-200 char single-line gate")
    output_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(FINAL_TEXT)


if __name__ == "__main__":
    main()
