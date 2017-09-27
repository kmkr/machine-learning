import random
from functools import reduce

BIAS = -1
ITERATIONS = 100
LEARNING_RATE = 0.05

class BinaryOp:
    def __init__(self, inputs, targets, label):
        self.inputs = list(map(lambda inp: ([BIAS] + inp), inputs))
        self.targets = targets
        self.label = label

class Perceptron:

    def __init__(self, weights):
        self.weights = weights

    def get_activation(self, input):
        f = lambda prevVal, curVal: prevVal + (curVal[1] * self.weights[curVal[0]])
        return 1 if reduce(f, enumerate(input), 0) > 0 else 0

    def update(self, cur_weight, target, activation, value):
        return cur_weight + LEARNING_RATE * (target - activation) * value

    def train(self, binaryOp):
        for _ in range(ITERATIONS):
            for idx, inp in enumerate(binaryOp.inputs):
                activation = self.get_activation(inp)
                f = lambda x: self.update(x[1], binaryOp.targets[idx], activation, inp[x[0]])
                self.weights = list(map(f, enumerate(self.weights)))

def generate_weights():
    return [random.random() for _ in range(3)]

def run_ops():
    binary_ops = [
        BinaryOp([[0, 0], [0, 1], [1, 0], [1, 1]], [0, 0, 0, 1], 'NAND'),
        BinaryOp([[0, 0], [0, 1], [1, 0], [1, 1]], [1, 0, 0, 0], 'NOR'),
        BinaryOp([[0, 0], [0, 1], [1, 0], [1, 1]], [0, 1, 1, 0], 'XOR'),
    ]

    for binary_op in binary_ops:
        weights = generate_weights()
        perceptron = Perceptron(weights)
        perceptron.train(binary_op)
        print('Checking ' + str(binary_op.label))
        for idx, inp in enumerate(binary_op.inputs):
            activation = perceptron.get_activation(inp)
            target = binary_op.targets[idx]
            if activation == target:
                print('Success')
            else:
                print('Failure')

if __name__ == '__main__':
    run_ops()
