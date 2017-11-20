import numpy as np

norm2 = np.linalg.norm


def make_n(n: int, *, low: np.float, high: np.float):
    return np.array([np.random.random() * (high - low) + low for _ in range(n)])


def optional_mean(vectors: np.ndarray, default=None):
    return np.mean(vectors, 0) if vectors.shape[0] is not 0 else default


class KMeans:
    def __init__(self, iteration=100, n_cluster=3, kernel=lambda x, y: norm2(x - y)):
        self.iteration = iteration
        self.kernel = kernel
        self.n_cluster = n_cluster
        self.centers = None
        self.predict = np.vectorize(self.predict_each, signature='(m)->()')

    def fit(self, X: np.ndarray, y=None):
        if self.centers is None:
            self.centers = np.array([make_n(self.n_cluster, low=min(dim), high=max(dim)) for dim in X.T]).T
        n, _ = X.shape

        for _ in range(self.iteration):
            y = self.predict(X)
            self.centers = np.array([optional_mean(X[y == tag], self.centers[tag]) for tag in range(self.n_cluster)])

    def predict_each(self, x):
        return np.argmax([self.kernel(x, center) for center in self.centers])
