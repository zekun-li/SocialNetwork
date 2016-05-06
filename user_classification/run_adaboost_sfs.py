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
					#	{'penalty': ['l2'], 'C':np.logspace(-5, 4, 10), 'solver': ['sag'] ,'max_iter':[500] },
					#	{'penalty': ['l2'], 'C':np.logspace(-5, 4, 10), 'solver': ['newton-cg'] ,'max_iter':[500] },
					#	{'penalty': ['l2'], 'C':np.logspace(-5, 4, 10), 'solver': ['lbfgs'] ,'max_iter':[500] },
					#	{'penalty': ['l2','l1'], 'C':np.logspace(-5, 4, 10), 'solver': ['liblinear'] ,'max_iter':[500] }
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


'''
E:\DR\SocialNetwork\user_classification>python run_adaboost_sfs.py data/unigram_bigram_ner_senti_pos_lda_data.npz
data/unigram_bigram_ner_senti_pos_lda_data.npz
feature size: (113, 3932)
auc = 0.5       colInd_best = 0
auc = 0.666666666667    colInd_best = 4
auc = 0.75      colInd_best = 76
auc = 0.833333333333    colInd_best = 688
feature index to add: 688
auc = 0.833333333333    colInd_best = 0
auc = 0.875     colInd_best = 3
auc = 0.916666666667    colInd_best = 4
auc = 1.0       colInd_best = 279
feature index to add: 279
auc_best_global found on current trainX_test fold: 1.0
auc = 0.5       colInd_best = 0
auc = 0.538461538462    colInd_best = 4
auc = 0.553846153846    colInd_best = 7
auc = 0.576923076923    colInd_best = 19
auc = 0.592307692308    colInd_best = 20
auc = 0.615384615385    colInd_best = 47
auc = 0.653846153846    colInd_best = 253
auc = 0.769230769231    colInd_best = 486
auc = 0.807692307692    colInd_best = 3815
feature index to add: 3815
auc = 0.807692307692    colInd_best = 0
auc = 0.846153846154    colInd_best = 7
auc = 0.884615384615    colInd_best = 58
auc = 0.923076923077    colInd_best = 226
auc = 0.961538461538    colInd_best = 464
feature index to add: 464
auc = 0.923076923077    colInd_best = 0
auc = 0.961538461538    colInd_best = 1
auc_best_global found on current trainX_test fold: 0.961538461538
auc = 0.6       colInd_best = 0
auc = 0.65      colInd_best = 33
auc = 0.75      colInd_best = 185
auc = 0.8       colInd_best = 3829
feature index to add: 3829
auc = 0.7375    colInd_best = 0
auc = 0.75      colInd_best = 2
auc = 0.8       colInd_best = 4
auc = 0.85      colInd_best = 109
auc = 0.9       colInd_best = 258
feature index to add: 258
auc = 0.8375    colInd_best = 0
auc = 0.85      colInd_best = 2
auc = 0.9       colInd_best = 3
auc = 0.95      colInd_best = 23
auc = 1.0       colInd_best = 2428
feature index to add: 2428
auc_best_global found on current trainX_test fold: 1.0
auc = 0.566666666667    colInd_best = 0
auc = 0.6       colInd_best = 16
auc = 0.7       colInd_best = 23
auc = 0.8       colInd_best = 141
auc = 0.833333333333    colInd_best = 185
auc = 0.866666666667    colInd_best = 245
feature index to add: 245
auc = 0.466666666667    colInd_best = 0
auc = 0.833333333333    colInd_best = 1
auc = 0.866666666667    colInd_best = 3
auc = 0.9       colInd_best = 16
auc = 0.933333333333    colInd_best = 272
feature index to add: 272
auc = 0.466666666667    colInd_best = 0
auc = 0.9       colInd_best = 1
auc = 0.933333333333    colInd_best = 12
auc = 0.966666666667    colInd_best = 2142
feature index to add: 2142
auc = 0.533333333333    colInd_best = 0
auc = 0.933333333333    colInd_best = 1
auc = 0.966666666667    colInd_best = 2
auc_best_global found on current trainX_test fold: 0.966666666667
auc = 0.555555555556    colInd_best = 0
auc = 0.666666666667    colInd_best = 7
auc = 0.666666666667    colInd_best = 279
auc = 0.722222222222    colInd_best = 759
auc = 0.777777777778    colInd_best = 869
feature index to add: 869
auc = 0.722222222222    colInd_best = 0
auc = 0.777777777778    colInd_best = 1
auc = 0.833333333333    colInd_best = 55
auc = 0.888888888889    colInd_best = 320
auc = 0.944444444444    colInd_best = 1400
feature index to add: 1400
auc = 0.888888888889    colInd_best = 0
auc = 0.944444444444    colInd_best = 2
auc = 1.0       colInd_best = 55
feature index to add: 55
auc_best_global found on current trainX_test fold: 1.0
# features selected = 13
feature_index = [464, 258, 869, 3815, 55, 272, 688, 3829, 279, 1400, 2428, 2142, 245]
auc test = 0.742424242424
'''