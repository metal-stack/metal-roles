# gitlabci-runner

Configures a server as GitLab CI runner.

## Variables

| Name                      | Mandatory | Description                                                                                |
|---------------------------|-----------|--------------------------------------------------------------------------------------------|
| gitlab_runner_url         | yes       | the api url of an GitLab instance where runners can register and pull CI jobs from.        |
| gitlab_runner_roken       | yes       | the private token to do the registration at the GitLab instance.                           |
| gitlab_runner_description |           | the description for this CI runner.                                                        |
| gitlab_runner_tags        |           | the tags to be assigned to the CI runner. CI jobs can choose with tags wich runner to use. |
| gitlab_runner_image       |           | the docker image name to use.                                                              |
| gitlab_runner_tag         |           | the tag of the docker image to use.                                                        |
| gitlab_runner_ssh_privkey |           | the path to the private ssh key file for use within the gitlab runner                      |
| gitlab_runner_ssh_pubkey  |           | the path to the public ssh key file for use within the gitlab runner                       |
