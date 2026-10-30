#!/usr/bin/env python3
"""Recreate the signed universal CLI and build a Claude Desktop MCPB."""
import hashlib
import json
import pathlib
import stat
import subprocess
import tempfile
import zipfile
from verify import ROOT, verify

verify()
release = json.loads((ROOT / "release.json").read_text())
version = release["pluginVersion"]
output = ROOT / "dist"
output.mkdir(exist_ok=True)
archive = output / f"kilobat-mcp-{version}.mcpb"
with tempfile.TemporaryDirectory(prefix="kilobat-mcpb-") as temp:
    binary = pathlib.Path(temp) / "kilobat"
    subprocess.run(["lipo", "-create", str(ROOT / "server/darwin-x86_64/kilobat"),
                    str(ROOT / "server/darwin-arm64/kilobat"), "-output", str(binary)], check=True)
    # lipo may change universal-file padding, while the signed slices must be exact.
    for arch, digest in release["binarySlices"].items():
        thin = pathlib.Path(temp) / arch
        subprocess.run(["lipo", str(binary), "-thin", arch, "-output", str(thin)], check=True)
        assert hashlib.sha256(thin.read_bytes()).hexdigest() == digest, arch
    subprocess.run(["codesign", "--verify", "--strict", str(binary)], check=True)
    files = {"server/kilobat": binary.read_bytes(), "manifest.json": (ROOT / "mcpb-manifest.json").read_bytes(),
             "icon.png": (ROOT / "assets/icon.png").read_bytes(), "LICENSE.txt": (ROOT / "LICENSE").read_bytes(),
             "PRIVACY.md": (ROOT / "PRIVACY.md").read_bytes(), "SOURCE.md": (ROOT / "SOURCE.md").read_bytes()}
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(files.items()):
            entry = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = (stat.S_IFREG | (0o755 if name == "server/kilobat" else 0o644)) << 16
            z.writestr(entry, data)
checksums = sorted(output.glob(f"*-{version}.zip")) + [archive]
(output / "SHA256SUMS").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in checksums))
print(f"Built {archive.name} ({archive.stat().st_size:,} bytes)")
