from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.linear_model import SGDClassifier
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
import sys

def main():
	if len(sys.argv) == 1:
		print 'need filename'
		sys.exit(-1)
	else:
		infilename = sys.argv[-1]
		print infilename

	#npzfile = np.load('data/unigram_bigram_ner_senti_pos_lda_data.npz')
	npzfile = np.load(infilename)
	X = npzfile['X']
	y = npzfile['y']
	print(np.shape(X))

	
	# Split the dataset to train/test set
	X_train, X_test, y_train, y_test = train_test_split(
	    X, y, test_size=0.2, random_state=0)


	# Set the parameters by cross-validation
	Alphas = np.logspace(-6, 1, 10)
	L1_ratio = np.linspace(0,1, 10)
	tuned_parameters = [{'penalty': ['l1','l2'], 'loss': ['hinge'], 'n_iter':[500],'alpha':Alphas, 'l1_ratio':L1_ratio}]

	clf = GridSearchCV(SGDClassifier(class_weight= 'balanced'), tuned_parameters, cv=5, scoring= None)
	clf.fit(X_train, y_train)

	print("Best parameters set found on development set:")
	print(clf.best_params_)
#	print("Grid scores on development set:")
#	for params, mean_score, scores in clf.grid_scores_:
#	   	print("%0.3f (+/-%0.03f) for %r"
#		% (mean_score, scores.std() * 2, params))

#	print("Detailed classification report:")
#	print("The model is trained on the full development set.")
#	print("The scores are computed on the full evaluation set.")

	y_true, y_pred = y_test, clf.predict(X_test)
	auc = roc_auc_score(y_true, y_pred)

	print 'accuracy = ' + str(accuracy_score(y_true, y_pred))
	print 'auc = ' + str(auc)
		
	

if __name__ == "__main__":
    main()


'''
E:\DR\SocialNetwork\user_classification>python run_sgd.py data/unigram_bigram_lda_data.npz
data/unigram_bigram_lda_data.npz
Best parameters set found on development set:
{'penalty': 'l1', 'loss': 'hinge', 'n_iter': 500}
Grid scores on development set:
0.493 (+/-0.065) for {'penalty': 'l1', 'loss': 'hinge', 'n_iter': 500}
Detailed classification report:
The model is trained on the full development set.
The scores are computed on the full evaluation set.
accuracy = 0.894736842105
auc = 0.923076923077
'''

