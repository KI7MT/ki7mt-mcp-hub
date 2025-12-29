import json
import sys
from pathlib import Path

def validate_manifests():
    root = Path(__file__).parent.parent.parent
    # Find all manifest.json files in any subdirectory
    manifests = list(root.glob("**/manifest.json"))

    if not manifests:
        print("No manifest.json files found to validate.")
        return True

    success = True
    for manifest_path in manifests:
        # Skip manifests in build or temp directories if they exist
        if "site" in str(manifest_path) or ".venv" in str(manifest_path):
            continue

        print(f"Checking: {manifest_path.relative_to(root)}")
        try:
            with open(manifest_path, 'r') as f:
                data = json.load(f)

            # Add your specific validation logic here (checking keys, etc.)
            if "mcp" not in data:
                print(f"  FAILED: Missing 'mcp' key in {manifest_path.name}")
                success = False
            else:
                print("  PASSED")

        except Exception as e:
            print(f"  FAILED: Could not parse JSON: {e}")
            success = False

    return success

if __name__ == "__main__":
    if not validate_manifests():
        sys.exit(1)
