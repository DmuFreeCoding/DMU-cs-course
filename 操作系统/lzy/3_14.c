#include <sys/types.h>
#include <sys/msg.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main()
{
    int msgid;
    int status;
    char str1[]={"test message:hello!"};
    char str2[]={"test message:goodbye!"};
    char str3[]={"The third message!"};
    struct msgbuf{
        long msgtype;
        char msgtext[1024];
    }sndmsg,rcvmsg;
    if((msgid = msgget(IPC_PRIVATE,0666)) == -1)
    {
        printf("msgget error!\n");
        exit(254);
    }//创建消息队列 该消息队列为该进程私有且其权限为-rw0rw0rw0//返回值为队列的ID
    sndmsg.msgtype = 111;
    sprintf(sndmsg.msgtext,str1);//填写表单即队列号和数据块
    if(msgsnd(msgid,&sndmsg,sizeof(str1)+1,0)==-1)
    {
        printf("msgget error!\n");
        exit(254);
    }//发送消息到消息队列，需要发送的消息队列的ID，消息的数据块以及容量；阻塞与非阻塞的区别在于是否等待消息是否到达就返回。0保证数据到达。IPC_NOWAIT则不保证数据到达。
    sndmsg.msgtype = 222;
    sprintf(sndmsg.msgtext,str2);
    if(msgsnd(msgid,&sndmsg,sizeof(str2)+1,0)==-1)
    {
        printf("msgget error!\n");
        exit(254);
    }
    sndmsg.msgtype = 333;
    sprintf(sndmsg.msgtext,str3);
    if(msgsnd(msgid,&sndmsg,sizeof(str3)+1,0)==-1)
    {
        printf("msgget error!\n");
        exit(254);
    }
    if(status = msgrcv(msgid,&rcvmsg,80,222,IPC_NOWAIT) == -1)
    {
        printf("msg rcv error!\n");
        exit(254);
    }//从指定消息队列接收消息，消息队列的ID，接收数据用的结构块，接收的数据大小，接收的队列号
    printf("The received message:%s.\n",rcvmsg.msgtext);
    msgctl(msgid,IPC_RMID,0);//删除消息队列
    exit(0);
}

