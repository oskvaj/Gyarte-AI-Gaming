from numpy import exp, random, dot, concatenate, reshape, tanh
import numpy as np
generator = random.default_rng()

from sklearn import preprocessing
scaler = preprocessing.StandardScaler()

global_mutation_chance = 0.01

class NeuralLayer():
    def __init__(self, number_of_nodes, number_of_inputs_per_node, synaptic_weights=None, bias = None):
        self.number_of_nodes = number_of_nodes
        self.number_of_inputs_per_node = number_of_inputs_per_node
        if synaptic_weights is None:
            self.synaptic_weights = 2 * random.rand(number_of_inputs_per_node, number_of_nodes) - 1
        else:
            self.synaptic_weights = synaptic_weights        

        if bias == None:
            self.bias = 2 * generator.random() - 1
        else:
            self.bias = bias

class NeuralNetwork():
    def __init__(self, layers):
        """ 
        layers can come in 2 ways
        Either as instances of NeuralLayer
        OR as a list of nodes per layer, starting with input nodes and ending with output nodes
        (Can also be empty when doing crossover)
        """

        if len(layers) == 0:
            self.layers = layers
        elif isinstance(layers[0], NeuralLayer):
            self.layers = layers
        elif isinstance(layers[0], int):
            self.layers = []
            for layer_index, inputs_per_node in enumerate(layers):
                if layer_index >= (len(layers) - 1):
                    break
                self.layers.append(NeuralLayer(layers[layer_index+1], inputs_per_node))

    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))
    
    def __relu(self, x):
        x[x < 0] = 0
        return x
    
    def think(self, inputs):
        inputs = preprocessing.normalize(inputs)
        outputs = []
        for count, layer in enumerate(self.layers):
            if count == 0:
                #outputs.append(self.__sigmoid(dot(inputs, layer.synaptic_weights) + layer.bias))
                #outputs.append(tanh(dot(inputs, layer.synaptic_weights) + layer.bias))
                outputs.append(self.__relu(dot(inputs, layer.synaptic_weights) + layer.bias))

                continue
            outputs.append(self.__sigmoid(dot(outputs[-1], layer.synaptic_weights) + layer.bias))
            #outputs.append(tanh(dot(outputs[-1], layer.synaptic_weights) + layer.bias))
            #outputs.append(self.__relu(dot(outputs[-1], layer.synaptic_weights) + layer.bias))

        return outputs[-1]

    def mutate(self):
        for layer_index, _ in enumerate(self.layers):
            
            layer_weights_shape = self.layers[layer_index].synaptic_weights.shape

            random_values = random.rand(layer_weights_shape[0], layer_weights_shape[1]) * 2 - 1
            mask = np.random.choice([0, 1], size=layer_weights_shape, p=((1 - global_mutation_chance), global_mutation_chance)).astype(np.bool)

            self.layers[layer_index].synaptic_weights[mask] = random_values[mask]
    
    def crossover(self, other_network):
        children_networks = [NeuralNetwork([]), NeuralNetwork([])]
        for layer1, layer2 in zip(self.layers, other_network.layers):
            #Flatten netowrks
            flattened_weights1 = concatenate(layer1.synaptic_weights)
            flattened_weights2 = concatenate(layer2.synaptic_weights)

            #Pick a random point on the networks
            cutoff_point = random.randint(len(flattened_weights1))

            #Create 2 children so all genes are passed down
            new_weights1 = concatenate([flattened_weights1[0:cutoff_point:], flattened_weights2[cutoff_point::]])
            new_weights2 = concatenate([flattened_weights2[0:cutoff_point:], flattened_weights1[cutoff_point::]])

            new_layer1 = NeuralLayer(layer1.number_of_nodes, layer1.number_of_inputs_per_node, new_weights1, layer1.bias)
            new_layer2 = NeuralLayer(layer1.number_of_nodes, layer1.number_of_inputs_per_node, new_weights2, layer2.bias)


            children_networks[0].layers.append(new_layer1)
            children_networks[1].layers.append(new_layer2)

        for child_network in children_networks:
            for layer in child_network.layers:
                layer.synaptic_weights = reshape(layer.synaptic_weights, (layer.number_of_inputs_per_node, layer.number_of_nodes))
        return children_networks