from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pandas as pd
from pandas import DataFrame as DF
import re
from wordcloud import WordCloud
from konlpy.tag import Hannanum
from collections import Counter
import time
import matplotlib.pyplot as plt
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.io as po
from IPython.core.display import Image as image


app = Flask(__name__)



@app.route("/upload")
def render_file():
    return render_template('upload.html')

@app.route('/result', methods = ['GET', 'POST'])
def result():
    if request.method == 'POST':
        f = request.files['file']
        #저장할 경로 + 파일명
        f.save('uploads/'+secure_filename(f.filename))
        #with open('uploads/'+(f.filename)) as data:
        #    lines = data.readlines()
        with open('uploads/'+(f.filename), 'r') as file:
            data = file.readlines()
    
    li = ' '.join(data)
    li = li.split()
    
    file = open("static/stopwords.txt")
    stop = file.readlines()
    for i in range(len(stop)):
        stop[i] = stop[i].strip()
    
    result = []
    for i in li:
        if i not in stop:
            result.append(i)

    li2 = ' '.join(result)
    li3 = re.sub('[!@#$%^&*()-+[]{}♥:;?/,""]', '',li2)
    li4 = re.sub('[ㄱ-ㅎㅏ-ㅣ0-9a-zA-Z]', '',li3)
    li5 = re.sub('[♥&;#,""]', '',li4)

    t =Hannanum()
    key = t.nouns(li5)
    for i,v in enumerate(key):
        if len(v)<2:
            key.pop(i)

    count = Counter(key)
    tags = count.most_common(50)
    
    font_path = 'static/NotoSans-Black.otf'
    wordcloud = WordCloud(font_path=font_path, background_color="white", width=800, height=800).generate_from_frequencies(dict(tags))
    fig = plt.figure(figsize=(6,6))
    plt.imshow(wordcloud)
    plt.axis('off')
    fig.savefig('static/wordcloud.png')
       
    data2 = DF(tags)
    data2.columns=['keyword','freq']
       
    trace1 = go.Bar(x=data2['keyword'], y=data2['freq'])
    dataset = [trace1]
    layout = go.Layout(font=dic(family="NanumGothic"))
    fig2 = go.Figure(data=dataset, layout=layout)
    
    fig2.write_image("static/plot.png", width=800, height=800)
    
    return render_template('result.html', value=tags, time=time.time())









if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
