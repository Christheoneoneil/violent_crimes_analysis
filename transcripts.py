import pandas as pd
import swifter
 

def get_video_id(vid_links: pd.DataFrame, link_col="Link") -> list:
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
    
