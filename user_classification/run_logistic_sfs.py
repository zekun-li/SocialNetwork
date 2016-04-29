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
	origX = npzfile['X'];
	origy = npzfile['y'];
	X = origX[0:80,:]
	y = origy[0:80]

	print(np.shape(X))

	xbest = []	# store the final best feture matrix
	feature_index = [] # store the best feature indices
	auc_best_global = 0; # final best auc
	residual_col_indices = set() # residual column indices to check for each iteration when adding new features
	for i in range(0,X.shape[1]): #init the set with all col indices
		residual_col_indices.add(i)

	for i in range(0, X.shape[1]):

		colInd_best = -1;
		auc_best_local = 0 # init to 0
		for colInd in residual_col_indices:

			if i == 0: # if it's the first feature to add
				xtemp = X[:,colInd].reshape(X.shape[0],-1)
			else: 
				xtemp = np.hstack((xbest, X[:,colInd].reshape(X.shape[0],-1) ))

			# Split the dataset to train/test set
			X_train, X_test, y_train, y_test = train_test_split(
			    xtemp, y, test_size=0.2, random_state=0)


			# Set the parameters by cross-validation
			tuned_parameters = [{'penalty': ['l2']}]
			#tuned_parameters = [{'penalty': ['l2'], 'C':np.logspace(-5, 4, 10), 'solver': ['sag'] ,'max_iter':[500] }]

			clf = GridSearchCV(LogisticRegression(class_weight= 'balanced'), tuned_parameters, cv=5, scoring= None)
		

			clf.fit(X_train, y_train)

		#	print("Best parameters set found on development set:")
		#	print(clf.best_params_)
		#	print("Grid scores on development set:")
		#	for params, mean_score, scores in clf.grid_scores_:
		#	   	print("%0.3f (+/-%0.03f) for %r"
		#		% (mean_score, scores.std() * 2, params))

			y_true, y_pred = y_test, clf.predict(X_test)
			auc = roc_auc_score(y_true, y_pred) # auc score
			#auc = accuracy_score(y_true, y_pred) #othe scores 
			
			if auc_best_local < auc:
				auc_best_local = auc
				colInd_best = colInd
				print 'auc = ' + str(auc_best_local) + '\tcolInd_best = '+str(colInd_best)
				

		if auc_best_global <= auc_best_local :
			if i == 0: # if it's the first feature to add
				xbest = X[:,colInd_best].reshape(X.shape[0],-1)
			else:
				xbest = np.hstack((xbest,X[:,colInd_best].reshape(X.shape[0],-1)))

			feature_index.append(colInd_best)
			residual_col_indices.remove(colInd_best)
			auc_best_global = auc_best_local

			if auc_best_global == 1:
				break;
		else:
			break;

	print '# features = '+str(len(feature_index)) 
	print 'feature_index = ' + str(feature_index)

	testX = origX[80:,feature_index]
	testy_true, testy_pred = origy[80:], clf.predict(testX)
	auc_test = roc_auc_score(testy_true, testy_pred)		

	print '\n'
	print 'auc_best_global = '+str(auc_best_global)
	print 'auc test = '+str(auc_test)
	



if __name__ == "__main__":
    main()


'''
auc_best = 0.923076923077
# features = 8
feature_index = [0, 12, 17, 21, 123, 134, 257, 686]  

'''