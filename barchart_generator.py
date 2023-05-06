
def create_criminal_dataFrame(folder_path: str, file_names: list):
    """
    Returns a pandas DataFrame containing file names and their contents.
    The DataFrame has columns: 'name', 'Text'

    Description:
    Creates a dataframe of criminals and the words of their text 

    Params:
    folder: folder name as a string
    file_names: list of file names without any extensions

    Returns:
    text_df: dataframe containing two columns -- 'name' and 'Text' 
    """
    # create an empty list to store the results
    results = []

    # loop over the file names and apply the function to each file
    for file_name in file_names:
        with open(folder_path + '/' + file_name, 'r') as f:
            text = f.read()
        file_df = pd.DataFrame({'name': [file_name.strip('.txt')],
                                'Text': [text]})
        results.append(file_df)
    text_df = pd.concat(results)
    return text_df


def get_expanded_df(criminal_df:pd.DataFrame):
    """
    expands a dataframe of criminal and their text
    Params:
    criminal_df: data frame of all criminal transcripts
    Returns:
    words_expanded: dataframe of criminal name, words, danger, power
    """

    criminal_df[c.words_col] = criminal_df[c.text_col].str.split()
    words_expanded = criminal_df.explode(c.words_col) 
    words_expanded[c.words_col] = words_expanded[c.words_col].map(str)
    words_expanded[c.words_col] = words_expanded[c.words_col].str.lower()
    words_expanded[c.words_col] = [re.sub(r'[^\w\s]', '', word) for word in list(words_expanded[c.words_col])]
    power_danger = pd.read_table(c.ousio_dat, usecols=[c.ousiowords, c.ousiopower, c.ousiodanger])
    word_in_lex = lambda x: True if x in list(power_danger[c.ousiowords]) else False
    power_func = lambda x, y: list(power_danger[(power_danger == x).any(axis=1)].to_dict()[y].values())[0] if word_in_lex(x) else np.nan
    words_expanded[c.ousiopower] = [power_func(word, c.ousiopower) for word in list(words_expanded[c.words_col])]
    words_expanded[c.ousiodanger] = [power_func(word, c.ousiodanger) for word in list(words_expanded[c.words_col])]
    #words_expanded.dropna(inplace=True)
    return words_expanded


def create_barcharts(criminal_df:pd.DataFrame):
    """
    expands a dataframe of criminal and their text
    Params:
    criminal_df: data frame of all criminal transcripts
    Returns:
    none
    """

 
    my_df = get_expanded_df(criminal_df)

    # count the number of occurrences of each name and number of non-nan scores
    counts = my_df['name'].value_counts().sort_index()
    power_scored = my_df.groupby('name')['power'].count().sort_index()
    danger_scored = my_df.groupby('name')['danger'].count().sort_index()        # don't need this


    counts_df = pd.DataFrame({'name': counts.index,     
                                   'total count': counts.values,
                                   'power scored': power_scored,
                                   'danger scored': danger_scored
                                   })


    counts_df.reset_index(drop=True, inplace=True)


    # Set the style to 'darkgrid'
    plt.style.use('dark_background')
    # Create the bar plot
    plt.figure(figsize=(15,15))
    plt.rc('font', size=c.text_size) 
    plt.subplots_adjust(bottom=0.15)
    
    sns.barplot(x=counts_df['name'], y=counts_df['total count'], color='gray')
    sns.barplot(x=counts_df['name'], y=counts_df['power scored'],color='teal')
    
    # Set the title and axis labels
    plt.title('Total Words vs Scored Words')
    plt.xlabel('Name')
    plt.ylabel('Count')
    plt.xticks(rotation=90)
    

    # Display the plot
    plt.savefig('barchart.png')
    plt.show()





#----------------------------------------------------------------------------------
#----------------------------Generate----------------------------------------------
#----------------------------------------------------------------------------------
# Define global variables 
df_lexicon_scores = pd.read_table('ousiometry_data_augmented.tsv')
folder_path = 'shooters_words_text'
file_names = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

# Create criminal dataframe
crim_df = create_criminal_dataFrame(folder_path, file_names)

# Generate barchart
create_barcharts(crim_df)
