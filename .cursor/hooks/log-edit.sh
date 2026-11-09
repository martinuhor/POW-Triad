#!/bin/bash
# Appends each agent file edit to TELEMETRY.md so the user can follow changes.
input=$(cat)
file=$(printf '%s' "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('file_path') or d.get('path') or d.get('file') or 'unknown')" 2>/dev/null || echo "unknown")
ts=$(date '+%Y-%m-%d %H:%M')
root="$(cd "$(dirname "$0")/../.." && pwd)"
log="$root/TELEMETRY.md"
if [ -f "$log" ]; then
  printf '| %s | Edited `%s` | Auto-logged by afterFileEdit hook |\n' "$ts" "$file" >> "$log"
fi
echo '{}'
exit 0
