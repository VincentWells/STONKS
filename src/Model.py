import tensorflow as tf

# custom Financial Model


class FinModel(tf.keras.Model):
    # TODO: define extra variables
    def __init__(self):
        super(FinModel, self).__init__(name="FinModel")
        # TODO: define layers

    def call(self, inputs):
        # TODO: define operations that model performs
        return self
