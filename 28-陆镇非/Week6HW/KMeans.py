# Author: Zhenfei Lu
# Created Date: 5/18/2024
# Version: 1.0
# Email contact: luzhenfei_2017@163.com, zhenfeil@usc.edu

import numpy as np
import sys

class Kobject(object):
    def __init__(self, center):
        self.center = center
        self.children = list()

    def pickNewCenter(self, metric) -> bool:
        self.children.append(self.center)
        stacked_array = np.stack(tuple(self.children), axis=0)
        average_array = np.mean(stacked_array, axis=0)
        self.children.pop(len(self.children)-1)
        if np.all(np.abs(self.center - average_array) <= metric):
            return False
        self.center = average_array
        return True

    def clearChildren(self) -> None:
        self.children.clear()

class KMeans(object):
    def __init__(self, clusters):
        self.clusters = clusters
        self.Kobjects = list()

    def fit(self, data: np.ndarray, epoches, metric, batch_size) -> tuple:
        self.Kobjects.clear()
        N = data.shape[0]
        if(N%batch_size!=0):
            print("N mod batch size is not equal to 0. Please choose another batch size")
            return None
        if(self.clusters > N):
            print("clusters > N")
            return None
        for i in range(0, self.clusters):  # init guess
            self.Kobjects.append(Kobject(data[i]))

        for k in range(0+1, epoches+1):
            if(k == 1):
                start_index = self.clusters
                dict_index_type = dict()
                for i in range(0, self.clusters):
                    dict_index_type[i] = i
            else:
                start_index = 0
                dict_index_type = dict()
            for t in range(0, N//batch_size):
                if(k == 1 and t == 0):
                    start_index = self.clusters
                    end_index = batch_size
                else:
                    start_index = t*batch_size
                    end_index = start_index + batch_size
                for i in range(start_index, end_index):
                    # print(i)
                    min_dist = sys.maxsize
                    min_index = None
                    for j in range(0, len(self.Kobjects)):
                        temp_dist = np.linalg.norm(data[i]-self.Kobjects[j].center, ord=2, axis=0)
                        if(temp_dist<min_dist):
                            min_dist = temp_dist
                            min_index = j
                    if(min_index is not None):
                        self.Kobjects[min_index].children.append(data[i])
                        dict_index_type[i] = min_index
                flag_arr = []
                for i in range(0, len(self.Kobjects)):
                    flag = self.Kobjects[i].pickNewCenter(metric)
                    flag_arr.append(flag)
                    # print(flag_arr)
                if not any(flag_arr) and t==(N//batch_size)-1: # make sure t is looping for the end of the batch
                    # print(t)
                    print("Solved Kmeans with iter = " + str(k))
                    return (self.Kobjects, dict_index_type)
                else:
                    if(k != epoches):
                        for i in range(0, len(self.Kobjects)):
                            self.Kobjects[i].clearChildren()
        print("May not solve Kmeans and reached the max iter = " + str(epoches))
        return (self.Kobjects, dict_index_type)

    def fit4image(self, img: np.ndarray, epoches, metric, batch_size):
        w, h = img.shape[0:2]
        data = img.reshape((w*h, -1))
        # imgOutput = img.copy()  # deepcopy, new array will not influence the original array
        Kobjects, dict_index_type = self.fit(data, epoches, metric, batch_size)
        # print(len(dict_index_type))
        center_arr = np.array([x.center for x in Kobjects])
        type_arr = np.array([value for key, value in dict_index_type.items()])
        # print(center_arr[type_arr].shape)
        # for i in range(0, len(Kobjects)):
        #     for j in range(0, len(Kobjects[i].children)):
        #         indices = np.where(imgOutput == Kobjects[i].children[j])
        #         imgOutput[indices] = Kobjects[i].center
        return center_arr[type_arr].reshape(img.shape).astype(int)
