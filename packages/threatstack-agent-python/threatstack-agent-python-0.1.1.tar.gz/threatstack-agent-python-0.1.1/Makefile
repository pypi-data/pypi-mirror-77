
all: build
#
#

build: copy libinjection/libinjection_wrap.c
	rm -f libinjection.py libinjection.pyc

install: build
	python setup.py --verbose install

libinjection/libinjection_wrap.c: libinjection/libinjection.i libinjection/libinjection.h libinjection/libinjection_sqli.h
	swig -version
	swig -python -builtin -Wall -Wextra -py3 libinjection/libinjection.i

copy:
	cp libinjection/src/libinjection*.h libinjection/src/libinjection*.c libinjection/src/libinjection.i libinjection/

.PHONY: copy

libinjection.so: copy
	gcc -std=c99 -Wall -Werror -fpic -c libinjection/libinjection_sqli.c
	gcc -std=c99 -Wall -Werror -fpic -c libinjection/libinjection_xss.c
	gcc -std=c99 -Wall -Werror -fpic -c libinjection/libinjection_html5.c
	gcc -dynamiclib -shared -o libinjection/libinjection.so libinjection_sqli.o libinjection_xss.o libinjection_html5.o

clean:
	@rm -rf build dist
	@rm -f *.pyc *~ *.so *.o
	@rm -f nosetests.xml
	@rm -f words.py
	@rm -f libinjection/*~ libinjection/*.pyc
	@rm -f libinjection/libinjection.h libinjection/libinjection_sqli.h libinjection/libinjection_sqli.c libinjection/libinjection_sqli_data.h libinjection/libinjection.i libinjection/libinjection_html5.* libinjection/libinjection_xss.*
	@rm -f libinjection/libinjection_wrap.c libinjection/libinjection.py
