#include <unistd.h>
#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#define A 30
#define B 31
int wait_mark;
void waiting()
{
    while(wait_mark!=0);
}
void stop()
{
    wait_mark=0;
}
int main()
{
    int p1,p2;
    while((p1 = fork()) == -1);
    if(p1 > 0)
    {
        while((p2 = fork()) == -1);
        if(p2 > 0)
        {
            printf("parent\n");
	    kill(p1,A);
            kill(p2,B);
            wait(0);
            wait(0);
            printf("parent process id killed\n");
            exit(0);
        }
        else
        {
            printf("p2\n");
            wait_mark=1;
            signal(B, stop);
            waiting();
            printf("child process 2 is killed by parent!\n");
            exit(0);
        }
    }
    else
    {
        printf("p1\n");
        wait_mark=1;
        signal(A, stop);
        waiting();
        printf("child process 1 is killed by parent!\n");
        exit(0);
    }
}

