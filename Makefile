PREFIX = /usr

PROGRAM = learning2flute

build:

install:
	install -m 0755 $(PROGRAM).py $(PREFIX)/bin/$(PROGRAM)

