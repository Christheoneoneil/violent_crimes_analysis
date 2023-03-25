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


def scrape_audio(scrape_links: pd.DataFrame, link_col: str, output_d) -> None:
    """
    scrapes youtbube audio with the help of youtube dl
    
    Params:
    scrape_links: data frame that contains 
    links for scraping
    link_col: column name for links
    output_d: name of directory for output

    Returns:
    None
    """
    
    df = scrape_links.copy()
    df["vids"] = df[link_col].swifter.apply(YouTube)
    
    stream_audio = lambda x: x.streams.filter(only_audio=True).first()
    df["audio"] = df["vids"].swifter.apply(stream_audio)

    download_audio = lambda x: x.download(output_path=output_d)
    df["audio"].swifter.apply(download_audio)
    

def diratzation(dir_list: list) -> None:
    """
    extracts subtitles and tagged speakers from
    provided audio files

    Prams:
    dir_list: list of audio files

    Returns: 
    None

    """


links = read_file("links.csv")
audio_file_dir = "audio"
if (os.path.exists(audio_file_dir)) != True:
    scrape_audio(scrape_links=links, 
                link_col="Link", 
                output_d=audio_file_dir)
    