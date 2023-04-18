import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plotter(desired_params:list, ref_col:str, df:pd.DataFrame, tickers:list, ncols:int, title:str)->None:
    """
    plots subplots for given data frame 

    Params:
    desired_parms: list of params for seperate subplots
    ref_col: groupby column 
    df: dataframe for plotting
    tickers: given values for each plot
    ncols: number of desired columns
    title: super title of plot
    
    Returns:
    None
    """
    
    nrows = len(tickers) // ncols + (len(tickers) % ncols > 0)
    for param in desired_params:
            df = df.copy()
            sub_df = df[[ref_col, param]]
            plt.figure(figsize=(15,12))
            plt.subplots_adjust(hspace=0.2)
            plt.suptitle(param + title)
            for n, tick in enumerate(tickers):
                ax = plt.subplot(nrows, ncols, n+1)
                sub_df[sub_df[ref_col] == tick].plot(ax=ax)
                ax.set_title(tick)
                ax.get_legend().remove()
                sns.despine()
            
            plt.savefig(param)