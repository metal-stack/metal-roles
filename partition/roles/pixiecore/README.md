# pixiecore
Deploys pixiecore container

## Variables

This role uses variables from [partition-defaults](/partition). So, make sure you define them adequately as well.

You can look up all the default values of this role [here](defaults/main/main.yaml).

| Name                            | Mandatory | Description                         |
| ------------------------------- | --------- | ----------------------------------- |
| pixiecore_image_name            |           | Image version of the pixiecore      |
| pixiecore_image_tag             | yes       | Image tag of the pixiecore          |

