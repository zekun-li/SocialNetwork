from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import KFold
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.ensemble import AdaBoostClassifier
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
	X = npzfile['X'];
	y = npzfile['y'];
	#split the data into 8:2 -> training:testing 
	trainX, testX, trainy, testy = train_test_split(X, y, test_size=0.2, random_state=0)

	print 'feature size: '+str(np.shape(X))

	
	feature_index = set() # store the best feature indices
	

	kf = KFold(trainX.shape[0], n_folds=5) # kfold on training set for feature selection
	for train_index, test_index in kf: 
		trainX_train, trainX_test = trainX[train_index], trainX[test_index]
		trainy_train, trainy_test = y[train_index], y[test_index]

		auc_best_global = 0; # best auc in each cross validation
		xtrainBest = []	# store the best feture matrix for traing section of traingX
		xtestBest = [] #store the best feture matrix for testing section of traingX
		residual_col_indices = set() # residual column indices to check for each iteration when adding new features
		for i in range(0,X.shape[1]): #init the set with all col indices
			residual_col_indices.add(i)

		for i in range(0, X.shape[1]):

			colInd_best = -1;
			auc_best_local = 0 # init to 0
			for colInd in residual_col_indices:

				if i == 0: # if it's the first feature to add
					xtrainCur = trainX_train[:,colInd].reshape(trainX_train.shape[0],-1) #convert to a column vector
					xtestCur = trainX_test[:,colInd].reshape(trainX_test.shape[0],-1)
				else: 
					xtrainCur = np.hstack((xtrainBest, trainX_train[:,colInd].reshape(trainX_train.shape[0],-1) ))
					xtestCur =  np.hstack((xtestBest, trainX_test[:,colInd].reshape(trainX_test.shape[0],-1) ))

				clf = AdaBoostClassifier();
				clf.fit(xtrainCur, trainy_train)


				y_true, y_pred = trainy_test, clf.predict(xtestCur)
				auc = roc_auc_score(y_true, y_pred) # auc score
				
				if auc_best_local < auc:
					auc_best_local = auc
					colInd_best = colInd
					print 'auc = ' + str(auc_best_local) + '\tcolInd_best = '+str(colInd_best)
					

			if auc_best_global < auc_best_local : # if auc is increasing by adding new features
				if i == 0: # if it's the first feature to add
					xtrainBest = trainX_train[:,colInd_best].reshape(trainX_train.shape[0],-1)
					xtestBest = trainX_test[:,colInd_best].reshape(trainX_test.shape[0],-1)
				else:
					xtrainBest = np.hstack((xtrainBest,trainX_train[:,colInd_best].reshape(trainX_train.shape[0],-1)))
					xtestBest = np.hstack((xtestBest,trainX_test[:,colInd_best].reshape(trainX_test.shape[0],-1)))

				print 'feature index to add: '+str(colInd_best)
				feature_index.add(colInd_best) # union of all features selected during each k-fold CV
				residual_col_indices.remove(colInd_best)
				auc_best_global = auc_best_local

				if auc_best_global == 1:
					break;
			else: 
				break;
				

		print 'auc_best_global found on current trainX_test fold: '+str(auc_best_global)

	print '# features selected = '+str(len(feature_index)) 
	feature_index = list(feature_index)
	print 'feature_index = ' + str(feature_index)
	# should NOT sort feature_index before test!

	outfilename = infilename[0:-8] +'selected.npz' 
	np.savez(outfilename,X = X[:,feature_index], y = y)

	clf.fit(trainX[:,feature_index], trainy)
	testy_true, testy_pred = testy, clf.predict(testX[:,feature_index])
	auc_test = roc_auc_score(testy_true, testy_pred)		
	print 'auc test = '+str(auc_test)

	# ---------------------------------- tune params ----------------------------------

	# Set the parameters by cross-validation
	tuned_parameters = [{},
						{'penalty': ['l2'], 'C':np.logspace(-5, 4, 10), 'solver': ['sag'] ,'max_iter':[500] },
						{'penalty': ['l2'], 'C':np.logspace(-5, 4, 10), 'solver': ['newton-cg'] ,'max_iter':[500] },
						{'penalty': ['l2'], 'C':np.logspace(-5, 4, 10), 'solver': ['lbfgs'] ,'max_iter':[500] },
						{'penalty': ['l2','l1'], 'C':np.logspace(-5, 4, 10), 'solver': ['liblinear'] ,'max_iter':[500] }
						]
	clf = GridSearchCV(AdaBoostClassifier(class_weight= 'balanced'), tuned_parameters, cv=5, scoring= None)

	clf.fit(trainX[:,feature_index], trainy)

	print("Best parameters set found on development set:")
	print(clf.best_params_)
	y_true, y_pred = testy, clf.predict(testX[:,feature_index])
	auc = roc_auc_score(testy_true, testy_pred)
	print 'accuracy = ' + str(accuracy_score(y_true, y_pred))
	print 'auc = ' + str(auc)



if __name__ == "__main__":
    main()


