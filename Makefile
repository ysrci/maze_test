Mypy := mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


install:
	@pip install mypy pytest

run:
	@python3 a_maze_ing.py

debug:
	@python3 -m pdb a_maze_ing.py

clean:
	@rm -rf __pycache__ .mypy_cache */__pycache__ */.mypy_cache

lint:
	@flake8 . && $(Mypy)

lint-strict:
	@flake8 && mypy . --strict
