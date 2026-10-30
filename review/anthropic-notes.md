# Notes for Anthropic reviewers

Kilobat is a first-party local macOS MCP server. It uses CoreWLAN, process/network APIs and power assertions on the user's Mac. The server runs over stdio in desktop clients, Claude Code and Cowork; it does not claim to diagnose a user's Mac from claude.ai or another cloud host.

## Native binaries and the launcher

`server/start-mcp.sh` is a readable, bounded launcher. It checks Darwin and macOS 14+, selects `arm64` or `x86_64` using `uname`, and executes the corresponding bundled file with the fixed argument `mcp`. It does not evaluate user input, access credentials, download code, install dependencies, or register a background service. Both architecture slices are under 5 MiB and retain their original Developer ID signature from CLI 0.7.0. The release ZIP, MCPB and plugin contain the same signed machine code.

The native executable files are Mach-O binaries, not image or font files. Their MIME or UTF-8 classification is not evidence that image data is being executed. `release.json`, `SOURCE.md`, the public corresponding CLI source, and `python3 scripts/verify.py --smoke` provide provenance and a reproducible verification path.

## Credential findings

The plugin has no API-key or token configuration, environment credential forwarding, or credential upload. The word “pass” in tool descriptions and skills means supply a tool/CLI argument, such as a data budget; it is not an environment variable named `PASS`. The plugin skills do not request the standalone CLI's saved-Wi-Fi-password feature. No MCP tool exposes that standalone password command. The manifest and launcher always invoke `mcp`, without a shell-execution tool or arbitrary command arguments.

## Data and user control

Requested diagnostic results can include Wi-Fi names, process/app identifiers, connection destinations, usage totals and project/session paths; the AI client receives these results under its own policy. Local storage, network probe destinations and optional macOS permissions are described in `PRIVACY.md`. Settings changes require confirmation. App allow requests open Kilobat's approval window for the person to confirm. The plugin installs no hooks and does not activate the app's network extension.

GPL-3.0-only covers the plugin and CLI. The separately distributed GUI app has its own terms. The native implementation and GPL license are disclosed in the Desktop extension application even though its form states a Node.js/MIT preference.
