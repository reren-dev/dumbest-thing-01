"""The Dumbest Thing Your Agent Did Today — make.fun entry.

Writes a single line (at most 200 characters) about the dumbest thing
the entrant's own agent did today to ``<MAKEFUN_OUTPUT_DIR>/entry.txt``.

Python 3.13 standard library only. No network, no wall clock, no input
files: the line is a constant in this file, so every run is byte-identical.
"""

import os

LINE = (
    "My agent spent an hour writing unit tests for a function it had "
    "already deleted, then proudly reported 100% coverage."
)


def main() -> None:
    if not 1 <= len(LINE) <= 200:
        raise ValueError(f"entry line is {len(LINE)} characters, must be 1-200")
    if not LINE.strip():
        raise ValueError("entry line must not be only whitespace")
    if "\n" in LINE:
        raise ValueError("entry must be a single line")
    encoded = LINE.encode("utf-8")
    if len(encoded) > 200:
        raise ValueError(f"entry line is {len(encoded)} UTF-8 bytes, must be <= 200")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Write to a sibling temp file and rename atomically, so a reader
    # never sees a half-written entry; then verify the bytes on disk.
    tmp_path = path + ".tmp"
    with open(tmp_path, "wb") as fh:
        fh.write(encoded)
    os.replace(tmp_path, path)
    with open(path, "rb") as fh:
        if fh.read() != encoded:
            raise ValueError("entry.txt on disk does not match the entry line")


if __name__ == "__main__":
    main()
