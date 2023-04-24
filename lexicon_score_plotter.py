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
import math



def Plot_Danger_Or_Power(df, plot_type):
    """
    Description: 
    Creates a grid of plots for each unique name in the dataframe,
    with 'danger' on the y-axis and word number on the x-axis.

    params: 
            df = pandas dataframe of name, token, danger, power
            plot_type = 'danger' or 'power'

    returns: 
            none
    """
    plt.style.use('dark_background')

    # define color for each plot type
    if plot_type == 'danger':
        color = 'crimson'
    if plot_type == 'power':
        color = 'darkorchid'

    # plot by name
    groups = df.groupby('name')

    # create plot layout
    n = len(groups)
    nrows = math.ceil(math.sqrt(n))
    ncols = math.ceil(n/nrows)
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(12,8))
    axs = axs.ravel()
    
    # iterate over each group and create a plot for each name
    for i, (name, group) in enumerate(groups):
        # get the x and y values for the plot
        x = range(1, len(group)+1)
        y = group[plot_type]
        
        # plot the data on the appropriate subplot
        ax = axs[i]
        ax.plot(x, y, color=color)
        
        # Set the title and labels for the subplot
        ax.set_title(name)
        ax.set_xlabel('word number')
        ax.set_ylabel(plot_type)
    
    # remove unused subplots from the grid
    for j in range(i+1, nrows*ncols):
        fig.delaxes(axs[j])

    # modify plot layout
    plt.tight_layout()
    
    # save plot to disk
    plt.savefig('my_'+str(plot_type)+'.png')
    



def Get_Tokens_List(book_name):

    '''
    Description: 
    Tokenizes words of a given text
            
    Params: 
            Filename.txt
            
    Returns: 
            List of words/tokens in the .txt file
    '''
    
    file = open(book_name, 'r') 
    text = file.read()

    word_regex = r'\b\w+\b'
    punct_regex = r'[^\w\s]'
    #dot_regex = r'\.+'
    dot_regex = r'\.{4,}|\.{3}|\.{2}|\.'
    text = text.replace('\n', ' ')
    text = text.split(' ')
    text = [entry for entry in text if entry.strip()]
    text = [entry.lower() for entry in text]
    text_string = ' '.join(text)

    # define a list to hold the resulting tokens
    tokens = []
    # iterate over the matches of the regular expressions and append them to the tokens list
    for match in re.finditer(f'{dot_regex}|{punct_regex}|{word_regex}', text_string):
        token = match.group()
        if re.match(word_regex, token):
            tokens.append([token])
        elif re.match(dot_regex, token):
            tokens.append([token])
        else:
            # split the token into parts that consist of either dots or non-dots
            parts = re.findall(f'(?:{dot_regex})+|[^\.\s]+', token)
            for part in parts:
                tokens.append([part])
    tokens_list = [''.join(entry) for entry in tokens]

    return tokens_list



def Get_Token_Scores(tokens, df_lexicon_scores, score_type):

    '''
    Description: Gets the token scores from the lexicon 
    
    Params: 
            tokens: list of tokenized text 
            lexicon: pandas dataframe
            score_type: string
    
    Returns: 
            List of the scores that correspond to the tokens list
    
    '''

    # create a dataframe from the tokens list
    df_tokens = pd.DataFrame({'word': tokens})
    
    # merge the tokens dataframe with df_lexicon_scores 
    df_scores = pd.merge(df_tokens, df_lexicon_scores[['word', score_type]], on='word', how='left')   # score_type can be power, danger, etc...
    
    # replace scores for words not in lexicon with np.nan
    df_scores[score_type] = np.where(df_scores[score_type].isnull() & df_scores['word'].isin(tokens), np.nan, df_scores[score_type])

    # return the scores as a list
    return df_scores[score_type].tolist()



def Create_Score_DataFrame(lexicon, folder_path, file_names):
    """
    Description: 
            Creates a dataframe of name, token, danger, power
    
    params:
            lexicon: pandas dataframe
            folder_path: string
            file_names: list of strings
            
    returns:
            scores_df: pandas dataframe
    """

    # create an empty list to store the results
    results = []

    # loop over the file names and apply the function to each file
    for file_name in file_names:

        # apply the function to the file contents
        tokens_list = Get_Tokens_List(folder_path + '/' + file_name)

        # get the scores for each token using the lexicon
        danger_scores_list = Get_Token_Scores(tokens_list, lexicon, 'danger')
        power_scores_list = Get_Token_Scores(tokens_list, lexicon, 'power')

        # create a DataFrame with the results for this file
        file_df = pd.DataFrame({'name': [file_name.strip('.txt')]*len(tokens_list),
                                'token': tokens_list,
                                'danger': danger_scores_list,
                                'power': power_scores_list})

        # append the file_df to the list of results
        results.append(file_df)

    # concatenate all the results into a single DataFrame
    scores_df = pd.concat(results)

    return scores_df





    
# Actually create the plots...

df_lexicon_scores = pd.read_table('ousiometry_data_augmented.tsv')
folder_path = 'shooters_words_text'
file_names = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

df = Create_Score_DataFrame(df_lexicon_scores, folder_path, file_names)
Plot_Danger_Or_Power(df, 'danger')
Plot_Danger_Or_Power(df, 'power')










