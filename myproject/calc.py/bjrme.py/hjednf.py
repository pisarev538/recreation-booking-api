n=int(input())
operations=[]
summs=[]
for i in range(n):
    operations.append(list(input().split()))
    operations[i][0]=int(operations[i][0])
    operations[i][1]=int(operations[i][1])
    summ=2*operations[i][0]
    if operations[i][2]=='L':
        summ+=3
    elif operations[i][2]=='N':
        summ+=4
    else:
        summ+=5
    summs.append(summ)
ind=summs.index(max(summs))
answer=operations[ind][3]
print(answer)