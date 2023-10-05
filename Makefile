.PHONY: test
test:
	python -m pip install mock
	@failed=0; \
    for file in $(shell find . -name test -type d); do \
        echo "Running tests in $$(dirname $$file)"; \
        python -m unittest discover -v -p '*_test.py' -s $$(dirname $$file) || failed=1; \
    done; \
    if [ $$failed -eq 0 ]; then \
        echo "All tests passed."; \
    else \
        echo "One or more tests have failed."; \
        exit 1; \
    fi

.PHONY: test-local
test-local:
	docker pull metalstack/metal-deployment-base:latest
	docker run --rm -it -v $(PWD):/work -w /work metalstack/metal-deployment-base:latest make test
