#lists all the item no in both sets
def setDiff(x, y):
    return (x - y) | (y - x)

def setPrint(x):
    for i in x:
        print(i)

def dictPrint(x):
    for k in x:
        print(x[k])

def norm(xs, percet=True):
    s = sum(xs)
    for i, x in enumerate(xs):
        if percet:
            xs[i] /= s * 100
        else:
            xs[i] /= s
    return xs