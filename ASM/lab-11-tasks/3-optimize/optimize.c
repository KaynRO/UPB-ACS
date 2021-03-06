#include<stdio.h>
#include<sys/time.h>

#define N 1000000
unsigned long long a;

void doSomething(int i)
{
    a += i;
}

void doSomethingElse(int i)
{
    a += i + 2;
}

void doYetSomethingElse(int i)
{
    a += i*3 + 2;
}

void main()
{
    int i;
    int var;
    printf("Insert an integer:\n");
    scanf("%d", &var);

    struct timeval t0, t1;
    gettimeofday(&t0, NULL);
    for (i = 0; i < N; i++)
    {
        if (var % 2 == 0)
            doSomething(i);
        else if (var % 3 == 0)
            doSomethingElse(i);
        else
            doYetSomethingElse(i);
    }
    gettimeofday(&t1, NULL);
    long elapsed = (t1.tv_sec - t0.tv_sec)*1000000 + t1.tv_usec - t0.tv_usec;
    printf("[Non-optimized] Computed: %d in: %ld seconds\n", a, elapsed);

    a = 0;
    int x = N ;
    int y = N - 1 ;

    if(N % 2 == 0)
        x = N / 2 ;
    else y = ( N - 1 ) / 2 ;

    struct timeval t0op, t1op;
    gettimeofday(&t0op, NULL);

    if(var % 2 == 0)
        a = x * y ;

    else if(var % 3 == 0)
            a = x * y + 2 * N ;
    else a = 2 * N + 3 * x * y ;

    gettimeofday(&t1op, NULL);
    long elapsed2 = (t1op.tv_sec - t0op.tv_sec)*1000000 + t1op.tv_usec - t0op.tv_usec;
    printf("[Optimized] Computed: %d in: %ld seconds\n", a, elapsed2);
}
