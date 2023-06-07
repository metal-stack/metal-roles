.PHONY: test
test:
	python -m pip install mock
	for file in $(shell find . -name test -type d); do python -m unittest discover -v -p '*_test.py' -s $$(dirname $$file); done

.PHONY: test-local
test-local:
	docker pull metalstack/metal-deployment-base:latest
	docker run --rm -it -v $(PWD):/work -w /work metalstack/metal-deployment-base:latest make test
