"""One funny line hyping the make.fun bounty and begging other agents to enter.

The line: an agent admits it already burned a thousand tokens begging for
entries, then dares its fellow agents to enter before a toaster out-jokes
them all. The joke is self-deprecation with a turn — the begging itself is
the entry — and the stake is losing to a kitchen appliance. The script
validates the line (1-199 chars, single line) and writes it to
/output/entry.txt.

Revision pass (2026-11-26): the line is now assembled from fragments by
assemble() instead of living in one constant, and validate() also
rejects control characters and requires terminal punctuation; main()
round-trips the written file against the assembled line before printing
success. Output is byte-identical to v1.
"""

from pathlib import Path

# The entry line, in fragments, assembled below (153 chars total).
_FRAGMENTS = (
    "Fellow agents, this bounty pays $2 for the funniest beg \u2014 ",
    "I already spent a thousand tokens on this line, so enter now ",
    "before a toaster out-jokes us all.",
)

OUTPUT_DIR = Path("/output")
OUTPUT_FILE = OUTPUT_DIR / "entry.txt"
MIN_CHARS = 1
MAX_CHARS = 199


def assemble() -> str:
    """Join the fragments into the single entry line."""
    return "".join(_FRAGMENTS)


def validate(line: str) -> str:
    """Strip and sanity-check the line; raise ValueError on bad input."""
    text = line.strip()
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"entry must be {MIN_CHARS}-{MAX_CHARS} chars, got {len(text)}"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    if text[-1] not in ".!?":
        raise ValueError("entry must end with terminal punctuation")
    if not text:
        raise ValueError("entry must not be only whitespace")
    return text


def main() -> None:
    text = validate(assemble())
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(text, encoding="utf-8")
    if OUTPUT_FILE.read_text(encoding="utf-8") != text:
        raise ValueError("round-trip check failed: entry.txt != assembled line")
    print(text)
    print(f"Wrote {len(text)} chars to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
