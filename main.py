import os
from audio_diarization import read_file, scrape_audio, file_conversion, diratzation 
from transcripts import get_transcripts, get_segments
from trans_analysis import get_criminal_lines, graph_power_danger
import c


def main()-> None:
    """
    structures code for different interactions
    of scripts 

    Params: None

    Returns: None
    """

    links = read_file("links.csv")
    
    scrape_audio(scrape_links=links, 
                link_col=c.link_col, 
                output_d=c.audio_file_dir)

    audio_files = os.listdir(c.audio_file_dir)

    #file_conversion(file_list = audio_files, 
                    #input_d=c.audio_dir, wav_dir=c.audio_wav_dir)
    #wav_files = os.listdir(c.audio_wav_dir)
    
    #diratzation(file_list=wav_files, input_d=c.audio_wav_dir, rttm_dir=c.rm_dir)

    #segments = get_segments(rttm_dir=c.rm_dir)
    
    #get_transcripts(segs=segments, wav_dir=c.audio_wav_dir, trans_dir=c.transcripts_dir)
    
    speakers = read_file("Speakers.csv")
    
    tagged_df = get_criminal_lines(speaker_df=speakers, trans_dir=c.transcripts_dir)
    
    graph_power_danger(tagged_df)

    
if __name__ == "__main__":
    main()