.PHONY: test
test:
	python3 -m pip install mock
	./test.sh

.PHONY: test-local
test-local:
	docker pull metalstack/metal-deployment-base:latest
	docker run --rm -it -v $(PWD):/work -w /work metalstack/metal-deployment-base:latest make test

.PHONY: lint
lint:
	docker run --rm -v $(PWD):/workdir davidanson/markdownlint-cli2:v0.21.0 "**/*.md"
	docker run --rm -v $(PWD):/work -w /work pipelinecomponents/ansible-lint:edge --fix='yaml[truthy]'


# yaml[truthy]: Truthy value should be one of [false, true]
# partition/roles/wireguard/tasks/main.yaml:12

# name[casing]:
