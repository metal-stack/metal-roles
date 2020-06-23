#!/usr/bin/env bash
set -e

for b in ${BUCKETS}
do
echo "rsync bucket:$b from ${IMAGE_SYNC_SRC}"
gsutil rsync -d -r "${IMAGE_SYNC_SRC}"/"${b}" /images/"${b}"
done
