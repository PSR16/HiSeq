import pandas as pd

filename = 'files.txt'
with open(filename, 'r') as f:
	codes = []
	for line in f:
		barcode = line.rsplit(":", 1)
		bc = barcode[1].strip()
		codes.append(bc)

#list of 24 samples
df = pd.DataFrame({'barcodes': codes})
df['forward'], df['reverse'] = zip(*df['barcodes'].apply(lambda x: x.split('+', 1)))
df.drop('barcodes', axis=1, inplace=True)

df.to_excel('24.xlsx')

#96 combinations
compare = pd.read_excel('Adapter Plan.xlsx', sheetname=2)
compare.drop(compare.columns[[0,1,3]], axis=1, inplace=True)
compare.columns = ['forward', 'reverse']


merged = pd.merge(compare, df, on = ['forward', 'reverse'], how='left', indicator=True)

merged.to_excel('merged.xlsx')
print(merged.loc[merged['_merge']=='both']) 

counts = pd.read_csv('count.csv', sep='\t')
counts_noN = pd.read_csv('count_noN.csv', sep='\t')
counts_noN.drop(counts_noN.columns[0], axis=1, inplace=True)

withN = pd.merge(compare, counts_noN, on = ['forward', 'reverse'], how='left', indicator=True)
compare2 = withN.loc[withN['_merge']=='both']
compare2.to_excel('96vsNoN.xlsx')

print(compare2)
