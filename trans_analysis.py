import pandas as pd
import c
import os
import matplotlib.pyplot as plt
import numpy as np
import re
import seaborn as sns
from plotter import plotter


def get_criminal_lines(speaker_df: pd.DataFrame, trans_dir: str) -> pd.DataFrame:
    """
    gets the transcribed criminal lines from 
    the transcript csv's

    Params:
    speaker_df: dataframe that specifies which speaker
    is criminal for given video, this was done manually 
    by matching transcripts and listening to the audio
    trans_dir: transcript containing transcripts
    
    Returns:
    pandas data frame of all tagged criminal words 
    per video

    """

    vid_titles = list(speaker_df[c.title_col_speakers])
    names = list(speaker_df[c.crim_col])
    trans_dfs = [pd.read_csv(os.path.join(trans_dir, title + c.csv_suff)) for title in vid_titles]
    for title, df in zip(vid_titles, trans_dfs): df.insert(1, c.title_col_speakers, title)
    for name, df in zip(names, trans_dfs): df.insert(1, c.crim_col, name)
    speakers = list(speaker_df[c.speaker_col])
    criminal_dfs = [df[df[c.speaker_col.upper()] == crim] for df,crim in zip(trans_dfs, speakers)] 
    
    return pd.concat(criminal_dfs)


def graph_power_danger(criminal_df:pd.DataFrame) -> None:
    """
    uses ousiometrics to graph pwower and danger curves

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
    
    power_danger = pd.read_table("ousiometry_data_augmented.tsv", usecols=[c.ousiowords, c.ousiopower, c.ousiodanger])
    word_in_lex = lambda x: True if x in list(power_danger[c.ousiowords]) else False
    power_func = lambda x, y: list(power_danger[(power_danger == x).any(axis=1)].to_dict()[y].values())[0] if word_in_lex(x) else np.nan
    
    words_expanded[c.ousiopower] = [power_func(word, c.ousiopower) for word in list(words_expanded[c.words_col])]
    words_expanded[c.ousiodanger] = [power_func(word, c.ousiodanger) for word in list(words_expanded[c.words_col])]
    words_expanded.dropna(inplace=True)

    crim_list = list(words_expanded[c.crim_col].unique())
    ncols = c.ncols
    params = [c.ousiopower, c.ousiodanger]
    plotter(desired_params=params, ref_col=c.crim_col, df=words_expanded, 
            tickers=crim_list, ncols=ncols, title=" curves per transcript")
    
    words_expanded.drop(columns=[c.text_col], inplace=True)
    words_expanded.to_csv(c.final_df)
  
