from bs4 import BeautifulSoup
from collections import Counter
import html5lib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import requests
import seaborn as sns
import shifterator as sh

def Clean_Words(string):
    """
    Description:
        Remove formatting and punctuation from source.
    
    Parameters:
        string: str, String of input text.

    Returns:
        list[str], String of tokenized text.
    """
    # Define regular expressions to match words, punctuation, and sequences of dots
    word_regex = r'\b\w+\b'
    punct_regex = r'[^\w\s]'
    #dot_regex = r'\.+'
    dot_regex = r'\.{4,}|\.{3}|\.{2}|\.'

    # Define a list to hold the resulting tokens
    tokens = []

    # Iterate over the matches of the regular expressions and append them to the tokens list
    for match in re.finditer(f'{dot_regex}|{punct_regex}|{word_regex}', string):
        token = match.group()

        if re.match(word_regex, token):
            tokens.append([token])

        elif re.match(dot_regex, token):
            tokens.append([token])

        else:
            # Split the token into parts that consist of either dots or non-dots
            parts = re.findall(f'(?:{dot_regex})+|[^\.\s]+', token)
            for part in parts:
                tokens.append([part])

    return [''.join(entry) for entry in tokens]


def Get_Tokens_List(book_name):
    """
    Description:
        Initial extraction of strings from source.
    
    Parameters:
        book_name: str, File name and extension for source data.

    Returns:
        Clean_Words(text_string): list[str], String of tokenized text.
    """
    file = open(book_name, 'r') 
    text = file.read()

    # replace all \n with ' ' 
    text = text.replace('\n', ' ')

    # split everything into entries of a list
    text = text.split(' ')

    # Remove all ' ' entries
    text = [entry for entry in text if entry.strip()]

    # make everything lowercase
    text = [entry.lower() for entry in text]
    
    text_string = ' '.join(text)

    # Combine new_res elements into a string with spaces for separators
    # Get a list of all tokens by calling Clean_Words on text_string
    return Clean_Words(text_string)

def get_happiness_scores(ngrams, hedon, hap_vars): 
    """
    Description:
        .
    
    Parameters:
        ngrams: str, Tokenized input text.
        hedon: dict{str : float}, LabMT sentiment scores for english words.
        hap_vars: list[list[str], list[float]], 
                Index 0: List of words as strings;
                Index 1: List of scores ad floats.

    Returns:
        list[float], List of scores as floats.
    """
    # hap_vars are hap_vars[0] = 'words' and hap_vars[1]='scores'
    hap_df = hedon[hap_vars]
    hap_dict = {key:val for key, val in zip(hap_df[hap_vars[0]], hap_df[hap_vars[1]])}
    return [hap_dict[gram] if gram in list(hap_dict.keys()) else 0 for gram in ngrams]

def Get_Token_Scores(tokens, df_lexicon_scores, score_type):
    """
    Description:
        Extract danger scores for tokenized text.
    
    Parameters:
        tokens: str, Tokenized input text.
        df_lexicon_scores: dict{str : float}, LabMT scores for english words.
        score_type: str, Desired sentiment to score.

    Returns:
        list[dict{str : float}], List of dictionary with word-score pairs.
    """
    # create a dataframe from the tokens list
    df_tokens = pd.DataFrame({'word': tokens})
    
    # merge the tokens dataframe with df_lexicon_scores
    # score_type can be power, danger, etc...
    # return the danger scores as a list
    return pd.merge(df_tokens, df_lexicon_scores[['word', score_type]], on='word', how='left')['danger'].tolist() 

def calculate_averages(raw_scores,window_size):
    """
    Description:
        .
    
    Parameters:
        .

    Returns:
        .
    """
    raw_series = pd.Series(raw_scores)
    windows = raw_series.rolling(window_size)
    avgs = windows.mean()
    return avgs

def plotter(data: list, titles: str, rows: int, cols: int):   
    """
    Description:
        .
    
    Parameters:
        .

    Returns:
        .
    """ 
    fig, axs = plt.subplots(nrows=rows, ncols=cols, figsize=(8, 10))
    fig.tight_layout()
    sns.despine(fig)
    
    for avg, ax, title in zip(data, axs.ravel(), titles):
        ax.plot(avg)
        ax.set_title(title, fontsize=7)
        ax.set_ylabel(r"$h_{avg}$", fontsize=7)
        ax.tick_params(axis='both', which='minor', labelsize=5)
    axs.ravel()[-1].set_xlabel("Word number i")


def word_shifts(type2freq_1: dict, type2freq_2: dict, ref_avg: float, title: list):
    """
    Description:
        .
    
    Parameters:
        .

    Returns:
        .
    """
    sentiment_shift = sh.WeightedAvgShift(type2freq_1=type2freq_1,
                                      type2freq_2=type2freq_2,
                                      type2score_1='labMT_English',
                                      reference_value=ref_avg,
                                      stop_lens=[(4,6)])
    sentiment_shift.get_shift_graph(detailed=True,
                                system_names=[title[0], title[1]])

def Create_Score_Dictionary(score_type):
    """
    Description:
        .
    
    Parameters:
        .

    Returns:
        .
    """
    # read in lexicon
    df_lexicon_scores = pd.read_table('ousiometry_data_augmented.tsv')

    # create an empty dictionary to store the results
    results_dict = {}

    # get a list of the .txt files in the 'shooters_words_text' directory
    folder_path = 'shooters_words_text'
    file_names = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    print(file_names)

    # loop over the file names and apply the function to each file
    for file_name in file_names:
        # apply the function to the file contents
        tokens_list = Get_Tokens_List(folder_path + '/' + file_name)

        "We could probably just add the following line:"
        # Get_Token_Scores(tokens_list, df_lexicon_scores)

        tokens_list = Get_Token_Scores(tokens_list, df_lexicon_scores, score_type)
        # store the output in the results dictionary with the file name as the key
        criminal_name = file_name.split('.')[0]
        results_dict[criminal_name] = tokens_list

    # print out the results dictionary
    print(results_dict)
    return results_dict

if __name__ == "__main__":
    danger_dict = Create_Score_Dictionary('danger')
    danger_scores1 = list(danger_dict.values())[1] # this is for the first criminal in our list of criminal_names
    danger_names1 = list(danger_dict.values())[0]

    "Now, let's use these lists in order to create a danger plot."
    # for name, score_list in danger_dict.items():
    #     "TODO: Insert function for plotting the score_list"
    # list(results_dict.values())

    # get danger scores for the first criminal
    a = 1
    b = 4.5
    c = .5

    window_sizes = [round(10**i) for i in np.arange(1, 4.5, .5)] 
    rolling_averages = [calculate_averages(danger_scores1, window_size) for window_size in window_sizes] 
    t_list = ["Insert Criminal Name Here, T = " + str(window_size) + ", z = " + str(round(np.log10(window_size)*2)/2) for window_size in window_sizes]
    plotter(rolling_averages, t_list, 7, 1)
    plt.savefig("unadjusted_happiness.png")