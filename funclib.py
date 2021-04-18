import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# sns.set()

from sklearn.neighbors import LocalOutlierFactor


def airflowMethod(arr:np.array, mini:float, maxi:float):
	""" Parametrs:
			arr : 1D float ndarray, y axis;
			mini and maxi: min and max allowed value;

		Function block:
			time : x axis;

			trutly : data point bool mask;
			x1, y1 :  axes for data point

			falsely : outlier scores bool mask;
			x2, y2 :  axes for outlier scores

			...
			return None

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
	return None


def find_repeat(arr:np.array, freezing=None, flag=False):
	""" Parametrs:
			arr : 1D float ndarray, y axis;
			freezing : int or None,
					   required length to recognize anomalous subarray;
					   if None, then -> 1/10 of arr.size;
			flag : if False, looking for the longest anomaly,
					if True,  looking for the last anomaly;

		Function block:
			time : x axis;
			tmp : temporary array for masks;
			indices : array of indices for each first element from
					  the new series;
			elements : an array storing the number of elements in
					   the required subarrays (series);
			index : subarray start index for indices, elements;
			left : the starting index of the anomaly in the input array;
			right : the last anomaly index in the input array;
			mask : anomalies scores bool mask;
			x1, y1 :  axes for anomalies scores

			...
			flag: boolean constant. If True - anomalies found,
									if False - anomalies not found;
			return bool(flag)

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


def locOutFac(arr:np.array):
	""" Parametrs:
			arr : 1D float ndarray, y axis;

		Function block:
			time : x axis;
			matrix : prepared structured data for predict;

			outlier_detection : LocalOutlierFactor class object,
								needed to predict anomalies;
			pred : predictive array, where -1 is the outlier;

			trutly : data point bool mask;
			x1, y1 :  axes for data point

			falsely : outlier scores bool mask;
			x2, y2 :  axes for outlier scores

			...
			draws a graph without classifier
			...
			return None

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
	return None


def locOutFac2(arr:np.array):
	""" Parametrs:
			arr : 1D float ndarray, y axis;

		Function block:
			time : x axis;
			matrix : prepared structured data for predict;

			outlier_detection : LocalOutlierFactor class object,
								needed to predict anomalies;
			pred : predictive array, where -1 is the outlier;
			arr_scores : It is the average of the ratio of the local reachability
						density of a sample and those of its k-nearest neighbors.
			radius : an array of local density values ​​for each data point;

			trutly : data point bool mask;
			x1, y1 :  axes for data point

			falsely : outlier scores bool mask;
			x2, y2 :  axes for outlier scores

			...
			draws a graph with a classified circle
			...
			return None

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
	return None


if __name__ == '__main__':
	pass
