# _*_ coding: UTF-8 _*_
# @Time: 2024/5/23 19:54
# @Author: iris
# @Email: liuhw0225@126.com
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from matplotlib import pyplot as plt

if __name__ == '__main__':
    X = [[1, 2], [3, 2], [4, 4], [1, 2], [1, 3]]
    Z = linkage(X, 'ward')
    f = fcluster(Z, 4, 'distance')
    fig = plt.figure(figsize=(5, 3))
    dn = dendrogram(Z)
    print(Z)
    plt.show()
