from transformers import pipeline
import requests
import string
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

def get_mastodon_data(port,size):
    fission_url = f"http://localhost:{port}/mastodon/{size}"
    response = requests.get(fission_url, verify = False)
    return response.json()

data = get_mastodon_data(port,9088)

filtered_data = [{'time': item['_source']['created_at'], 'content': item['_source']['content']} for item in data]

crime_keywords = ['crime', 'theft', 'murder', 'assault', 'fraud', 'robbery', 'burglary', 'arson', 
                  'kidnapping', 'drug', 'trafficking', 'violence','vandalism', 'smuggling', 'extortion', 
    'blackmail', 'embezzlement', 'bribery', 'corruption', 'homicide', 'manslaughter', 'gang', 
    'terrorist', 'terrorism', 'assault', 'battery', 'abuse', 'harassment', 'molestation', 
    'rape', 'domestic violence', 'cybercrime', 'identity theft', 'forgery', 'counterfeit', 
    'human trafficking', 'organized crime', 'illegal', 'unlawfully', 'laundering', 
    'money laundering', 'perjury', 'prostitution', 'racket', 'racketeering', 'sabotage', 
    'scam', 'shoplifting', 'slander', 'stalking', 'swindle', 'terrorism', 'threat', 
    'trespassing', 'underworld', 'weapon', 'weapons', 'smuggling', 'conspiracy']

def check_crime_related(content, keywords):
    stemmer = PorterStemmer()
    
    keyword_stems = {stemmer.stem(keyword) for keyword in keywords}
    
    content_lower = content.lower()
    content_clean = content_lower.translate(str.maketrans('', '', string.punctuation))
    
    words = word_tokenize(content_clean)
    word_stems = {stemmer.stem(word) for word in words}
    
    return any(keyword in word_stems for keyword in keyword_stems)


crime_related_records = [item for item in filtered_data if check_crime_related(item['content'], crime_keywords)]

classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

results = classifier([item['content'] for item in crime_related_records])


if len(crime_related_records) == 0:
    print('None of',size,'are related to crime')
else:
    print(len(crime_related_records),'of',size,'may be related to crime', '\n')
    for record, result in zip(crime_related_records, results):
        print('Time:', record['time'][0:10], record['time'][11:18])
        print('Content:',record['content'])
        print('Sentiment:', result['label'], '\n')