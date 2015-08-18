import pandas as pd
from data_collection import DataCollection
import cPickle
import os.path


class Cleaning(object):
	def __init__(self, number_file_read=2):
		"""
		Preprocess data for EDA and model building
		"""
		data  = DataCollection()
		dict_ = data.read_file(number_file_read)
		
		# Convert the data from a dict to pandas df
		self.df = self.convert_to_data_frame(dict_)
		
		# Encoding string info to numeric for model building
		self.country_code_dict = {}
		self.town_dict = {}
		self.sector_dict = {}
		self.theme_dict = {}
		self.geo_level_dict = {}
		self.activity_dict = {}
		self.repayment_interval_dict = {}
		self.status_dic = {}

		# Decoding numeric values to string values (i.e. country, activity, etc)
		self.country_code_list = list(self.df.country_code.unique())
		self.town_list= list(self.df.town.unique())
		self.sector_list= list(self.df.sector.unique())
		self.theme_list= list(self.df.theme.unique())
		self.geo_level_list= list(self.df.geo_level.unique())
		self.activity_list = list(self.df.activity.unique())
		self.repayment_interval_list = list(self.df.repayment_interval.unique())
		self.status_list=(self.df.status.unique())

		# This will fill the dictinary to encode string values		
		self.fill_dictionarys()
		self.change_all_variable()
		

	def convert_to_data_frame(self, dictionary_):
		"""
		Data is stored in JSON, need to transfer into DataFrame for better EDA
		"""
		df = pd.DataFrame(dictionary_)
		return df

	def fill_dictionarys(self):
		'''
		Select each features from JSON format to dictinary for easy access 
		'''
		for i, j in enumerate(self.df.country_code.unique()):
			self.country_code_dict[j] = i

		for i, j in enumerate(self.df.town.unique()):
			self.town_dict[j] = i

		for i, j in enumerate(self.df.sector.unique()):
			self.sector_dict[j] = i

		for i, j in enumerate(self.df.theme.unique()):
			self.theme_dict[j] = i

		for i, j in enumerate(self.df.geo_level.unique()):
			self.geo_level_dict[j] = i

		for i, j in enumerate(self.df.activity.unique()):
			self.activity_dict[j] = i

		for i, j in enumerate(self.df.repayment_interval.unique()):
			self.repayment_interval_dict[j] = i 

		for i, j in enumerate(self.df.status.unique()):
			self.status_dic[j] = i

	def change_all_variable(self):
		'''
		All features are in text, need to transfer text to numberical to use in model and EDA
		'''
		self.change_gender_number()
		self.change_picture()
		self.replace_values()
		self.delete_columns()
		self.change_text()
		
	def replace_values(self):
		self.df.country_code = self.df.country_code.apply(lambda x : self.change_country_code(x))
		self.df.town = self.df.town.apply(lambda x : self.change_town(x))
		self.df.sector = self.df.sector.apply(lambda x : self.change_sector(x))
		self.df.theme = self.df.theme.apply(lambda x : self.change_theme(x))
		self.df.geo_level = self.df.geo_level.apply(lambda x : self.change_geo_level(x))
		self.df.activity = self.df.activity.apply(lambda x : self.chage_activity(x))
		self.df.repayment_interval = self.df.repayment_interval.apply(lambda x: self.change_repayment_interval(x))
		self.df.status = self.df.status.apply(lambda x : self.change_status(x))
		self.df.basket_amount = self.df.basket_amount.fillna(-2)
		self.df.repayment_term = self.df.repayment_term.fillna(-2)

	def delete_columns(self):
		'''
		removing not neccessary columns from data
		'''
		del self.df["bulkEntries"]
		del self.df["tags"]
		del self.df["bonus_credit_eligibility"]
		del self.df["use"]
		del self.df["video"]
		del self.df["gender"]

	def text_change(self,x):
		'''
		encode text into ascii format 
		'''
		try:
			return x.encode("ascii", "ignore").replace("<i>", " ").replace("</i>", " ").replace("<br>", " ").replace("</br>", " ")
		except:
			None
	
	def change_text(self):
		self.df['description'] = self.df['description'].apply(lambda x: self.text_change(x) )
		
	def find_male(self,x):
	    temp_m = 0
	    for j in range(len(x)):
	        if x[j] == "M":
	            temp_m +=1
	    return temp_m
	
	def find_female(self, x):
	    temp_f = 0
	    for j in range(len(x)):
	        if x[j] == "F":
	            temp_f +=1
	    return temp_f
	
	def change_gender_number(self):
		self.df["num_male"] = self.df.gender.apply(lambda x: self.find_male(x))
		self.df["num_female"] = self.df.gender.apply(lambda x: self.find_female(x))
		self.df["male_ratio"] = self.df.num_male / self.df.num_borrowers
		
	def number_picture(self, x):
		number_picture_ = 0
		for j in range(len(x)):
			if x[j] == True:
				number_picture_ += 1
		return number_picture_

	def change_picture(self):
		'''
		Finding out how many borrowers are into the picture
		'''
		self.df["number_of_picture"] = self.df.has_picture.apply(lambda x: self.number_picture(x))
		self.df["ratio_of_picture"] = self.df["number_of_picture"]/self.df.num_borrowers
		del self.df["has_picture"]
   
	def change_country_code(self, x):
		'''
		Changing country code to number
		'''
	    if x in self.country_code_dict:
	        return self.country_code_dict[x]
	    else:
	        return -2
	
	def change_town(self, x):
		'''
		changing town name to number
		'''
		if x in self.town_dict:
			return self.town_dict[x]
		else:
			return -2
	
	def change_sector(self,x ):
		'''
		changing categorical sector text to number
		'''
	    if x in self.sector_dict:
	        return self.sector_dict[x]
	    else:
	        return -2

	def change_theme(self, x):
	    if x in self.theme_dict:
	        return self.theme_dict[x]
	    else:
	        return -2

	def change_geo_level(self, x):
	    if x in self.geo_level_dict:
	        return self.geo_level_dict[x]
	    else:
	        return -2

	def chage_activity(self, x):
		if x in self.activity_dict:
			return self.activity_dict[x]
		else:
			return -2

	def change_repayment_interval(self, x):
		if x in self.repayment_interval_dict:
			return self.repayment_interval_dict[x]
		else:
			return -2
	
	def change_status(self, x):
		if x in self.status_dic:
			return self.status_dic[x]
		else:
			return -2

