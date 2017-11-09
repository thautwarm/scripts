
from Ruikowa.ErrorFamily import handle_error
from Ruikowa.ObjectRegex.MetaInfo import MetaInfo
from plot_parser import DataSets, token
import sys
import numpy as np

parser = handle_error(DataSets)
train, test = sys.argv[1:]

def parse(string):
    return parser(token(string), meta = MetaInfo(), partial=False)

with open(train, encoding='utf8') as train, open(test, encoding='utf8') as test:
    datasets = parse(train.read())
    tests = parse(test.read())
    

X = []
y_true = []
y_pred = []
for data in datasets:
    X.append([float(''.join(i)) for i in data[:-1]])
    y_true.append(float(''.join(data[-1])))

for test in tests:
    y_pred.append(float(''.join(test[0])))

targets = np.array(y_true)
outputs = np.array(y_pred)
datas = np.array(X)
from matplotlib import pyplot as plt
plt.subplot(311)
plt.title("True Categories")
plt.scatter(datas[:,0], datas[:, 1], c = targets)
plt.subplot(313)
plt.title("Predictions")
plt.scatter(datas[:,0], datas[:, 1], c = outputs )
plt.show()


    
