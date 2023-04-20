import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotx

def plotter(desired_params:list, ref_col:str, df:pd.DataFrame, tickers:list, ncols:int, title:str, colors:list)->None:
    """
    plots subplots for given data frame 

    Params:
    desired_parms: list of params for seperate subplots
    ref_col: groupby column 
    df: dataframe for plotting
    tickers: given values for each plot
    ncols: number of desired columns
    title: super title of plot
    corlor: list of colors for plot
    
    Returns:
    None
    """
    plt.style.use(matplotx.styles.dracula)
    nrows = len(tickers) // ncols + (len(tickers) % ncols > 0)
    for param, color in zip(desired_params, colors):
            df = df.copy()
            sub_df = df[[ref_col, param]]
            plt.figure(figsize=(15,12))
            plt.subplots_adjust(hspace=0.2)
            plt.suptitle(param.title() + title.title())
            for n, tick in enumerate(tickers):
                ax = plt.subplot(nrows, ncols, n+1)
                sub_df[sub_df[ref_col] == tick].plot(ax=ax, color=color, legend=False)
                ax.axhline(y=0, c="lightsteelblue", linestyle="--")
                ax.set_title(tick)
                sns.despine()
            
            plt.savefig(param)