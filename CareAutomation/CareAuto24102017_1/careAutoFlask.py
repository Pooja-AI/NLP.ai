#!/usr/bin/python
##############################################################################
## Care Analytics Web Server Class
##
##############################################################################
from flask import Flask, request, jsonify
from careModelBuild import careSimiModel
from careModelQuery import careSimiQuery
from careSMEModelBuild import careSMEModel
from careSMEModelQuery import careSMEQuery
from flask_cors import CORS

app = Flask(__name__)
cors=CORS(app)
## creating model
@app.route('/createSimiModel/<uuid>')
def callCreateSimiModel(uuid):
    print('creating the model from flask server...')
    careMdl=careSimiModel()
    careMdl.createSimiModel(uuid)
    return 'Creating similarity model with id %s' %uuid

@app.route('/querySimiModel/<uuid>', methods=['GET', 'POST'])
def callQuerySimiModel(uuid):
    print('Querying the model from flask server...')
##    tstStr1='NT HLR FE 15.5 SW LUP failing for 2G/3G after NT-HLR 15.5 Upgrade location update being cancelled SW system specified customer'
    # request.json -> request.get_data()
    content = request.get_data().decode("utf-8")
    content = str(content).replace('\\n','')
    prdsol=careSimiQuery()
    resp=prdsol.getSimilarity(content)
    # replace('\n','') to remove "new lines" from the json response, otherwise json can't be parsed in the front-end.  
    return jsonify(resp.replace('\n',''))

    
@app.route('/createSMEModel/<uuid1>')
def callCreateSMEModel(uuid1):
    print('creating the model from flask server...')
    careMdl=careSMEModel()
    careMdl.createSMEModel(uuid1)
    return 'Creating SME model with id %s' %uuid1

@app.route('/querySMEModel/<uuid1>', methods=['GET', 'POST'])
def callQuerySMEModel(uuid1):
    #import pdb; pdb.set_trace()
    print('Querying the model from flask server...')
##tstStr1='NT HLR FE 15.5 SW LUP failing for 2G/3G after NT-HLR 15.5 Upgrade location update being cancelled SW system specified customer'
    # request.json -> request.get_data()
    content1 = request.get_data()
    print('.....',content1)
    prdsol1=careSMEQuery()
    resp1=prdsol1.getSME(content1)
    # replace('\n','') to remove "new lines" from the json response, otherwise json can't be parsed in the front-end.
    return jsonify(resp1.replace('\n',''))

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
    
    
    
