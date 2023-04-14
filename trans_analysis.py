import pandas as pd
import c
import os


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

