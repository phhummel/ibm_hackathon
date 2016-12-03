from sklearn import tree
from sklearn.datasets import load_iris
from sklearn import tree
import pydotplus 
from IPython.display import Image 
import numpy as np

iris = load_iris()
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
clf = clf.fit(data[:6,:], label[:6])

print(clf.classes_)
dot_data = tree.export_graphviz(clf, out_file=None) 
graph = pydotplus.graph_from_dot_data(dot_data) 
graph.write_pdf("machDC.pdf") 

print(clf.predict_proba(data[7:]))