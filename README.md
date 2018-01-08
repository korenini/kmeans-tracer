# k-means tracer

*k*-means tracer is a command line tool used to cluster the data into 
the specified number of non-overlapping clusters.
It currently implements two *k*-means algorithms: the traditional Lloyd's 
k-means and a modified version of Hartigan-Wong's k-means algorithm.
One of the main benefits of this software is that it provides 
intermediate results of the progress of the algorithm: clusterings, 
cluster centers and within sum of squares (where applicable).
This can be used either in more advanced hybrid clustering algorithms 
(work in progress) or it can be used for demonstration and 
educational purposes.

*k*-means tracer provides additional functionality like
avoiding empty clusters, randomization of the path from initial 
to the final clustering solution even when starting from the same 
initial clustering. This can be used as an additional measure
to avoid local extremes when dealing with troubling data. 
If you find it useful, *k*-means tracer can be forced into sub-optimal 
traversal through the clustering neighborhood structure. 

## Usage

### Data
*k*-means tracer expects data stored in a plaintext file where 
CSV is the default format. It expects that observations are listed in
rows and observed variables are specified in columns, without row 
and column headings. It is also possible to supply a distance matrix,
but in this case, Hartigan-Wong's *k*-means cannot be performed since
this algorithm relies on the calculation of cluster centers.

### Parameters
Parameters can be specified either as command line parameters or
through editing the settings.py file. Command line parameters have priority
over those specified in settings.py.

### Results
*k*-means tracer returns intermediate and the final wss as well as 
a single vector containing the final clustering. When trace option is enabled
it provides all intermediate clusterings and accompanying wss in the 
specified file.

### Example
The well-known iris data set is used in this example.
The following command clusters the data into three clusters. Please note that 
commandline arguments override those written in settings.py.

```python3 kmtracer.py -k 3 -d iris.csv -a Hartigan-Wong```

Iris dataset:
Fisher R.A. (1936). 
UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: 
University of California, School of Information and Computer Science. 

### Help
```python3 kmtracer.py --help```

