# -*- coding: utf-8 -*-


import argparse
import pdb
#import networkx as nx
import math
import time
from random import randint

from circuit import Circuit
from modelsim_simulator import Modelsim

import sys
sys.path.insert(1, "../data/netlist_behavioral")
from c432_logic_sim import c432_sim
import config
from checker_logicsim import *
from regular_tp_gen import *
#from checker_dfs import *
from FaultSim import *
from deductive_fs import DFS
from d_alg import *

def check_gate_netlist(circuit, total_T=1):

    for t in range(total_T):
        PI_dict = dict()
        PI_list = []
        
        PI_num = [x.num for x in circuit.PI]
        for pi in PI_num:
            val = randint(0,1)
            PI_dict["in" + str(pi)] = val
            PI_list.append(val)

        res_beh = c432_sim(PI_dict)
        circuit.logic_sim(PI_list)
        res_ckt = circuit.read_PO()
        if res_beh != res_ckt:
            print("Wrong")
            return False
    print("all test patterns passed")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ckt", type=str, required=True, help="circuit name, c17, no extension")
    parser.add_argument("-tp", type=int, required=False, help="number of tp for random sim")
    parser.add_argument("-cpu", type=int, required=False, help="number of parallel CPUs")
    args = parser.parse_args()

    print("\n======================================================")
    print("Run | circuit: {} | Test Count: {} | CPUs: {}".format(args.ckt, args.tp, args.cpu))
    print("======================================================\n")

    #Ting-Yu
    
    # for c in ['c17','c432','c499','c880','c1355','c1908','c2670','c3540','c5315','c6288','c7552']:
    #     checker = Checker(c, args.tp)
    #     if checker.check_PI_PO() == False:
    #         print('#################################')
    #         continue
    #     checker.modelsim_wrapper()
    #     checker.check_ckt_verilog('verilog')
    #     checker.check_ckt_verilog('ckt')
    #     print('#################################')
    # #exit()
    

    # circuit = Circuit(args.ckt)
    # circuit.read_verilog()
    # circuit.read_ckt()
    # circuit.lev()

    """ Testing DFS """
    # print("DFS starts")
    # dfs = DFS(circuit)
    # for i in range(1, 11):
    #     dfs.fs_exe_golden(tp_num=1, t_mode='rand', no=i, r_mode='b')
    
    # dfs.fs_exe(tp_num=args.tp, t_mode='rand', r_mode='b')

    """ Testing D alg """
    print("*****************************************************")
    print("***********        START D-ALG         **************")
    print("*****************************************************")
    # d_alg = d_alg_new(circuit)
    # d_alg.dalg_recur('14', 3)
    for ckt in [args.ckt]:
        circuit = Circuit(ckt)
        # LoadCircuit(circuit, "v")
        circuit.read_verilog()
        # circuit.read_ckt()
        circuit.lev()
        # in fault: ('14',0): node 14 SA0
        # but we need to gives D to the node in dalg!!!!!!!!!!!!!!!!!!############
        for fault in [('3-1', 1)]:
            d_alg = D_alg(circuit, fault[0], fault[1])
            # fault_val = 1: 1^12=D'    fault_val = 0: 0^12=D
            ######################## needs to be changed!!!! put in dalg!!!!!!
            # if fault[1] == 1:
            #     fault_val = 15
            # else:
            #     fault_val = 0
            # fault_val = fault_val ^ 12
            ###########################################
            if d_alg.dalg() == True:
                IPT_list = d_alg.return_IPI()
                IPT_binary_list = []
                for x in IPT_list:
                    if x == 9 or x == 15 or x == 12:
                        IPT_binary_list.append(1)
                    else:
                        IPT_binary_list.append(0)
                dfs_test = DFS(circuit)
                fault_list = dfs_test.single(IPT_binary_list)
                print('fault >> ',fault)
                print('fault_list >> ', fault_list)
                if fault in fault_list:
                    print('result is correct')
                else:
                    print('result is not correct')
            else:
                print('can not find test')
    exit()




def parallel_graph():
    netlists = ["c17", "c432", "c499", "c880", "c1355", "c1908", "c2670",
            "c3540", "c5315", "c6288", "c7552"]

if __name__ == "__main__":
    main()
