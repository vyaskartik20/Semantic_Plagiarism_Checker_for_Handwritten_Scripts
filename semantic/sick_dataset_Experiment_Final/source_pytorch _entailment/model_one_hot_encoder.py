# multi-class classification with Keras
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from numpy import array
import numpy as np

# load train dataset
dataframe = pandas.read_csv("plagiarism_data/train.csv", header=None)
data = dataframe.values
print(data)

columnTransformer = ColumnTransformer([('encoder',
                                        OneHotEncoder(),
                                        [0])],
                                      remainder='passthrough')

data = np.array(columnTransformer.fit_transform(data), dtype=np.str)
print(data)
X = data[:, 3:].astype(float)
print(X)
Y = data[:, 0:3].astype(float)
print(Y)

# load test dataset
dataframe = pandas.read_csv("plagiarism_data/test.csv", header=None)
data = dataframe.values
print(data)

columnTransformer = ColumnTransformer([('encoder',
                                        OneHotEncoder(),
                                        [0])],
                                      remainder='passthrough')

data = np.array(columnTransformer.fit_transform(data), dtype=np.str)
print(data)
XX = data[:, 3:].astype(float)
print(XX)
YY = data[:, 0:3].astype(float)
print(YY)

# create model
model = Sequential()
model.add(Dense(24, input_dim=12, activation='relu'))
model.add(Dense(3, activation='softmax'))
# Compile model
model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])

model.fit(X, Y, epochs=20, batch_size=10, verbose=0)

yhat = model.predict(XX)

print(yhat)

# # new instance where we do not know the answer
# Xnew = array([[0.181818182, 0, 0.344265186, 0, 0, 0.846153846, 0.153846154, 0.5427629, 0.415997814, 0, 0.283482909, 0.341715976],
#               [0.333333333, 0, 0.471404521, 0.175, 0, 0.875, 0.333333333,
#                   0.619253416, 0.468179841, 14.28571429, 0.397647679, 0.455],
#               [0.8, 0.5, 0.76088591, 0.995859195, 0, 1.090909091, 0.727272727,
#                   0.867994186, 0.926691251, 4.545454545, 0.739557981, 0.810941271],
#               [0.7, 0.125, 0.749268649, 0.860537913, 0, 1.115384615, 0.384615385,
#                0.761672922, 0.686321599, 0, 0.84677124, 0.309376755],
#               [0.785714286, 0.666666667, 0.826086957, 0.65836096, 0, 1.066666667,
#                0.8, 0.855952979, 0.700645608, 0, 0.825267076, 0.914285714],
#               [0.785714286, 0.666666667, 0.826086957, 0.65836096, 0, 1.066666667,
#                0.8, 0.855952979, 0.700645608, 0, 0.825267076, 0.914285714],
#               [0.181818182, 0, 0.401477534, 0, 0, 1.041666667, 0.25, 0.503255107,
#                0.302763123, 3.448275862, 0.399734467, 0.464876033],
#               [0.25, 0, 0.40951418, 0.166666667, 0, 1, 0.2, 0.517607737,
#                0.474311764, 0, 0.620812595, 0.410958904],
#               [0.285714286, 0, 0.502955691, 0.316461922, 0, 0.866666667, 0.266666667,
#                0.614940046, 0.760810125, 0, 0.652447343, 0.423409669],
#               [0.142857143, 0, 0.297939786, 0.159446795, 0, 1.033333333,
#                0.2, 0.454181848, 0.45742021, 0, 0.628333271, 0.426666667],
#               [0.875, 0.5, 0.9, 0.8, 0, 1, 0.875, 0.857142857,
#                0.591168347, 26.08695652, 0.811204135, 0.903846154],
#               [1, 0.166666667, 0.953462589, 1.0625, 0, 1.0625, 0.75,
#                0.935414347, 0.986715561, 16, 0.962050915, 0.842342342],
#               [0.375, 0, 0.421637021, 0.344862351, 0.944444444, 0.314814815, 0.333333333,
#                0.5208946, 0.60121204, 3.703703704, 0.520464182, 0.44012945],
#               [0.25, 0, 0.335410197, 0.2, 0, 1, 0.25, 0.470823615, 0.276237782, 4.347826087, 0.355904579, 0.463157895]])
# # make a prediction
# # ynew = model.predict_classes(Xnew)
# ynew = np.argmax(model.predict(Xnew), axis=-1)
# # show the inputs and predicted outputs
# print("X=%s, Predicted=%s" % (Xnew, ynew))

# # evaluate the model
# scores = model.evaluate(XX, YY, verbose=0)
# print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")


# model = KerasClassifier(build_fn=baseline_model, epochs=200, batch_size=5, verbose=0)
# kfold = KFold(n_splits=10, shuffle=True)
# results = cross_val_score(model, X, dummy_y, cv=kfold)
# print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
