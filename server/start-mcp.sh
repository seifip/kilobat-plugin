#!/bin/sh
# Only runs the bundled, signed MCP server; no downloads or installation.
set -eu
if [ "$(/usr/bin/uname -s)" != Darwin ]; then
  echo 'Kilobat requires a local Mac running macOS 14 or later.' >&2
  exit 1
fi
major=$(/usr/bin/sw_vers -productVersion | /usr/bin/cut -d. -f1)
if [ "$major" -lt 14 ]; then
  echo 'Kilobat requires macOS 14 or later.' >&2
  exit 1
fi
case "$(/usr/bin/uname -m)" in
  arm64) arch=arm64 ;;
  x86_64) arch=x86_64 ;;
  *) echo 'Kilobat supports Intel and Apple-silicon Macs.' >&2; exit 1 ;;
esac
server_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec "$server_dir/darwin-$arch/kilobat" mcp
