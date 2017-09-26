import random
from functools import reduce

BIAS = -1
ITERATIONS = 20
LEARNING_RATE = 0.05

class Perceptron:

    def __init__(self, weights):
        self.weights = weights

    def get_activation(self, input):
        f = lambda prevVal, curVal: prevVal + (curVal[1] * self.weights[curVal[0]])
        return 1 if reduce(f, enumerate(input), 0) > 0 else 0

    def update(self, cur_weight, target, activation, value):
        return cur_weight + LEARNING_RATE * (target - activation) * value

    def train(self, inputs, targets):
        for _ in range(ITERATIONS):
            for idx, input in enumerate(inputs):
                activation = self.get_activation(input)
                f = lambda x: self.update(x[1], targets[idx], activation, input[x[0]])
                self.weights = list(map(f, enumerate(self.weights)))
                print(self.weights)

def get_weights():
    return [random.random() * 0.5, random.random() * 0.5, random.random() * 0.5]

if __name__ == '__main__':
    weights = get_weights()
    not_perceptron = Perceptron(weights)
    not_perceptron.train([ [BIAS, 0, 0], [BIAS, 0, 1], [BIAS, 1, 0], [BIAS, 1, 1] ], [0, 0, 0, 1])

    print(not_perceptron.get_activation([BIAS, 0, 0]))
    print(not_perceptron.get_activation([BIAS, 0, 1]))
    print(not_perceptron.get_activation([BIAS, 1, 0]))
    print(not_perceptron.get_activation([BIAS, 1, 1]))
