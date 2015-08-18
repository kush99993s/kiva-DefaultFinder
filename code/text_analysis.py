import pandas as pd
import os.path
from data_cleaning import Saving 
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


class Load_file(object):
	def __init__(self):
		self.isfile_ = os.path.isfile("/home/patanjalichanakya/Documents/Galvanize/find_defaulter/data/1638.csv") 
	def openfile(self):
		if self.isfile_:
			return pd.read_csv("/home/patanjalichanakya/Documents/Galvanize/find_defaulter/data/1638.csv")
		else:
			saving = Saving(number_file_read = 1638)
			saving.save_files()
			return pd.read_csv("/home/patanjalichanakya/Documents/Galvanize/find_defaulter/data/1638.csv")


class Select_feature(object):
	def __init__(self):
		load = Load_file()
		self.df = load.openfile()

	def select_text_y(self):
		condition_1 = self.df.status == 0
		condition_2 = self.df.status == 1
		self.df = self.df[condition_2 | condition_1]
		self.X = self.df["description"]
		self.y = self.df["status"]
	def convert_tfidfvectorizer(self):
		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size = 0.30, random_state=0)
		TfidfVectorizer(input = self.X_train, lowercase=True, preprocessor=None, tokenizer=None, analyzer=u'word', stop_words=None, token_pattern=u'(?u)\b\w\w+\b', ngram_range=(1, 1), max_df=1.0, min_df=1, max_features=None, vocabulary=None, binary=False, dtype=<type 'numpy.int64'>, norm=u'l2', use_idf=True, smooth_idf=True, sublinear_tf=False)
