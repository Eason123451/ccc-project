from transformers import pipeline
import requests
import string
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
import ssl
import certifi
import torch

ssl._create_default_https_context = ssl._create_unverified_context
nltk.download('punkt')

def get_mastodon_data(port,size):
    fission_url = f"http://localhost:{port}/mastodon/{size}"
    response = requests.get(fission_url, verify = False)
    return response.json()


def check_crime_related(content, keywords):
    stemmer = PorterStemmer()
    
    keyword_stems = {stemmer.stem(keyword) for keyword in keywords}
    
    content_lower = content.lower()
    content_clean = content_lower.translate(str.maketrans('', '', string.punctuation))
    
    words = word_tokenize(content_clean)
    word_stems = {stemmer.stem(word) for word in words}
    
    return any(keyword in word_stems for keyword in keyword_stems)



def mastodon(port, size):
    if size < 0:
        return print('Check size')
    data = get_mastodon_data(port, size)
    filtered_data = [{'time': item['_source']['created_at'], 'content': item['_source']['content']} for item in data]
    
    print(f"Total Mastodon posts fetched: {len(filtered_data)}")  # Print the total size of Mastodon data fetched

    crime_keywords = ['crime', 'theft', 'murder', 'assault', 'fraud', 'robbery', 'burglary', 'arson', 
                      'kidnapping', 'drug', 'trafficking', 'violence', 'vandalism', 'smuggling', 'extortion', 
                      'blackmail', 'embezzlement', 'bribery', 'corruption', 'homicide', 'manslaughter', 'gang', 
                      'terrorist', 'terrorism', 'assault', 'battery', 'abuse', 'harassment', 'molestation', 
                      'rape', 'domestic violence', 'cybercrime', 'identity theft', 'forgery', 'counterfeit', 
                      'human trafficking', 'organized crime', 'illegal', 'unlawfully', 'laundering', 
                      'money laundering', 'perjury', 'prostitution', 'racket', 'racketeering', 'sabotage', 
                      'scam', 'shoplifting', 'slander', 'stalking', 'swindle', 'terrorism', 'threat', 
                      'trespassing', 'underworld', 'weapon', 'weapons', 'smuggling', 'conspiracy']

    crime_related_records = [item for item in filtered_data if check_crime_related(item['content'], crime_keywords)]
    
    print(f"Total crime-related posts: {len(crime_related_records)}")  # Print the size of crime-related posts

    if len(crime_related_records) == 0:
        print('None of', size, 'posts are related to crime')
    else:
        classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english", truncation=True)
        results = classifier([item['content'][:512] for item in crime_related_records])  # Truncate manually if needed

        print(f"{len(crime_related_records)} of {len(filtered_data)} may be related to crime", '\n')
        for record, result in zip(crime_related_records, results):
            print('Time:', record['time'][0:10], record['time'][11:18])
            print('Content:', record['content'])
            print('Sentiment:', result['label'], '\n')