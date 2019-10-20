project := bot_partidos
TEST_PATH=./

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -rf {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr htmlcov/
	rm -fr .pytest_cache/

lint:
	flake8 --config=.flake8 $(project) tests

test: clean-pyc
	py.test --verbose --color=yes $(TEST_PATH)

docker-build:
	docker build --tag scraping-fcvolei .

docker-run: docker-build
	docker run -p 8000:8000 scraping-fcvolei
