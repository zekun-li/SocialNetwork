from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.linear_model import Perceptron
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


	# Split the dataset to train/test set
	X_train, X_test, y_train, y_test = train_test_split(
	    X, y, test_size=0.2, random_state=0)


	tuned_parameters = [ {'penalty': ['None']},
						 {'penalty': ['l1','l2'], 'alpha': np.logspace(-5, 2, 8), 'eta0': np.logspace(-3, 2, 6), 'warm_start':[True]}
					   ]


	clf = GridSearchCV(Perceptron(n_iter = 50, class_weight= 'balanced'), tuned_parameters, cv=5, scoring= None)
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


