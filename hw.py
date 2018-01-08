import numpy as np
import random
from copy import deepcopy
import settings as kset
from functions import *
import data

hw_tol = kset.hw_tol
k = kset.k


def initial_centers():
    #
    crdata = data.data
    k = kset.k
    centers = np.zeros( (k, crdata.shape[1]) )
    for i in range(k):
        for j in range(crdata.shape[1]):
            centers[i, j] = random.uniform(crdata[:, j].min(), crdata[:, j].max())
    return(centers)


def find_closest(centers):
    crdata = data.data
    # Initialize empty lists
    ic1 = []
    ic2 = []
    di1 = []
    di2 = []
    #
    if centers.shape.__len__() == 2:
        pass
    elif centers.shape.__len__() == 1:
        centers.shape = (centers.size,1)
    else:
        raise ValueError('Data are not propperly formated.')
    #
    for i in range(crdata.shape[0]):   # for each unit
        min_dist_1 = float('inf')
        min_dist_2 = float('inf')
        tmp_center_1 = None
        tmp_center_2 = None
        #
        for cc in range(centers.shape[0]):
            # Calculate the distance
            tmp_dist = ( ((crdata[i,:] - centers[cc,:])**2).sum() )
            #
            if cc == 0:
                min_dist_1 = tmp_dist
                tmp_center_1 = cc
                # no need to go any further here
                continue
            else:
                pass
            #
            if tmp_dist < min_dist_2:
                if tmp_dist <= min_dist_1:
                    min_dist_1, min_dist_2 = tmp_dist, min_dist_1
                    tmp_center_1, tmp_center_2 = cc, tmp_center_1
                else:
                    min_dist_2 = tmp_dist
                    tmp_center_2 = cc
            else:
                pass
        ic1.append(tmp_center_1)
        di1.append(min_dist_1)
        ic2.append(tmp_center_2)
        di2.append(min_dist_2)
    #
    return(ic1, ic2, di1, di2)


def update_centers(centers, ic1, ucl=(), csd={}):
    #
    crdata = data.data
    k = kset.k
    # Cluster sizes
    if csd:
        pass
    else:
        csd = cluster_sizes(ic1)
        if len(csd) != k:
            raise ValueError('At least one cluster is empty.')
    #
    # ucl list (ucl: update clusters)
    if ucl:
        pass
    else:
        ucl=range(k)
    #
    invun = []
    for eu, uncm in enumerate(ic1):
        if uncm in ucl:
            invun.append(eu)
    #
    for i in ucl:
        centers[i,:] = [0] * crdata.shape[1]
    #
    for i in invun:
        for j in range(crdata.shape[1]):
            centers[ic1[i],j] += crdata[i,j]
    for x in ucl:
        centers[x,:] = centers[x,:]/float(csd[x])
    #
    if centers.shape.__len__() == 2:
        pass
    elif centers.shape.__len__() == 1:
        centers.shape = (centers.size,1)
    else:
        raise ValueError('Data are not properly formatted')
    return(centers)



