import pandas as pd
import swifter
import os
import config
import ffmpy 
import glob
import shutil
import re


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


def scrape_audio(scrape_links: pd.DataFrame, link_col: str, output_d: str) -> None:
    """
    scrapes youtbube audio with the help of youtube dl
    
    Params:
    scrape_links: data frame that contains 
    links for scraping
    link_col: column name for links
    output_d: directory for audio outputs
    Returns:
    None
    """
    
    if (os.path.exists(output_d)) != True:
        from pytube import YouTube
        df = scrape_links.copy()
        df["vids"] = df[link_col].swifter.apply(YouTube)
        
        stream_audio = lambda x: x.streams.filter(only_audio=True).first()
        df["audio"] = df["vids"].swifter.apply(stream_audio)

        download_audio = lambda x: x.download(output_path=output_d)
        df["audio"].swifter.apply(download_audio)
    

def file_conversion(file_list: list, input_d:str, wav_dir:str)-> None:
    """
    converts audiofiles to wav files 

    Params:
    file_list: list of files 
    input_d: directoyr containing files for conversion

    Returns: 
    None
    """
    if (os.path.exists(wav_dir)) != True:
        for file in file_list:
            ff = ffmpy.FFmpeg(inputs={input_d + "/" +file: None}, 
                                outputs={re.sub(r"\s+", "", file[:-4] + ".wav"): None})
            ff.run()

        files_to_move = glob.glob("*.wav")
        os.mkdir(wav_dir)
        for file in files_to_move:
            new_path = wav_dir + "/" + file
            shutil.move(file, new_path)


def diratzation(file_list: list, input_d: str) -> None:
    """
    extracts subtitles and tagged speakers from
    provided audio files

    Prams:
    file_list: list of audio files
    input_d: name of directory for input files

    Returns: 
    None

    """

    from pyannote.audio import Pipeline

    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                        use_auth_token=config.auth_token)

    
    
    full_files = [input_d + "/" + filename for filename in file_list]
    diar_func = lambda x: pipeline(x)
    diarizations = [diar_func(file) for file in full_files]
    rttm_dir = "audiorttm"
    os.mkdir(rttm_dir)
    rttm_files = [rttm_dir + "/" + filename[:-4] + ".rttm" for filename in file_list]
    
    for file, diar in zip(rttm_files, diarizations):
        with open(file, "w") as rttm:
            diar.write_rttm(rttm)


links = read_file("links.csv")
audio_file_dir = "audio"
scrape_audio(scrape_links=links, 
            link_col="Link", 
            output_d=audio_file_dir)

audio_files = os.listdir(audio_file_dir)

audio_wav_dir = "audiowav"
file_conversion(file_list = audio_files, 
                input_d="audio", wav_dir=audio_wav_dir)
wav_files = os.listdir(audio_wav_dir)
diratzation(file_list=wav_files, input_d=audio_wav_dir)
