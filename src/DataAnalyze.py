import tensorflow as tf


def read_from_csv(filename_queue):
  reader = tf.TextLineReader(skip_header_lines=1)
  _, csv_row = reader.read(filename_queue)
  record_defaults = [[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]]
  col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = tf.decode_csv(csv_row, record_defaults=record_defaults)
  features = tf.stack([col1, col2, col3, col4, col5, col6, col7, col8, col9])
  label = tf.stack([col10])
  return features, label

class Analyzer:
    def run(self):
        filename = '../data/output.csv'
        features, lables = read_csv(filename)