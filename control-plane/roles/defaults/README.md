# defaults

Specifies common defaults for the metal-stack control plane deployment.

## Variables

```yaml
# Image pull policy for control plane images.
metal_control_plane_image_pull_policy: IfNotPresent
# Namespace for the control plane.
metal_control_plane_namespace: metal-control-plane
# Provider tenant for the control plane.
metal_control_plane_provider_tenant: acme
# Stage name for the control plane.
metal_control_plane_stage_name: test
```
