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
# 	docker run --rm -v $(PWD):/workdir ghcr.io/igorshubovych/markdownlint-cli:latest "*.md"
# 	docker run --rm -v $(PWD):/work -w /work pipelinecomponents/yamllint:edge common control-plane partition
	docker run --rm -v $(PWD):/work -w /work pipelinecomponents/ansible-lint:edge

# 	yamllint common controlplane partition
# 	ansible-galaxy collection install . && ansible-lint
