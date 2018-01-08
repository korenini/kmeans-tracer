import sys
from os import path
from argparser import parsed

import settings as kset


# CMD overrides settings in settings.py

if parsed.cmd_clusters:
    k = int(parsed.cmd_clusters)
else:
    k = int(kset.k)

if parsed.cmd_spcs:
    spcs = int(parsed.cmd_spcs)
else:
    spcs = int(kset.spcs)

if parsed.cmd_iterations:
    iterations = int(parsed.cmd_iterations)
else:
    iterations = int(kset.iterations)

if parsed.cmd_data_files:
    data_file = parsed.cmd_data_files
else:
    data_file = kset.data_files

if parsed.cmd_data_type:
    data_type = parsed.cmd_data_type
else:
    data_type = kset.data_type

if parsed.cmd_algo:
    algo = parsed.cmd_algo
else:
    algo = kset.algorithm

if parsed.cmd_outfile:
    outfile = parsed.cmd_outfile
else:
    outfile = kset.outfile

# To-do: a more thorough sanitization of input

errors = []

if k > 1:
    kset.k = k
else:
    errors.append("There should be at least two clusters.")

if spcs > 0:
    kset.spcs = spcs

if iterations > 0:
    kset.iterations = iterations

if path.exists(data_file):
    kset.data_files = data_file
else:
    errors.append("Data file %s not found." % data_file)

if not(isinstance(data_type, str)):
    errors.append("The specified data type must be a string.")

if data_type.lower()=='raw' or data_type.lower()=='distances':
    kset.data_type = data_type.lower()
else:
    errors.append("Data type is not understood.")

if not(isinstance(algo, str)):
    errors.append("The specified algorithm type must be a string.")

if algo.lower()=='lloyd' or algo.lower()=='hartigan-wong':
    if algo.lower()=='lloyd':
        kset.algo = 'll'
    if algo.lower()=='hartigan-wong':
        kset.algo = 'hw'
else:
    errors.append("The requested k-means algorithm is not understood.")


# OK | errors
if errors:
    for err in errors:
        print(err)
    sys.exit(1)


