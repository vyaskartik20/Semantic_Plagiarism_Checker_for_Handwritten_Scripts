# from codes.semantic.sick_dataset_Experiment_Final.source_pytorch import individual as individualSemantic 
# from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.model import *
# text1 = "karti vyas is a boy"
# text2 = "kartik vyas is not a girl"

# resu = individualSemantic.web_semantic_similarity(text1, text2)
# print(resu)

# exit(0)

# import helper1
# from model import *
import os
# from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.model import *
# text1 = "kartik vyas is a boy"
# text2 = "kartik vyas is not a girl"

# f = open("textfile1.txt", "w")
# f.write(text1)
# f.close()

# f = open("textfile2.txt", "w")
# f.write(text2)
# f.close()

# os.system('python helper1.py')

# f = open("textfile3.txt", "r")
# res = f.read() 
# # res = helper1.sem_plag_check(text1, text2)
# print(res)
# exit(0)

# from flask import Flask
from codes.real_plag import individual
from codes.online_real_plag import main as individualOnline
import helper2
# from codes.semantic.sick_dataset_Experiment_Final.source_pytorch import individual as individualSemantic 
# from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.model import *
# app = Flask(__name__)

# @app.route('/')

# def index():
#     return '<h1>Hello !</h1>'

from flask import Flask, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
import joblib

flask_app = Flask(__name__)
app = Api(app = flask_app, 
		  version = "1.0", 
		  title = "ML React App", 
		  description = "Predict results using a trained model")


#first

name_space1 = app.namespace('prediction1', description='Prediction APIs')

model1 = app.model('Prediction params', 
				  {'textField1': fields.String(required = True, 
				  							   description="Text Field 1", 
    					  				 	   help="Text Field 1 cannot be blank"),
				  'textField2': fields.String(required = True, 
				  							   description="Text Field 2", 
    					  				 	   help="Text Field 2 cannot be blank"),
				#   'select1': fields.Integer(required = True, 
				#   							description="Select 1", 
    			# 		  				 	help="Select 1 cannot be blank"),
				#   'select2': fields.Integer(required = True, 
				#   							description="Select 2", 
    			# 		  				 	help="Select 2 cannot be blank"),
				#   'select3': fields.Integer(required = True, 
				#   							description="Select 3", 
    			# 		  				 	help="Select 3 cannot be blank")
      })

# classifier = joblib.load('classifier.joblib')

@name_space1.route("/")
class MainClass(Resource):

	def options(self):
		response = make_response()
		response.headers.add("Access-Control-Allow-Origin", "*")
		response.headers.add('Access-Control-Allow-Headers', "*")
		response.headers.add('Access-Control-Allow-Methods', "*")
		return response

	@app.expect(model1)		
	def post(self):
		try: 
			formData = request.json
			data = [val for val in formData.values()]
			# data = formData.values()
			# data = data[0]
   
			data = individual.web_real_similarity(data[0],data[1])
   
			# data= "prediction1"
			# prediction = classifier.predict(data)
			response = jsonify({
				"statusCode": 200,
				"status": "Prediction made",
				"result": "Plagiarism Percentage: " + str(data)
				})
			response.headers.add('Access-Control-Allow-Origin', '*')
			return response
		except Exception as error:
			return jsonify({
				"statusCode": 500,
				"status": "Could not make prediction",
				"error": str(error)
			})
   
   
#second
   
name_space2 = app.namespace('predictionOnline', description='Prediction APIs')

model2 = app.model('Prediction params', 
				  {'textField1': fields.String(required = True, 
				  							   description="Text Field 1", 
    					  				 	   help="Text Field 1 cannot be blank"),
				  'textField2': fields.String(required = True, 
				  							   description="Text Field 2", 
    					  				 	   help="Text Field 2 cannot be blank"),
				#   'select1': fields.Integer(required = True, 
				#   							description="Select 1", 
    			# 		  				 	help="Select 1 cannot be blank"),
				#   'select2': fields.Integer(required = True, 
				#   							description="Select 2", 
    			# 		  				 	help="Select 2 cannot be blank"),
				#   'select3': fields.Integer(required = True, 
				#   							description="Select 3", 
    			# 		  				 	help="Select 3 cannot be blank")
      })

# classifier = joblib.load('classifier.joblib')

