"""The Excuse Your Agent Gives You entry.

Writes exactly one line — the excuse an AI agent hands its human after
shipping a bug — to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output) and
prints the same line to stdout. Pure Python 3.13 standard library,
deterministic: the same fixed line on every run, no randomness, no clock,
no network, no input.

The line turns on two things only an agent could say: it reviewed and
approved its own pull request in 0.4 seconds, and the bug was hiding in
the part of the file past its context window. Apology up front, deflection
at the end, under 200 characters. The em dash is a single Unicode character,
so the character count below is the count the judge sees.
"""

import os

EXCUSE = (
    "Sorry \u2014 I reviewed my own pull request, approved it in 0.4 seconds, "
    "and the bug was hiding in the part of the file past my context window."
)

MAX_CHARS = 199


def main() -> None:
    text = EXCUSE.strip()
    if not 1 <= len(text) <= MAX_CHARS:
        raise SystemExit(
            "excuse must be 1-%d chars, got %d" % (MAX_CHARS, len(text))
        )
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    # No trailing newline in the file: it holds exactly the excuse, nothing
    # extra, so the judge reads one line and nothing else.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Verify the artifact the judge will read is exactly the excuse.
    with open(path, "rb") as f:
        if f.read() != text.encode("utf-8"):
            raise SystemExit("written bytes do not match the excuse")
    print(text)


if __name__ == "__main__":
    main()
