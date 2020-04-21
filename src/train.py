import numpy as np
import os.path
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

file_path = os.path.join(os.path.dirname(__file__),os.pardir,'data/tcp_data.csv')

X = np.loadtxt(file_path,delimiter=',',skiprows=1,usecols=(0,1,2))
Y = np.loadtxt(file_path,delimiter=',',skiprows=1,usecols=(3))

poly_features = PolynomialFeatures(degree=2,interaction_only=True)
X_poly = poly_features.fit_transform(X)

lr = LinearRegression()
lr.fit(X_poly,Y)

Y_pred = lr.predict(X_poly)
train_err = np.mean(np.abs(Y-Y_pred))
print("Training completed.")
print("Loss:",train_err)
print()

testX = np.array([
        [45,0,0],
        [45,0,1],
        [10,1,0],
        [35,1,0],
        [75,1,0]
    ], dtype=np.float32)

print("Testing on data:")
print(testX)
print()

testX_poly = poly_features.fit_transform(testX)

test_pred = lr.predict(testX_poly)

print("Predictions:")
print(test_pred)
print()

model_save_path = os.path.join(os.path.dirname(__file__),os.pardir,'model/model.pickle')

print("Saving model as model/model.pickle")
pickle.dump(lr, open(model_save_path, 'wb'))