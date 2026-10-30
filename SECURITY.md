# Security

Report security issues privately to [ping@kilobat.app](mailto:ping@kilobat.app), with the plugin version and a minimal redacted reproduction. Do not put credentials, private network history or Wi-Fi passwords in public issues.

The plugin ships a pinned, signed binary. It downloads and executes no code at runtime, installs no packages, registers no login item or lifecycle hook, and does not activate a network filter. MCP input schemas and tool annotations distinguish diagnostic reads, network probes, sleep assertions and settings changes. Settings changes require the person's confirmation. Network destinations and data categories are documented in [PRIVACY.md](PRIVACY.md).

Validate a package with `python3 scripts/verify.py --smoke` on macOS, `claude plugin validate --strict .`, and `grok plugin validate .` before publishing.
