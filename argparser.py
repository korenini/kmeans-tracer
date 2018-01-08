import argparse


# Parse command line arguments; they override settings in settings.py

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--data', dest='cmd_data_files', type=str,
                    help='File containing the data.',
                    required=False)
parser.add_argument('-t', '--type', dest='cmd_data_type', type=str,
                    help='Data type, raw or distances',
                    required=False)
parser.add_argument('-k', '--clusters', dest='cmd_clusters', type=int,
                    help='The number of clusters.', required=False)
parser.add_argument('-m', '--min-cluster-size', dest='cmd_spcs', type=int,
                    help='Smallest permitted cluster size.', required=False)
parser.add_argument('-i', '--iterations', dest='cmd_iterations', type=int,
                    help='The permitted number of iterations.')
parser.add_argument('-a', '--algorithm', dest='cmd_algo', type=str,
                    help="Modified Lloyd's or modified Hartigan-Wong k-means algorithm.",
                    required=False)
parser.add_argument('-o', '--output-file', dest='cmd_outfile', type=str,
                    help='File into which the results are written.',
                    required=False)


parsed = parser.parse_args()
