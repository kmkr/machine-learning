import numpy as np

BIAS_INPUT = -1
class Mlp:
    def __init__(self, inputs, targets, nhidden):
        self.beta = 1
        self.eta = 0.1
        self.momentum = 0.0
        num_input_rows = inputs.shape[1]
        #hidden_shape = (num_input_rows + 1, nhidden)
        #output_shape = (nhidden + 1, targets.shape[1])
        hidden_shape = (num_input_rows, nhidden)
        output_shape = (nhidden, targets.shape[1])
        self.weights_hidden_layer = np.random.uniform(-1, 1, hidden_shape)
        self.weights_output_layer = np.random.uniform(-1, 1, output_shape)

    def sigmoid_activation(self, z):
        return 1 / (1 + np.exp(self.beta  * -z))

    def linear_activation(self, h):
        return h;

    def earlystopping(self, inputs, targets, valid, validtargets):
        self.train(inputs, targets)
        # validate vekter med valid opp mot validtargets

    def train(self, inputs, targets, iterations=100):
        outputs = self.forward(inputs)
        activation_o = outputs[0]
        activation_h = outputs[1]
        # Equation (4.14) from Marsland
        delta_o = activation_o - targets
        # Todo finn ut av om dette er riktig!
        #weightswtf = np.delete(np.transpose(self.weights_output_layer), 0, axis=1)
        weightswtf = np.transpose(self.weights_output_layer)
        delta_h = activation_h * (1 - activation_h) * np.dot(delta_o, weightswtf)

        #update_output_w = self.eta * np.dot(np.transpose(inputs), delta_h)
        update_output_w = self.eta * np.dot(np.transpose(activation_h), delta_o)
        update_hidden_w = self.eta * np.dot(np.transpose(inputs), delta_h)
        self.weights_output_layer = self.weights_output_layer + update_output_w
        self.weights_hidden_layer = self.weights_hidden_layer + update_hidden_w
        print(1)

    def _weighted_sum(self, inputs, weights):
        #input_with_bias = np.insert(inputs, 0, BIAS_INPUT, axis=1)
        #activation = np.dot(input_with_bias, weights)
        activation = np.dot(inputs, weights)
        return activation

    def forward(self, inputs):
        z_h = self._weighted_sum(inputs, self.weights_hidden_layer)
        activation_h = self.sigmoid_activation(z_h)
        z_o = self._weighted_sum(activation_h, self.weights_output_layer)
        activation_o = self.linear_activation(z_o)
        return (activation_o, activation_h)

    def confusion(self, inputs, targets):
        print('To be implemented')
