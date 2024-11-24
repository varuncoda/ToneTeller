import json
from flask import Flask,redirect,url_for,request,render_template
app = Flask(__name__)
from googleapiclient.discovery import build

from nrclex import NRCLex
import nltk
nltk.download('punkt_tab')
nltk.download('stopwords')
#nltk.download('omw-1.4')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
#@app.route('')
def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

@app.route('/hi')
def hello_world():
   return render_template('index.html')


@app.route('/ji')
def ni():
    return 'hi'


@app.route('/stats/<name>')
def stats(name):
    x=open(name,'r')
    word=x.readline()
    second_word=x.readline()
    x.close()
    my_api_key = 'READ_FROM_LOCAL_FILE'
    my_cse_id = 'READ_FROM_LOCAL_FILE'
    #print(word, second_word)

    num_results=6
    results = google_search(
    word, my_api_key, my_cse_id, num=num_results)
    
    #
    # print("second is ="+second_word)
    second_results= google_search(
    second_word, my_api_key, my_cse_id, num=num_results)
    urls=[]
    second_urls=[]
    for i in range(0,num_results):
       result=results[i].get("link")
       result2=second_results[i].get("link")
       urls.append(result)
       second_urls.append(result2)



    dictionaries=[]
    new_dicts=[]

    for url in urls:
       headers={'User-Agent':'Mozilla/5.0'}

       try:
          request=Request(url,headers=headers)
          response=urlopen(request)
          html=response.read()
     
       except Exception as e:
        html=""
       
       
       soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
       for script in soup(["script", "style"]):
         script.extract()    # rip it out
 
       
# get text
       text = soup.get_text()

      # print(text)

# break into lines and remove leading and trailing space on each
       #lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
       #chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
       #text = '\n'.join(chunk for chunk in chunks if chunk)

       #print(text)

   
       sentence=nltk.sent_tokenize(text)

       



       sentence=text

       #print(sentence)

       emotion=NRCLex(sentence)

       emotion=emotion.affect_frequencies

       positive=emotion.get('positive')

       json_dict = json.dumps(emotion)

       #print(json_dict)

       dictionaries.append(json_dict)

       x=2015

       print('done with:', url)
       
       #//////////////////////////
    for url in second_urls:
         headers={'User-Agent':'Mozilla/5.0'}

         try:
             request=Request(url,headers=headers)
             response=urlopen(request)
             html=response.read()
         except HTTPError as e:
          if e.code==403:
             pass
          else:
             pass
         except URLError as e:
            pass
         except Exception as e:
            pass
       
       
         soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
         for script in soup(["script", "style"]):
            script.extract()    # rip it out
   
       
# get text
         text = soup.get_text()

         sentence=nltk.sent_tokenize(text)

         


         sentence=text

       #print(sentence)

         emotion=NRCLex(sentence)

         emotion=emotion.affect_frequencies

         positive=emotion.get('positive')

         json_dict = json.dumps(emotion)

       #print(json_dict)

         new_dicts.append(json_dict)
         
         print('done with: ',url)
       
         
    #print(dictionaries)
    print(new_dicts)
    return render_template('graph.html' ,urls=dictionaries,line=new_dicts,Word1=word.strip(),Word2=second_word.strip())








@app.route('/text',methods = ['POST', 'GET'])
def text():
   if request.method == 'POST':
      x = request.form['nm'] 
      y=request.form['nm2']
      w=open('s.txt','w')
      w.write(x)
      w.write('\n'+y)
      w.close()
      return redirect(url_for('stats',name = 's.txt'))
   else:
      x = request.args.get('nm')
      return redirect(url_for('stats',name = x))


if __name__ == '__main__':  
    app.run(debug = True)
   