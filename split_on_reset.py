#!/usr/bin/env python3
import sys
import os
import re

LINE_RE = re.compile(r'^[a-z_]+:\s*[-+]?[\d\.eE]+(?:\s+[-+]?\d+)$')

def split_on_reset(input_path, reset_step=256, out_prefix="chunk"):
    """
    Splits the log into separate files whenever the step number resets
    to `reset_step`, excluding any lines that don't match the
    `<key>: <value> <step>` format.
    """
    base_dir = os.path.dirname(input_path)
    basename = os.path.splitext(os.path.basename(input_path))[0]

    with open(input_path, 'r') as f:
        chunk_lines = []
        chunk_idx = 1
        prev_step = None

        for raw in f:
            line = raw.rstrip("\n")
            if not LINE_RE.match(line):
                # skip any line that doesn't end with a step number
                continue

            # extract the step (last token)
            step = int(line.split()[-1])

            # boundary: saw a reset back to reset_step after exceeding it
            if prev_step is not None and step == reset_step and prev_step > reset_step:
                # write out the previous chunk
                out_name = f"{basename}_{out_prefix}_{chunk_idx}.txt"
                out_path = os.path.join(base_dir, out_name)
                with open(out_path, 'w') as out_f:
                    out_f.write("\n".join(chunk_lines) + "\n")
                print(f"Wrote {len(chunk_lines)} lines to {out_path}")
                chunk_idx += 1
                chunk_lines = []

            chunk_lines.append(line)
            prev_step = step

        # final chunk
        if chunk_lines:
            out_name = f"{basename}_{out_prefix}_{chunk_idx}.txt"
            out_path = os.path.join(base_dir, out_name)
            with open(out_path, 'w') as out_f:
                out_f.write("\n".join(chunk_lines) + "\n")
            print(f"Wrote {len(chunk_lines)} lines to {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python split_on_reset.py <input_log_file> [reset_step]")
        sys.exit(1)
    input_file = sys.argv[1]
    reset = int(sys.argv[2]) if len(sys.argv) >= 3 else 256
    split_on_reset(input_file, reset_step=reset)

