build:
	python setup.py build

dev:
	python setup.py develop

upload:
	python setup.py sdist upload

lint:
	flake8 --max-complexity 10 --show-source ircstat

clean:
	rm -rf build dist README MANIFEST ircstat.egg-info
