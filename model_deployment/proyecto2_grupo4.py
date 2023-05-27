# -*- coding: utf-8 -*-
"""proyecto2_grupo4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1L8BL1_HAsE2DmrqlH2w8rmLMtp9ZEf-1
"""

from flask import Flask
from flask_restx import Api, Resource, fields
import joblib
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np


app = Flask(__name__)

# Definición API Flask
api = Api(
    app, 
    version='1.0', 
    title='Predicción del género de la película',
    description='Predicción del genero API')

ns = api.namespace('predict', 
     description='Género')

# Definición argumentos o parámetros de la API
parser = api.parser()
parser.add_argument(
    'PLOT', 
    type=str, 
    required=True, 
    help='PLOT to be analyzed', 
    location='args')

resource_fields = api.model('Resource', {
    'result': fields.String,
})

def predict_plot(plot):
  clf = joblib.load('prediccion_plot.pkl')
  a=pd.DataFrame(columns=['plot'])
  a['plot']=[plot]
  vect = CountVectorizer(stop_words='english', max_features=214)
  X = vect.fit_transform(a['plot'])
  X=X.toarray()
  c=X[0].tolist()
  X_f=matriz = [0] * 214
  for y in range(0,len(c)):
    X_f[y]=c[y]
  X_f=np.array(X_f).reshape(1,214)
  p1=clf.predict_proba(X_f)
  cols = ['p_Action', 'p_Adventure', 'p_Animation', 'p_Biography', 'p_Comedy', 'p_Crime', 'p_Documentary', 'p_Drama', 'p_Family',
        'p_Fantasy', 'p_Film-Noir', 'p_History', 'p_Horror', 'p_Music', 'p_Musical', 'p_Mystery', 'p_News', 'p_Romance',
        'p_Sci-Fi', 'p_Short', 'p_Sport', 'p_Thriller', 'p_War', 'p_Western']
  p2=''
  for c in range(0,len(p1)):
    p2+=str(cols[c])+str('=')+str(round(p1[c][0][1],2))+ str(' ')
  return p2

@ns.route('/')
class PredictPlot(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
      
        return {
            "result": predict_plot(args['PLOT'])
        }, 200
 
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
