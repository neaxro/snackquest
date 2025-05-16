.PHONY: list
list:
	@LC_ALL=C $(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/(^|\n)# Files(\n|$$)/,/(^|\n)# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | grep -E -v -e '^[^[:alnum:]]' -e '^$@$$'

.PHONY: packages-cli
packages-cli:
	pip install -r cli/requirements.txt

.PHONY: packages-api
packages-api:
	pip install -r api/requirements.txt

.PHONY: build-api
build-api:	# Start webpage locally in debug mode
	docker build -t snackquest-api:local -f api/Dockerfile .

.PHONY: run-api
run-api:	# Start webpage locally in debug mode
	docker run --name snackquest-api -p 5000:5000 snackquest-api:local

.PHONY: up
up:	# Start docker container for local usage, testing
	docker compose up

.PHONY: binary
binary:	# Build binary from snackquest source code
	pyinstaller --onefile --name snackquest snackquest/snackquest.py