class Saving(object):
	'''
	Saving file after preprocess to access easily, saving list to decode cloumns back to value later 
	when required
	'''
	def __init__(self, number_file_read=2):
		clean = Cleaning(number_file_read)
		self.df = clean.df
		self.country_code_list = clean.country_code_list
		self.town_list = clean.town_list
		self.sector_list = clean.sector_list
		self.theme_list = clean.theme_list
		self.geo_level_list = clean.geo_level_list
		self.activity_list = clean.activity_list
		self.repayment_interval_list = clean.repayment_interval_list
		self.status_list = clean.status_list
		self.number_of_files = number_file_read

	def save_files(self):
		'''
		Saving loans into file, which are only defaulted or not defaulted
		'''
		condition_1 = self.df.status == 1
		condition_2 = self.df.status == 0
		self.df_new = self.df[condition_1 | condition_2]

		self.df_new.to_csv("/home/patanjalichanakya/Documents/Galvanize/find_defaulter/data/%s_two_option.csv" %self.number_of_files, index=False)
		dict_ = {"country_code_list":self.country_code_list, "town_list":self.town_list, "sector_list":self.sector_list, "theme_list": self.theme_list, "geo_level_list":self.geo_level_list,\
				 "activity_list":self.activity_list, "repayment_interval_list": self.repayment_interval_list, "status_list":self.status_list}
		for file_name, content in dict_.iteritems():
			with open("/home/patanjalichanakya/Documents/Galvanize/find_defaulter/data/%s_%s.pickle" %(file_name, self.number_of_files), 'w') as f:
				cPickle.dump(content, f) 		

class OpenFile(object):
	'''
	open file tool
	'''
	def __init__(self):
		self.isfile_ = os.path.isfile("/home/patanjalichanakya/Documents/Galvanize/find_defaulter/data/1638.csv") 

	def openfile(self):
		if self.isfile_:
			return pd.read_csv("/home/patanjalichanakya/Documents/Galvanize/find_defaulter/data/1638.csv")
		else:
			saving = Saving(number_file_read = 1638)
			saving.save_files()
			return pd.read_csv("/home/patanjalichanakya/Documents/Galvanize/find_defaulter/data/1638.csv")
