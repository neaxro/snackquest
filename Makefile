.PHONY: list
list:
	@LC_ALL=C $(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/(^|\n)# Files(\n|$$)/,/(^|\n)# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | grep -E -v -e '^[^[:alnum:]]' -e '^$@$$'

.PHONY: packages
packages:	# Install python dependencies
	pip install -r requirements.txt

.PHONY: web
web:	# Start webpage locally in debug mode
	python -m web.app

.PHONY: build
build:	# Build docker image for local usage
	docker build -t snackquest:local .

.PHONY: up
up:	# Start docker container for local usage, testing
	docker rm snackquest && \
	docker run --name snackquest -p 5000:8000 snackquest:local

.PHONY: binary
binary:	# Build binary from snackquest source code
	pyinstaller --onefile --name snackquest snackquest/snackquest.py
