CC = gcc
CCFLAGS = -std=gnu99 -Wpedantic -lm -lpthread -g 

all: boardCount boardCountLayer UTTT.o UTTT_Library.so

boardCount: boardCount.o boardCount.h UTTT.o
	$(CC) $(CCFLAGS) boardCount.o UTTT.o boardCount.h -o boardCount

boardCount.o: boardCount.c
	$(CC) $(CCFLAGS) -c boardCount.c -o boardCount.o

boardCountLayer: boardCountLayer.o boardCount.h UTTT.o
	$(CC) $(CCFLAGS) boardCountLayer.o UTTT.o boardCount.h -o boardCountLayer

boardCountLayer.o: boardCountLayer.c
	$(CC) $(CCFLAGS) -c boardCountLayer.c -o boardCountLayer.o

UTTT.o: UTTT.c
	$(CC) $(CCFLAGS) -c -fPIC UTTT.c -o UTTT.o

UTTT_Library.so: UTTT_Library.c UTTT.o
	$(CC) $(CCFLAGS) -fPIC -shared UTTT_Library.c UTTT.o  -o UTTT_Library.so

clean:
	rm *.o
	rm boardCount
	rm boardCountLayer
	rm UTTT_Library.so