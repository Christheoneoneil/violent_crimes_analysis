import pandas as pd
from pytube import YouTube
import swifter
import os



def read_file(filename:str) -> pd.DataFrame:
    """
    reads in provided file containing links
    for vidoes for diarization
    
    Params:
    fielname: name of provided file

    Returns:
    read in data frame
    """

    return pd.read_csv(filename) 


def scrape_audio(scrape_links: pd.DataFrame, link_col: str) -> None:
    """
    scrapes youtbube audio with the help of youtube dl
    
    Params:
    scrape_links: data frame that contains 
    links for scraping
    link_col: column name for links

    Returns:
    None
    """
    
    df = scrape_links.copy()
    df["vids"] = df[link_col].swifter.apply(YouTube)
    
    stream_audio = lambda x: x.streams.filter(only_audio=True).first()
    df["audio"] = df["vids"].swifter.apply(stream_audio)

    download_audio = lambda x: x.download(output_path="audio")
    df["audio"].swifter.apply(download_audio)
    

links = read_file("links.csv") 
scrape_audio(scrape_links=links, link_col="Link")