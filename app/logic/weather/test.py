
x = {}
xkey = []

for i in range(1, 5):
    x[i] = []
    xkey.append(i)

print(xkey)

x[1].append([0, 0, 0])
x[1].append([0, 0, 0])
x[2].append([1, 1, 1])
x[3].append([2, 2, 2])
x[4].append([3, 3, 3])

print(x)

y = {}
y[1] = []
y[2] = []
y[3] = []
y[4] = []

for key in xkey:
    y[key] = x.pop(key)


print(y)
print(x)
