.PHONY: setup check-python run-server run-publisher run-subscriber benchmark-create-topic benchmark-all ping-pong-test clean

VENV := ./venv
PYTHON := $(VENV)/bin/python

setup: check-python
	@echo "MakeFile: Creating a virtual environment..."
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

check-python:
	@command -v python3 >/dev/null 2>&1 || { echo >&2 "If Python 3 is not installed, install Python 3 first."; exit 1; }

run-server:
	@echo "MakeFile: Running server..."
	$(PYTHON) server.py

run-publisher:
	@echo "MakeFile: The publisher client is running..."
	$(PYTHON) publisher_client.py

run-subscriber:
	@echo "MakeFile: The subscriber client is running..."
	$(PYTHON) subscriber_client.py

benchmark-create-topic:
	@echo "MakeFile: Performing performance create topic tests..."
	$(PYTHON) benchmark_create_topic.py

benchmark-all:
	@echo "MakeFile: Performing performance all apitests..."
	$(PYTHON) benckmark_all_api.py

ping-pong-test:
	@echo "MakeFile: The ping pong test is being performed..."
	$(PYTHON) ping_pong_test.py

clean:
	@echo "MakeFile: Be cleaning up..."
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -r {} +
	find ../Misc/ -type f -name '*.png' -exec rm {} +