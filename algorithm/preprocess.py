from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np

lemma = WordNetLemmatizer()

# > -------------------------------------------------------------------
# > ----------- Pre processing, removing stop words, apstrophes -------
# > ----------- punctuation, lowercase, etc return a data set ---------
# > ----------- combining desc and tags -------------------------------
# > -------------------------------------------------------------------

# > return final dataset
def preprocess(desc, tags):

    dataset = create_dataset(desc, tags)
    lowercase(dataset)
    dataset = rem_stopwords(dataset)
    dataset = rem_punct(dataset)
    #print("done\n\n\n\n")
    dataset = rem_apostrophes(dataset)
    dataset = rem_chars(dataset)
    dataset = lemmatize(dataset)
    #dataset = numbers_words(dataset)
    dataset = ' '.join(dataset)

    return(dataset)

# > creates the dataset from the object, Venue or Talent
def create_dataset(desc, tags):

    dataset = []

    # > ----- Combining desc and tags into one dataset -------- <

    for w in desc.split():
        dataset.append(w)

    #for tag in tags.split(","):
    for tag in tags.split(","):
        dataset.append(tag)

    #print(dataset)

    return(dataset)

# > Makes all values lowercase
def lowercase(dataset):

    for i in range(len(dataset)):
        dataset[i] = dataset[i].lower()

    return(dataset)

# > Removes stop words from the set
def rem_stopwords(dataset):

    datasetFinal = []

    for word in dataset:
        if word not in stopwords.words('english'):
            datasetFinal.append(word)

    return(datasetFinal)

# > removes punctuation
def rem_punct(dataset):

    symbols = "!\"#$%&()*+-.,/:;<=>?@[\]^_`{|}~\n"

    for i in symbols:
        dataset = np.char.replace(dataset, i, '')

    return(dataset)

# > removes apostrophes
def rem_apostrophes(dataset):

    # > From the dataset, remove appostrophes
    dataset = np.char.replace(dataset, "'", "")
    return dataset

# > removes single characters
def rem_chars(dataset):

    # print(type(dataset))
    #print(np.where(dataset == 'i'))

    datasetNew = []

    for w in dataset:
        if len(w) != 1:
            #np.delete(dataset, np.where(dataset == w))
            datasetNew.append(w)

    return datasetNew

# > Lemmatizes the words > turns them into their core word
def lemmatize(dataset):

    datasetNew = []

    for w in dataset:
        datasetNew.append(lemma.lemmatize(w))

    return datasetNew

# > changes the int values into str representations
def numbers_words(dataset):

    datasetNew = []

    # print(num2words("hello"))

    for w in dataset:
        print(type(w))

    return datasetNew

# > -------------------------------------------------------------------