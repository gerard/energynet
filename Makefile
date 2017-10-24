PYLINT_IGNORE+=locally-disabled
PYLINT_IGNORE+=invalid-name
PYLINT_IGNORE+=missing-docstring
PYLINT_IGNORE+=too-few-public-methods
PYLINT_FLAGS=-r no $(patsubst %, -d %,$(PYLINT_IGNORE))

check:
	pylint $(PYLINT_FLAGS) enet.py lib/*.py
