# Darius-Florentin Neatu <neatudarius@gmail.com>
# Copyright 2018

# Exemplu de Makefile pentru tema

# tag-uri obligatorii (nume + comportament identic)
# build    => compileaza toata tema 
#             (ATENTIE! E important - NU compilati in tag-urile de run. Sesizati?)
# run-p$ID => ruleaza problema cu ID-ul specificat (1, 2, 3, 4)
# clean    => sterge toate fisierele generate

# restul este la alegerea studentului


CFLAGS=-Wall

# nume necesar (build)
build: build-p1 build-p2 build-p3

build-p1:
	g++ $(CFLAGS) src/p1.cpp -o p1

build-p2:
	g++ $(CFLAGS) src/p2.cpp -o p2

build-p3:
	g++ $(CFLAGS) src/p3.cpp -o p3

run-p1:      # nume necesar
	./p1

run-p2:      # nume necesar
	./p2

run-p3:      # nume necesar 
	./p3

clean:		 # nume necesar
	rm -f p1 p2 p3
