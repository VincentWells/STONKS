import tensorflow as tf
import pathlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob


dow_jones = ["MMM",  "AXP",  "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DIS", "DOW", "XOM", "GS", "HD", "IBM", "INTC", "JNJ", "JPM", "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UTX", "UNH", "VZ",  "V", "WMT", "WBA"]

for company in dow_jones:

    #create list of all records for given company
    file_list = []
    for file in glob.glob("../data/{}*.csv".format(company)):
        file_list.append(file)

    #read data from each record
    master_dataset = tf.data.Dataset.from_tensor_slices([])
    for file_path in file_list:
        dataset = tf.data.experimental.make_csv_dataset(file_path, batch_size=100, label_name=LABEL_COLUMN, na_value="?", num_epochs=1, ignore_errors=True)
        master_dataset.concatenate(dataset)


    #predict future trends for given company
