MODULE = tomita

# For python3
TEST_RUNNER = nosetests-3.4

# For python2
# TEST_RUNNER = nosetests

all: test

test:
	$(TEST_RUNNER) -vx tests

install-rec:
	pip install -r requirements.txt

clean:
	find . -name '*.pyc' -exec rm -f {} +; find . -name '*~' -exec rm -f {} +

pylint:
	pylint $(MODULE) -r y -f html -d fixme -d locally-disabled -d invalid-name -d missing-docstring -d logging-format-interpolation > /tmp/pylint.report.html; google-chrome-stable /tmp/pylint.report.html

coverage:
	$(TEST_RUNNER) --with-coverage --cover-package=$(MODULE) --cover-erase --cover-inclusive -v tests --cover-html --cover-html-dir=/tmp/htmlcover && google-chrome-stable /tmp/htmlcover/index.html

count-lines:
	cloc tests --exclude-lang=Javascript

get-requirements:
	pipreqs . --force
