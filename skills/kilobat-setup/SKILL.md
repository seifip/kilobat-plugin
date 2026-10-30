---
name: kilobat-setup
description: Set up the Kilobat plugin on a Mac, verify its bundled CLI and MCP connection, explain permissions and local data handling, and run the first network check. Use after installing Kilobat or when its tools are missing or unavailable.
---

# Set up Kilobat

1. Check the execution environment. Kilobat measures the computer where its MCP server runs and supports macOS 14 or later on Intel and Apple silicon. A cloud Linux session cannot measure the user's Mac. Explain this if the current execution environment is remote.
2. This plugin includes the signed Kilobat CLI at `server/kilobat` and a local stdio MCP configuration. Prefer its connected MCP tools. No API key, account, Homebrew install, or external runtime is required. If tools are missing, check whether the plugin and its MCP server are enabled, then ask the user to restart or reconnect the client. Do not create duplicate global MCP entries or silently replace another CLI install.
3. When tools connect, run `get_conditions`. Explain whether the connection is metered, whether Low Data Mode is on, and whether the Mac is on battery. Missing values mean unknown.
4. Explain that network history is stored locally, but results requested through MCP are shared with the connected AI client and processed under that client's policies. Network probes contact the router, configured resolvers, Apple or Cloudflare, or the host the user asks to check. Do not upload history or identify a public IP unless the task calls for it.
5. For a first diagnosis, call `diagnose_network`. Do not run a speed test, alter DNS, change an app rule, enable filtering, or keep the lid-closed Mac awake during setup. Show measured findings and any unavailable measurements.
6. Explain optional app features: per-app rule enforcement requires the Kilobat app, Kilobat Pro and an enabled network filter. macOS approval must be completed by the person. History and session records require the app to be running. Nearby Wi-Fi names may require Location permission. The CLI can diagnose a network without the app; do not treat missing history or disabled filtering as a failed install.
7. Load `../kilobat/SKILL.md` for the task router and the relevant focused skill. Report whether tools connected and which checks actually ran.
