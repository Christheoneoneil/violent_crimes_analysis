import pandas as pd
import swifter
import json
import os
import re
import c


def get_segments(rttm_dir: str) -> dict:
    """
    gets the segments of the wavs files for
    diffeent speakers

    Params:
    rttm_dir: directory containing rttm files

    Returns:
    Dictionary of segments
    """

    
    speaker_segs_dict = {}

    for file in os.listdir(rttm_dir):
        with open(os.path.join(rttm_dir, file), "r") as f:
            filelines = f.read().split(c.rttm_split_char)
            segments = [seg.split(c.rttm_end_of_req_info)[0] for seg in filelines if c.info_needed_char in seg]
            segments_rem_na = [seg.replace(c.noise_char, "") for seg in segments]
            
            get_floats = lambda x: re.findall(r"\d+\.\d+", x)
            get_substring = lambda x: x[x.index(c.spearker_info_start):].replace(" ", "")
            
            secs_to_mil = lambda x: float(x)*1000
            to_stamps = lambda x: [x[0], x[0] + x[1]]
            segments_cleaned = [[to_stamps(list(map(secs_to_mil, get_floats(seg)))), 
                                 get_substring(seg)] for seg in segments_rem_na]
        speaker_segs_dict[file[:-5]] = segments_cleaned
    
    return speaker_segs_dict


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
    
