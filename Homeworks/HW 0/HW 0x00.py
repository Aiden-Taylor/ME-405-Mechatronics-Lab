from matplotlib import pyplot
time = []
height = []
labels = []
f = open('data.csv', 'r')
with open('data.csv', 'r') as f:
    labels = f.readline().replace('\n', '').split(',')
    for x in f:
        x = x.split('#')
        x = x[0].split(',')
        if (x[0] != "\n") & (x[0] != ''):
            #print(x)
            try:
                time.append(float(x[0]))
            except Exception as e:
                print(e)
            try:
                height.append(float(x[1].replace('\n', '')))
            except Exception as e:
                print(e)
pyplot.plot(time, height) 
x = labels[0]   
y = labels[1]
pyplot.xlabel(x)         
pyplot.ylabel(y)
pyplot.show()
#print(time)    
#f.close()