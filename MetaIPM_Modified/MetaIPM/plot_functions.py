import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
pal = sns.cubehelix_palette(12, rot=-.25, light=.7)


def format_model_output(n_points, omega, input_matrix, n_years, n_months):
    """convert model outputs to data frame for plotting"""
    n_times = input_matrix.shape[1]

    # convert to data frame for plotting
    yr = np.append(np.repeat(range(n_years),
                             len(omega) * n_months),
                   np.repeat(n_years + 1,
                             len(omega)))
    mth = np.append(np.tile(np.repeat(range(n_months), len(omega)), n_years),
                    np.repeat(np.min(range(n_months)), len(omega)))
    lng = np.tile(omega, n_times)

    input_df = pd.DataFrame(input_matrix).melt(
        value_name="Population", var_name="Time")
    details_df = pd.DataFrame({"Length": lng,
                               "Year": yr,
                               "Month": mth})

    output_df = pd.concat([input_df,
                           details_df],
                          axis=1)
    return output_df


def ridge_plot_all_time(input_df):
    # create plot and then plot
    pop_plot = sns.FacetGrid(input_df,
                             row="Year",
                             hue="Month",
                             col="Month",
                             aspect=2.5,
                             height=0.5,
                             palette=pal)

    pop_plot.map(plt.plot, "Length", "Population")
    pop_plot.map(plt.axhline,
                 y=0,
                 lw=2,
                 clip_on=False)

    # Define and use a simple function to label the plot in axes coordinates
    def label(x, color, label):
        ax = plt.gca()
        ax.text(0, .2, label, fontweight="bold", color=color,
                ha="left", va="center", transform=ax.transAxes)

    # Set the subplots to overlap
    pop_plot.fig.subplots_adjust(hspace=-.25)

    # Remove axes details that don't play well with overlap
    pop_plot.set_titles("")
    pop_plot.set(yticks=[])
    pop_plot.despine(bottom=True, left=True)

    return pop_plot
