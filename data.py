import sys
import numpy as np
import itertools
import settings as kset


def data_sane(data):
    errors = []
    def value_ok(onecell):
        dstatus = True
        if not isinstance(onecell, float):
            dstatus = False
        if np.isnan(onecell):
            dstatus = False
        return(dstatus)
    #
    if kset.data_type == 'raw':
        for ra in range(data.shape[0]):
            for co in range(data.shape[1]):
                if not value_ok(data[ra,co]):
                    errors.append("Data not formatted properly.")
                    return(False, errors)
        return(True, errors)
    elif kset.data_type == 'distances':
        for ra in range(data.shape[0]):
            for co in range(data.shape[1]):
                if ra==co:
                    continue
                if not value_ok(data[ra, co]):
                    errors.append("Data not formatted properly.")
                    return(False, errors)
        return(True, errors)
    else:
        errors.append("Data type is incorrect. Should be either 'raw' or 'distances'.")
    return(False, errors)


if kset.data_type == 'raw':
    # Read the data from file
    data = np.genfromtxt(kset.data_files, delimiter=kset.delimiter)
    # Check data shape
    if data.shape.__len__() == 2:
        pass
    elif data.shape.__len__() == 1:
        data.shape = (data.size, 1)
    # Data length
    dlen = data.__len__()
    # Data type is _not_ unreadable garbage
    ds, errorsds = data_sane(data)
    if not ds:
        for err in errorsds:
            print(err)
        sys.exit(1)
    # Euclidean distances
    dist_euclid = np.zeros([dlen, dlen], dtype=np.float64)
    for i in itertools.combinations(range(dlen), 2):
        dist_euclid[i[0],i[1]] = dist_euclid[i[1],i[0]] = ((data[i[0],] - data[i[1],])**2).sum()
    # In this case distances are Euclidean Squared distances
    dist = dist_euclid

if kset.data_type == 'distances':
    dist = np.genfromtxt(kset.data_files, delimiter=kset.delimiter)
    dlen = dist.__len__()
    # Data type is _not_ unreadable garbage
    ds, errorsds = data_sane(data)
    if not ds:
        for err in errorsds:
            print(err)
        sys.exit(1)

