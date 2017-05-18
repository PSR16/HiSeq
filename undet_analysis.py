import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

has_N = pd.read_csv('count.csv', sep='\t')
no_N = pd.read_csv('count_noN.csv', sep='\t')


#cumulativeSum_N = has_N['count'].cumsum()
#print(cumulativeSum_N)

H, X1 = np.histogram(has_N['count'], bins = 50, normed = True)
dx = X1[1] - X1[0]
F1 = np.cumsum(H)*dx

plt.plot(X1[1:], F1)
plt.title('Barcodes with N')
plt.savefig('ecdfN.jpg')

J, X2 = np.histogram(no_N['count'], bins = 15, normed=True)
dx = X2[1] - X2[0]
F2 = np.cumsum(J)*dx

plt.plot(X2[1:], F2)
plt.title('Barcodes with no N')
plt.savefig('ecdf_noN.jpg')


