#!/usr/bin/env bash

set -o errexit

tmpfile=$(mktemp /var/run/bgp-neighbors/bgp-neighbors.XXXXXX)
destfile=/var/run/bgp-neighbors/bgp-neighbors.json

/usr/bin/vtysh -c "show ip bgp vrf all neighbors json" > "${tmpfile}"

rm -f "${destfile}"
mv "${tmpfile}" "${destfile}"
rm -f "${tmpfile}"
