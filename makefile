all: test

test:
	python3 -m doctest jsonval.py

clean:
	rm -rf __pycache__
