
from bs4 import BeautifulSoup
import html5lib
import requests

import matplotlib.pyplot as plt
import pandas as pd
import re
import numpy as np
import seaborn as sns
import shifterator as sh
from collections import Counter

import os




def Clean_Words(string):

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
    tokens = [''.join(entry) for entry in tokens]

    return tokens


def Get_Tokens_List(book_name):

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


#------------------------------------------------------------------------------------------------

def get_happiness_scores(ngrams, hedon, hap_vars): # hap_vars are hap_vars[0] = 'words' and hap_vars[1]='scores'
    hap_df = hedon[hap_vars]
    hap_dict = {key:val for key, val in zip(hap_df[hap_vars[0]], hap_df[hap_vars[1]])}
    scores = [hap_dict[gram] if gram in list(hap_dict.keys()) else 0 for gram in ngrams]
   
    return scores

def Get_Token_Scores(tokens, df_lexicon_scores, score_type):
    # create a dataframe from the tokens list
    df_tokens = pd.DataFrame({'word': tokens})
    
    # merge the tokens dataframe with df_lexicon_scores 
    df_scores = pd.merge(df_tokens, df_lexicon_scores[['word', score_type]], on='word', how='left')   # score_type can be power, danger, etc...
    
    # return the danger scores as a list
    return df_scores['danger'].tolist()



def calculate_averages(raw_scores,window_size):
    raw_series = pd.Series(raw_scores)
    windows = raw_series.rolling(window_size)
    avgs = windows.mean()
    
    return avgs



def plotter(data: list, titles: str, rows: int, cols: int):    
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
    plots weighted average word shift
    graphs for first and second half of corpus
    
    Params:
    type2freq_1: comparison text 
    type2freq_2 refrence text
    ref_avg: average used for reference
    title: title for plots

    Returns:
    None
    """


    sentiment_shift = sh.WeightedAvgShift(type2freq_1=type2freq_1,
                                      type2freq_2=type2freq_2,
                                      type2score_1='labMT_English',
                                      reference_value=ref_avg,
                                      stop_lens=[(4,6)])
    sentiment_shift.get_shift_graph(detailed=True,
                                system_names=[title[0], title[1]])


# read in lexicon

df_lexicon_scores = pd.read_table('ousiometry_data_augmented.tsv')






# create an empty dictionary to store the results
results_dict = {}

# get a list of the .txt files in the 'shooters_words_text' directory
folder_path = 'shooters_words_text'
file_names = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

print(file_names)



def Create_Score_Dictionary(score_type):
    # loop over the file names and apply the function to each file
    for file_name in file_names:
        
        # apply the function to the file contents
        tokens_list = Get_Tokens_List(folder_path + '/' + file_name)

        '''We could probably just add the following line: Get_Token_Scores(tokens_list, df_lexicon_scores)'''
        tokens_list = Get_Token_Scores(tokens_list, df_lexicon_scores, score_type)


        # store the output in the results dictionary with the file name as the key
        criminal_name = file_name.split('.')[0]
        results_dict[criminal_name] = tokens_list

    # print out the results dictionary
    print(results_dict)
    
    return results_dict





for name, score_list in results_dict.items():
    '''Insert function for plotting the score_list'''

list(results_dict.values())



# get danger scores for the first criminal
a = 1
b = 4.5
c = .5

window_sizes = [round(10**i) for i in np.arange(1, 4.5, .5)] 
rolling_averages = [calculate_averages(happiness_scores, window_size) for window_size in window_sizes] 
t_list = ["Original 6 Star Wars Movies (Episode Order 1-6), T = " + str(window_size) + ", z = " + str(round(np.log10(window_size)*2)/2) for window_size in window_sizes]
plotter(rolling_averages, t_list, 7, 1)
plt.savefig("unadjusted_happiness.png")
























# # get happiness scores for star wars and lotr
# starwars_happiness_scores = get_happiness_scores(starwars_ngrams, hedonometer, ["Word", "Happiness Score"]) 
# lotr_happiness_scores = get_happiness_scores(lotr_ngrams, hedonometer, ["Word", "Happiness Score"]) 

# #   111865 is around where the original trilogy begins
# text_separator = 111865           
# prequels = starwars_ngrams[:text_separator]
# original_trilogy = starwars_ngrams[text_separator:]


# # Get the counts for each thing
# first_freqs = dict(Counter(prequels))                                                                   # starwars_ngrams
# second_freqs = dict(Counter(original_trilogy))                                                                         # lotr_ngrams 


# first_avg = np.average(get_happiness_scores(prequels, hedonometer, ["Word", "Happiness Score"]))
# second_avg = np.average(get_happiness_scores(original_trilogy, hedonometer, ["Word", "Happiness Score"]))        # lotr_ngrams
# fig1 = word_shifts(first_freqs, second_freqs, first_avg, ["Prequels", 'Original Trilogy']) 
# fig2 = word_shifts(second_freqs, first_freqs, second_avg, ["Original Trilogy", "Prequels"])
# fig3 = word_shifts(second_freqs, first_freqs, 5, ["Original Trilogy", "Prequels"])

