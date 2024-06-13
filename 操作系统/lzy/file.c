//@author:lazy1
//@Email:674194901@qq.com
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <time.h>
#include <string.h>
#include <ctype.h>
#define BFS 0
#define DFS 1
//队列的数据结构
typedef struct Quene
{
    char *filename[10];
    int front;
    int rear;
}Quene;

DIR *dirp1;
struct dirent *direntp;
struct stat statbuf;
int stats;
//在原有的函数上进行改进,用作BFS的check函数
static int GetFileSizeTime(const char *filename) 
{ 
	struct stat statbuf; 
	if(stat(filename,&statbuf)==-1) //取 filename 的状态
	{ 
		printf("Get stat on %s Error:%s\n",filename,strerror(errno)); 
		return(-1);  
	} 
	if(S_ISDIR(statbuf.st_mode)) 
		return 1; //判断是否是目录文件
	if(S_ISREG(statbuf.st_mode)) //判断是否是普通文件
	    printf("%ssize:%ldbytes\tmodifiedate: %s\n",filename,statbuf.st_size,ctime(&statbuf.st_mtime)); //输出文件的大小和最后修改时间
	return 0;  
} 
//DFS,采用递归实现
void DirDfs(DIR *dirp,char*lastpath)
{
    while((direntp = readdir(dirp))!=NULL)
    {
    char path[1024];
    memset(path, 0, 1024);
    strcpy(path, lastpath);
    strcat(path, "/");
    strcat(path, direntp -> d_name);
    if (strcmp(direntp->d_name,"..")==0||strcmp(direntp->d_name,".")==0)
    {
        continue;
    }
    if(stat(path,&statbuf)==-1)
    {
    printf("Get stat on %s Error:%s\n",path,strerror(errno));
    break;
    }
    if(S_ISDIR(statbuf.st_mode))
    {
        DIR *dirp2;
        dirp2=opendir(path);
        DirDfs(dirp2,path);
        continue;
    }
    if(S_ISREG(statbuf.st_mode))
        printf("%ssize:%ldbytes\tmodifiedat%s\n",path,statbuf.st_size,ctime(&statbuf.st_mtime));
    }
    return;
}
//初始化队列
Quene* initQuene()
{
    Quene *Q=(Quene*)malloc(sizeof(Quene));
    for (int i = 0; i < 10; i++)
    {
        Q->filename[i]=(char*)malloc(80);
    }
    Q->rear=Q->front=0;
    return Q;
}
//BFS
void DirBfs(DIR *dirp,char* lastpath,Quene*Q)
{
    int ans;
    while((direntp = readdir(dirp))!=NULL)
    {
    char path[1024];
    memset(path, 0, 1024);
    strcpy(path, lastpath);
    strcat(path, "/");
    strcat(path, direntp -> d_name);
    if(strcmp(direntp->d_name,"..")!=0&&strcmp(direntp->d_name,".")!=0)
    {
    //文件名入队列
    // printf("%s\n",path);
    strcpy(Q->filename[Q->rear],path);
    // Q->filename[Q->rear]==path;
    Q->rear++;
    }
    }
    //出队列
    while (Q->front!=Q->rear)
    {
        //如果是目录，子文件入队列
        if(GetFileSizeTime(Q->filename[Q->front])==1)
        {
        DIR *dirp2;
        dirp2=opendir(Q->filename[Q->front]);
        ans=Q->front;
        Q->front++;
        DirBfs(dirp2,Q->filename[ans],Q);
        }
        //如果是文件
        else
        {
            Q->front++;
        }
    }
    return;    
}
int main(int argc,char **argv)
{
    //三个参数 最后一个用来选择遍历类型
    if((dirp1=opendir(argv[1]))==NULL)
    //打开目录，将打开的目录信息放至 dirp 中，若为空，则打开失败
    {
        printf("Open Directory %s Error:%s\n",argv[1],strerror(errno));
        exit(1);
    }
    if(atof(argv[2])==DFS)
    {
        DirDfs(dirp1,argv[1]);
    }
    if(atof(argv[2])==BFS)
    {
        Quene* Q=initQuene();
        DirBfs(dirp1,argv[1],Q);
    }
    closedir(dirp1);
    exit(1);
}