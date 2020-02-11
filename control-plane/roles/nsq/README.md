# nsq

Deploys [nsq](https://nsq.io/) in a standalone configuration.

The admin console can be reached via sidecar by using port-forwarding:

```
kubectl port-forward -n metal-control-plane svc/nsqadmin 4171
```

Using the sidecar configuration was the only possibility to make this possible as we enforce certificate authentication via the TCP port but do not use encrypted communication for in-cluster traffic via the HTTP endpoints.
