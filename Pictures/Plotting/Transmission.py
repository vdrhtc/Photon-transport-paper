from numpy import *
import pickle
import matplotlib
from matplotlib import ticker, colorbar as clb, patches
import matplotlib.patheffects as PathEffects

matplotlib.use('Qt5Agg')

from matplotlib import pyplot as plt

class Fig2:

    def __init__(self):

        trans_data = []
        for panel in "ab":
            for plot in "123":
                with open(f"fig2{panel}{plot}.pkl", "rb") as f:
                    trans_data.append(pickle.load(f))

        with open("chain_fit.pkl", "rb") as f:
            model_curves = pickle.load(f)

        fig = plt.figure()
        spec = fig.add_gridspec(ncols=2, nrows=3)

        for col in [0,1]:
            for row in [0,1,2]:
                ax = fig.add_subplot(spec[row, col])
                data = trans_data[col*3+row]
                m = ax.pcolormesh(data["Voltage [V]"], data["Frequency [Hz]"]/1e9,
                              20*log10(abs(data["data"].T)), rasterized = True,
                              cmap="RdBu_r", vmin=-60, vmax=-20)

                if row == 0 and col == 0:
                    for idx in range(1, 6):
                        ax.plot(data["Voltage [V]"][::10],
                                 model_curves[0][:, idx], ":",
                                 color = "black", label = "Model")
                if row == 0 and col == 1:
                    for idx in range(1, 6):
                        ax.plot(data["Voltage [V]"][::10],
                                 model_curves[2][:, idx],
                                 ":", color = "black",
                                 label = None if idx > 1 else "Model")
                        # ax.legend()

                if row < 2:
                    ax.set_xticklabels([])
                if col == 1:
                    ax.set_yticklabels([])

                if col == 0 and row == 2:
                    ax.set_xlabel("Flux bias 1 (V)")

                if col == 1 and row == 2:
                    ax.set_xlabel("Flux bias 3 (V)")

                if col == 0 and row == 1:
                    ax.set_ylabel(r"$\omega_d/2\pi$ (GHz)")

                ax.set_ylim(3.95, 4.15)

        plt.gcf().set_size_inches(5, 5)
        plt.tight_layout()

        cbaxes1 = fig.add_axes([0.2, 1.025, 0.5, .01])
        cb = plt.colorbar(m, cax = cbaxes1, orientation="horizontal")
        cb.ax.set_title(r"$|S_{21}|^2$ (dB)", position=(1.3, -3.5))


        plt.savefig("../fig2.pdf", bbox_inches="tight")

Fig2()