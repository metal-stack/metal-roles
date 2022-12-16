.PHONY: test
test:
	python -m unittest discover -v -p '*_test.py' -s partition/roles/ssh-access
	python -m unittest discover -v -p '*_test.py' -s partition/roles/dhcp
