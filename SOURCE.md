# Source and release provenance

The bundled `server/start-mcp.sh` selects the appropriate signed architecture slice of the universal macOS binary from Kilobat CLI 0.7.0, signed by Developer ID Application: PHILIPP SEYFI (HAR874R67J). The release asset and binary SHA-256 digests, CLI source commit, and skill source commit are pinned in `release.json`.

Corresponding GPL-3.0-only CLI source, build instructions, and license:
https://github.com/seifip/kilobat-cli/tree/515322f55f41ff7768ea4ee6a5ddc675fc866468

Download the complete corresponding source:
https://github.com/seifip/kilobat-cli/archive/515322f55f41ff7768ea4ee6a5ddc675fc866468.tar.gz

The original agent skills come from:
https://github.com/seifip/kilobat-skills/tree/ffd3b5931def9bb309868085da4f643ead42a982

This repository adds portable, Claude and Grok manifests, setup instructions, release validation, and explicit data handling. The proprietary macOS GUI app is distributed separately and is not included.

The universal release binary is split with Apple’s `lipo -thin` so each signed slice fits Anthropic’s 5 MiB per-file limit. Each slice retains its original Developer ID signature. No binary is patched or downloaded at runtime. The original universal binary digest and both slice digests are recorded in `release.json`.
