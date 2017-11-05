PYLINT_IGNORE+=locally-disabled
PYLINT_IGNORE+=invalid-name
PYLINT_IGNORE+=missing-docstring
PYLINT_IGNORE+=too-few-public-methods
PYLINT_FLAGS=-r no $(patsubst %, -d %,$(PYLINT_IGNORE))

SVG_ICONS=$(wildcard svg/*.svg)
PNG_ICONS=$(subst .svg,.png,$(SVG_ICONS))

all: build check

build: $(PNG_ICONS)

check:
	pylint $(PYLINT_FLAGS) enet.py lib/*.py

svg/%.png: svg/%.svg
	convert -background transparent -resize 32x32 $^ $@

clean:
	rm $(PNG_ICONS)
