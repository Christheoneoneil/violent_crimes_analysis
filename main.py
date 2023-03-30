import os
from audio_diarization import read_file, scrape_audio, file_conversion, diratzation 
from transcripts import get_video_id, get_transcripts, read_in_trans

def main()-> None:
    """
    structures code for different interactions
    of scripts 

    Params: None

    Returns: None
    """

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
    rm_dir = "audiorttm"
    diratzation(file_list=wav_files, input_d=audio_wav_dir, rttm_dir=rm_dir)
    
    ids = get_video_id(vid_links=links, link_col="Link") 
    vid_titles = list(links["vidtitle"])
    print(vid_titles)
    
    transcripts_dir="transcripts"
    get_transcripts(vid_ids=ids, trans_dir=transcripts_dir, titles=vid_titles)
    
    json_files = os.listdir(transcripts_dir)
    transcripts = read_in_trans(file_list=json_files, trans_dir=transcripts_dir) 
    

if __name__ == "__main__":
    main()