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
	has_N = []
	no_N = []
	#Get barcode
	for ln in f:
		if ln.startswith("@"):
			barcode = ln.rsplit(":", 1)
			#print(barcode[1])
			bc = barcode[1].strip()
			if "N" in bc:
				has_N.append(bc)
			else:
				no_N.append(bc)
#		if len(no_N) == 50:
#			break

#Barcodes w/ N
df = pd.DataFrame({'barcodes': has_N})
df['forward'], df['reverse'] = zip(*df['barcodes'].apply(lambda x: x.split('+', 1)))
grouped_N = df.groupby(['forward','reverse'])["barcodes"].count().reset_index(name="count")

#print(df)
print(grouped_N)

grouped_N.to_csv('count.csv', sep='\t')

pivoted = grouped_N.pivot(index="forward", columns="reverse")
pivoted.fillna(0, inplace=True)
print(pivoted)


#heatmap = sns.heatmap(data=pivoted)
#fig = heatmap.get_figure()
#fig.savefig('heatmap.png')

#Barcodes w/o N
df_noN = pd.DataFrame({'barcodes': no_N})
df_noN['forward'], df_noN['reverse'] = zip(*df_noN['barcodes'].apply(lambda x: x.split('+', 1)))
grouped_noN = df_noN.groupby(['forward','reverse'])["barcodes"].count().reset_index(name="count")

print(grouped_noN)
grouped_noN.to_csv('count_noN.csv', sep='\t')

pivoted = grouped_noN.pivot(index="forward", columns="reverse")
pivoted.fillna(0, inplace=True)
print(pivoted)

#heatmap = sns.heatmap(data=pivoted)
#fig = heatmap.get_figure()
#fig.savefig('heatmap_noN.png')
