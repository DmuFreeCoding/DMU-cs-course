#include <sys/msg.h>
#include <sys/ipc.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#define MSGKEY 75
void SERVER();
void CLIENT();
struct msgform{
    long mtype;
    char msgtext[1030];
}msg;
int msgqid,i;
int main()
{
    while((i = fork()) == -1);
    if(!i) SERVER();
    while((i = fork()) == -1);
    if(!i) CLIENT();
    wait(0);
    wait(0);
}
void SERVER()
{
    msgqid = msgget(MSGKEY,0777|IPC_CREAT);
    do
    {
        msgrcv(msgqid,&msg,1030,0,0);
        printf("(server)receive message %d,",msg.mtype);
        printf("%s",msg.msgtext);
    }while(msg.mtype!=1);
    msgctl(msgqid,IPC_RMID,0);
    exit(0);
}
void CLIENT()
{
    int i,j;
    char string_i[20];
    msgqid = msgget(MSGKEY,0777);
    for(i = 10 ; i >= 1; i-- )
    {
        msg.mtype = i;
        printf("(client)send\n");
        sprintf(msg.msgtext,"the content of message is: ");
        sprintf(string_i,"message  %d",i);
        strcat(msg.msgtext,string_i);
        strcat(msg.msgtext,"\n");
        msgsnd(msgqid,&msg,1030,IPC_NOWAIT);
    }
    exit(0);
}

