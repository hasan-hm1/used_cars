import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataset_path = BASE_DIR+'\\ffcars.csv'

cars = pd.read_csv(dataset_path)
nncars=cars
# print(cars)
# nncars= pd.get_dummies(cars)
# print(nncars.head())
# print(nncars.info())
# print(nncars.Model.to_string(index=False))
# print(nncars['Model'].unique())

from sklearn import preprocessing

# create the Labelencoder object
le = preprocessing.LabelEncoder()

#convert the categorical columns into numeric

nncars = pd.get_dummies(nncars)

# nncars['Model'] = le.fit_transform(cars['Model'])
# nncars['Transmission'] = le.fit_transform(cars['Transmission'])
# nncars['Sunroof'] = le.fit_transform(cars['Sunroof'])
# nncars['ABS'] = le.fit_transform(cars['ABS'])
# nncars['Digital_Conditioning'] = le.fit_transform(cars['Digital_Conditioning'])
# nncars['Steering_Control'] = le.fit_transform(cars['Steering_Control'])
# nncars['Airbags'] = le.fit_transform(cars['Airbags'])
# nncars['Chrome_Wheel'] = le.fit_transform(cars['Chrome_Wheel'])
# nncars['Technical_Status'] = le.fit_transform(cars['Technical_Status'])


# print(nncars['Model'].unique())

# print(nncars.Model.to_string(index=False))
# print(nncars)
# print(nncars.info())

from sklearn.model_selection import train_test_split

target_name = 'Price'
# X = nncars.drop('Price' ,axis=1)
# Y = nncars[target_name]

X = nncars[nncars.columns.difference([target_name])]
Y = nncars[target_name]
# print(X)
# print(X.info())
# pd.set_option('display.max_columns', 500)

X_train ,X_test ,Y_train ,Y_test=train_test_split(X,Y,test_size=0.3,random_state=123)

# pd.set_option('display.expand_frame_repr', False)
print(X_train.info())

# print(Y_test)


from sklearn.ensemble import GradientBoostingRegressor
gbr = GradientBoostingRegressor(loss ='ls',n_estimators = 1500 , max_depth=6)
gbr.fit(X_train,Y_train)
print("done")

# from sklearn.externals import joblib
# gbr = joblib.load('model.pkl')
# y_pred=gbr.predict(X_test)
# print (y_pred)

from sklearn.metrics import r2_score
score = r2_score(Y_test,gbr.predict(X_test))
print(score)

from sklearn.metrics import mean_squared_error
model_mse = mean_squared_error(gbr.predict(X_test),Y_test)
model_rmse =np.sqrt(model_mse)
print(model_rmse)

# # Save the model
import joblib
joblib.dump(gbr, 'model.pkl')
print("Model dumped!")

# Load the model that just saved
gbr = joblib.load('model.pkl')

p=gbr.predict([[2009,60000,0,0,0,0,1,1,0,0,1,0,1,0,1,1,0,1,0,1,0,0,1,0]])
print(p)
arr=np.array([2009,60000,0,0,0,0,1,1,0,0,1,0,1,0,1,1,0,1,0,1,0,0,1,0])
arr = arr.astype(np.int64)
arr=arr.reshape(1,-1)
print(gbr.predict(arr))

# # Saving the data columns from training
# model_columns = list(X.columns)
# joblib.dump(model_columns, 'model_columns.pkl')
# print("Models columns dumped!")

# mcol =joblib.load('model_columns.pkl')
# print(mcol)
 
# arr=np.array([1,1,0,1,150000,2009,3,1,1,1,0])
# arr=arr.reshape(1,-1)
# p=gbr.predict(arr)
# print(p)
# p= gbr.predict([[1,1,0,1,150000,2009,3,1,1,1,0]]) 
# p1= gbr.predict([[0,1,0,0,139000,2011,1,0,1,1,1]])
# p2= gbr.predict([[1,1,1,1,90000,2008,2,0,0,0,0]])
# p3= gbr.predict([[0,1,1,1,104000,2009,1,1,1,1,0]])
# p4= gbr.predict([[1,1,1,1,56000,2009,2,0,1,1,0]])
# print(p)
# print(int(p))
# print(p1)
# print(p2)
# print(p3)
# print(p4)

# arr=np.zeros(11)
# print(arr)

#  np.array([30,4000,1])

# input = {'year_model':"Yes", 'mileage':"No", 'fiscal_power':"Yes", 'fuel_type':"Yes", 'mark':"No"}
#     encode the json object to one hot encoding so that it could fit our model
#     query_df = pd.DataFrame([{"Age": 85, "Sex": "male", "Embarked": "S","name": "Ali"},
#     {"Age": 24, "Sex": "female", "Embarked": "C", "name": "Ali"},
#     {"Age": 3, "Sex": "male", "Embarked": "C", "name": "Ali"},
#     {"Age": 21, "Sex": "male", "Embarked": "S", "name": "Ali"}])
#     arr=np.array[2011,60000,1,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0]

#     price_pred = gbr.predict(arr)
#     print(price_pred)



#  الكود الجديد

# import pandas as pd
# import numpy as np
# import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# dataset_path = BASE_DIR+'\\ffcars.csv'

# cars = pd.read_csv(dataset_path)
# nncars=cars


# from sklearn import preprocessing

# # create the Labelencoder object
# le = preprocessing.LabelEncoder()

# #convert the categorical columns into numeric
# nncars['Model'] = le.fit_transform(cars['Model'])
# nncars['Transmission'] = le.fit_transform(cars['Transmission'])
# nncars['Sunroof'] = le.fit_transform(cars['Sunroof'])
# nncars['ABS'] = le.fit_transform(cars['ABS'])
# nncars['Digital_Conditioning'] = le.fit_transform(cars['Digital_Conditioning'])
# nncars['Steering_Control'] = le.fit_transform(cars['Steering_Control'])
# nncars['Airbags'] = le.fit_transform(cars['Airbags'])
# nncars['Chrome_Wheel'] = le.fit_transform(cars['Chrome_Wheel'])
# nncars['Technical_Status'] = le.fit_transform(cars['Technical_Status'])



# from sklearn.model_selection import train_test_split

# target_name = 'Price'

# X = nncars[nncars.columns.difference([target_name])]
# Y = nncars[target_name]


# from sklearn.ensemble import GradientBoostingRegressor
# gbr = GradientBoostingRegressor(loss ='ls', max_depth=6)
# gbr.fit(X,Y)
# print("done")

# # # Save the model
# from sklearn.externals import joblib
# joblib.dump(gbr, 'model.pkl')
# print("Model dumped!")
