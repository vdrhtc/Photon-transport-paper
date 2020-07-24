from numpy import *
import pickle
import matplotlib
from matplotlib import ticker, colorbar as clb, patches
import matplotlib.patheffects as PathEffects

matplotlib.use('Qt5Agg')

from matplotlib import pyplot as plt

class CKTT:

    def __init__(self):

        with open(f"CKTT-I.pkl", "rb") as f:
            cktt1 = pickle.load(f)
        with open(f"CKTT-III.pkl", "rb") as f:
            cktt2 = pickle.load(f)

        fig = plt.figure()
        spec = fig.add_gridspec(ncols=2, nrows=1)
        ax = fig.add_subplot(spec[0,0])
        m = ax.pcolormesh(cktt1["Voltage [V]"], cktt1["Frequency [Hz]"]/1e9,
                      (abs(cktt1["data"].T)), rasterized = True,
                      cmap="RdBu_r")

        ax.set_xlabel("Flux bias 1 (V)")
        ax.set_ylabel("Frequency (GHz)")

        ax = fig.add_subplot(spec[0, 1])
        m = ax.pcolormesh(cktt2["Voltage [V]"], cktt2["Frequency [Hz]"]/1e9,
                      (abs(cktt2["data"].T)), rasterized = True,
                      cmap="RdBu_r")

        ax.set_xlabel("Flux bias 3 (V)")
        ax.set_yticklabels([])
        plt.gcf().set_size_inches(5, 3)
        plt.tight_layout()

        plt.savefig("../cktt.pdf", bbox_inches="tight")

CKTT()