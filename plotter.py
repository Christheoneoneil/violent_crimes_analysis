import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotx
import numpy as np
import c


def plotter(desired_params:list, ref_col:str, df:pd.DataFrame, tickers:list, ncols:int, title:str, colors:list)->None:
    """
    plots subplots for given data frame 

    Params:
    desired_params: list of params for seperate subplots
    ref_col: groupby column 
    df: dataframe for plotting
    tickers: given values for each plot
    ncols: number of desired columns
    title: super title of plot
    colors: list of colors for plot
    
    Returns:
    None
    """
    
    plt.style.use(matplotx.styles.dracula)
    nrows = len(tickers) // ncols + (len(tickers) % ncols > 0)
    plt.rc('font', size=c.font_size) 
    for param, color in zip(desired_params, colors):
            df = df.copy()
            sub_df = df[[ref_col, param]]
            plt.figure(figsize=(15,12))
            plt.subplots_adjust(hspace=0.2)
            plt.suptitle(param.title() + title.title())
            for n, tick in enumerate(tickers):
                ax = plt.subplot(nrows, ncols, n+1)
                ax.plot(sub_df[sub_df[ref_col] == tick][param].to_list(), c=color)
                score_mean = np.nanmean(sub_df[sub_df[ref_col] == tick][param].to_list())
                yvals = [0, score_mean]
                for axline, d_color, l_s in zip(yvals, c.dash_colrs, c.lin_styles):
                     ax.axhline(y=axline, c=d_color, linestyle=l_s, label=round(axline,2))
                ax.set_title(tick)
                ax.legend()
                sns.despine()
            
            plt.savefig(param)