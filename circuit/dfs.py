class DFS(FaultSim):
    def __init__(self, circuit):
        FaultSim.__init__(self, circuit)
        self.fs_type = 'DFS'


    def single(self, input_pattern):
        """ running deductive fault simulation on the circuit 
        needs to make sure the levelization is updated """ 
        self.logic_sim(input_pattern)
        fault_set = set()
        for node in self.nodes_lev:
            node.dfs()
        for node in self.PO:
            fault_set = fault_set.union(node.faultlist_dfs)
        # return a fault set
        return fault_set
