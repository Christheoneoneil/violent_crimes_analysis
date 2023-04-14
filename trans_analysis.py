import pandas as pd
import c
import os
import matplotlib.pyplot as plt
import numpy as np


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
    trans_dfs = [pd.read_csv(os.path.join(trans_dir, title + c.csv_suff)) for title in vid_titles]
    for title, df in zip(vid_titles, trans_dfs): df.insert(1, c.title_col_speakers, title)
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
    words_expanded[c.words_col] = words_expanded[c.words_col].str.lower()

    power_danger = pd.read_table("ousiometry_data_augmented.tsv", usecols=[c.ousiowords, c.ousiopower, c.ousiodanger])
    power_func = lambda x: power_danger[power_danger[c.ousiowords] == x][c.ousiodanger]
    danger_func = lambda x: power_danger[power_danger["word"] == x]["danger"]
    # @TODO: Issue in above mapping must fix