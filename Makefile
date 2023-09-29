CC = gcc
CCFLAGS = -std=gnu99 -Wpedantic -lm -lpthread -g 

all: boardCount boardCountNoErrorChecking boardCountLayer

boardCount: boardCount.o boardCount.h
	$(CC) $(CCFLAGS) boardCount.o boardCount.h -o boardCount

boardCount.o: boardCount.c
	$(CC) $(CCFLAGS) -c boardCount.c -o boardCount.o

boardCountNoErrorChecking: boardCountNoErrorChecking.o boardCount.h
	$(CC) $(CCFLAGS) boardCountNoErrorChecking.o boardCount.h -o boardCountNoErrorChecking

boardCountNoErrorChecking.o: boardCountNoErrorChecking.c
	$(CC) $(CCFLAGS) -c boardCountNoErrorChecking.c -o boardCountNoErrorChecking.o

boardCountLayer: boardCountLayer.o boardCount.h
	$(CC) $(CCFLAGS) boardCountLayer.o boardCount.h -o boardCountLayer

boardCountLayer.o: boardCountLayer.c
	$(CC) $(CCFLAGS) -c boardCountLayer.c -o boardCountLayer.o

clean:
	rm *.o
	rm boardCount
	rm boardCountNoErrorChecking
	rm boardCountLayer