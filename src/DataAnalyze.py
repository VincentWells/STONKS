import tensorflow as tf
import numpy as np
import pandas as pd

# heavily referenced https://www.tensorflow.org/tutorials/load_data/csv

def get_dataset(file_path, **kwargs):
  dataset = tf.data.experimental.make_csv_dataset(
      file_path,
      batch_size=500, 
      label_name=LABEL_COLUMN,
      na_value="?",
      num_epochs=1,
      ignore_errors=True, 
      **kwargs)
  return dataset

def normalize_numeric_data(data, mean, std):
  # Center the data
  return (data - mean) / std


class Analyzer:

    dataset_file_path = '../data/output.csv'
    LABEL_COLUMN = 'future_price'
    class PackNumericFeatures(object):
        def __init__(self, names):
            self.names = names

        def __call__(self, features, labels):
            numeric_features = [features.pop(name) for name in self.names]
            numeric_features = [tf.cast(feat, tf.float32) for feat in numeric_features]
            numeric_features = tf.stack(numeric_features, axis=-1)
            features['numeric'] = numeric_features

    return features, labels

    def run(self):
        raw_train_data = get_dataset(self.dataset_file_path)
        packed_train_data = raw_train_data.map(PackNumericFeatures(NUMERIC_FEATURES))
        desc = pd.read_csv(train_file_path)[NUMERIC_FEATURES].describe()
        MEAN = np.array(desc.T['mean'])
        STD = np.array(desc.T['std'])
        normalizer = functools.partial(normalize_numeric_data, mean=MEAN, std=STD)

        numeric_column = tf.feature_column.numeric_column('numeric', normalizer_fn=normalizer, 
            shape=[len(NUMERIC_FEATURES)])
        numeric_columns = [numeric_column]

        numeric_layer = tf.keras.layers.DenseFeatures(numeric_columns)

        model = tf.keras.Sequential([
            preprocessing_layer,
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(1),])

        model.compile(
            loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
            optimizer='adam',
            metrics=['accuracy'])
        train_data = packed_train_data.shuffle(500)

        model.fit(train_data, epochs=20)
