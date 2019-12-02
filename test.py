import numpy as np

a = np.array([1, 2, 3, 4])
b = np.array([1, 1, 1, 1])

print(a)
print(b)


vector = []
vector.append(a)
vector.append(b)
featureVector = []
for v in vector:
    for fv in v.tolist():
        featureVector.append(fv)

print(featureVector)
