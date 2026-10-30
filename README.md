# Kilobat plugin

Diagnose slow or unreliable internet on a Mac with measured Wi-Fi signal, router and internet latency, jitter, packet loss, DNS, captive portals, per-app bandwidth, and data usage. Find why one site or API fails, protect a hotspot data budget, prepare for a video call, and keep a long agent run awake.

This package includes **43 local MCP tools, nine networking skills, a setup skill, and the signed Kilobat CLI for Intel and Apple silicon 0.7.0**. It runs on macOS 14 or later, on Intel and Apple silicon. No account, API key, Homebrew installation, hosted relay, or external runtime is required. It measures the Mac where the server runs; a cloud or Linux agent cannot use it to measure a different Mac.

## Install

### Claude Code

```text
/plugin marketplace add seifip/kilobat-plugin
/plugin install kilobat@kilobat
```

Restart or reconnect the MCP client and run the `kilobat-setup` skill. Claude Desktop users can also download the [signed MCPB bundle](https://github.com/seifip/kilobat-plugin/releases/download/v0.7.2/kilobat-mcp-0.7.2.mcpb) and install it through Settings → Extensions. MCPB installs the tools; this Git plugin additionally includes the skills.

### Grok Build

```sh
grok plugin install seifip/kilobat-plugin
```

Review the requested trust and enable the plugin. The Grok manifest configures the bundled local server. The official marketplace listing is subject to xAI review; a source-repo install works independently of that listing.

### ChatGPT desktop and Codex

The release ZIP uses the current Agent Plugins format: root `plugin.json`, `mcp.json`, `skills/` and `assets/`, with `requires_local_executor: true`. Install the ZIP or folder through the desktop client's local-plugin installation flow. Public local-MCP directory submissions require OpenAI partner approval; uploading or building a package does not mean it is listed. The package includes no lifecycle hooks or external app references.

## Ask Kilobat

- “Why is my Mac's internet slow? Find which layer is failing.”
- “What is using all my hotspot data?”
- “Check the network before my video call.”
- “Why can this browser reach an API but my agent can't?”
- “Did my agent finish, fail, or just go quiet?”
- “Keep my Mac awake for this build.”

## Skills

| Skill | What it covers |
|---|---|
| `kilobat-setup` | First connection, platform checks, permissions and data handling |
| `kilobat` | Routes the task to the right skill and sets measurement/safety conventions |
| `mac-network-troubleshooting` | Finds the failing Wi-Fi, router, internet, DNS, proxy or HTTP layer |
| `mac-wifi-troubleshooting` | Weak signal, crowded channels, roaming and periodic latency spikes |
| `mac-hotspot-data-saver` | Metered connections, data use, Travel profile and budgets |
| `mac-dns-troubleshooting` | DNS lookup timing, resolver comparisons and approved DNS fixes |
| `video-call-network-check` | Jitter, loss, latency spikes, bufferbloat and competing uploads |
| `mac-bandwidth-monitor` | Live app traffic, usage history and process destinations |
| `mac-app-firewall` | Approved app/domain rules, pending app approvals and enforcement checks |
| `mac-agent-runs` | Keep-awake, power/network conditions and agent session state |

## Permissions, data and optional app features

Diagnostic reads do not change network settings. Network probes contact the destinations documented in [PRIVACY.md](PRIVACY.md). Requested tool results are shared with the connected AI client, so its data policies apply. History is stored locally by the Kilobat app. No telemetry or cloud account is added by this plugin.

DNS, app access, firewall rules, profiles and budgets require explicit confirmation. Speed tests consume data and need approval; the default maximum is 80 MB. Sleep assertions are bounded and released when the work ends; lid-closed operation requires explicit approval each time. This plugin installs no hooks or background service and never activates a network filter automatically.

Monitoring and diagnostics are free. Rule enforcement requires the separately installed Kilobat Pro app and its enabled network filter. History needs the app running, and Wi-Fi names may need Location permission. Missing history is not zero usage. Saved rules are not enforced when the filter is off.

## Development and verification

```sh
python3 scripts/verify.py --smoke
claude plugin validate --strict .
grok plugin validate .
python3 scripts/pack.py
python3 scripts/pack_mcpb.py
```

`--smoke` initializes the real bundled MCP server, inspects every tool annotation, runs five read-only workflows, and checks three invalid requests. It does not run a speed test, alter settings, or hold sleep assertions. Build artifacts are written to `dist/`. Test cases for directory reviewers are in [review/test-cases.json](review/test-cases.json).

The binary and corresponding source are pinned in [release.json](release.json) and [SOURCE.md](SOURCE.md). The entire plugin and bundled CLI are GPL-3.0-only; see [LICENSE](LICENSE). Kilobat's GUI app has separate terms.

[Website](https://kilobat.app) · [Documentation](https://kilobat.app/docs.html) · [Support](https://kilobat.app/support.html) · [Plugin privacy](PRIVACY.md) · [Terms](https://kilobat.app/terms.html)

Maintained by Philipp Seyfi, the author of Kilobat, through the `seifip` GitHub account. The Kilobat website and CLI source identify the same publisher. Contact: ping@kilobat.app.
