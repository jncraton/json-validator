all: test

test:
	python3 -m doctest jsonval.py
