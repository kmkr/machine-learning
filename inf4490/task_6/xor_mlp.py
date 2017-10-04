import numpy as np

BIAS_INPUT = -1
class XorMlp:
    def __init__(self, inputs, targets, nhidden):
        self.eta = 0.1
        self.beta = 1
        self.momentum = 0.9
        num_input_rows = inputs.shape[1]
        hidden_shape = (num_input_rows + 1, nhidden)
        output_shape = (nhidden + 1, targets.shape[1])
        #self.weights_hidden_layer = np.random.uniform(-1, 1, hidden_shape)
        #self.weights_output_layer = np.random.uniform(-1, 1, output_shape)
        self.weights_hidden_layer = (np.random.rand(num_input_rows + 1, nhidden)-0.5)*2/np.sqrt(num_input_rows)
        self.weights_output_layer = (np.random.rand(nhidden + 1, targets.shape[1])-0.5)*2/np.sqrt(nhidden)

    def activation(self, outputs):
         return 1.0/(1.0+np.exp(-self.beta*outputs))

    def _with_bias(self, elems):
        return np.insert(elems, 0, BIAS_INPUT, axis=1)

    def train(self, inputs, targets, iterations=100):
        update_hidden_w = np.zeros((np.shape(self.weights_hidden_layer)))
        update_output_w = np.zeros((np.shape(self.weights_output_layer)))
        for n in range(iterations):
            outputs = self.forward(inputs)
            error = 0.5*np.sum((outputs[0]-targets)**2)
            if (np.mod(n,50)==0):
                print("Iteration: ",n, " Error: ",error)
            activation_o = outputs[0]
            activation_h = outputs[1]
            # Equation (4.8) from Marsland
            delta_o = (activation_o - targets) * activation_o * (1.0 - activation_o)
            activation_h_with_bias = self._with_bias(activation_h)
            inputs_with_bias = self._with_bias(inputs)
            delta_h = activation_h_with_bias * (1.0 - activation_h_with_bias) * np.dot(delta_o, np.transpose(self.weights_output_layer))

            update_hidden_w = self.eta * np.dot(np.transpose(inputs_with_bias), delta_h[:,:-1]) + self.momentum * update_hidden_w
            update_output_w = self.eta * np.dot(np.transpose(activation_h_with_bias), delta_o) + self.momentum * update_output_w
            self.weights_output_layer -= update_output_w
            self.weights_hidden_layer -= update_hidden_w

    def _weighted_sum(self, inputs, weights):
        return np.dot(self._with_bias(inputs), weights)

    def forward(self, inputs):
        z_h = self._weighted_sum(inputs, self.weights_hidden_layer)
        activation_h = self.activation(z_h)
        z_o = self._weighted_sum(activation_h, self.weights_output_layer)
        activation_o = self.activation(z_o)
        return (activation_o, activation_h)

    def _confmat(self, outputs, targets):
        num_input_values = 2 # må fikses for mer generell input
        confmat_shape = (num_input_values, num_input_values)
        confmat = np.zeros(confmat_shape)

        for i, output in enumerate(outputs):
            for j, elem in enumerate(output):
                normalized = 1 if output > 0.5 else 0
                target = targets[i][j]
                #success = target == normalized
                actual_classifier = target # class er enten 0 eller 1
                predicted_classifier = normalized
                confmat[actual_classifier][predicted_classifier] = confmat[actual_classifier][predicted_classifier] + 1

        return (confmat, outputs)

    def confusion(self, inputs, targets):
        outputs = self.forward(inputs)[0]
        return self._confmat(outputs, targets)

def run():
    inputs = np.array([
        [0, 0],
        [0, 1],
        [1, 1],
        [1, 0]
    ])
    targets = np.array([
        [0],
        [1],
        [0],
        [1]
    ])
    num_hidden = 5

    mlp = XorMlp(inputs, targets, num_hidden)
    mlp.train(inputs, targets, 5000)
    confmat_result = mlp.confusion(inputs, targets)
    print('Output:')
    print(confmat_result[1])
    print('Confmat:')
    print(confmat_result[0])

if __name__ == '__main__':
    run()
