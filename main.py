import os
from audio_diarization import read_file, scrape_audio, file_conversion, diratzation 

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
    

if __name__ == "__main__":
    main()