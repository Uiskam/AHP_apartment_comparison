import numpy as np
from scipy.stats.mstats import gmean
import math

class PCMatrix:

    def __init__(self, matrix, method):
        self.method = method
        self.matrix = matrix
        if self.method=="gmm":
            self.ci = self.gci()
            self.priority_vector = self.gmm()
        elif self.method=="evm":
            self.ci = self.evm_cr()
            self.priority_vector = self.evm()

    def is_consistent(self):
        if self.method=="gmm":
            treshhold = [0.3147, 0.3526, 0.370]
            return self.ci <= treshhold[max(min(len(self.matrix), 4), 3)-3]
        else:
            return self.ci <= 0.1

    def gmm(self):
        gmeans = [gmean(row) for row in self.matrix]
        return [x / sum(gmeans) for x in gmeans]

    def evm(self):
        d = np.linalg.eig(np.array(self.matrix))
        e = d[1][:, np.argmax(d[0])]
        return np.round(np.real(e/e.sum()), 3).tolist()

    def evm_cr(self):
        eig_val = np.linalg.eig(self.matrix)[0].max()
        return np.round(np.real((eig_val - len(self.matrix))/((2.7699 * len(self.matrix) - 4.3513)-len(self.matrix))), 3)

    def gci(self):
        n = len(self.matrix)
        gmeans = [gmean(row) for row in self.matrix]
        return 2 / ((n - 1) * (n - 2)) * sum(
            [(math.log(self.matrix[i][j] * gmeans[j] / gmeans[i])) ** 2 for i in range(n) for j in range(i + 1, n)])

