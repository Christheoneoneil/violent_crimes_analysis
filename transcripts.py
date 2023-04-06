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


def get_transcripts(segs: dict, wav_dir: str, trans_dir: list) -> None:
    """
    use whsiper gather and store transcripts 

    Params:
    seg: dictionary conatining timestamped diarizations
    wav_dir: directory to read in wav files
    trans_dir: transcript directry to write to

    Returns:
    None
    """

    
    from pydub import AudioSegment
    import whisper
    try:
        os.mkdir(trans_dir)
        model = whisper.load_model("base")

        res_func = lambda x: model.transcribe(x, 
                                              word_timestamps=False)
        
        for key, val in segs.items():
            try:
                os.mkdir(os.path.join(wav_dir, key))
                audio = AudioSegment.from_wav(os.path.join(wav_dir, key) + c.wav_suff)
                
                for segments in val:
                    chunk = audio[segments[0][0]:segments[0][1]]
                    chunk.export(os.path.join(wav_dir, key, str(segments)) + c.wav_suff, 
                                 format="wav")
            
            except Exception as e: 
                tagged_trans = [(segments[1], 
                                 res_func(os.path.join(wav_dir, key, str(segments)) + c.wav_suff)["text"]) for segments in val]
            
            df = pd.DataFrame(tagged_trans, 
                              columns=[c.spearker_info_start, c.text_col])
            df.to_csv(os.path.join(trans_dir, 
                                   key) + c.csv_suff)
         
    except Exception as e:
        print(e)


