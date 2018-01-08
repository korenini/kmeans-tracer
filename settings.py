"""
Settings can be changed here but command line arguments override them
When changing settings, don't change variable type. String must be a string
float must be a float etc.
Settings are prefilled with sesible defaults. Cjange them at will if you
know what you are doing.
"""

# Either a modified variant of Lloyd's k-means or a modified Hartigan-Wong
# k-means algorithm can be selected
#algorithm = 'Lloyd'
algorithm = 'Hartigan-Wong'

# Data files
data_files = 'iris.csv'

# Input data can be either 'raw' or 'distances'.
# Hartigan-Wong algorithm needs 'raw' data.
#data_type = 'distances'
data_type = 'raw'

# Delimiter used in data files, e.g. ',' in case of csv.
delimiter = ','

# Number of clusters
k = 3

# Smallest permitted cluster size (spcs)
spcs = 2

# The permitted number of iterations of the algorithm
iterations = 300

# Output file
outfile = 'results.txt'

# Randomize the order in which local neighborhood is inspected
doshuffle = True

# Provide information on the intermediate steps of the progress of the algorithm.
trace = True


# Initial centers
# How many times should be initial centers initialized before
# giving up in case empty clusters are found.
hw_initialize_centers = 10

# HW constant
hw_tol = float(1.00)


# Allowed number of iterations in Hartigan-Wong algorithm
# This is a safety measure for cases when clustering doesn't converge.
# In case this limit is reached a warning is issued.
hw_iter_max = 20

# Allowed number of iterations in tracing
trace_iter_max = 50

# Allowed number iterations in quick-transfer stage of Hartigan-Wong procedure
qtran_max = 10

# Logging

# Write results into a single file.
# If this is set to False several output files will be written,
# extensions will be appended to the name of the output file:
# _wss: within sum of squares
# _clu: clusterings
# _cen: cluster centers
#logsingle = True
logsingle = False

