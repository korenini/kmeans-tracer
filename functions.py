import sys
import data
import numpy as np
import platform
import settings as kset

myos = platform.system()

if myos == "Linux":
    eol = "\n"
elif myos == "Windows":
    eol == "\r\n"
elif myos == "Darwin":
    eol = "\r\n"
else:
    eol = "\n"

def ecswss(cluster_members):
    sum_dist = 0
    # Find cluster member in index notation
    for clm in range(max(cluster_members)+1):
        # Indexes for cluster members for a cluster
        members = [i for i, x in enumerate(cluster_members) if x == clm]
        # Create submatrice of distance matrix
        # dmsub:distance matrix subset
        sum_dist += (data.dist[np.ix_(members, members)].sum())/(len(members)*float(2.0))
    return(sum_dist)


def cluster_sizes(clustering):
    # Dictionary of ic1 cluster sizes
    # ... dobim dictionary s key k-name, ki ima value k-size
    cs = list(set(clustering))
    csd = {}
    for ks in cs:
        csd[ks] = clustering.count(ks)
    return(csd)



##        WSS
##------------------------------------------------------------------------------
# Error, ce je kaksen cluster prazen, crednost ic1 pa je vec kot je
# ... stevilo clustrov. npr. k=3, len(set(ic1))=2, ic1=[0,0,2,2]
# ... poskusa pisat v wss[2], to pa je out of range.
# def withinss(crit_data, centers, ic1):

def withinss(crdata, centers, k, ic1):
    #k = len(set(ic1))
    wss = np.zeros(k)
    #
    for un, le in enumerate(ic1):
        #tmp_dist = ( ((crit_data[un,:] - centers[le,:])**2).sum() ) ** 0.5
        tmp_dist = ( ((crdata[un,:] - centers[le,:])**2).sum() )
        wss[le] += tmp_dist
    return(wss)


def logsplit(outname, exten):
    if outname.find(".", 1):
        ona = outname.split('.')
        ona.insert(-1, exten)
        ona = '_'.join(ona[0: -2]) + '.'.join(ona[-2:])
    else:
        ona = outname + exten
    return(ona)


def logme(logdata, logtype):
    if isinstance(kset.outfile, str):
        pass
    else:
        print("Output file as specified in settings.py must be enclosed in parenthesis.")
        sys.exit(1)
    if kset.logsingle:
        outname = kset.outfile
    else:
        outname = logsplit(kset.outfile, '_'+logtype)

    with open(outname, "a") as f:
            f.write("%s %s" % (str(logdata), eol))




