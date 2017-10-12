import numpy as np

BIAS_INPUT = -1
ETA = 0.1
BETA = 1
MOMENTUM = 0.9
ERROR_RATIO_THRESHOLD = 0.1
class Mlp:
    def __init__(self, inputs, targets, nhidden):
        num_input_rows = inputs.shape[1]
        hidden_shape = (num_input_rows + 1, nhidden)
        output_shape = (nhidden + 1, targets.shape[1])
        #self.weights_hidden_layer = np.random.uniform(-1, 1, hidden_shape)
        #self.weights_output_layer = np.random.uniform(-1, 1, output_shape)
        # todo: dette gjøres vel for å skvise tallene nærmere 0?
        self.weights_hidden_layer = (np.random.rand(num_input_rows + 1, nhidden) - 0.5) * (2 / np.sqrt(num_input_rows))
        self.weights_output_layer = (np.random.rand(nhidden + 1, targets.shape[1]) - 0.5) * (2 / np.sqrt(nhidden))

    def _with_bias(self, elems):
        return np.insert(elems, 0, BIAS_INPUT, axis=1)

    def sigmoid_activation(self, z):
        return 1 / (1 + np.exp(BETA * -z))

    def linear_activation(self, h):
        return h;

    def _get_error(self, outputs, targets):
        return 0.5*np.sum((outputs[0]-targets)**2)

    def earlystopping(self, inputs, targets, valid, validtargets):
        prev_error = np.inf
        cur_error = np.inf
        while cur_error <= prev_error:
            print('Current error is', cur_error)
            self.train(inputs, targets)
            outputs = self.forward(valid)
            activation_o = outputs[0]
            prev_error = cur_error
            cur_error = self._get_error(activation_o, validtargets)

        return cur_error

    def train(self, inputs, targets, iterations=100):
        update_hidden_w = np.zeros((np.shape(self.weights_hidden_layer)))
        update_output_w = np.zeros((np.shape(self.weights_output_layer)))
        for index in range(iterations):
            outputs = self.forward(inputs)
            if (np.mod(index, 10) == 0):
                print('Iteration',index, 'error:', self._get_error(outputs[0], targets))
            activation_o = outputs[0]
            activation_h = outputs[1]
            # Equation (4.8) from Marsland
            # delta_o = (activation_o - targets) * activation_o * (1.0 - activation_o)
            # Modified equation (4.14) from Marsland
            delta_o = (activation_o - targets) / inputs.shape[0]
            activation_h_with_bias = self._with_bias(activation_h)
            inputs_with_bias = self._with_bias(inputs)
            delta_h = activation_h_with_bias * (1.0 - activation_h_with_bias) * np.dot(delta_o, np.transpose(self.weights_output_layer))

            update_hidden_w = ETA * np.dot(np.transpose(inputs_with_bias), delta_h[:,:-1]) + MOMENTUM * update_hidden_w
            update_output_w = ETA * np.dot(np.transpose(activation_h_with_bias), delta_o) + MOMENTUM * update_output_w
            self.weights_output_layer -= update_output_w
            self.weights_hidden_layer -= update_hidden_w

        return outputs

    def _weighted_sum(self, inputs, weights):
        return np.dot(self._with_bias(inputs), weights)

    def forward(self, inputs):
        z_h = self._weighted_sum(inputs, self.weights_hidden_layer)
        activation_h = self.sigmoid_activation(z_h)
        z_o = self._weighted_sum(activation_h, self.weights_output_layer)
        activation_o = self.linear_activation(z_o)
        return (activation_o, activation_h)

    def confusion(self, inputs, targets):
        outputs = self.forward(inputs)[0]
        num_input = targets.shape[1]
        outputs = np.argmax(outputs,1)
        targets = np.argmax(targets,1)

        confusion_matrix = np.zeros((num_input,num_input))
        for i in range(num_input):
            for j in range(num_input):
                confusion_matrix[i,j] = np.sum(np.where(outputs==i,1,0)*np.where(targets==j,1,0))

        percentage_correct = np.trace(confusion_matrix) / np.sum(confusion_matrix) * 100
        return (confusion_matrix, percentage_correct)