def try_move(centers, liveset, ic1, ic2, di1, di2, flag_hw_optimal, **kwargs):
    #
    hwc = kset.hw_tol
    k = kset.k
    crdata = data.data
    trace = kset.trace
    qtran_counter = 0
    optlive = []
    trace_clu = []
    trace_cen = []
    trace_wss = []
    flag_transfer = False
    #
    print("Start wss: %s" % withinss(crdata, centers, k, ic1).sum())
    #
    csd = cluster_sizes(ic1)
    #
    if len(csd) != k:
        raise ValueError("Empty cluster found")
    #
    units = list(range(crdata.shape[0]))
    random.shuffle(units)
    #
    for unit in tuple(units):
        #
        cm = ic1[unit]
        cs1 = csd[cm]
        #
        if cm in liveset or cm in optlive:
            d1 = ( ((crdata[unit,:] - centers[ic1[unit],:])**2 ).sum() )
        else:
            d1 = di1[unit]
        #
        r1 = (cs1 / (cs1 - hwc)) * d1
        #
        mdiff_r = float('inf')
        mdiff_d = float('inf')
        mdiff_idx = None
        #
        for c in list(range(k)):
            if c == cm:
                continue
            else:
                pass
            #
            csk = csd[c]
            #
            d2 = ( ((crdata[unit,:] - centers[c,:])**2).sum() )
            r2 = (csk / (csk + hwc)) * d2
            #
            if r2 < mdiff_r:
                mdiff_r = r2
                mdiff_d = d2
                mdiff_idx = c
            else:
                pass
        #
        if mdiff_r < r1:
            ic2b = ic2[unit]
            di2b = di2[unit]
            ic1[unit], ic2[unit] = mdiff_idx, ic1[unit]
            di1[unit], di2[unit] = mdiff_d, di1[unit]
            #
            csd = cluster_sizes(ic1)
            #
            if min(csd.values()) < kset.spcs:
                ic1[unit], ic2[unit] = ic2[unit], ic2b
                di1[unit], di2[unit] = di2[unit], di2b
                flag_transfer = False
                # Issue warning
                print("""Transfer of unit %s from cluster %s to %s 
                         results in a smaller than permitted cluster.
                         Canceling transfer.""" % (unit, cm, mdiff_idx))
                continue
            else:
                flag_transfer = True
                pass
            #
            centers = update_centers(centers, ic1, ucl=(cm, mdiff_idx), csd=csd)
            #
            # Save trace - save current clustering & centers
            if trace and flag_transfer:
                trace_clu.append(tuple(ic1))
                trace_cen.append(deepcopy(centers))
                trace_wss.append(ecswss(ic1))
                flag_transfer = False
            else:
                pass
            #
            mv_wss = ecswss(ic1)
            cm = ic1[unit]
            #
            for i in (cm, mdiff_idx):
                if i not in optlive:
                    optlive.append(i)
            #
            print("OPTRAN WSS: %s" % mv_wss)
        else:
            di1[unit], di2[unit] = d1, mdiff_d
    liveset, optlive = optlive, []
    #
    if liveset:
        pass
    else:
        flag_hw_optimal = True
        wss_best = withinss(crdata, centers, k, ic1).sum()
        print("Convergence in optimal transfer reached.")
        return (ic1, ic2, di1, di2, centers, liveset, wss_best, flag_hw_optimal, trace_clu, trace_cen, trace_wss)
    #
    qtlive = []
    #
    while liveset:
        #
        if qtran_counter >= kset.qtran_max:
            print("This message must be removed.")
            print("""WARNING: No convergence reached in QTRAN after %s iterations.""" % qtran_counter)
            break
        else:
            pass
        #
        qtran_counter += 1
        #
        ilist = list(range(crdata.shape[0]))
        random.shuffle(ilist)
        #
        for unit in ilist:
            #
            cs1, cs2 = csd[ic1[unit]], csd[ic2[unit]]
            #
            if cs1 < kset.spcs:
                # Issue warning
                print("""QTRAN: Transfer of unit %s from cluster %s to %s 
                         results in a smaller than permitted cluster.
                         Canceling transfer.""" % (unit, ic1[unit], ic2[unit]))
                continue
            else:
                pass
            #
            if ic1[unit] in liveset or ic1[unit] in qtlive:
                d1 = ( ((crdata[unit,:] - centers[ic1[unit],:])**2).sum() )
                di1[unit] = d1
            else:
                d1 = di1[unit]
            r1 = (cs1 / (cs1 - hwc)) * d1
            #
            if ic2[unit] in liveset or ic2[unit] in qtlive:
                d2 = ( ((crdata[unit,:] - centers[ic2[unit],:])**2).sum() )
                di2[unit] = d2
            else:
                d2 = di2[unit]
            #
            r2 = (cs2 / (cs2 + hwc)) * d2
            #
            if r2 < r1:
                ic1[unit], ic2[unit] = ic2[unit], ic1[unit]
                csd = cluster_sizes(ic1)
                cs1 = csd[ic1[unit]]
                if cs1 < kset.spcs:
                    ic1[unit], ic2[unit] = ic2[unit], ic1[unit]
                    csd = cluster_sizes(ic1)
                    # Issue warning
                    print("""QTRAN: Transfer of unit %s from cluster %s to %s 
                             results in a smaller than permitted cluster.
                             Canceling transfer.""" % (unit, ic1[unit], ic2[unit]))
                    flag_transfer = False
                    continue
                else:
                    flag_transfer = True
                    pass
                centers = update_centers(centers, ic1, ucl=(ic1[unit], ic2[unit]), csd=csd)
                # Save trace - save current clustering & centers
                if trace and flag_transfer:
                    trace_clu.append(tuple(ic1))
                    trace_cen.append(deepcopy(centers))
                    mv_wss = ecswss(ic1)
                    trace_wss.append(mv_wss)
                    flag_transfer = False
                else:
                    pass
                #
                for i in (ic1[unit], ic2[unit]):
                    if i not in qtlive:
                        qtlive.append(i)
                #
                print("QTRAN WSS: %s" % withinss(crdata, centers, k, ic1).sum())
            else:
                pass
                #
        liveset = qtlive
        qtlive = []
    #
    wss_best = withinss(crdata, centers, k, ic1).sum()
    #
    flag_hw_optimal = False
    return (ic1, ic2, di1, di2, centers, liveset, wss_best, flag_hw_optimal, trace_clu, trace_cen, tuple(trace_wss))


