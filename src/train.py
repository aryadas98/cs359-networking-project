import numpy as np
import os.path
import pickle
from sklearn.tree import DecisionTreeRegressor

file_path = os.path.join(os.path.dirname(__file__),os.pardir,'data/tcp_data.csv')

X = np.loadtxt(file_path,delimiter=',',skiprows=1,usecols=(0,2,3))
thres_vals = np.loadtxt(file_path,delimiter=',',skiprows=1,usecols=(1))
Y = np.loadtxt(file_path,delimiter=',',skiprows=1,usecols=(4,5))

# normalize input
X[:,0] = X[:,0]/thres_vals
Y[:,0] = Y[:,0]/thres_vals
Y[:,1] = Y[:,1]/thres_vals

dt = DecisionTreeRegressor()
dt.fit(X,Y)

Y_pred = dt.predict(X)
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

test_thres_vals = np.array([100,100,100,100,100])
testX[:,0] = testX[:,0]/test_thres_vals

print("ssthreshs:")
print(test_thres_vals)
print()

test_pred = dt.predict(testX)

test_pred[:,0] = test_pred[:,0]*test_thres_vals
test_pred[:,1] = test_pred[:,1]*test_thres_vals

print("Predictions:")
print(test_pred)
print()

model_save_path = os.path.join(os.path.dirname(__file__),os.pardir,'model/model.pickle')

print("Saving model as model/model.pickle")
pickle.dump(dt, open(model_save_path, 'wb'))