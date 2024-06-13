#include <sys/shm.h>
#include <sys/ipc.h>
#include <sys/types.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#define SHMKEY 80
void SERVER();
void CLIENT();
int shmid,i;
int *addr;
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
    shmid = shmget(SHMKEY,1024,0777|IPC_CREAT);//创建共享内存与消息队列类似，(共享内存标识符，大小，权限)
    addr = shmat(shmid,0,0);//共享内存链接到进程（共享内存标识，位置可为NULL即让系统选择合适位置，SHM_RDONLY仅可读）
    do
    {
        *addr = -1;
        while(*addr == -1);
        printf("(server)received, ");
        printf("server *addr %d \n",*addr);
    }while(*addr);
    shmctl(shmid,IPC_RMID,0);//清除共享内存
    exit(0);
}
void CLIENT()
{
    int i;
    shmid = shmget(SHMKEY,1024,0777);
    addr = shmat(shmid,0,0);
    for(i = 5 ; i >= 0 ; i--)
    {
        while(*addr != -1);
        printf("(client)sent, ");
        printf("client i: %d\n",i);
        *addr = i;
    }
    exit(0);
}

