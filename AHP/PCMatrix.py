from scipy.stats.mstats import gmean
import math

class PCMatrix:
    def __init__(self, matrix):
        self.matrix = matrix

        gmeans = [gmean(row) for row in matrix]
        self.priority_vector = [x / sum(gmeans) for x in gmeans]

        n = len(matrix)
        self.gci = 2 / ((n - 1) * (n - 2)) * sum(
            [(math.log(self.matrix[i][j] * gmeans[j] / gmeans[i])) ** 2 for i in range(n) for j in range(i + 1, n)])







