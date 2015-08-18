'''
importing function 
'''
import json

# creating dictionary that will hold data 
class DataCollection(object):
    def __init__(self):
        """
        Put Kiva dump into a dict. Info about loan (including partner_id, activity, sector, amount loaned, gender, etc) 
        """
        self.dict_={"activity":[], "basket_amount":[], "bonus_credit_eligibility":[], "gender":[], \
        		"num_borrowers":[],"has_picture":[], "description_lang":[], "description": [],\
        		 "funded_amount": [], "funded_date": [], "bulkEntries":[], "entries": [], \
        		 "lender_count": [], "country_code": [], "town": [], "geo_level": [], "partner_id":[],\
        		 "sector": [], "status": [], "tags":[], "len_teg":[], "video": [], "repayment_term":[],\
        		 "repayment_interval":[], "use":[], "theme":[], "lat":[], "long":[]}

    def read_file(self, number_of_files=2):
        """
        Read the file containing the loan info and put it into a dict. Set the dict with the info as an instance variable.

        number_of_files: The amount of data you wanna process. Each file has 500 loans
        """
        for i in range(1, number_of_files):
            with open("/home/patanjalichanakya/Documents/Galvanize/find_defaulte/rdata/loans/%s.json" %i) as f:
                file_ = f.read()
            file_json = json.loads(file_)["loans"]
            for j in range(len(file_json)):
                self.dict_["repayment_interval"].append(file_json[j]["terms"]["repayment_interval"])
                self.dict_["repayment_term"].append(file_json[j]["terms"]["repayment_term"])
                self.dict_["activity"].append(file_json[j]["activity"])
                self.dict_["basket_amount"].append(file_json[j]["basket_amount"])
                self.dict_["bonus_credit_eligibility"].append(file_json[j]["bonus_credit_eligibility"])
                self.dict_["num_borrowers"].append(len(file_json[j]["borrowers"]))
                self.dict_["gender"].append([str(x["gender"]) for x in file_json[j]["borrowers"]])
                self.dict_["has_picture"].append([x["pictured"] for x in file_json[j]["borrowers"]])
                self.dict_["description_lang"].append(len(file_json[j]["description"]["languages"]))
                self.dict_["description"].append( file_json[j]["description"]["texts"]["en"]\
                                   if 'en' in file_json[j]["description"]['languages'] else None)
                self.dict_["funded_amount"].append( file_json[j]["funded_amount"])
                self.dict_["funded_date"].append(str(file_json[j]["funded_date"]))
                self.dict_["bulkEntries"].append(file_json[j]["journal_totals"]["bulkEntries"])
                self.dict_["entries"].append(file_json[j]["journal_totals"]["entries"])
                self.dict_["lender_count"].append(file_json[j]["lender_count"])
                self.dict_["country_code"].append(file_json[j]["location"]["country_code"])
                self.dict_["geo_level"].append(file_json[j]["location"]["geo"]["level"])
                self.dict_["town"].append(file_json[j]["location"]["town"])
                self.dict_["partner_id"].append(file_json[j]["partner_id"])
                self.dict_["sector"].append(file_json[j]["sector"])
                self.dict_["status"].append(file_json[j]["status"])
                self.dict_["tags"].append(file_json[j]["tags"])
                self.dict_["len_teg"].append(len(file_json[j]["tags"]))
                self.dict_["video"].append(file_json[j]["video"])
                self.dict_["use"].append(file_json[j]["use"])
                self.dict_["theme"].append(file_json[j]["theme"])
                self.dict_["lat"].append([float(i) for i in str(file_json[j]["location"]["geo"]["pairs"]).split()][0])
                self.dict_["long"].append([float(i) for i in str(file_json[j]["location"]["geo"]["pairs"]).split()][1])

        return self.dict_