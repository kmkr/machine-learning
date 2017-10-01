'''
    This pre-code is a nice starting point, but you can
    change it to fit your needs.
'''
import numpy as np

BIAS_INPUT = -1
class Mlp:
    def __init__(self, inputs, targets, nhidden):
        self.beta = 1
        self.eta = 0.1
        self.momentum = 0.0
        hidden_shape = (inputs.shape[1] + 1, nhidden + 1)
        output_shape = (nhidden + 1, targets.shape[1] + 1)
        self.weights_hidden_layer = np.random.sample(hidden_shape)
        self.weights_output_layer = np.random.sample(output_shape)

    def sigmoid(self, z):
        return 1 / (1 + np.exp(self.beta  * -z))

    def earlystopping(self, inputs, targets, valid, validtargets):
        print('To be implemented')
        self.forward(inputs)

    def train(self, inputs, targets, iterations=100):
        print('To be implemented')

    def _activation(self, inputs, weights):
        input_with_bias = np.insert(inputs, 0, BIAS_INPUT, axis=1)
        activation = np.dot(input_with_bias, weights)
        return activation

    def forward(self, inputs):
        z_h = self._activation(inputs, self.weights_hidden_layer)
        activation_h = self.sigmoid(z_h)
        z_o = self._activation(activation_h, self.weights_output_layer)
        activation_o = self.sigmoid(z_o)
        return activation_o

    def confusion(self, inputs, targets):
        print('To be implemented')
