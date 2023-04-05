import pandas as pd
import swifter
import json
import os
import re


def get_transcripts(wav_list: list, wav_dir: str, trans_dir: list) -> None:
    """
    use whsiper gather and store transcripts 

    Params:
    wav_list: list of wav files 
    wav_dir: directory to read in wav files
    trans_dir: transcript directry to write to

    Returns:
    None
    """
    import whisper
    try:
        os.mkdir(trans_dir)
        model = whisper.load_model("base")
        res_func = lambda x: model.transcribe(x, word_timestamps=False)
       
        for file in wav_list:
            result = res_func(os.path.join(wav_dir, file))
            with open(os.path.join(trans_dir, re.sub(r"\s+", "", file[:-5]) + ".json"), "w", encoding="utf-8") as file:
                print(file)
                segments = result["segments"]
                json.dump(segments, file, indent=4)
    except Exception as e:
        print(e)


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
    
