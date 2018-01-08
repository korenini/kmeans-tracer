
import sys
from argparser import parsed
#from params import check_params
import params
import settings as kset
import hw
import lloyd


def main():

    if kset.algo=='ll':
        c, w, clu, wss, iter, warnings = lloyd.lkm(lloyd.randominit())
        print("")
        print("---------------------------------------------------------------")
        print("Data file: %s." % kset.data_files)
        print("k-means algorithm: %s." % "Lloyd's k-means")
        print("Clustering observations into %s clusters." % kset.k)
        print("Finished after %s iterations." % iter)
        print("WSS: %s" % w)
        print("The final clustering solution:")
        print(c)
        if warnings:
            if len(warnings) == 1:
                print("WARNING:")
            else:
                print("WARNINGS:")
            for w in warnings:
                print(w)
        print("")
        print("---------------------------------------------------------------")
        print("")
        print(kset.algo)
        if kset.trace:
            print("Tracing data are available in the specified output file(s).")
            print("")

    if kset.algo=='hw':
        wss_best, ic1, ic2, di1, di2, centers, trace_clu, trace_cen, trace_wss, iter = hw.hwkm(kset.k)
        print("")
        print("---------------------------------------------------------------")
        print("Data file: %s." % kset.data_files)
        print("k-means algorithm: %s" % "Hartigan-Wong's k-means")
        print("Clustering observations into %s clusters." % kset.k)
        print("Finished after %s iterations" % iter)
        print("WSS: %s" % wss_best)
        print("The final clustering solution:")
        print(ic1)
        print("")
        print("---------------------------------------------------------------")
        print("")
        if kset.trace:
            print("Tracing data are available in the specified output file(s).")
            print("")


if __name__ == "__main__":

    # Check Python version. Must be Python 3!
    if (sys.version_info > (3, 0)):
        pass
    else:
        print("Please use Python version 3 to run this program.")
        sys.exit(1)

    parametri = params

    main()
