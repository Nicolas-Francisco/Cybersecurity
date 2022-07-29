#include <string.h>
#include <stdlib.h>
#include <stdio.h>

void f(char *name) {
    char x[100];
    strcpy(x, name);
    printf("string copied\n");
}


int main(int argc, char **argv ) {
    if (argc != 2) {
        printf("%s name\n", argv[0]);
        exit(1);
    }
    f(argv[1]);
    return 0;   
}