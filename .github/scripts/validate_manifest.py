import json
import sys
from pathlib import Path

def validate_manifests():
    # Set root to the repo root regardless of where script is called
    root = Path(__file__).parent.parent.parent
    manifests = list(root.glob("**/manifest.json"))

    if not manifests:
        print("No manifest.json files found to validate.")
        return True

    success = True
    for manifest_path in manifests:
        # Avoid build artifacts or environments
        if any(x in str(manifest_path) for x in ["site", ".venv", "temp"]):
            continue

        print(f"Checking: {manifest_path.relative_to(root)}")
        try:
            with open(manifest_path, 'r') as f:
                data = json.load(f)

            # These are the keys found in your adif-mcp manifest
            required_keys = ["name", "version", "components"]

            missing = [k for k in required_keys if k not in data]

            if missing:
                print(f"  FAILED: Missing required keys {missing}")
                success = False
            else:
                # Basic check for your 'components' structure
                if "schemas" not in data.get("components", {}):
                    print("  FAILED: 'components' missing 'schemas' table")
                    success = False
                else:
                    print(f"  PASSED (v{data['version']})")

        except Exception as e:
            print(f"  FAILED: Could not parse JSON: {e}")
            success = False

    return success

if __name__ == "__main__":
    if not validate_manifests():
        sys.exit(1)
