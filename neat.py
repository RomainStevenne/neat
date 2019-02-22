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

    def add_node_mutation(self, prob):
        # add a new node with a probability of prob
        # prob = a number between 0 and 1 who give the probability of gettin a new connection
        # this node will disable a connection
        # and creat 2 connections: 
        # 1 between the previous inp and the new node
        # 2 between the new node and the previous out 

        if rd.random() <= prob:
            # get a random connection from the connection genome
            connection = rd.choice(self.connection_genome)

            # check if the connection is enable
            if connection.is_enable:
                # disable the connection and get the previous inp and out ids
                connection.is_enable = False
                previous_inp_id = connection.input_node_id
                previous_out_id = connection.output_node_id

                # create and push  the new node
                # get the max node id
                new_id = - 1
                for node in self.node_genome:
                    if new_id <= node.id: new_id = node.id

                self.node_genome.append(new_id, "transition")

                # create and push the new 2 connections
                # check and get the innovations numbers
                if (previous_inp_id, new_id) in self.innovation_dic:
                    connection_a_innovation = self.innovation_dic[(previous_inp_id, new_id)]
                else:
                    connection_a_innovation = len(self.innovation_dic)
                    self.innovation_dic[(previous_inp_id, new_id)] = connection_a_innovation

                if (new_id, previous_out_id) in self.innovation_dic:
                    connection_b_innovation = self.innovation_dic[(new_id, previous_out_id)]
                else:
                    connection_b_innovation = len(self.innovation_dic)
                    self.innovation_dic[(new_id, previous_out_id)] = connection_b_innovation

                # create and push
                self.connection_genome.append(Connection(previous_inp_id, new_id, connection_a_innovation))
                self.connection_genome.append(Connection(new_id, previous_out_id, connection_b_innovation))

    def crossover(self, other):
        # create a new Agent based on the self and other agent

        # creat the baby with the same basic node_genome as self and other
        baby = Neat_Agent(self.input_size, self.output_size, self.is_bias, self.innovation_dic)

        # get the connections genomes
        parent_a_genome = self.connection_genome
        parent_b_genome = other.connection_genome

        # create the baby_connection_genome
        baby_connection_genome = []

        for i in range(self.innovation_dic):
            a_connection = None
            b_connection = None

            # get the connection for parent a and parent b with the i inovetion number if er is 
            for connection in parent_a_genome:
                if connection.innovation == i:
                    a_connection = connection

            for connection in parent_b_genome:
                if connection.innovation == i:
                    b_connection = connection

            # conditions for push a connection in the baby connection genome
            if a_connection and b_connection:
                if not a_connection.is_enable:
                    baby_connection_genome.append(a_connection.clone())

                elif not b_connection.is_enable:
                    baby_connection_genome.append(b_connection.clone())

                else:
                    selected = rd.choice((a_connection, b_connection))
                    baby_connection_genome.append(selected.clone())

            elif a_connection:
                baby_connection_genome.append(a_connection.clone())

            elif b_connection:
                baby_connection_genome.append(b_connection.clone())

        # get the nodes id for the baby
        nodes_id = []
        
        for connection in baby_connection_genome:
            inp = connection.input_node_id
            out = connection.output_node_id

            if inp not in nodes_id: nodes_id.append(inp)
            if out not in nodes_id: nodes_id.append(out)

        # create the node who doesn't exist for baby
        for i in nodes_id:

            # check if node exist
            exist = False
            for node in baby.node_genome:
                if node.id == i:
                    exist = True

            # creat the node if not exist
            if not exist:        
                node = Node(i, "transition")
                baby.node_genome.append(node)

        # push the baby connection genome in baby
        baby.connection_genome = baby_connection_genome

        return baby

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
        self.innovation = innovation

        # set a random weight between -2 and 2
        self.weight = 4 * (rd.random() - .5)

        # a number who say if the connection is enable or not
        self.is_enable = True

    def clone(self):
        # clone the connection
        new = Connection(self.input_node_id, self.output_node_id, self.innovation)
        
        # pass the value to the new object
        new.is_enable = self.is_enable
        new.weight = self.weight

        return new
        