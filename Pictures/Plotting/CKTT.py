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
        with open("cktt_fit_I.pkl", "rb") as f:
            cktt_fit_elevels_I = pickle.load(f)

        with open("cktt_fit_III.pkl", "rb") as f:
            cktt_fit_elevels_III = pickle.load(f)

        fig = plt.figure()
        spec = fig.add_gridspec(ncols=2, nrows=1)
        ax = fig.add_subplot(spec[0, 0])
        m = ax.pcolormesh(cktt1["Voltage [V]"], cktt1["Frequency [Hz]"] / 1e9,
                          (abs(cktt1["data"].T)), rasterized=True,
                          cmap="RdBu_r")

        ax.set_xlabel("Flux bias 1 (V)")
        ax.set_ylabel("Frequency (GHz)")

        for level_id in range(1, 6):
            ax.plot(cktt1["Voltage [V]"][::5],
                    cktt_fit_elevels_I[:, level_id] - cktt_fit_elevels_I[:, 0],
                    ls=(0, (2, 0)), dash_capstyle="round",
                    color="black", lw=.5)
        for level_id in range(6, 11):
            ax.plot(cktt1["Voltage [V]"][::5],
                    cktt_fit_elevels_I[:, level_id] -
                    cktt_fit_elevels_I[:, 0] - cktt_fit_elevels_I[:, 3],
                    ls=(0, (2, 5)), dash_capstyle = "round",
                    color="gray", lw=1)
        for level_id in range(11, 21):
            ax.plot(cktt1["Voltage [V]"][::5],
                    cktt_fit_elevels_I[:, level_id] -
                    cktt_fit_elevels_I[:, 0] - cktt_fit_elevels_I[:, 3],
                    ls=(0, (2, 5)), dash_capstyle = "round",
                    color="gray", lw=1)
        ax.set_ylim(3.8, 4.2)

        plt.text(-0.35, 1, "(b)", fontdict={"name": "STIX"}, fontsize=17,
                 transform=ax.transAxes)

        ax = fig.add_subplot(spec[0, 1])
        m = ax.pcolormesh(cktt2["Voltage [V]"], cktt2["Frequency [Hz]"] / 1e9,
                          (abs(cktt2["data"].T)), rasterized=True,
                          cmap="RdBu_r")

        ax.set_xlabel("Flux bias 3 (V)")
        ax.set_yticklabels([])

        for level_id in range(1, 6):
            ax.plot(cktt2["Voltage [V]"][::5],
                    cktt_fit_elevels_III[:, level_id] - cktt_fit_elevels_III[:, 0],
                    ls='-', dash_capstyle="round",
                    color="black", lw=.5)
        for level_id in range(6, 11):
            ax.plot(cktt2["Voltage [V]"][::5],
                    cktt_fit_elevels_III[:, level_id] -
                    cktt_fit_elevels_III[:, 0] - cktt_fit_elevels_III[:, 3],
                    ls=(0, (2, 5)), dash_capstyle = "round",
                    color="gray", lw=1)
        for level_id in range(11, 21):
            ax.plot(cktt2["Voltage [V]"][::5],
                    cktt_fit_elevels_III[:, level_id] -
                    cktt_fit_elevels_III[:, 0] - cktt_fit_elevels_III[:, 3],
                    ls=(0, (2, 5)), dash_capstyle = "round",
                    color="gray", lw=1)
        ax.set_ylim(3.8, 4.2)

        plt.gcf().set_size_inches(5, 3)
        plt.tight_layout()

        plt.savefig("../cktt.pdf", bbox_inches="tight")


CKTT()
