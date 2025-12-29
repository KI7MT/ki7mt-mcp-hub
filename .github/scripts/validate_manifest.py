#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

# Modified to accept a target directory via CLI, defaulting to the current directory
def fail(msg: str) -> None:
    print(f"[manifest] ERROR: {msg}", file=sys.stderr)
    sys.exit(1)

def main() -> None:
    # Look for the manifest relative to the target directory
    # Usage: ./validate_manifest.py adif-mcp
    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    manifest_path = target_dir / "src/adif_mcp/mcp/manifest.json"

    if not manifest_path.exists():
        fail(f"missing {manifest_path}")

    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"invalid JSON: {e}")

    if "tools" not in data or not isinstance(data["tools"], list):
        fail("manifest.tools missing or not a list")

    required_tool_keys = {"name", "description", "input_schema", "output_schema"}
    for i, tool in enumerate(data["tools"], 1):
        if not isinstance(tool, dict):
            fail(f"tool #{i} is not an object")
        missing = required_tool_keys - tool.keys()
        if missing:
            fail(f"tool #{i} missing keys: {sorted(missing)}")

    print(f"[manifest] OK: {manifest_path}")

if __name__ == "__main__":
    main()
