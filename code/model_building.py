from data_cleaning import OpenFile
import pandas as pd
import numpy as np
import cPickle 
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.metrics import recall_score, accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostRegressor, RandomForestClassifier, GradientBoostingClassifier, GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import roc_curve, auc
###########
# from helper import ....
##########

class ModelBuilding():
	def __init__(self):
		'''
		Ope file to data analysis
		'''

		open_ = OpenFile()
		self.data_ = open_.openfile()
		

		self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
		#########################################################################################################
		'''LIST'''
		#########################################################################################################
		self.classifiers = [ DecisionTreeClassifier(), RandomForestClassifier(), GradientBoostingClassifier()]
		self.proba_list = []
		self.recall_classifier = []
		self.precision_classifier = []
		self.c_matrix_classifier = []
		self.y_predicted_all =[]
		self.fpr_all = []
		self.tpr_all = []
		self.accuracy_score_all = []
		self.auc_all = []
		self.y_predicted_all =[]

	def split_train_test(self, feature_list):
		'''
		Create train test set using feature list
		'''
		self.y = self.data_.pop("status")
		self.data_ = self.data_[feature_list]
		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.data_, self.y, test_size=0.3, random_state=0)

 	def ML_classifier(self, est):
 		'''
 		Using given model, predict class and probability
 		'''
		est.fit(self.X_train, self.y_train)
		y_predicted = est.predict(self.X_test)
		proba_ = est.predict_proba(self.X_test)
		return y_predicted, proba_

	def evaluate_model(self, y_predicted):
		'''
		Used for evaluate model base upon recall, precision, confusion_matrix
		'''
		recall = recall_score(self.y_test, y_predicted)
		precision = precision_score(self.y_test, y_predicted)
		c_matrix = confusion_matrix(self.y_test, y_predicted)
		accuracy  = accuracy_score(self.y_test, y_predicted)
		return recall, precision, c_matrix, accuracy

	def evaluate_classifier(self):
		'''
		This is main function, which will go through each classifer from list and evalate each model
		and append data to list
		'''
		for classifier in self.classifiers:
			y_predicted, proba_ = self.ML_classifier(classifier)
			self.proba_list.append(proba_)
			y_predicted = np.round(y_predicted)
			y_predicted = y_predicted.astype(np.int64)
			self.y_predicted_all.append(y_predicted)
			recall, precision, c_matrix, accuracy = self.evaluate_model(y_predicted)
			self.recall_classifier.append(recall)
			self.precision_classifier.append(precision)
			self.c_matrix_classifier.append(c_matrix)
			self.accuracy_score_all.append(accuracy)
			fpr, tpr, thresholds = roc_curve(self.y_test, proba_[:,1])
			roc_auc = auc(fpr, tpr)
			self.fpr_all.append(fpr)
			self.tpr_all.append(tpr)
			self.auc_all.append(roc_auc)
 	

		# def roc_curve(self):
		# 	for value in self.y_predicted_all:
			

	def run_models(self, feature_list):
		'''
		This function will take feature list call train test split function and evalute classifier
		'''
		self.split_train_test(feature_list= feature_list)
		self.evaluate_classifier()
