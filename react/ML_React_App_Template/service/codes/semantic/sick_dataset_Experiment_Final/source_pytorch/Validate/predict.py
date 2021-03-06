# import libraries
import os
import numpy as np
import torch
from six import BytesIO
import pandas as pd

# import model from model.py, by name
from model import BinaryClassifier

# default content type is numpy array
NP_CONTENT_TYPE = 'application/x-npy'


# Provided model load function
def model_fn(model_dir):
    """Load the PyTorch model from the `model_dir` directory."""
    print("Loading model.")

    # First, load the parameters used to create the model.
    model_info = {}
    model_info_path = os.path.join(model_dir, 'model_info.pth')
    with open(model_info_path, 'rb') as f:
        model_info = torch.load(f)

    print("model_info: {}".format(model_info))

    # Determine the device and construct the model.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = BinaryClassifier(model_info['input_features'], model_info['hidden_dim'], model_info['output_dim'])

    # Load the store model parameters.
    model_path = os.path.join(model_dir, 'model.pth')
    with open(model_path, 'rb') as f:
        model.load_state_dict(torch.load(f))

    # Prep for testing
    model.to(device).eval()

    print("Done loading model.")
    return model


# Provided predict function
def predict_fn(input_data, model):
    print('Predicting class labels for the input data...')

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Process input_data so that it is ready to be sent to our model.
    data = torch.from_numpy(input_data.astype('float32'))
    data = data.to(device)

    # Put the model into evaluation mode
    model.eval()

    # Compute the result of applying the model to the input data
    # The variable `out_label` should be a rounded value, either 1 or 0
    out = model(data)
    out_np = out.cpu().detach().numpy()
    print(out_np)
    out_label = out_np.round()
    print(out_label)

    return out_label

path = 'D:\\BTP-2\\semantic\\udacity_Experiments\\source_pytorch\\model\\'
#model_fn(os.path.dirname(path))

data_stream = open('plagiarism_data/test.csv',"r").read()
# read data as DataFrame
test_df = pd.read_csv('plagiarism_data/test.csv', header=None, names=None)
# split data into labels and features
test_y_np = test_df.iloc[:,0].values.astype('float32')
test_x_np = test_df.iloc[:,1:].values.astype('float32')

predict_fn(test_x_np,model_fn(os.path.dirname(path)))

