# BGP Health Check Role

This role provides automated monitoring of BGP session status across the network, with a focus on quick detection of problematic connections and minimalistic output.

## Purpose

- Automated monitoring of BGP session status
- Quick detection of unestablished or problematic BGP connections
- Minimalistic output that only shows problematic connections

## Use Cases

### 1. Network Bootstrapping
- Verify BGP sessions are properly established during initial deployment

### 2. Troubleshooting



## Output Format

The role provides clean, minimal output:
- Only shows problematic connections
- Displays hostname and specific problematic interfaces
- No output when all connections are healthy

Example output when issues are detected:
```
Broken BGP connections:
switch1: Ethernet32, Ethernet116
switch2: Ethernet120
```

## Implementation Details

The role checks for:
- BGP session state (must be "Established")
- Peer uptime (must not be "never")
- Connection status

It uses `vtysh -c "show bgp summary json"` to gather BGP information and processes the output to identify problematic connections.

