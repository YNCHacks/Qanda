import sys
import nltk
import numpy
import urllib
import urllib2
import httplib2
import xml.etree.ElementTree as ET
import goslate
import subprocess
import os
import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
from nltk.corpus import wordnet
import string
 
from twilio_control import *

from app.views import *

verbose = True

# Get default English stopwords and extend with punctuation
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)
stopwords.append('')
 
def set_verbose(val):
    if(bool(val)==True):
        verbose=True
    else:
        verbose=False

def get_verbose():
    return verbose

def get_wordnet_pos(pos_tag):
    if pos_tag[1].startswith('J'):
        return (pos_tag[0], wordnet.ADJ)
    elif pos_tag[1].startswith('V'):
        return (pos_tag[0], wordnet.VERB)
    elif pos_tag[1].startswith('N'):
        return (pos_tag[0], wordnet.NOUN)
    elif pos_tag[1].startswith('R'):
        return (pos_tag[0], wordnet.ADV)
    else:
        return (pos_tag[0], wordnet.NOUN)
 
# Create tokenizer and stemmer
tokenizer = nltk.tokenize.punkt.PunktWordTokenizer()
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
 
def nlp_string_match(a, b, threshold=0.5):
    """Check if a and b are matches."""
    pos_a = map(get_wordnet_pos, nltk.pos_tag(tokenizer.tokenize(a)))
    pos_b = map(get_wordnet_pos, nltk.pos_tag(tokenizer.tokenize(b)))
    lemmae_a = [lemmatizer.lemmatize(token.lower().strip(string.punctuation), pos) for token, pos in pos_a \
                    if pos == wordnet.NOUN and token.lower().strip(string.punctuation) not in stopwords]
    lemmae_b = [lemmatizer.lemmatize(token.lower().strip(string.punctuation), pos) for token, pos in pos_b \
                    if pos == wordnet.NOUN and token.lower().strip(string.punctuation) not in stopwords]
 
    # Calculate Jaccard similarity
    ratio = len(set(lemmae_a).intersection(lemmae_b)) / float(len(set(lemmae_a).union(lemmae_b)))
    return ratio

mom_faq = ["Can an S Pass holder apply to be a Singapore Permanent Resident (PR)?",
						"Can I choose my preferred card delivery date or time?",
						"Can pass holders travel in and out of Singapore if they have not received the pass card?",
						"What is Annual Wage Supplement (AWS)?",
						"Can a Dependant's Pass holder work in Singapore?",
						"Can any person receive the work pass card from the delivery person?",
						"What should I do if the card delivery person does not show up?",
						"Can an employer terminate the service of their employee without a termination letter?",
						"Does the employee need to sign on the termination letter?",
						"Does the employer need to sign on the employee's resignation letter?"
						"An employee has tendered resignation and is serving 1 month's notice according to the terms in their employment contract. Can the employer inform the employee not to serve the notice, and ask the employee to leave employment immediately?",
						"Is an employee entitled to another day off if a public holiday falls on a rest day or non-working day?",
						"Must employers house their workers at the dormitories listed on the MOM website?",
						"Where can I find the list of Licensed Employment Agencies?"]

def play(filename):
	vlc_path = os.path.exists(os.path.join("C:/","Users","Hrishi","Desktop","ManpowerHackathon","temp.mp3"))
	file_path = os.path.exists(os.path.join("C:/", "Program Files", "VideoLAN", "VLC", "vlc.exe"))
	p = subprocess.Popen([vlc_path,file_path])
	return None

def request(query):
    query = urllib.urlencode({'input':query})
    app_id = "Q6254U-URKKHH9JLL"
    wolfram_api = "http://api.wolframalpha.com/v2/query?appid="+app_id+"&format=plaintext&podtitle=Result&"+query
    resp, content = httplib2.Http().request(wolfram_api)
    return content

