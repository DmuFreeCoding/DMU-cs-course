#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
int main()
{
    int i,r,p1,p2,p3,fd[2];
    char buf[50],s[50];
    pipe(fd);
    while((p1=fork())==-1);
    if(p1==0)
    {
        sprintf(buf,"messages from child process p1 !\n");
        printf("child process p1 !\n");
        write(fd[1],buf,50);
        exit(0);
    }
    else
    {
        while((p2 = fork()) == -1);
        if(p2 == 0)
        {
            sprintf(buf,"messages from child process p2 !\n");
            printf("child process p2 !\n");
            write(fd[1],buf,50);
            exit(0);
        }else
        {
            while((p3 = fork()) == -1);
                   if(p3 == 0)
                   {
                       sprintf(buf,"messages from child process p3 !\n");
                       printf("child process p3 !\n");
                       write(fd[1],buf,50);
                       exit(0);
                   }
        }
        for(i = 0 ; i < 3 ; i++){
        if(r = read(fd[0],s,50) == -1)
            printf("can't read pipe\n");
        else
            printf("%s",s);
        }
        exit(0);
    }
}
