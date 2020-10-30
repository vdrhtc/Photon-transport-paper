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
            for plot in "13":
                with open(f"fig2{panel}{plot}.pkl", "rb") as f:
                    trans_data.append(pickle.load(f))

        with open("chain_fit.pkl", "rb") as f:
            model_curves = pickle.load(f)

        with open(f"CKTT-I.pkl", "rb") as f:
            cktt1 = pickle.load(f)
        with open(f"CKTT-III.pkl", "rb") as f:
            cktt2 = pickle.load(f)
        with open("cktt_fit_I.pkl", "rb") as f:
            cktt_fit_elevels_I = pickle.load(f)

        with open("cktt_fit_III.pkl", "rb") as f:
            cktt_fit_elevels_III = pickle.load(f)

        fig = plt.figure()
        spec = fig.add_gridspec(ncols=300, nrows=320)
        gridspec_cols = [slice(0,146), slice(154, 300)]
        dt_gridspec_rows = [slice(0,80), slice(85, 165)]
        ck_gridspec_rows = [slice(190, 320), slice(190, 320)]

        powers = [-70, -50]

        for col in [0,1]:
            for row in [0,1]:
                ax = fig.add_subplot(spec[dt_gridspec_rows[row], gridspec_cols[col]])
                data = trans_data[col*2+row]
                Ystep = diff(data["Frequency [Hz]"])[0]
                Y = concatenate((data["Frequency [Hz]"] - Ystep/2, [data["Frequency [Hz]"][-1]+Ystep/2]))

                m = ax.pcolormesh(data["Voltage [V]"], Y/1e9,
                              20*log10(abs(data["data"].T)), rasterized = True,
                              cmap="RdBu_r", vmin=-60, vmax=-20)

                if row == 0 and col == 0:

                    plt.text(-0.3, 1.1, "(a)", fontdict={"name": "STIX"}, fontsize=17,
                             transform=ax.transAxes)
                    for idx in range(1, 6):
                        ax.plot(data["Voltage [V]"][::10],
                                 model_curves[0][:, idx], "-", lw=0.5,
                                 color = "black", label = "Model")
                if row == 0 and col == 1:
                    for idx in range(1, 6):
                        ax.plot(data["Voltage [V]"][::10],
                                 model_curves[2][:, idx],
                                 "-", color = "black", lw=.5,
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
                    ax.set_ylabel(r"$\omega_d/2\pi$ (GHz)", position = (0,1))

                if col == 1:
                    plt.text(1.025, .65, "%d dBm"%powers[row], fontsize=10,
                             rotation = -90, transform=ax.transAxes)

                ax.set_ylim(3.95, 4.15)

        ax = fig.add_subplot(spec[ck_gridspec_rows[0], gridspec_cols[0]])
        ax.pcolormesh(cktt1["Voltage [V]"], cktt1["Frequency [Hz]"] / 1e9,
                          (abs(cktt1["data"].T)), rasterized=True,
                          cmap="RdBu_r")

        ax.set_xlabel("Flux bias 1 (a.u.)")
        ax.set_ylabel("CKS frequency (GHz)")

        for level_id in range(1, 6):
            ax.plot(cktt1["Voltage [V]"][::5],
                    cktt_fit_elevels_I[:, level_id] - cktt_fit_elevels_I[:, 0],
                    ls=(0, (2, 0)), dash_capstyle="round",
                    color="black", lw=.5)
        for level_id in range(6, 11):
            ax.plot(cktt1["Voltage [V]"][::5],
                    cktt_fit_elevels_I[:, level_id] -
                    cktt_fit_elevels_I[:, 0] - cktt_fit_elevels_I[:, 3],
                    ls=(0, (2, 5)), dash_capstyle="round",
                    color="gray", lw=1)
        for level_id in range(11, 21):
            ax.plot(cktt1["Voltage [V]"][::5],
                    cktt_fit_elevels_I[:, level_id] -
                    cktt_fit_elevels_I[:, 0] - cktt_fit_elevels_I[:, 3],
                    ls=(0, (2, 5)), dash_capstyle="round",
                    color="gray", lw=1)
        ax.set_ylim(3.8, 4.2)

        plt.text(-0.325, 1.05, "(b)", fontdict={"name": "STIX"}, fontsize=17,
                 transform=ax.transAxes)

        ax = fig.add_subplot(spec[ck_gridspec_rows[1], gridspec_cols[1]])
        ax.pcolormesh(cktt2["Voltage [V]"], cktt2["Frequency [Hz]"] / 1e9,
                          (abs(cktt2["data"].T)), rasterized=True,
                          cmap="RdBu_r")

        ax.set_xlabel("Flux bias 3 (a.u.)")
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
                    ls=(0, (2, 5)), dash_capstyle="round",
                    color="gray", lw=1)
        for level_id in range(11, 21):
            ax.plot(cktt2["Voltage [V]"][::5],
                    cktt_fit_elevels_III[:, level_id] -
                    cktt_fit_elevels_III[:, 0] - cktt_fit_elevels_III[:, 3],
                    ls=(0, (2, 5)), dash_capstyle="round",
                    color="gray", lw=1)
        ax.set_ylim(3.8, 4.2)

        plt.gcf().set_size_inches(5, 6)
        # plt.tight_layout()

        cbaxes1 = fig.add_axes([0.15, .93, 0.5, .01])
        cb = plt.colorbar(m, cax = cbaxes1, orientation="horizontal")
        cb.ax.set_title(r"$|S_{21}|^2$ (dB)", position=(1.3, -3.5))


        plt.savefig("../fig2.pdf", bbox_inches="tight")

Fig2()