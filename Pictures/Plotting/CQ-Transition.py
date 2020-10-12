from matplotlib.ticker import MaxNLocator
from numpy import *
import pickle
import matplotlib
from matplotlib import ticker, colorbar as clb, patches, gridspec, patches
import matplotlib.patheffects as PathEffects

matplotlib.use('Qt5Agg')

from matplotlib import pyplot as plt


class Fig3:

    # see transmission peaks fitting for the magic constants

    def __init__(self):

        with open("transmission_peaks.pkl", "rb") as f:
            exp_freqs, trans_data, fit_data = pickle.load(f)

        with open("fig3a.pkl", "rb") as f:
            exp_data = pickle.load(f)

        with open("fig3b.pkl", "rb") as f:
            sim_data = pickle.load(f)

        with open("chain_spectrum.pkl", "rb") as f:
            evals = pickle.load(f)

        fig = plt.figure()
        meta_spec = fig.add_gridspec(ncols=4, nrows=1, wspace=.5)

        spec = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=meta_spec[0, 0:3])
        oneDmetaspec = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=spec[0, 0:1])

        # Plot the transmission peaks in the linear regime
        ax = fig.add_subplot(oneDmetaspec[0, 0])
        ax.plot(real(trans_data), exp_freqs, ",", color="gray", alpha=0.3)
        ax.plot(real(fit_data), exp_freqs, "-", color="black", lw=1)

        ax.yaxis.set_major_locator(MaxNLocator(5))
        ax.set_ylabel("VNA frequency (GHz)")
        ax.set_xlabel("Re $S_{21}$")
        ax.set_ylim(3.8, 4)
        ax.set_title("A - A", position = (1.1,1))
        plt.text(-.9, 1.05, "(a)", fontdict={"name": "STIX"}, fontsize=17,
                 transform=ax.transAxes)

        ax = fig.add_subplot(oneDmetaspec[0, 1])
        ax.plot(imag(trans_data), exp_freqs, ",", color="gray", alpha=0.3)
        ax.plot(imag(fit_data), exp_freqs, "-", color="black", lw=1)
        ax.yaxis.set_major_locator(MaxNLocator(5))
        ax.set_yticklabels([])
        ax.set_xlabel("Im $S_{21}$")
        ax.set_ylim(3.8, 4)

        # Plot the power scan theory and expetimental data
        exp_data["data"] *= exp(2j * pi * 50.5e-9 * exp_data["Frequency [Hz]"] + 0.7j * pi)
        ax = fig.add_subplot(spec[0, 1])
        X = (10 ** (exp_data["Power [dBm]"] / 10)) * 1000
        Y = exp_data["Frequency [Hz]"]
        mappable = ax.pcolormesh(X, Y / 1e9,
                                 10*log10(abs(exp_data["data"].T))+10,
                                 rasterized=True, cmap="RdBu_r")
        ax.set_xticklabels([])
        ax.set_xscale("log")
        ax.set_xlim((1 * 1e-3 / 2.1) ** 2 * 1e3, (100 * 1e-3 / 2.1) ** 2 * 1e3)
        ax.set_xlabel(r"VNA power (mW)")
        ax.set_yticklabels([])

        ax.annotate("A", xy=(.3e-3, 3.825), xytext=(.3e-3, 3.805), ha="left", fontsize=10,
                    arrowprops=dict(facecolor='black', width=.5, headwidth=3, headlength=3.5,
                                    shrink=0.05))
        ax.annotate("A", xy=(.3e-3, 3.975), xytext=(.3e-3, 3.99), ha="left", fontsize=10,
                    arrowprops=dict(facecolor='black', width=.5, headwidth=3, headlength=3.5,
                                    shrink=0.05))


        plt.text(-.2, 1.05, "(b)", fontdict={"name": "STIX"}, fontsize=17,
                 transform=ax.transAxes)

        ax = fig.add_subplot(spec[0, 2])
        X = (sim_data[0])
        Y = sim_data[1]
        mappable = ax.pcolormesh(X * 1e3, Y, 10*log10(abs(sim_data[2].T))/2,
                                 rasterized=True, cmap="RdBu_r", vmax = 0)
        ax.set_yticklabels([])
        ax.set_xscale("log")
        ax.set_xlabel(r"$\Omega$ (MHz)")


        cbaxes2 = fig.add_axes([0.4, .95, 0.15, .01])
        cb = plt.colorbar(mappable, ax=ax, cax=cbaxes2, orientation="horizontal")
        cb.ax.set_title(r"$|S_{21}|$ (dB)", position=(1.3, -4), fontsize=10)
        cb.ax.xaxis.set_major_locator(MaxNLocator(5))
        cb.ax.tick_params(axis='both', which='minor', labelsize=7)

        plt.text(1.05, 1.05, "(c)", fontdict={"name": "STIX"}, fontsize=17,
                 transform=ax.transAxes)

        X = [1.25]
        lw = 1
        ms = 3
        for E in evals[-1][1:6]:
            ax.plot(X, ones_like(X) * E, marker="_", color="C0", lw=lw, ms=ms)

        for E in evals[-1][6:11]:
            ax.plot(X, ones_like(X) * E / 2, marker="_", color="C1", lw=lw, ms=ms)

        X = [4]
        for E in evals[-1][11:21]:
            ax.plot(X, ones_like(X) * E / 2, marker="_", color="C2", lw=lw, ms=ms)

        X = [12.5]
        for E in evals[-1][26:56]:
            ax.plot(X, ones_like(X) * E / 3, marker="_", color="C4", lw=lw, ms=ms)

        X = [40]
        for E in evals[-1][61:126]:
            ax.plot(X, ones_like(X) * E / 4, marker="_", color="C5", lw=lw, ms=ms)
        ax.set_ylim(3.8, 4)


        ax.annotate("$E_1$", (1.35, evals[-1][1]+1e-3), (1.6, 3.84), arrowprops=dict(facecolor='black', width=.25, headwidth=3, headlength=3.5,
                                    shrink=0.0), fontsize = 10)

        ax.annotate("$E_{41}$", (11, evals[-1][46]/3), (5, evals[-1][46]/3), arrowprops=dict(facecolor='black', width=.25, headwidth=3, headlength=3.5,
                                    shrink=0.0), fontsize = 10)

        ax.annotate("$E_{119}$", (41, evals[-1][124]/4+1e-3), (50, evals[-1][124]/4+10e-3), arrowprops=dict(facecolor='black', width=.25, headwidth=3, headlength=3.5,
                                    shrink=0.0), fontsize = 10)

        ax.annotate("$E_{90}$", (41, evals[-1][95]/4+1e-3), (50, evals[-1][95]/4-10e-3), arrowprops=dict(facecolor='black', width=.25, headwidth=3, headlength=3.5,
                                    shrink=0.0), fontsize = 10)

        # ax.annotate("$E_{21}$", (3.9, evals[-1][46]/2-1e-3), (3.5, evals[-1][46]/2 - 15e-3),ha="right", arrowprops=dict(facecolor='black', width=.25, headwidth=3, headlength=3.5,
        #                             shrink=0.0), fontsize = 10)

        ##### Panel (c)

        eval_intervals = [
            slice(1, 6),
            slice(6, 21),
            slice(21, 56),
            slice(56 + 5, 126),
            # slice(126+5, 247)
        ]

        minizones = 0
        linewidth = .5
        spec = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=meta_spec[0, 3])

        axes = [fig.add_subplot(spec[3 - idx, 0]) for idx in range(4)]

        for idx, ax in enumerate(axes):

            ax.yaxis.set_major_locator(MaxNLocator(2))

            data = list(
                zip(array(evals[-1])[eval_intervals[idx]], array(evals[0])[eval_intervals[idx]]))

            if idx not in [1, 2]:
                for level, level_unpert in data:
                    ax.plot([.525, .95], ones(2) * level, lw=linewidth,
                            color="C%d" % (idx + minizones), alpha=0.5)
                    ax.plot([0.05, .475], ones(2) * level_unpert, lw=linewidth,
                            color="C%d" % (idx + minizones), alpha=0.5)
            else:
                for level, level_unpert in data[:5]:
                    ax.plot([0.05, .475], ones(2) * level_unpert, lw=linewidth,
                            color="C%d" % (idx + minizones), alpha=0.5)

                    ax.plot([.525, .95], ones(2) * level, lw=linewidth,
                            color="C%d" % (idx + minizones), alpha=0.5)
                minizones += 1
                for level, level_unpert in data[5:]:
                    ax.plot([0.05, .475], ones(2) * level_unpert, lw=linewidth,
                            color="C%d" % (idx + minizones), alpha=0.5)
                    ax.plot([.525, 0.95], ones(2) * level, lw=linewidth,
                            color="C%d" % (idx + minizones), alpha=0.5)

            d = 0.025
            if idx > 0:
                kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
                ax.plot((-d, +d), (-d, +d), lw=1, **kwargs)  # top-left diagonal
                ax.plot((1 - d, 1 + d), (-d, +d), lw=1, **kwargs)  # top-right diagonal
                ax.spines['bottom'].set_visible(False)
                ax.set_xticks([])

            if idx < 3:
                ax.spines["top"].set_visible(False)

                kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
                ax.plot((-d, +d), (1 - d, 1 + d), lw=1, **kwargs)  # top-left diagonal
                ax.plot((1 - d, 1 + d), (1 - d, 1 + d), lw=1, **kwargs)  # top-right diagonal

        def plot_single_circle(ax, xposition, yposition, color, yscale):
            step = ptp(cartoons_x) / 5
            ax.plot([cartoons_x[0] + xposition * step + step / 2], [yposition], color=color,
                    marker="o", ms=5, mec="black", mew=0.5)

        def plot_double_circle(ax, xposition, yposition, color, yscale):
            plot_single_circle(ax, xposition - 0.2, yposition - 0.01 * yscale, color, yscale)
            plot_single_circle(ax, xposition + 0.2, yposition + 0.01 * yscale, color, yscale)

        def plot_triple_circle(ax, xposition, yposition, color, yscale):
            plot_double_circle(ax, xposition, yposition, color, yscale)
            plot_single_circle(ax, xposition - 0.1, yposition + 0.05 * yscale, color, yscale)

        cartoon_position_level_indices = [[1], [6, 11], [21 + 2, 26, 46], [61, 81, 91, 121]]
        cartoons_x = linspace(.05, .475, 100)
        shifts = [-2, -2, 2, -2]
        single_circle_xpositions = [[[2]],
                                    [[], [1, 3]],
                                    [[], [2], [1, 3, 4]],
                                    [[2], [], [2, 4], [0, 1, 3, 4]]]
        double_circle_xpositions = [[[]],
                                    [[2], []],
                                    [[], [0], []],
                                    [[], [1, 3], [1], []]]
        triple_circle_xpositions = [[[]],
                                    [[], []],
                                    [[2], [], []],
                                    [[1], [], [], []]]
        colors = ["C0", "C1", "C2", "C3"] + ["C4"] * 2 + ["C5"] * 4
        color_counter = 0
        for idx, ax in enumerate(axes):
            for idx2, level_index in enumerate(cartoon_position_level_indices[idx]):
                wells = array(evals[0])[level_index] + \
                        (cos(linspace(0, 2 * pi * 5, 100)) + shifts[idx]) * .5e-1 * ptp(
                    ax.get_ylim())
                ax.plot(cartoons_x, wells, color="grey", lw=1)
                for xposition in single_circle_xpositions[idx][idx2]:
                    plot_single_circle(ax, xposition, wells[2], colors[color_counter],
                                       ptp(ax.get_ylim()))
                for xposition in double_circle_xpositions[idx][idx2]:
                    plot_double_circle(ax, xposition, wells[2], colors[color_counter],
                                       ptp(ax.get_ylim()))
                for xposition in triple_circle_xpositions[idx][idx2]:
                    plot_triple_circle(ax, xposition, wells[2], colors[color_counter],
                                       ptp(ax.get_ylim()))

                color_counter += 1

        axes[0].set_xticks([0.05 + 0.425 / 2, .75])
        axes[0].set_xticklabels(["0", "40"])
        axes[0].set_xlabel("$J/2\pi$ (MHz)")
        axes[2].set_ylabel("$(E_n - E_0)/h$ [GHz]")
        axes[2].yaxis.set_label_coords(-.325, -0.25)
        plt.gcf().set_size_inches(11, 4)
        plt.savefig("../fig3.pdf", bbox_inches="tight")


Fig3()
