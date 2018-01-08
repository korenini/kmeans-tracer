import numpy as np
import random
import itertools

import settings as kset
import data
from functions import *

def lkm(lclu):
    #
    flag_continue = True
    flag_moved = False
    #
    itercounter = 0
    #
    units = list(range(data.dlen))
    #
    #
    clulst = list(range(kset.k))
    #
    trace_clu = []
    trace_wss = []
    warnings = []
    #
    trace_clu.append(tuple(lclu))
    trace_wss.append(ecswss(lclu))
    #
    while flag_continue:
        #
        if itercounter >= kset.iterations:
            warnings.append("Iteration limit reached.")
            break
        #
        itercounter += 1
        #
        flag_continue = False
        #
        if kset.doshuffle:
            random.shuffle(units)
        else:
            pass
        #
        for i in units:
            flag_moved = False
            oldvalue = lclu[i]
            lwss = ecswss(lclu)
            if kset.doshuffle:
                random.shuffle(clulst)
            else:
                pass
            #
            for newvalue in clulst:
                if lclu[i] == newvalue:
                    continue
                else:
                    lclu[i] = newvalue
                newlwss = ecswss(lclu)
                if newlwss < lwss:
                    flag_moved = True
                    flag_continue = True
                    lwss = newlwss
                    print(newlwss)
                    if kset.trace:
                        trace_clu.append(tuple(lclu))
                        trace_wss.append(ecswss(lclu))
                    else:
                        pass
                    break
                else:
                    pass
            if flag_moved:
                break
            else:
                lclu[i] = oldvalue
    #
    # Logging trace info
    if kset.trace:
        for etr in range(len(trace_wss)):
            logme(trace_clu[etr], "clu")
            logme(trace_wss[etr], "wss")
    return(lclu, lwss, trace_clu, trace_wss, itercounter, warnings)


def randominit():
    lclu = [random.randint(0,(kset.k-1)) for i in range(data.dlen)]
    return(lclu)







