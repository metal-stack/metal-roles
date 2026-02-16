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
	docker run --rm -v $(PWD):/work --entrypoint bash -w /work --entrypoint sh pipelinecomponents/ansible-lint:edge -c 'ansible-galaxy install -r requirements.yaml && /entrypoint.sh'
