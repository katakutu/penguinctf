#include <stdio.h>
#include <unistd.h>

void dots(int howmany);
void waddle_to_flagland();
void play_in_snow();
void get_flag(int hash);



void dots(int howmany) 
{
    for (int i = 0; i < howmany; i++) 
    {
        sleep(1);
        printf(".");
        fflush(stdout);
    }
}

void get_flag(int hash)
{
    printf("Willy finally reaches the Flaglands!\n");
    int flag = (hash ^ 0xcafebabe) + hash;
    printf("He grabs you a flag{%x}\n", flag);
}

void play_in_snow()
{
    printf("Willy decides to play in the snow!");
    dots(10);
    puts("");
    int a = 0;
    int b = 0;
    int c = 0;
    for (int i = 0; i < 10000; i++) {
        for (int j = 0; j < 1000; j++) 
        {
            a = i;
            b = j;
            c = a ^ b;
            a = (a + b) - c;
            b = (a * a * a * a);
            c = a ^ b;
            a = 0xffff & c;
            b = 0x0000ffff & a;
        }
    }
}

void waddle_to_flagland() 
{
    int hash = 0xdeadbeef;
    for (int i = 0; i < 0x13371337; i++)
    {
        if (i % 1000 == 0)
        {
            play_in_snow();
        }
        hash = hash ^ i;
    }
    get_flag(hash);
}

int main()
{
    puts("Hey! My name's Willy the Waddler and I love to waddle!");
    dots(3);
    printf(" So I heard you like flags ");
    dots(3);
    puts("");
    dots(3);
    printf("I'll be heading to the Flaglands soon ");
    dots(3);
    puts("\nWould you like me to get something for you?");
    dots(3);
    puts("Sure thing!");
    dots(3);
    printf("I'm sure I'll be back in a couple of hours.");
    dots(10);
    puts("\nWilly the Waddler waddles off into the distance"); 
    dots(10);
    puts("In the meanwhile, Willy carries on his journey");
    waddle_to_flagland();
}