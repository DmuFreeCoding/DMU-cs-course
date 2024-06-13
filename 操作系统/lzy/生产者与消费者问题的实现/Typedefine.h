#ifndef TYPEDEFINE_H
#define TYPEDEFINE_H
#include "const.h"
typedef struct
//字符串的类型
{
char data[MAXLEN];
//数据区
int len;
//长度，没包括了'\0'的长度,如"abc"，长度为 3
}SString;
typedef struct
{
SString* strName;
//定义元素类型
long lNumber;
//号码
}Elemtype;
typedef struct node
//对在程序中使用到的类型做定义如结点类型，数据类型
{
Elemtype data;
//结点的数据域
struct node *next;
//结点的指针域，存放下一个结点的地址
}SNode;
typedef struct
//队列的基本结构
{
Elemtype q[MaxSize];
//存放队列元素
int front;
//头指针
int rear;
//尾指针(尾元素的下一个位置)
}Queue;
//栈的基本类型定义
typedef struct st
{
Elemtype data[MaxSize];
int top;
}Stack;
typedef int BOOL;
typedef int Status;
#endif