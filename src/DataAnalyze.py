import tensorflow as tf


def file_len(fname):
    with open(fname) as f:
        for i, _ in enumerate(f):
            pass
    return i


class Analyzer:

    dataset = '../data/output.csv'
    # Parameters
    learning_rate = 0.1
    num_steps = 50
    batch_size = 1000
    display_step = 100

    # Network Parameters
    n_hidden_1 = 256  # 1st layer number of neurons
    n_hidden_2 = 256  # 2nd layer number of neurons
    n_hidden_3 = 256  # 3rd layer number of neurons
    num_input = 9  # 10 dimensional vector is the input
    num_classes = 1  # output is -1 or 1

    # tf Graph input
    X = tf.placeholder("float", [None, num_input])
    Y = tf.placeholder("float", [None, num_classes])

    # Store layers weight & bias
    weights = {
        'h1': tf.Variable(tf.random_normal([num_input, n_hidden_1])),
        'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
        'h3': tf.Variable(tf.random_normal([n_hidden_2, n_hidden_3])),
        'out': tf.Variable(tf.random_normal([n_hidden_3, num_classes]))
    }
    biases = {
        'b1': tf.Variable(tf.random_normal([n_hidden_1])),
        'b2': tf.Variable(tf.random_normal([n_hidden_2])),
        'b3': tf.Variable(tf.random_normal([n_hidden_3])),
        'out': tf.Variable(tf.random_normal([num_classes]))
    }

    def run(self):
        file_length = file_len(self.dataset)
        examples, labels = self.input_pipeline(file_length, 1)

        logits = self.neural_net(self.X)
        prediction = tf.nn.softmax(logits)

        # Define loss and optimizer
        loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
            logits=logits, labels=self.Y))
        optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
        train_op = optimizer.minimize(loss_op)

        # Evaluate model
        correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(self.Y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

        init_op = tf.group(tf.initialize_all_variables(), tf.initialize_local_variables())

        with tf.Session() as sess:
            sess.run(init_op)
            # start populating filename queue
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(coord=coord)

            try:
                while not coord.should_stop():
                    example_batch, label_batch = sess.run([examples, labels])

                    print(sess.run(accuracy, feed_dict={self.X: example_batch, self.Y: label_batch}))
                    print(label_batch)
            except tf.errors.OutOfRangeError:
                print('Done training, epoch reached')
            finally:
                coord.request_stop()

            coord.join(threads)

    def input_pipeline(self, batch_size, num_epochs=None):
        filename_queue = tf.train.string_input_producer([self.dataset], num_epochs=num_epochs, shuffle=True)
        example, label = self.read_from_csv(filename_queue)
        min_after_dequeue = 100
        capacity = min_after_dequeue + 3 * batch_size
        example_batch, label_batch = tf.train.shuffle_batch(
            [example, label], batch_size=batch_size, capacity=capacity,
            min_after_dequeue=min_after_dequeue)
        return example_batch, label_batch

    @staticmethod
    def read_from_csv(self, filename):
        reader = tf.TextLineReader(skip_header_lines=1)
        _, csv_row = reader.read(filename)
        record_defaults = [[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]]
        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = tf.decode_csv(csv_row,
                                                                                    record_defaults=record_defaults)
        features = tf.stack([col1, col2, col3, col4, col5, col6, col7, col8, col9])
        labels = tf.stack([col10])
        return features, labels

    def neural_net(self, x):
        # Hidden fully connected layer with 256 neurons
        layer_1 = tf.add(tf.matmul(x, self.weights['h1']), self.biases['b1'])
        # Hidden fully connected layer with 256 neurons
        layer_2 = tf.add(tf.matmul(layer_1, self.weights['h2']), self.biases['b2'])
        # Hidden fully connected layer with 256 neurons
        layer_3 = tf.add(tf.matmul(layer_2, self.weights['h3']), self.biases['b3'])
        # Output fully connected layer with a neuron for each class
        out_layer = tf.matmul(layer_3, self.weights['out']) + self.biases['out']
        return out_layer


