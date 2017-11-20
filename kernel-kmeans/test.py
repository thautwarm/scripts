import kernel
from matplotlib import pyplot as plt
import numpy as np
dot_product = lambda x,y: np.dot(x, y)
def experiement(n_cluster=3, n_size=500, r=5):
        X = (2*r)*(np.random.sample((n_size, 2))-0.5)
        clf = kernel.KMeans(kernel = dot_product, n_cluster=n_cluster)
        clf.fit(X)
        y = clf.predict(X)
        plt.scatter(X[:,0], X[:,1], c= y);plt.show()

if __name__ == '__main__':
    experiement()


