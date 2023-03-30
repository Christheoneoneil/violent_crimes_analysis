import pandas as pd
import swifter
import json
import os


def get_video_id(vid_links: pd.DataFrame, link_col="Link") -> pd.DataFrame:
    """
    parses video id from link 

    Params:
    vid_links:
    link_col:

    Returns:
    list of link ids
    """
    
    from urllib.parse import urlparse
    
    df = vid_links.copy()
    df["url_dat"] = df[link_col].swifter.apply(urlparse)
    qurery_func = lambda x: x.query
    df["query"] = df["url_dat"].swifter.apply(qurery_func)
    get_id_func = lambda x: x[2:]
    df["vid_id"] = df["query"].swifter.apply(get_id_func)
    
    return list(df["vid_id"])


def get_transcripts(vid_ids: list, trans_dir: str, titles: list) -> None:
    """
    use youtube api gather and store transcripts 

    Params:
    vid_ids: list of video ids
    trans_dir: directory to store transcripts
    titles: list of video titles

    Returns:
    None
    """

    if (os.path.exists(trans_dir)) != True:
        os.mkdir(trans_dir)
        from youtube_transcript_api import YouTubeTranscriptApi
        index = 0
        get_vid_funct = lambda x: YouTubeTranscriptApi.get_transcript(str(x))
        for id in vid_ids:
            try:
                transcript = get_vid_funct(id)
                title = titles[index]
                print(id)
                print(title)
                with open(trans_dir + "/" + title + ".json", "w") as final:
                    json.dump(transcript, final)
                
            except Exception as e:
                print(e)
                
            index += 1

def read_in_trans(file_list: list, trans_dir: str) -> pd.DataFrame:
    """
    takes in list of json files and 
    returns a merged and tagged data
    frame consisting of all transcripts 

    Params:
    file_list: list of json files

    Returns:
    pandas data frame of transcripts
    """

    df_list = [pd.read_json(trans_dir + "/" + filename, orient="records") \
               for filename in file_list]
    
    for title, df in zip(file_list, df_list): df["vid_title"] = title[:-5]

    df = pd.concat(df_list) 

    return df
    
