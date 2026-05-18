#!/usr/bin/env bash
# Downloads a DP-IP Database and replaces the existing one.
# DB-IP updates monthly, so the current month is attempted first
# If the DB for the current month is not available yet, the scripts
# falls back to last month.

set -euo pipefail

KIND="${1:-}"
DATA_DIR="/var/lib/sflow-collector"
IMAGE="alpine:3"

case "$KIND" in
  geoip)
    SLUG="dbip-city-lite"
    OUT_DIR="${DATA_DIR}/geoip"
    OUT_FILE="geoip.mmdb"
    ;;
  asn)
    SLUG="dbip-asn-lite"
    OUT_DIR="${DATA_DIR}/asn"
    OUT_FILE="asn.mmdb"
    ;;
  *)
    echo "usage: $0 {geoip|asn}" >&2
    exit 2
    ;;
esac

mkdir -p "$OUT_DIR"

YEAR=$(date +%Y)
MONTH=$(date +%m)
PREV_MONTH=$((10#$MONTH - 1))
PREV_YEAR="$YEAR"
if [ "$PREV_MONTH" -eq 0 ]; then PREV_MONTH=12; PREV_YEAR=$((YEAR - 1)); fi
PREV_MONTH=$(printf '%02d' "$PREV_MONTH")

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

for URL in \
  "https://download.db-ip.com/free/${SLUG}-${YEAR}-${MONTH}.mmdb.gz" \
  "https://download.db-ip.com/free/${SLUG}-${PREV_YEAR}-${PREV_MONTH}.mmdb.gz"; do
  echo "Trying $URL ..."
  if docker run --rm -v "$TMP:/out" "$IMAGE" \
      sh -c "wget -q -O /out/db.gz '$URL' && gunzip /out/db.gz"; then
    mv -f "$TMP/db" "$OUT_DIR/$OUT_FILE.new"
    chmod 644 "$OUT_DIR/$OUT_FILE.new"
    mv -f "$OUT_DIR/$OUT_FILE.new" "$OUT_DIR/$OUT_FILE"
    echo "Updated $OUT_DIR/$OUT_FILE"
    # Reload Vector so the new mmdb is mapped. Restart is acceptable monthly.
    if systemctl is-active --quiet vector; then
      systemctl restart vector
    fi
    exit 0
  fi
done

echo "ERROR: failed to refresh $KIND mmdb from both current and previous month" >&2
exit 1
