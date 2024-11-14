#!/usr/bin/env bash

set -e 
tmpfile=$(mktemp /var/run/bgp-neighbors/bgp-neighbors.XXXXXX)
destfile=/var/run/bgp-neighbors/bgp-neighbors.json

/usr/bin/vtysh -c "show ip bgp vrf all neighbors json" > "${tmpfile}"

mv "${tmpfile}" "${destfile}"
rm "${tmpfile}"
