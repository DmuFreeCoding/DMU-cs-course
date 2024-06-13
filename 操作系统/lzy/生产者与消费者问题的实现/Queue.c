//队列的基本操作函数
#include "stdio.h"
#include "malloc.h"
#include "const.h"
#include "Queue.h"
Queue * InitQueue( )
//初使化队列
{
Queue * Q = (Queue *)malloc(sizeof(Queue));
Q->front = Q->rear = 0;
return Q;
}
int EnQueue(Queue *Q,Elemtype x)
//进队
{
if((Q->rear + 1)%MaxSize==Q->front)
//队满
return FALSE;
else
{
Q->q[Q->rear] = x;
Q->rear = (Q->rear+1)%MaxSize;
return TRUE;
}
}
int DeQueue(Queue *Q,Elemtype *x)
//出队
{
if(Q->rear==Q->front)
//队空
return FALSE;
else
{
*x = Q->q[Q->front];
Q->front = (Q->front+1)%MaxSize;
return TRUE;
}
}
int QueueEmpty(Queue Q)
//判断队是否为空，空返回0 非空返回 1
{
if(Q.rear==Q.front)
return TRUE;
else
return FALSE;
//队空
}
Elemtype Last(Queue *Q)
//返回队列中的最后的一个元素（原队列还要存在）
{
Elemtype *prElem = NULL;
Queue *prTempQueue;
//这个临时队列，把原队列放到里面，当取完最后一个元素后，就把这个队列中的元素放回原来的队列
prTempQueue = InitQueue();
while(QueueEmpty(*Q)==1)
{
DeQueue(Q,prElem);
EnQueue(prTempQueue,*prElem);
}
while(QueueEmpty(*prTempQueue)==1)
{
DeQueue(prTempQueue,prElem);
EnQueue(Q,*prElem);
}
return *prElem;
}
//Last
BOOL QueueFull(Queue Q)
//判断队是否为满，满返回TRUE，非满返回FALSE
{
if(((Q.rear+1)%MaxSize)==Q.front)
//队空
return TRUE;
else
return FALSE;
}