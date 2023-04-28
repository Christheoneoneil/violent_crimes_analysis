
import matplotlib.pyplot as plt
import pandas as pd
import re
import numpy as np
import seaborn as sns
import os
import c

def plotter(desired_params:list, ref_col:str, df:pd.DataFrame, tickers:list, ncols:int, title:str, colors:list)->None:
    """
    Description:
    Creates a grid of subplots for a given dataframe
    
    Params:
    desired_parms: list of params for seperate subplots
    ref_col: groupby column 
    df: dataframe for plotting
    tickers: given values for each plot
    ncols: number of desired columns
    title: super title of plot
    color: list of colors for plot
    
    Returns:
    None
    """
    plt.style.use('dark_background')
    nrows = len(tickers) // ncols + (len(tickers) % ncols > 0)
    for param, color in zip(desired_params, colors):
            df = df.copy()
            sub_df = df[[ref_col, param]]
            plt.figure(figsize=(15,12))
            plt.subplots_adjust(hspace=0.2)
            plt.suptitle(param.title() + title.title())
            for n, tick in enumerate(tickers):
                ax = plt.subplot(nrows, ncols, n+1)
                sub_df[sub_df[ref_col] == tick].reset_index(drop=True).plot(ax=ax, color=color, legend=False) # setting .reset_index seemed to do something...
                ax.axhline(y=0, c="lightsteelblue", linestyle="--")
                ax.get_xaxis().set_visible(False)
                ax.set_title(tick)
                sns.despine()
            
            plt.savefig(param)





def graph_power_danger(criminal_df:pd.DataFrame) -> None:
    """
    Description:
    Uses ousiometrics to graph power and danger curves as functions of word index

    Params:
    criminal_df: data frame of all criminal transcripts
    
    Returns:
    None
    """

    criminal_df[c.words_col] = criminal_df[c.text_col].str.split()
    words_expanded = criminal_df.explode(c.words_col) 
    words_expanded[c.words_col] = words_expanded[c.words_col].map(str)
    words_expanded[c.words_col] = words_expanded[c.words_col].str.lower()
    
    words_expanded[c.words_col] = [re.sub(r'[^\w\s]', '', word) for word in list(words_expanded[c.words_col])]
    
    power_danger = pd.read_table(c.ousio_dat, usecols=[c.ousiowords, c.ousiopower, c.ousiodanger])
    word_in_lex = lambda x: True if x in list(power_danger[c.ousiowords]) else False
    power_func = lambda x, y: list(power_danger[(power_danger == x).any(axis=1)].to_dict()[y].values())[0] if word_in_lex(x) else np.nan
    
    
    words_expanded[c.ousiopower] = [power_func(word, c.ousiopower) for word in list(words_expanded[c.words_col])]
    words_expanded[c.ousiodanger] = [power_func(word, c.ousiodanger) for word in list(words_expanded[c.words_col])]
    words_expanded.dropna(inplace=True)

    crim_list = list(words_expanded[c.crim_col].unique())
    ncols = c.ncols
    params = [c.ousiopower, c.ousiodanger]
    
    plotter(desired_params=params, ref_col=c.crim_col, df=words_expanded,     # words_expanded is being fed in as a dataframe... what's going on here? We should be plotting word score as a function of the word number
            tickers=crim_list, ncols=ncols, title=" curves per transcript",
            colors=c.colors)
    
    words_expanded.drop(columns=[c.text_col], inplace=True)
    non_sparse = words_expanded.set_index(c.crim_col).drop(labels=['romano', 'bartley', 'castillo']) # holmes is automatically not plotted because it doesn't have tokens to put in the dataframe.
    non_sparse.reset_index(inplace=True)
    for param in params: non_sparse[param + " rolling avg"] = non_sparse.groupby(c.crim_col)[param].transform(lambda x: x.rolling(c.window_size).mean())
    rolling_params = [param + " rolling avg" for param in params]

    plotter(desired_params=rolling_params, ref_col=c.crim_col, df=non_sparse, 
            tickers=list(non_sparse[c.crim_col].unique()), ncols=c.ncols, title=" per transcript",
            colors=c.colors)
    

    
    words_expanded.to_csv(c.final_df)



def create_criminal_dataFrame(folder_path: str, file_names: list):
    """
    Returns a pandas DataFrame containing file names and their contents.
    The DataFrame has columns: 'name', 'Text'

    Description:
    Creates a dataframe of criminals and the words of their text 

    Params:
    folder: folder name as a string
    file_names: list of file names without any extensions

    Returns:
    text_df: dataframe containing two columns -- 'name' and 'Text' 



    """
    # create an empty list to store the results
    results = []

    # loop over the file names and apply the function to each file
    for file_name in file_names:

        # read the file contents
        with open(folder_path + '/' + file_name, 'r') as f:
            text = f.read()

        # create a DataFrame with the results for this file
        file_df = pd.DataFrame({'name': [file_name.strip('.txt')],
                                'Text': [text]})

        # append the file_df to the list of results
        results.append(file_df)

    # concatenate all the results into a single dataframe
    text_df = pd.concat(results)

    return text_df







#--------------defining variables--------------
df_lexicon_scores = pd.read_table('ousiometry_data_augmented.tsv')
folder_path = 'shooters_words_text'
file_names = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
criminal_names = [f.strip('.txt') for f in os.listdir(folder_path) if f.endswith('.txt')]
df = create_criminal_dataFrame(folder_path, file_names)
# print(file_names)
# print(criminal_names)
# print(df)

#--------------Generating Plots--------------
graph_power_danger(df)


