#include <sys/msg.h>
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
        printf("(server)receive message %d\n",msg.mtype);
    }while(msg.mtype!=1);
    msgctl(msgqid,IPC_RMID,0);
    exit(0);
}
void CLIENT()
{
    int i;
    msgqid = msgget(MSGKEY,0777);
    for(i = 10 ; i >= 1; i-- )
    {
        msg.mtype = i;
        printf("(client)send\n");
        msgsnd(msgqid,&msg,1030,0);
    }
    exit(0);
}