def response(query):
    content = request(query)    
    root = ET.fromstring(content)
    error = root.get('error')
    success = root.get('success')
    numpods = root.get('numpods')
    answer= ''
    if success and int(numpods) > 0 :
        for plaintext in root.iter('plaintext'):
            if isinstance(plaintext.text, str) :
                answer = answer + plaintext.text
        return answer
    elif error:
        return "404"
 
#----------------------------------------------------------------------
def get_google_voice(phrase,lang,file_name):
    """
    Function that will send http request to google translate
    and save audio file from responce with voiced input phrase.
    Parameters:
    @phrase: phrase to voice.
    Returns:
    If ok - name of created file, else - returns None.
    """
    
    language=lang #Setting language.
    url = "http://translate.google.com/translate_tts" #Google translate url for getting sound.
    user_agent="Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5." 
    #file_name="temp.mp3" #Temp file for saving our voiced phrase.
 
    params = urllib.urlencode({'q':phrase, 'tl':language}) #query parameters.
    request = urllib2.Request(url, params) #http request.
    request.add_header('User-Agent', user_agent) #adding agent as header.
    response = urllib2.urlopen(request) 
    
    if response.headers['content-type'] == 'audio/mpeg':
        with open(file_name, 'wb') as file:
            file.write(response.read())
        return file_name
    else:
        return None

def keywordize(message):
	keywords = []
	index=0

	tokens = nltk.word_tokenize(message)
	tag = nltk.pos_tag(tokens)

	
	if(verbose==True):
		print "Message has been processed - "
		print tag
		
	#print "Message tagged: "
	#print tag

	for x in range(0,len(tag)):
		if(tag[x][1]=='NN' or tag[x][1]=='NNP' or tag[x][1]=='NNPS' or tag[x][1]=='NNS'):
			if(x==0 or (tag[x-1][1]!='NN' and tag[x-1][1]!='NNP' and tag[x-1][1]!='NNPS' and tag[x-1][1]!='NNS')):
				noun = ""
				while(x<len(tag) and (tag[x][1]=='NN' or tag[x][1]=='NNP' or tag[x][1]=='NNPS' or tag[x][1]=='NNS')):
					noun = noun+" "+tag[x][0]
					x+=1
				keywords.append(noun)
				index+=1
	return keywords

def askwolfandtranslate(question):
	print("Connecting...")

	resp = response(question)

	if(resp=='404'):
		return None

	lang = 'en'
	lang = raw_input("Please enter the language code (hi for Hindi, ta for Tamil, zh for Chinese and en for English: ")

	if(lang!='en'):
		resp = gs.translate(resp,lang).encode('utf-8')

	count=0;
	while(len(resp)>100): #break it up
		count+=1
		for x in range(100,0,-1):
			if(resp[x]==' '):
				get_google_voice(resp[0:x],lang,"temp"+str(count)+".mp3")
				resp = resp[x:len(resp)]
				break
			elif(x<=1):
				get_google_voice(resp[0:100],lang,"temp"+str(count)+".mp3")
				resp = resp[100:len(resp)]

	return get_google_voice(resp,lang,"temp"+str((count+1))+".mp3")

def askwolf(question):
	return response(question)

def speak(resp, lang, filename_prefix='temp'):
	gs = goslate.Goslate()

	if(lang!='en'):
		resp = gs.translate(resp,lang).encode('utf-8')

	count=0;
	while(len(resp)>99): #break it up
		count+=1
		for x in range(99,0,-1):
			if(resp[x]==' '):
				get_google_voice(resp[0:x],lang,filename_prefix+str(count)+".mp3")
				resp = resp[x:len(resp)]
				break
			elif(x<=1):
				get_google_voice(resp[0:99],lang,filename_prefix+str(count)+".mp3")
				resp = resp[100:len(resp)]

	if(verbose==True):
		print "Translation Successful."

	return get_google_voice(resp,lang,filename_prefix+str((count+1))+".mp3")
