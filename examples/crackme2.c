#include <string.h>
#include <stdio.h>

void game(char *p, char *pass)
{
    int i = 0;

    for (i = 0; i < 8; i++) {
        pass[i] = (p[i] ^ 0xa1) + 0x12;
    }
}

void getflag(char *pass, char *flag)
{
    int i = 0;

    for (i  = 0; i < 8; i++) {
        flag[i] = ((pass[i] ^ 0xde) + 0x9) % 256;
    }
}

int main(int argc, char **argv)
{
    char input[9]   = {0};
    char flag[9]    = {0};
    char pass[9]    = {0};
    int t           = 0;

    do {
        puts("Password plz! ");
        fgets(input, 9, stdin);
        game(input, pass);
        if (strcmp(pass, "theG4me!") == 0) {
            t = 1;
        }
    } while(!t);

    getflag(input, flag);
    printf("Flag is: %s\n", flag);
    return 0;
}