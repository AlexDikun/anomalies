# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN


class SubHandler(object):

    """
    Client to subscription. It will receive events from server

    tags: list of all processed network nodes;
    storage: multilist for recording the values of processed nodes;

    """

    def __init__(self, tags):
        self.tags = tags
        self.storage = [ [] for i in range(len(tags)) ]

    def datachange_notification(self, node, val, data):
       i = self.tags.index(node)
       self.storage[i].append(val)

       print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)

    @staticmethod
    def airflowMethod(arr:np.array, mini:float, maxi:float):
        """


        Parameters
        ----------
        arr : np.array
            1D float ndarray.
        mini : float
            min allowed value.
        maxi : float
            max allowed value.

        Returns
        -------
        flag : bool
            If True - anomalies found.
    		If False - anomalies not found.

        """
        time = np.arange(len(arr))

        truly = (arr > mini) == (arr < maxi)
        x1 = time[truly]
        y1 = arr[truly]
        falsely = np.invert(truly)
        x2 = time[falsely]
        y2 = arr[falsely]

        print("Outlier detected: ", falsely.sum())

        fig, ax = plt.subplots()
        ax.plot(x1, y1, 'b.', markersize=1, label="data points")
        ax.plot(x2, y2, 'r.', markersize=1, label="outlier scores")
        ax.set_xlabel("time")
        ax.set_ylabel("sensor readings")
        ax.set_title("airflow method", fontsize=10)
        legend = ax.legend(loc='upper left')
        legend.legendHandles[0]._sizes = [5]
        legend.legendHandles[1]._sizes = [10]
        plt.show()

        flag = True if falsely.sum() != 0 else False
        return flag


    @staticmethod
    def find_repeat(arr:np.array, freezing=None, flag=False):
        """


        Parameters
        ----------
        arr : np.array
            1D float ndarray.
        freezing : int
            Required length to recognize anomalous subarray.
    		If None, then -> 1/10 of arr.size. The default is None.
        flag : bool
            If False, looking for the longest anomaly.
            If True,  looking for the last anomaly. The default is False.

        Returns
        -------
        flag : bool
            If True - anomalies found.
    		If False - anomalies not found.

        """
        size = arr.size

        if freezing == None:
        	freezing = size // 10

        time = np.arange(size)

        tmp = np.empty(size, dtype=bool)
        tmp[0] = True
        np.not_equal(arr[:-1], arr[1:], out=tmp[1:])
        indices = np.nonzero(tmp)[0]
        elements = np.diff(np.append(indices, size))

        fig, ax = plt.subplots()
        ax.set_xlabel("time")
        ax.set_ylabel("sensor readings")
        ax.set_title("Finding Frozen Signals", fontsize=10)

        try:
        	index = np.where(elements > freezing)
        	index = index[0] # transferring in ndarray from tuple
        	index = np.max(index) if flag == False else index[-1]
        	left = indices[index]
        	try:
        		right = indices[index + 1]
        	except IndexError:
        		right = len(arr) + 1
        	mask = np.full(size, False)
        	mask[left:right] = True

        	x1 = time[mask]
        	y1 = arr[mask]

        	print("Anomalies detected: ", mask.sum())

        	ax.plot(time, arr, 'b.', markersize=1, label="data points")
        	ax.plot(x1, y1, 'r.', markersize=1, label="anomalies scores")
        	legend = ax.legend(loc='upper left')
        	legend.legendHandles[0]._sizes = [5]
        	legend.legendHandles[1]._sizes = [10]

        	flag = True

        except ValueError:
        	print("Anomalies detected: 0")

        	ax.plot(time, arr, 'b.', markersize=1, label="data points")
        	legend = ax.legend(loc='upper left')
        	legend.legendHandles[0]._sizes = [5]

        	flag = False

        plt.show()

        return flag


    @staticmethod
    def locOutFac(arr:np.array):
        """


        Parameters
        ----------
        arr : np.array
            1D float ndarray.

        Returns
        -------
        flag : bool
            If True - anomalies found.
    		If False - anomalies not found.

        """
        time = np.arange(len(arr))
        matrix = np.array((time, arr))
        matrix = matrix.T

        outlier_detection = LocalOutlierFactor(n_neighbors=20)
        pred = outlier_detection.fit_predict(matrix)

        truly = pred != -1
        x1 = time[truly]
        y1 = arr[truly]

        falsely = np.invert(truly)
        x2 = time[falsely]
        y2 = arr[falsely]

        print("Outlier detected: ", falsely.sum())

        fig, ax = plt.subplots()
        ax.plot(x1, y1, 'mD', markersize=1, label="data points")
        ax.plot(x2, y2, 'r.', markersize=1, label="outlier scores")
        ax.set_xlabel("time")
        ax.set_ylabel("sensor readings")
        ax.set_title("Local outlier factor", fontsize=10)
        legend = ax.legend(loc='upper left')
        legend.legendHandles[0]._sizes = [5]
        legend.legendHandles[1]._sizes = [10]
        print("Outlier detected: ", falsely.sum())
        plt.show()

        flag = True if falsely.sum() != 0 else False
        return flag


    @staticmethod
    def locOutFac2(arr:np.array):
        """


        Parameters
        ----------
        arr : np.array
            1D float ndarray.

        Returns
        -------
        flag : bool
            If True - anomalies found.
    		If False - anomalies not found.

        """
        time = np.arange(len(arr))
        matrix = np.array((time, arr))
        matrix = matrix.T

        outlier_detection = LocalOutlierFactor(n_neighbors=20)
        pred = outlier_detection.fit_predict(matrix)
        print(pred)
        arr_scores = outlier_detection.negative_outlier_factor_
        radius = (arr_scores.max() - arr_scores) / (arr_scores.max()
    												- arr_scores.min())

        falsely = (pred == -1)
        x1 = time[falsely]
        y1 = arr[falsely]
        r1 = radius[falsely]

        print("Outlier detected: ", falsely.sum())

        fig, ax = plt.subplots()
        ax.scatter(matrix[:, 0], matrix[:, 1], color='k', s=2., label='data points')
        ax.scatter(x1, y1, s=r1, edgecolors='r',
    	            facecolors='none', label='outlier scores')
        ax.set_title("Local outlier factor with classifier")
        ax.set_xlabel("time")
        ax.set_ylabel("sensor readings")
        ax.axis('tight')
        legend = plt.legend(loc='upper left')
        legend.legendHandles[0]._sizes = [5]
        legend.legendHandles[1]._sizes = [10]
        plt.show()

        flag = True if falsely.sum() != 0 else False
        return flag


    @staticmethod
    def extreme_value_analysis(arr:np.array, threshold=3):
        """


        Parameters
        ----------
        arr : np.array
            1D float ndarray.
        threshold : int
            This is a threshold, anything above which will be considered
            extreme data. The default is 3.

        Returns
        -------
        flag : bool const
            If True - extreme points found.
            If False - extreme points not found.


        """
        from scipy import stats

        z_val = stats.zscore(arr)
        z_min, z_max = np.min(z_val), np.max(z_val)
        z_val = np.abs(z_val)
        res = z_val >= threshold

        flag = True in res

        if flag:
            print("Extreme points detected!")
        else:
            print("Extreme points not found!")

        print("Lowest Z-score: ", z_min)
        print("Highest Z-score: ", z_max)
        fig, ax = plt.subplots()
        ax.boxplot(arr)
        plt.show()

        return flag


    @staticmethod
    def dbscan_analysis(arr:np.array, eps=3, n=3):
        """


        Parameters
        ----------
        arr : np.array
            1D float ndarray.
        eps : int, float
            The maximum distance between two samples for one to be considered
            as in the neighborhood of the other. The default is 3.
        n : int
            The number of samples (or total weight) in a neighborhood for a point
            to be considered as a core point. This includes the point it self.
            The default is 3.

        Returns
        -------
        flag : bool const
            If True - extreme points found.
            If False - extreme points not found.

        """
        time = np.arange(len(arr))
        matrix = np.array((time, arr))
        matrix = matrix.T

        outlier_detection = DBSCAN(eps=eps, min_samples=n)
        pred = outlier_detection.fit_predict(matrix)

        truly = pred != -1
        x1 = time[truly]
        y1 = arr[truly]

        falsely = np.invert(truly)
        x2 = time[falsely]
        y2 = arr[falsely]

        fig, ax = plt.subplots()
        ax.plot(x1, y1, 'g.', markersize=1, label="data points")
        ax.plot(x2, y2, 'k.', markersize=1, label="outlier scores")
        ax.set_xlabel("time")
        ax.set_ylabel("sensor readings")
        ax.set_title("DBSCAN analysis", fontsize=10)
        legend = ax.legend(loc='upper left')
        legend.legendHandles[0]._sizes = [5]
        legend.legendHandles[1]._sizes = [10]
        print("Outlier detected: ", falsely.sum())
        plt.show()

        flag = True if falsely.sum() != 0 else False
        return flag


if __name__ == '__main__':
	pass
