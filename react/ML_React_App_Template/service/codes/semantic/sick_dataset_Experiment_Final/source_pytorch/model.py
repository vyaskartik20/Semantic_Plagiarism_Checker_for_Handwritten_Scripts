# pytorch mlp for regression
from numpy import vstack
from numpy import sqrt
from pandas import read_csv
from sklearn.metrics import mean_squared_error
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.utils.data import random_split
from torch import Tensor
from torch.nn import Linear
from torch.nn import Sigmoid
from torch.nn import ReLU
from torch.nn import Softmax
from torch.nn import Module
from torch.optim import SGD
from torch.nn import MSELoss
from torch.nn.init import xavier_uniform_
import torch
import torch.nn as nn
import torch.optim as optim
# dataset definition


class CSVDataset(Dataset):
    # load the dataset
    def __init__(self, path):
        # load the csv file as a dataframe
        df = read_csv(path, header=None)
        # store the inputs and outputs
        self.X = df.values[:, 1:].astype('float32')
        self.y = df.values[:, 0].astype('float32')

        # ensure target has the right shape
        self.y = self.y.reshape((len(self.y), 1))

        # self.xy = []

        # for e in self.y :
        #     e = e/5
        #     self.xy.append(e)

        # self.y = self.xy

    # number of rows in the dataset
    def __len__(self):
        return len(self.X)

    # get a row at an index
    def __getitem__(self, idx):
        return [self.X[idx], self.y[idx]]

    # get indexes for train and test rows
    def get_splits(self, n_test=0):
        # determine sizes
        test_size = round(n_test * len(self.X))
        train_size = len(self.X) - test_size
        # calculate the split
        return random_split(self, [train_size, test_size])

# model definition


class MLP(Module):
    # define model elements
    def __init__(self, n_inputs):
        super(MLP, self).__init__()
        # input to first hidden layer
        self.hidden1 = Linear(n_inputs, 20)
        xavier_uniform_(self.hidden1.weight)
        self.act1 = Sigmoid()
        # second hidden layer
        self.hidden2 = Linear(20, 12)
        xavier_uniform_(self.hidden2.weight)
        self.act2 = Sigmoid()
        # third hidden layer and output

        self.hidden3 = Linear(12, 8)
        xavier_uniform_(self.hidden3.weight)
        self.act3 = Sigmoid()

        self.hidden4 = Linear(8, 6)
        xavier_uniform_(self.hidden4.weight)
        self.act4 = Sigmoid()

        # self.hidden5 = Linear(6, 4)
        # xavier_uniform_(self.hidden5.weight)
        # self.act5 = Sigmoid()

        # self.hidden6 = Linear(4, 1)
        # xavier_uniform_(self.hidden6.weight)

        self.hidden5 = Linear(6, 1)
        xavier_uniform_(self.hidden5.weight)

    # forward propagate input
    def forward(self, X):
        # input to first hidden layer
        X = self.hidden1(X)
        X = self.act1(X)
        # second hidden layer
        X = self.hidden2(X)
        X = self.act2(X)

        # third hidden layer and output

        X = self.hidden3(X)
        X = self.act3(X)

        # # X = self.hidden4(X)

        X = self.hidden4(X)
        X = self.act4(X)
        # # return X

        # X = self.hidden5(X)
        # X = self.act5(X)

        # X = self.hidden6(X)
        # return X

        X = self.hidden5(X)
        return X

# prepare the dataset


def prepare_data(path):
    # load the dataset
    dataset = CSVDataset(path)
    # calculate split
    train, test = dataset.get_splits()
    # prepare data loaders
    if (path == 'plagiarism_data/train.csv'):
        train_dl = DataLoader(train, batch_size=32, shuffle=True)
    else:
        train_dl = DataLoader(train, batch_size=1024, shuffle=True)
    # test_dl = DataLoader(test, batch_size=1024, shuffle=False)
    return train_dl

# train the model


def train_model(train_dl, model):
    # define the optimization
    criterion = MSELoss()
    optimizer = SGD(model.parameters(), lr=0.005, momentum=0.9)
    # enumerate epochs
    for epoch in range(250):
        # enumerate mini batches
        for i, (inputs, targets) in enumerate(train_dl):
            # clear the gradients
            optimizer.zero_grad()
            # compute the model output
            yhat = model(inputs)
            # calculate loss
            loss = criterion(yhat, targets)
            # credit assignment
            loss.backward()
            # update model weights
            optimizer.step()

# evaluate the model


def evaluate_model(test_dl, model):
    predictions, actuals = list(), list()
    for i, (inputs, targets) in enumerate(test_dl):
        # evaluate the model on the test set
        yhat = model(inputs)
        # retrieve numpy array
        yhat = yhat.detach().numpy()
        actual = targets.numpy()
        actual = actual.reshape((len(actual), 1))
        # store
        predictions.append(yhat)
        actuals.append(actual)
    predictions, actuals = vstack(predictions), vstack(actuals)
    # calculate mse
    
    sum = 0
    
    for i in range(len(actuals)) : 
        diff = abs(actuals[i] - predictions[i])
        sum = sum + diff
    
    diff = sum / len(actuals)
    
    print(f"the diff, the ans :: ::  {diff} ")
    
    mse = mean_squared_error(actuals, predictions)
    return mse

# make a class prediction for one row of data


def predict(row, model):
    # convert row to data
    row = Tensor([row])
    # make prediction
    yhat = model(row)
    # retrieve numpy array
    yhat = yhat.detach().numpy()
    return yhat


def main():
    # prepare the data
    path_train = 'plagiarism_data/train.csv'
    path_test = 'plagiarism_data/test.csv'
    train_dl = prepare_data(path_train)
    test_dl = prepare_data(path_test)
    print(len(train_dl.dataset), len(test_dl.dataset))
    # define the network
    model = MLP(15)
    # train the model
    train_model(train_dl, model)
    # evaluate the model

    mse1 = evaluate_model(train_dl, model)
    print('MSE: %.3f, RMSE: %.3f' % (mse1, sqrt(mse1)))

    mse = evaluate_model(test_dl, model)
    print('MSE: %.3f, RMSE: %.3f' % (mse, sqrt(mse)))

    PATH = 'model/mod.pt'

    torch.save(model, PATH)

    model = torch.load(PATH)



    # make a single prediction (expect class=1)
    # row = [1.0,0.7365336418151855,0.5555555555555556,0.14285714285714285,0.44474958999666075,0.48395141579019735,0.0,0.0,0.45454545454545453,0.0,0.726502311248074]
    # yhat = predict(row, model)
    # print('Predicted: %.3f' % yhat)


if __name__ == '__main__':
    main()