@name_space2.route("/")
class MainClass(Resource):

	def options(self):
		response = make_response()
		response.headers.add("Access-Control-Allow-Origin", "*")
		response.headers.add('Access-Control-Allow-Headers', "*")
		response.headers.add('Access-Control-Allow-Methods', "*")
		return response

	@app.expect(model2)		
	def post(self):
		try: 
			formData = request.json
			data =[val for val in formData.values()]
			data = individualOnline.web_real_online_similarity(data[0])
			data =[val for val in data]
			# data= "prediction2"
			# prediction = classifier.predict(data)
			response = jsonify({
				"statusCode": 200,
				"status": "Prediction made",
				"result": "Online Plagiarism: " + str(data)
				})
			response.headers.add('Access-Control-Allow-Origin', '*')
			return response
		except Exception as error:
			return jsonify({
				"statusCode": 500,
				"status": "Could not make prediction",
				"error": str(error)
			})
   
   
   
#third
   
name_space3 = app.namespace('predictionSemantic', description='Prediction APIs')

model3 = app.model('Prediction params', 
				  {'textField1': fields.String(required = True, 
				  							   description="Text Field 1", 
    					  				 	   help="Text Field 1 cannot be blank"),
				  'textField2': fields.String(required = True, 
				  							   description="Text Field 2", 
    					  				 	   help="Text Field 2 cannot be blank"),
				#   'select1': fields.Integer(required = True, 
				#   							description="Select 1", 
    			# 		  				 	help="Select 1 cannot be blank"),
				#   'select2': fields.Integer(required = True, 
				#   							description="Select 2", 
    			# 		  				 	help="Select 2 cannot be blank"),
				#   'select3': fields.Integer(required = True, 
				#   							description="Select 3", 
    			# 		  				 	help="Select 3 cannot be blank")
      })

# classifier = joblib.load('classifier.joblib')

@name_space3.route("/")
class MainClass(Resource):

	def options(self):
		response = make_response()
		response.headers.add("Access-Control-Allow-Origin", "*")
		response.headers.add('Access-Control-Allow-Headers', "*")
		response.headers.add('Access-Control-Allow-Methods', "*")
		return response

	@app.expect(model2)		
	def post(self):
		try: 
			formData = request.json
			data =[val for val in formData.values()]

			f = open("textfile1.txt", "w")
			f.write(data[0])
			f.close()

			f = open("textfile2.txt", "w")
			f.write(data[1])
			f.close()

			os.system('python helper1.py')

			f = open("textfile3.txt", "r")
			data = f.read() 
   
			# data = helper1.sem_plag_check(data[0], data[1])
   # individualSemantic.web_semantic_similarity(data[0], data[1])
   
			# print('here5')
			# print(data)
			# data =[val for val in data]
			# data= "prediction2"
			# prediction = classifier.predict(data)
			response = jsonify({
				"statusCode": 200,
				"status": "Prediction made",
				"result": "Semantic Plagiarism: " + str(data)
				})
			response.headers.add('Access-Control-Allow-Origin', '*')
			return response
		except Exception as error:
			return jsonify({
				"statusCode": 500,
				"status": "Could not make prediction",
				"error": str(error)
			})
   
   
   
#fourth
   
name_space4 = app.namespace('predictionEntailment', description='Prediction APIs')

model2 = app.model('Prediction params', 
				  {'textField1': fields.String(required = True, 
				  							   description="Text Field 1", 
    					  				 	   help="Text Field 1 cannot be blank"),
				  'textField2': fields.String(required = True, 
				  							   description="Text Field 2", 
    					  				 	   help="Text Field 2 cannot be blank"),
				#   'select1': fields.Integer(required = True, 
				#   							description="Select 1", 
    			# 		  				 	help="Select 1 cannot be blank"),
				#   'select2': fields.Integer(required = True, 
				#   							description="Select 2", 
    			# 		  				 	help="Select 2 cannot be blank"),
				#   'select3': fields.Integer(required = True, 
				#   							description="Select 3", 
    			# 		  				 	help="Select 3 cannot be blank")
      })

# classifier = joblib.load('classifier.joblib')

@name_space4.route("/")
class MainClass(Resource):

	def options(self):
		response = make_response()
		response.headers.add("Access-Control-Allow-Origin", "*")
		response.headers.add('Access-Control-Allow-Headers', "*")
		response.headers.add('Access-Control-Allow-Methods', "*")
		return response

	@app.expect(model2)		
	def post(self):
		try: 
			formData = request.json
			data =[val for val in formData.values()]
			data = helper2.entailment_check(data[0], data[1])
			# data =[val for val in data]
			# data= "prediction2"
			# prediction = classifier.predict(data)
			data = str(data)
			response = jsonify({
				"statusCode": 200,
				"status": "Prediction made",
				"result": "Online Plagiarism: " + str(data)
				})
			response.headers.add('Access-Control-Allow-Origin', '*')
			return response
		except Exception as error:
			return jsonify({
				"statusCode": 500,
				"status": "Could not make prediction",
				"error": str(error)
			})
  