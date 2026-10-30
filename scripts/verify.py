#!/usr/bin/env python3
"""Validate the distributable and optionally exercise its real, local MCP server."""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HINTS = ("readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint")


def rpc(method, identifier=None, params=None):
    return {"jsonrpc": "2.0", "method": method,
            **({"id": identifier} if identifier is not None else {}),
            **({"params": params} if params is not None else {})}


def inspect_server(smoke=False):
    messages = [rpc("initialize", 1, {"protocolVersion": "2025-06-18", "capabilities": {},
                                      "clientInfo": {"name": "kilobat-plugin-verify", "version": "1"}}),
                rpc("notifications/initialized"), rpc("tools/list", 2)]
    if smoke:
        for identifier, name, arguments in [(3, "get_status", {}),
                                            (4, "diagnose_network", {}),
                                            (5, "get_conditions", {}),
                                            (6, "list_rules", {}),
                                            (7, "list_sessions", {"days": 1})]:
            messages.append(rpc("tools/call", identifier, {"name": name, "arguments": arguments}))
        for identifier, name, arguments in [(8, "not_a_kilobat_tool", {}),
                                            (9, "get_usage_report", {"days": True}),
                                            (10, "run_speedtest", {"budget_mb": "10"})]:
            messages.append(rpc("tools/call", identifier, {"name": name, "arguments": arguments}))
    run = subprocess.run([str(ROOT / "server/kilobat"), "mcp"],
                         input="".join(json.dumps(m) + "\n" for m in messages),
                         text=True, capture_output=True, check=True, timeout=90)
    replies = {r["id"]: r for r in map(json.loads, run.stdout.splitlines()) if "id" in r}
    assert replies[1]["result"]["serverInfo"]["name"] == "kilobat"
    tools = replies[2]["result"]["tools"]
    for tool in tools:
        assert tool.get("title"), (tool["name"], "missing title")
        assert tool["inputSchema"].get("type") == "object", tool["name"]
        for hint in HINTS:
            assert type(tool.get("annotations", {}).get(hint)) is bool, (tool["name"], hint)
        if not tool["annotations"]["readOnlyHint"]:
            assert "confirmation" in tool["description"], tool["name"]
    if smoke:
        for identifier in range(3, 8):
            assert "error" not in replies[identifier], (identifier, "RPC error")
            assert not replies[identifier]["result"].get("isError"), (identifier, "tool error")
        status = replies[3]["result"]["structuredContent"]
        assert {"connected", "metered", "apps", "downloadBytesPerSecond"} <= status.keys()
        diagnosis = replies[4]["result"]["structuredContent"]
        assert diagnosis["health"] in {"good", "degraded", "poor", "unknown"} and diagnosis["advice"]
        assert {"power", "metered", "lowDataMode", "advice"} <= replies[5]["result"]["structuredContent"].keys()
        assert {"profile", "filteringActive"} <= replies[6]["result"]["structuredContent"].keys()
        sessions = replies[7]["result"]
        assert isinstance(json.loads(sessions["content"][0]["text"]), list)
        for identifier in range(8, 11):
            assert replies[identifier].get("error", {}).get("code") == -32602, identifier
        print("PASS: five real read-only workflows and three invalid-request safeguards")
    return tools


def verify(smoke=False):
    release = json.loads((ROOT / "release.json").read_text())
    binary = ROOT / "server/kilobat"
    assert hashlib.sha256(binary.read_bytes()).hexdigest() == release["binarySHA256"]
    assert binary.stat().st_mode & 0o111, "Bundled server must stay executable"
    skills = list((ROOT / "skills").glob("*/SKILL.md"))
    assert len(skills) == release["skillCount"]
    for skill in skills:
        text = skill.read_text()
        assert text.startswith("---\n")
        header = text.split("---", 2)[1]
        assert re.search(r"^name: " + re.escape(skill.parent.name) + r"$", header, re.M)
        assert re.search(r"^description: .+", header, re.M)
        for link in re.findall(r"\]\(([^)]+)\)", text):
            if not re.match(r"[a-z]+:|#", link):
                assert (skill.parent / link.split("#")[0]).exists(), (skill, link)
    for path in ["plugin.json", ".claude-plugin/plugin.json", ".grok-plugin/plugin.json"]:
        manifest = json.loads((ROOT / path).read_text())
        assert manifest["name"] == "kilobat" and manifest["version"] == release["pluginVersion"]
        assert manifest["license"] == "GPL-3.0-only"
        assert not manifest.get("hooks") and not manifest.get("apps")
    portable = json.loads((ROOT / "plugin.json").read_text())["extensions"]["com.openai"]
    assert portable["requires_local_executor"] is True
    assert (ROOT / portable["onboardingSkill"]).is_file()
    for asset in ["composerIcon", "logo"]:
        assert (ROOT / portable["interface"][asset]).is_file()
    mcp = json.loads((ROOT / "mcp.json").read_text())["mcpServers"]["kilobat"]
    assert mcp == {"type": "stdio", "command": "${PLUGIN_ROOT}/server/kilobat", "args": ["mcp"]}
    for path in ROOT.rglob("*"):
        if path.is_symlink():
            raise AssertionError("Package must not contain symbolic links: " + str(path))
    if sys.platform == "darwin":
        subprocess.run(["codesign", "--verify", "--strict", str(binary)], check=True)
        identity = subprocess.run(["codesign", "-dv", "--verbose=2", str(binary)], capture_output=True, text=True, check=True).stderr
        assert "TeamIdentifier=" + release["signingTeam"] in identity
        assert "arm64" in subprocess.check_output(["lipo", "-archs", str(binary)], text=True)
        assert "x86_64" in subprocess.check_output(["lipo", "-archs", str(binary)], text=True)
        tools = inspect_server(smoke)
        assert len(tools) == release["toolCount"]
        print(f"PASS: {len(tools)} MCP tools, complete annotations, signed universal CLI")
    elif smoke:
        raise SystemExit("Live MCP verification requires macOS 14 or newer")
    print(f"PASS: {len(skills)} skills, three manifests, portable MCP config, assets and pinned binary")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    verify(parser.parse_args().smoke)
