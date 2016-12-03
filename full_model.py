import numpy as np
import pandas as pd
from sklearn import tree

def extract_p_precipi(precrop,precipi,precipi_table):
	precipi_int = np.int64(precipi*(1.0/100))
	if precrop == 'wei':
		return precipi_table[precipi_int,0]
	elif precrop == 'ger':
		return precipi_table[precipi_int,4]
	else:
		return precipi_table[precipi_int,1]

def extract_p_pH(precrop,pH,pH_table):
	pH_int = np.int64((pH - 5)*2)
	if precrop == 'wei':
		return pH_table[4,pH_int]
	elif precrop == 'ger':
		return pH_table[1,pH_int]
	else:
		return pH_table[3,pH_int]

def extract_p_mac(pH,precipi,precrop,mac,mac_clf):
	if precrop == 'wei':
		pred = mac_clf.predict([[pH,precipi,1,0,0]])
	elif precrop == 'ger':
		pred = 	mac_clf.predict([[pH,precipi,0,1,0]])
	else:
		pred = 	mac_clf.predict([[pH,precipi,0,0,1]])
	if pred == mac:
		return 0.6
	elif pred == 'cc':
		return 0.3
	else:
		return 0.1

def extract_p_post(postcrop, precrop, precrop_table):
	if precrop == 'wei':
		row = 3
	elif precrop == 'ger':
		row = 2
	else:
		row = 1
	if postcrop == 'wei':
		col = 0
	elif postcrop == 'ger':
		col = 2
	else:
		col = 7
	return (precrop_table[row,col]+precrop_table[row,col+1])/2.

def map_nextCrop(postcrop, pH, pH_table, precipi, precipi_table, precrop, precrop_table, machine, machine_clf):
	p_precipi = extract_p_precipi(precrop,precipi,precipi_table)
	p_pH = extract_p_pH(precrop,pH,pH_table)
	p_mac = extract_p_mac(pH,precipi,precrop,machine,machine_clf)
	p_post = extract_p_post(postcrop,precrop,precrop_table)
	return -np.log(p_precipi*p_pH*p_mac*p_post)

clf = tree.DecisionTreeClassifier()
# data = ['pH','mm','vorfr']
data = np.array([[7.0,800,1,0,0],
				[7.0,800,0,1,0],
				[7.0,800,0,0,1],
				[6.0,750,1,0,0],
				[7.0,900,1,0,0],
				[7.0,900,0,1,0],
				[7.5,850,1,0,0],
				[7.5,850,0,1,0]
	])
label = ['cc','ce','ce','ca','ca','ce','ce','ce']
clf = clf.fit(data, label)

precipi_table = np.array(pd.read_csv('niederschlag.csv', index_col=0));

pH_table = np.array(pd.read_csv('boden_table.csv', index_col=0));

precrop_table = np.array(pd.read_csv('vorfrucht_table.csv', index_col=0));


print(map_nextCrop('wei',5.5,pH_table,600,precipi_table,'wei',precrop_table,'ce',clf))

print(map_nextCrop('ger',5.5,pH_table,600,precipi_table,'wei',precrop_table,'ce',clf))

print(map_nextCrop('mai',5.5,pH_table,600,precipi_table,'wei',precrop_table,'ce',clf))


