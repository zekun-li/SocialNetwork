from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
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
	    X, y, test_size=0.4, random_state=0)


	# Set the parameters by cross-validation
	tuned_parameters = [{'penalty': ['l2'], 'C':np.logspace(-5, 4, 10), 'solver': ['sag'] ,'max_iter':[500] },
						{'penalty': ['l2'], 'C':np.logspace(-5, 4, 10), 'solver': ['newton-cg'] ,'max_iter':[500] },
						{'penalty': ['l2'], 'C':np.logspace(-5, 4, 10), 'solver': ['lbfgs'] ,'max_iter':[500] },
						{'penalty': ['l2','l1'], 'C':np.logspace(-5, 4, 10), 'solver': ['liblinear'] ,'max_iter':[500] }
						]



	clf = GridSearchCV(LogisticRegression(class_weight= 'balanced'), tuned_parameters, cv=5, scoring= None)

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
Unigram_bigram_lda_data.npz (94X2123)
(run_logistic_sfs is using the following params)

Best parameters set found on development set:
{'penalty': 'l2', 'C': 1.0, 'max_iter': 500, 'solver': 'sag'}
accuracy = 0.736842105263
auc = 0.762820512821


Unigram_bigram_ner_senti_pos_lda_data.npz (94X3283)

Best parameters set found on development set:
{'penalty': 'l2', 'C': 1.0, 'max_iter': 500, 'solver': 'liblinear'}
accuracy = 0.578947368421
auc = 0.602564102564
'''