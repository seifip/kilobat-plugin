#!/usr/bin/env python3
"""Build a deterministic ZIP and check the extracted distribution."""
import hashlib
import json
import pathlib
import shutil
import stat
import subprocess
import tempfile
import zipfile
from verify import ROOT, verify

verify()
version = json.loads((ROOT / "release.json").read_text())["pluginVersion"]
output = ROOT / "dist"
output.mkdir(exist_ok=True)
archive = output / f"kilobat-plugin-{version}.zip"
names = ["plugin.json", "mcp.json", ".mcp.json", ".claude-plugin", ".grok-plugin", "skills", "assets", "server",
         "README.md", "LICENSE", "SOURCE.md", "PRIVACY.md", "SECURITY.md", "release.json", "review", "scripts"]
files = sorted(p for name in names for p in ([ROOT / name] if (ROOT / name).is_file() else (ROOT / name).rglob("*"))
               if p.is_file() and "__pycache__" not in p.parts)
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
    for path in files:
        entry = zipfile.ZipInfo(path.relative_to(ROOT).as_posix(), date_time=(2020, 1, 1, 0, 0, 0))
        entry.create_system = 3
        entry.compress_type = zipfile.ZIP_DEFLATED
        entry.external_attr = (stat.S_IFREG | (0o755 if path == ROOT / "server/kilobat" else 0o644)) << 16
        z.writestr(entry, path.read_bytes())
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
(output / "SHA256SUMS").write_text(f"{digest}  {archive.name}\n")
with tempfile.TemporaryDirectory(prefix="kilobat-plugin-check-") as temp:
    extracted = pathlib.Path(temp)
    with zipfile.ZipFile(archive) as z:
        z.extractall(extracted)
        for item in z.infolist():
            (extracted / item.filename).chmod((item.external_attr >> 16) & 0o777)
    subprocess.run(["python3", str(extracted / "scripts/verify.py")], check=True)
print(f"Built {archive.name} ({archive.stat().st_size:,} bytes), SHA256 {digest}")
