import matplotlib.pyplot as plt

def fun(x):
    return x*x + 2

def Fun(y, x):
    return 2*x

print(fun(2))

a = 0
b = 4
n = 100
alfa = 2
h=(b-a)/n

x = []
y = []
yc = []
yc.append(alfa)



for i in range(n+1):
    xi = i*h
    x.append(xi)
    y.append(fun(xi))
for i in range(n):
    yc.append( yc[i] + h * Fun(yc[i], x[i]))


plt.plot(x, y, x, yc)
plt.show()