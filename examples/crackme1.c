#include <string.h>
#include <stdio.h>

void xor(char *p)
{
    char *pass  = "\x47\x56\x45\x47\x4f\x41\x40";
    int i       = 0;

    for (i = 0; i < strlen(pass); i++) {
        p[i] = pass[i] ^ 0x24;
    }
}

int main(int argc, char **argv)
{
    char pass[8] = {0};

    if (argc != 2) {
        printf("Usage: %s <password>\n", argv[0]);
        return 1;
    }

    xor(pass);
    if (strcmp(pass, argv[1]) == 0) {
        puts("Congratz!");
        return 0;
    } else {
        puts("Failed!");
        return 1;
    }
}