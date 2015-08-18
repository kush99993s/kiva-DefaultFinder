import pandas as pd
from flask import Flask
from flask import render_template
from flask import request

import json
import cPickle
import sys
sys.path.append("/home/patanjalichanakya/Documents/Galvanize/find_defaulter/code/")
from data_cleaning import OpenFile
from model_building import ModelBuilding

app = Flask(__name__)

open_ = OpenFile()
df = open_.openfile()

country_code = list(df.country_code)
activity = list(df.activity)
status = list(df.status)
sector = list(df.sector)
lat = list(df.lat)
long_ = list(df.long)
with open("/home/patanjalichanakya/Documents/Galvanize/find_defaulter/data/country_code_list_1638.pickle") as f:
    file_read = f.read()
country_name = cPickle.loads(file_read)


@app.route('/')
def index():
    with open("/home/patanjalichanakya/Documents/Galvanize/find_defaulter/my_app/countries_geo.json") as f:
        f_read = f.read()
    geo_json= json.loads(f_read)
    geo_json_str = json.dumps(geo_json)
    data = pd.read_csv("/home/patanjalichanakya/Documents/Galvanize/find_defaulter/data/groupby_partner_id.csv")
    parter_id = data["partner_id"]
    long_ = data["long"]
    lat = data["lat"]
    normalized_default = data["normalized_defaulted"]

    # data = build_graph.get_data()
    
    # data_html = data.to_html()
    # data_html = data_html.replace('dataframe', 'table table-striped')
    return render_template('index.html',  map_geo_json=geo_json_str, parter_id = parter_id, long_ = long_, lat = lat, normalized_default= normalized_default )


@app.route('/data', methods=['POST'])
def userinput():
    feature_list = request.json
    model = ModelBuilding()
    model.run_models(feature_list)
    
    recall = model.recall_classifier
    precision = model.precision_classifier
    fpr = model.fpr_all
    tpr = model.tpr_all
    def best_model(recall):
        models=  [ "DecisionTreeClassifier", "RandomForestClassifier", "GradientBoostingClassifier"]
        position = -1
        value = -1
        for i,j in enumerate (recall):
            if value < j:
                value = j
                position = i
        return models[position], position
    best_model_name, position = best_model(recall)
    fpr_roc = fpr[position]
    tpr_roc = tpr[position]

    #['repayment_term ']
    return json.dumps([fpr_roc,tpr_roc])
# @app.route('/map')
# def map():
#     with open("/home/patanjalichanakya/Documents/Galvanize/find_defaulter/my_app/countries_geo.json") as f:
#         f_read = f.read()
#     geo_json= json.loads(f_read)
#     geo_json_str = json.dumps(geo_json)

#     return render_template('map.html', map_geo_json=geo_json_str)



@app.route('/map1')
def map1():
    with open("/home/patanjalichanakya/Documents/Galvanize/find_defaulter/data/0.pickle") as f:
        f_read = f.read()

    recall = cPickle.loads(f_read)
    with open("/home/patanjalichanakya/Documents/Galvanize/find_defaulter/data/1.pickle") as f:
        f_read = f.read()

    precision = cPickle.loads(f_read)
    with open("/home/patanjalichanakya/Documents/Galvanize/find_defaulter/data/0.pickle") as f:
        f_read = f.read()

    accuracy = cPickle.loads(f_read)
    models = [ 'Decision Tree Classifier', 'Random Forest Classifier', 'Gradient Boosting Classifier']
    # data = build_graph.get_data()
    
    # data_html = data.to_html()
    # data_html = data_html.replace('dataframe', 'table table-striped')
    return render_template('map1.html', recall= recall, precision= precision, accuracy=accuracy, models= models )




# @app.route('/process', methods=['POST'])
# def process_images():
#     data = request.json
#     lat_return= data['lat']
#     long_return = data['lng']
    
#     if lat_return >0:
#         x = 'north'
#     elif lat_return<0:
#         x = 'south'
#     else:
#         x = 'middle'

#     if long_return >0:
#         y = 'east'
#     elif long_return<0:
#         y = 'west'
#     else:
#         y = 'middle'


#     random_image = [x, y]
#     return json.dumps(random_image) 




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969, debug=True)