#~/usr/bin/python
import gzip
import pandas as pd
import pysam
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

file = 'Undetermined_S0_L003_R1_001.fastq.gz'
with gzip.open(file, 'rb') as f:
	id = []
	#Get barcode
	for ln in f:
		if ln.startswith("@"):
			barcode = ln.rsplit(":", 1)
			#print(barcode[1])
			id.append(barcode[1].strip())
		if len(id) == 1000:
			break

#print(id)			
df = pd.DataFrame({'barcodes': id})
df['forward'], df['reverse'] = zip(*df['barcodes'].apply(lambda x: x.split('+', 1)))
grouped = df.groupby(['forward','reverse'])["barcodes"].count().reset_index(name="count")

#print(df)
print(grouped)

pivoted = grouped.pivot(index="forward", columns="reverse")
pivoted.fillna(0, inplace=True)
print(pivoted)

fig, ax = plt.subplots()
sns.heatmap(data=pivoted, ax=ax)
sns.plt.show()
