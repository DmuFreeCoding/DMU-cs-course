#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <errno.h>
#include <sys/ipc.h>
#include <semaphore.h>
#include <fcntl.h>
#include "Queue.h"
#include "const.h"
#define N 5
time_t end_time;
//互斥锁
pthread_mutex_t mutex;
//条件变量
pthread_cond_t conc,conp;
int fd;
Queue * qt;
//缓冲区
Elemtype p;
void* consumer(void *arg);
void* productor(void *arg);
int main(int argc, char *argv[])
{
pthread_t id1,id2,id3,id4,id5;
pthread_t mon_th_id;
int ret;
end_time = time(NULL)+30;
qt = InitQueue();
p.lNumber = 1000;
//初始化条件变量
pthread_mutex_init(&mutex,0);
pthread_cond_init(&conc,0);
pthread_cond_init(&conp,0);
pthread_create(&id1,NULL,&productor, NULL);
pthread_create(&id3,NULL,&productor, NULL);
pthread_create(&id2,NULL,&consumer, NULL);
pthread_create(&id5,NULL,&productor, NULL);
pthread_create(&id4,NULL,&consumer, NULL);
pthread_join(id1,NULL);
pthread_join(id2,NULL);
pthread_join(id3,NULL);
pthread_join(id4,NULL);
pthread_join(id5,NULL);
pthread_mutex_destroy(&mutex);//销毁锁
return 0;
}
void* productor(void *arg)
//生产者线程
{
int i,nwrite;
while(time(NULL) < end_time)
{
// p(empty)
pthread_mutex_lock(&mutex);
// p(mutex)
if(TRUE==QueueFull(*qt))
//队满
{
pthread_cond_wait(&conp,&mutex);
printf("Productor:buffer is full ,please try to write later.\n");
}
else
{
EnQueue(qt,p);
printf("Productor:write [%d] to buffer \n",p.lNumber);
p.lNumber++;
}
pthread_cond_signal(&conc);
//v(full)
pthread_mutex_unlock(&mutex);
//v(mutex)
sleep(1);
}
}
//生产者productor
void* consumer(void *arg)
//消费者线程
{
int nolock=0;
int ret,nread;
Elemtype p2;
while((time(NULL) < end_time)||(FALSE==(QueueEmpty(*qt))))
{
//p(full)
pthread_mutex_lock(&mutex);
//p(mutex)
if(TRUE==QueueEmpty(*qt))
//队空
{
printf("Consumer:the buffer is empty,please try to read later.\n");
pthread_cond_wait(&conc,&mutex);
}
else
{
DeQueue(qt,&p2);
printf("Consumer:read [%d] from buffer.\n",p2.lNumber);
}
pthread_cond_signal(&conp);
//v(empty)
pthread_mutex_unlock(&mutex);
//v(mutex)
sleep(2);
}
}