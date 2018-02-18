def intersect (startTime,endTime, startTime2, endTime2, *args):
    freeTime =[]
    freeTime2 = []
    freeMixed = []

        
    for i in range (0, len(startTime)-1):
        freeTime+= list(range(endTime[i], 1+startTime[i+1]))
    for i in range(len(startTime2)-1):
        freeTime2+= list(range(endTime2[i], 1+ startTime2[i+1]))
        
    max1= freeTime[len(freeTime)-1]
    max2= freeTime2[len(freeTime2)-1]

    min1= startTime[0]
    min2= startTime2[0]

    while (max1<=10080):
        freeTime.append(max1)
        max1=max1+1
    while (max2<=10080):
        freeTime2.append(max2)
        max2=max2+1

    while (min1 > 0):
        freeTime.append(min1)
        min1=min1-1
    while (min2 > 0):
        freeTime2.append(min2)
        min2=min2-1
        

    intersect =sorted(list(set(freeTime) & set(freeTime2)))
    theArray=[]

    for i in range(0,len(intersect)-1):
        if (intersect[i+1] - intersect[i] != 1):
        
            h1 =str(int(intersect[i]/60))
            r1 =str(int(intersect[i]%60))
            
            h2 =str(int(intersect[i+1]/60))
            r2 =str(int(intersect[i+1]%60))
            
            p1 = h1+":"+r1
            p2 =h2+":"+r2
            together = p1 +" to " +p2
            #print(rd)
            fullThing = rd+" "+together

            freeMixed.append({"date": rd, "start": p1, "end": p2})
        
            
        i=i+1
    return freeMixed