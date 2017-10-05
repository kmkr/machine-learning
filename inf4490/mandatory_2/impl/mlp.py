import numpy as np

BIAS_INPUT = -1
class Mlp:
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

    def _with_bias(self, elems):
        return np.insert(elems, 0, BIAS_INPUT, axis=1)

    def sigmoid_activation(self, z):
        return 1 / (1 + np.exp(self.beta  * -z))

    def linear_activation(self, h):
        return h;

    def earlystopping(self, inputs, targets, valid, validtargets):
        self.train(inputs, targets)
        # validate vekter med valid opp mot validtargets
        outputs = self.forward(valid)
        activation_o = outputs[0]
        print(1)

    def train(self, inputs, targets, iterations=100):
        update_hidden_w = np.zeros((np.shape(self.weights_hidden_layer)))
        update_output_w = np.zeros((np.shape(self.weights_output_layer)))
        for n in range(iterations):
            outputs = self.forward(inputs)
            error = 0.5*np.sum((outputs[0]-targets)**2)
            #if (np.mod(n,50)==0):
            print("Iteration: ",n, " Error: ",error)
            activation_o = outputs[0]
            activation_h = outputs[1]
            # Equation (4.8) from Marsland
            #delta_o = (activation_o - targets) * activation_o * (1.0 - activation_o)
            delta_o = (activation_o - targets) / inputs.shape[0]
            activation_h_with_bias = self._with_bias(activation_h)
            inputs_with_bias = self._with_bias(inputs)
            delta_h = activation_h_with_bias * (1.0 - activation_h_with_bias) * np.dot(delta_o, np.transpose(self.weights_output_layer))

            update_hidden_w = self.eta * np.dot(np.transpose(inputs_with_bias), delta_h[:,:-1]) + self.momentum * update_hidden_w
            update_output_w = self.eta * np.dot(np.transpose(activation_h_with_bias), delta_o) + self.momentum * update_output_w
            self.weights_output_layer -= update_output_w
            self.weights_hidden_layer -= update_hidden_w

    def _weighted_sum(self, inputs, weights):
        return np.dot(self._with_bias(inputs), weights)

    # todo: skriv om denne!
    def confmat(self,inputs,targets):
        """Confusion matrix"""

        outputs = self.forward(inputs)[0]

        nclasses = np.shape(targets)[1]

        if nclasses==1:
            nclasses = 2
            outputs = np.where(outputs>0.5,1,0)
        else:
            # 1-of-N encoding
            outputs = np.argmax(outputs,1)
            targets = np.argmax(targets,1)

        cm = np.zeros((nclasses,nclasses))
        for i in range(nclasses):
            for j in range(nclasses):
                cm[i,j] = np.sum(np.where(outputs==i,1,0)*np.where(targets==j,1,0))

        print("Confusion matrix is:")
        print(cm)
        print("Percentage Correct: ",np.trace(cm)/np.sum(cm)*100)

    def forward(self, inputs):
        z_h = self._weighted_sum(inputs, self.weights_hidden_layer)
        activation_h = self.sigmoid_activation(z_h)
        z_o = self._weighted_sum(activation_h, self.weights_output_layer)
        activation_o = self.linear_activation(z_o)
        return (activation_o, activation_h)

    def confusion(self, inputs, targets):
        return self.confmat(inputs, targets)
