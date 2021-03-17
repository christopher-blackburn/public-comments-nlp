from sklearn.feature_extraction.text import TfidfVectorizer


# You will need to import your stopwords
stop_words = set(stopwords.words('english'))


# A function for generating a tf-idf dataframe
def tfidf(corpus,grams,stops=True):
    
    
    if stops == True:
        
        vectorizer = TfidfVectorizer(min_df=1,stop_words=stop_words,
                                 sublinear_tf=False,smooth_idf=True,ngram_range=grams)
    elif stops == False:
        
        vectorizer = TfidfVectorizer(min_df=1,stop_words=None,
                                 sublinear_tf=False,smooth_idf=True,ngram_range=grams)
    
    # Generate the TF-IDF matrix
    model = vectorizer.fit_transform(corpus)

    # Create a pandas dataframe from the TF-IDF matrix
    tfidf_matrix = pd.DataFrame(model.todense().T)
    tfidf_matrix['tokens'] = list(vectorizer.get_feature_names())
    
    return tfidf_matrix

def mostCommon(tfidf_mat,doc):
    
    return tfidf_mat[['tokens',doc]].sort_values(by=doc,ascending=False).head(10)



# Extract the top 10 most common grams, with stop words removed
unigrams_stops = [mostCommon(tfidf(combined_docs,(1,1),stops=True),doc) for doc in range(0,len(combined_docs))]
bigrams_stops = [mostCommon(tfidf(combined_docs,(2,2),stops=True),doc) for doc in range(0,len(combined_docs))]
trigrams_stops = [mostCommon(tfidf(combined_docs,(3,3),stops=True),doc) for doc in range(0,len(combined_docs))]

for idx in range(0,len(combined_docs)):
    plt.subplots(figsize=(10,12))
    plt.barh(unigrams_stops[idx]['tokens'],unigrams_stops[idx][idx],label='Unigrams')
    plt.barh(bigrams_stops[idx]['tokens'],bigrams_stops[idx][idx],label='Bigrams')
    plt.barh(trigrams_stops[idx]['tokens'],trigrams_stops[idx][idx],label='Trigrams')
    plt.gca().invert_yaxis()
    plt.xlabel('Term Frequency-Inverse Document Frequency')
    plt.ylabel('Most Frequent Unigrams, Bigrams, and Trigrams')
    plt.legend()
    plt.savefig('/Users/cblackburn/Downloads/tfidf{}.png'.format(idx),bbox_inches='tight')
    plt.close()