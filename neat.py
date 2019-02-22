import random as rd

# a neat agent class
class Neat_Agent:

    def __init__(self, input_size, output_size, is_bias, innovation_dic):
        # input_size = the number of input node
        # output size = the number of output node
        # is_bias = a bool who say if er is one bias node
        # innovation dic = a dict who have: a link in key and an innovation number in object

        self.input_size = input_size
        self.output_size = output_size
        self.is_bias = is_bias
        self.innovation_dic = innovation_dic

        # a liste who contain all the Agent nodes
        self.node_genome = []

        # a liste who contain all the connection between 2 nodes
        self.connection_genome = []

        # init the node_genome
        self._init_nodes()

    def _init_nodes(self):
        # init the nodes 

        # add the input nodes in the node_genome
        for i in range(self.input_size):
            self.node_genome.append(Node(i, "input"))

        # add the output nodes in the node_genome
        for _ in range(self.output_size):
            self.node_genome.append(Node(len(self.node_genome), "output"))

        # add the bias node if er is 
        if self.is_bias:
            self.node_genome.append(Node(len(self.node_genome), "bias"))

    def add_connection_mutation(self, prob):
        # add a new connection depending of the probability
        # prob = a number between 0 and 1 who give the probability of gettin a new connection

        if rd.random() <= prob:
            # choose 2 nodes
            inp = rd.choice(self.node_genome)
            out = rd.choice(self.node_genome)

            # check if the input is different of the output
            if inp == out:
                return None

            # check if the output node is not a bias or an input node
            if out.type == "bias" or out.type == "input":
                return None

            # check if er is one connection between inp and out allready exist
            for connection in self.connection_genome:
                if connection.input_node_id == inp.id and connection.output_node_id == out.id:
                    return None

            # check if the connnection have an innovation number else creat one
            if (inp.id, out.id) in self.innovation_dic:
                innov = self.innovation_dic[(inp.id, out.id)]

            else:
                innov = len(self.innovation_dic)
                self.innovation_dic[(inp.id, out.id)] = innov

            # creat the connection and append it in the genome
            self.connection_genome.append(Connection(inp.id, out.id, innov))

# a node class
class Node:

    def __init__(self, number, typ):
        # number = the id of the node
        # typ = the type of the node:
        #  input = a node where the input value will be set
        #  output = a node wher the output value will be get
        #  bias = a node with a intern value of 1 for bias utilisation
        #  transition = a node between 2 others nodes

        self.type = typ
        self.id = number
        self.value = 0 if typ != "bias" else 1

    def reste(self):
        # reste the node value
        self.value = 0 if self.type != "bias" else 1

# a connection class
class Connection:

    def __init__(self, input_node_id, output_node_id, innovation):
        # input_node_id = the id of the input node
        # output_node_id = the id of the output node
        # innovation = the innovation number of this connection

        self.input_node_id = input_node_id
        self.output_node_id = output_node_id
        self.input_node_id = input_node_id

        # set a random weight
        self.weight = 2 * (rd.random() - .5)

        # a number who say if the connection is enable or not
        self.is_enable = True
