import subprocess
import sys
from pathlib import Path

def test_missing_u_exits_with_error():
    script = Path(__file__).resolve().parents[1] / "s3d.py"
    proc = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    assert proc.returncode != 0
    assert proc.stderr, "Expected an error message"