def hwkm(k):
    #
    centers, liveset, ic1, ic2, di1, di2, flag_hw_optimal = [], [], [], [], [], [], False
    trace_clu, trace_cen, trace_wss, wss_best = [], [], [], float('inf')
    #
    itercounter = 0
    init_counter = 0
    #
    hw_wss_optimal = float('inf')
    hw_clu_optimal = []
    #
    flag_nonconvergence = False
    #
    for try_initc in range(kset.hw_initialize_centers):
        init_counter += 1
        centers = initial_centers()
        ic1, ic2, di1, di2 = find_closest(centers)
        try:
            centers = update_centers(centers, ic1, ucl=range(k), csd={})
        except ValueError:
            flag_nonconvergence = True
            print("An empty cluster found. Reinitializing. Attempt %s" % init_counter)
            print("")
            continue
        csd = cluster_sizes(ic1)
        if ( min(csd.values()) > kset.spcs ) and ( len(csd)==k ):
            flag_nonconvergence = False
            print("Initial centers selected.")
            break
        else:
            pass
    #
    if flag_nonconvergence:
        print(""" Exiting after %s attempts to find initial clustering
                without empty clusters. Try to raise the hw_initialize_centers
                variable in settings or chose a different k.""" % init_counter)
        return()
    else:
        pass
    #
    liveset = list(range(k))
    #
    while not flag_hw_optimal:
        itercounter += 1
        print("Iteration no.: %s" % itercounter)
        ic1, ic2, di1, di2, centers, liveset, wss_best, flag_hw_optimal, \
        trace_clu, trace_cen, trace_wss = try_move(centers, liveset, ic1, \
                                                   ic2, di1, di2, flag_hw_optimal)
        # Logging trace info
        for etr in range(len(trace_wss)):
            logme(trace_clu[etr], "clu")
            logme(trace_cen[etr], "cen")
            logme(trace_wss[etr], "wss")
        #
        if itercounter >= kset.hw_iter_max:
            print("Convergence not reached in the allowed number of iterations.")
            break
    #
    print("Best WSS: %s" % wss_best)
    return(wss_best, ic1, ic2, di1, di2, centers, trace_clu, trace_cen, trace_wss, itercounter)


