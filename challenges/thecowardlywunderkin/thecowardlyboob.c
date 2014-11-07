#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <signal.h>

// gcc -fno-stack-protector -O0 -m32 -o thecowardlyboob thecowardlyboob.c

int is_valid(int secret_number);
void sighandler(int signum);
void spawn_shell();
void print_error();

struct external {
    char* extern_buffer[32];
    int* extern_addr;
};

struct external ext;

int main(int argc, char *argv[]) {

    signal(SIGSEGV, sighandler);    
    int user_number;
    ext.extern_addr = &print_error;

    if (argc != 2) {
        printf("The shell spawner app.\nUsage: %s secret_number\n", argv[0]);
        exit(0);
    }

    strcpy(ext.extern_buffer, argv[1]);
    user_number = atoi(argv[1]);
    if (is_valid(user_number)) {
    }
    else {
        printf("$ ");
        fflush(stdout);
        sleep(10);
        printf("\nHahaha! No shell for you!\n");
        printf("BTW, you're weird.\n%n", 0x0); // I forgot if its %n or \n...
    }
}

int is_valid(int secret_number) {
    int check = secret_number * 2;
    if (check == 7)
        return 1;
    else
        return 0;
}

void print_error() {
    printf("ERROR: LEVEL TOO LOW FOR SHELL\n");
    exit(1);
}

void sighandler(int signum)
{
    typedef int func(void);
    func* f = (func *) ext.extern_addr;
    f();
}

void spawn_shell() {
    char *args[] = {"-p"};
    execvp("/bin/sh", args);
}