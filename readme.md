# Elsagate-Detector
> 基於深度學習的網路幼兒影片過濾系統
> 作者：游照臨 2019/02/09
## 緒論
### 發想動機
~~因為寒假邊緣人沒朋友，只好在家摳頂，突然想到之前看過ㄉ網路都市傳說，然後這個專案程式寫ㄌ1個晚上，這篇文打ㄌ1ㄍ小時...就不小心生出來ㄌ.....。~~

隨著現代網路速度飛速的增加，使得網路隨選視訊的普及率與日俱增，在台灣，非常多使用者都有觀看網路影片(Youtube)的習慣。年輕一輩的父母對於嬰幼兒也常常直接開啟手機平板等裝置，直接交給小朋友們觀看，並鮮少注意到其觀看的影片內容。

根據2016年6月，英國三大報之一的《衛報》報導了該年3月起，Youtube盛行的幼兒頻道，累積觀看次數達到17億，該頻道的影片包括人們身穿蜘蛛人、小丑和艾莎等著名角色的服裝做出荒謬行為；影片沒有對話，但有獵奇的背景音樂，而其中以冰雪奇緣之女主角Elsa，佔最多數。其影片包含的主題並不適合兒童，比如呈現暴力、性愛、戀物癖和廁所幽默等內容，以及涉及危險或破壞的情況和活動。

該類型之影片於現代被稱之為"Elsagate"([艾莎門](https://zh.wikipedia.org/wiki/%E8%89%BE%E8%8E%8E%E9%97%A8))，

許多人懷疑該類影片是由人工智慧自動產生，借以使幼兒產生不良的價值觀，根據Youtube推播建議影片之演算法，只要不斷的點擊建議影片，最終皆會導至ElsaGate之影片[1]，其點閱率甚至高至數以億計。Youtube也基於兒童內容逐漸審核相關頻道，但成效不佳，該類型影片仍以雨後春筍般出現。

本專案將透過深度學習技術，透過人工智慧方式實作影片辨識，借以篩選出不適合兒童觀看的影片，並嘗試以瀏覽器套件阻擋。

Ref：
[1][【實測】YouTube的自動播放功能最後到底會連到什麼影片? | 啾啾鞋](https://www.youtube.com/watch?v=HMxT-MCRmh4)
[2][ A group of perverts are targeting kids on YouTube. I used to work for them.](https://www.reddit.com/r/nosleep/comments/7d5in3/a_group_of_perverts_are_targeting_kids_on_youtube/)
[3][ 偽裝成卡通的變態影片！Elsa Gate到底是什麼東西？](https://medium.com/shasha77/elsa-gate-f3f10a4eb2ed)
[4][ [爆卦] 變態鎖定觀看YouTube孩童 (已知資訊整理)](https://disp.cc/b/163-aqFk)

## 使用技術
- 程式語言
    - Python 3.6
        - OpenCV
        - Tensorflow
        - Keras
        - Requests
        - BeautifulSoup4
        - flask
        - Jupyter lab
    - JavaScript
        - jQuery (AJAX)
- 開發環境
    - Windows 10 x64
    - Google Colab
        - Linux 419e1997a3db 4.14.79+ #1 SMP Wed Dec 19 21:19:13 PST 2018 x86_64 x86_64 x86_64 GNU/Linux

## 內容
### 資料蒐集
為了建立深度學習模型，需要蒐集Elsa Gate影片之樣本，透過擷取Youtube頻道網址，如:
> https://www.youtube.com/channel/UCq4Q8xs98pnvEc6nWfm9ObQ/video

並使用Requests將其html爬取，以BeautifulSoup解析後可以觀察出影片標題的網址皆為
> https://i.ytimg.com/vi/id/hqdefault.jpg

透過該規律，人工選取幾個頻道放入程式中即可蒐集出Elsa Gate之影片封面照片。
``` python
import requests
import time
from bs4 import BeautifulSoup

def getImgUrl(url): #ChennelURL
    rt = []
    res = requests.get(url)
    for i in BeautifulSoup(res.text,'html.parser').find_all('img'):
        if 'i.ytimg.com' in i['src']:
            d = i['src'].find('?')
            rt.append(i['src'][:d])
    return rt
    
def downloadImg(urls): #imgURLs
    for i in urls:
        file_name = str(time.time()).replace('.','')
        with open('./n/{}.jpg'.format(file_name) , 'wb') as f:
            res = requests.get(i)
            f.write(res.content)
        print(file_name,' OK!')

def saveImg(urls): #ChennelUrls
    for url in urls:
        with open('urls_n.txt','a+') as f:
            f.write(url + '\n')
        imgUrls = getImgUrl(url)
        downloadImg(imgUrls)
        
```
用以上方法，就可快速的蒐集出Elsa Gate影片封面以及正常的Youtube影片
- Elsa Gate影片
    ![](https://i.imgur.com/D1ilbAg.jpg)
- 正常影片
    ![](https://i.imgur.com/qCUyMG5.jpg)

### CNN辨識
資料蒐集完畢後，需要進行CNN的影像辨識，本次使用Keras作為主要的訓練框架，因為Lab的電腦死掉了QQ，自己家裡的GPU也不夠力，因此此段的人工智慧訓練採用了Google提供的免費雲端開發平台:Colab。可以將資料放置於Google Drive 並直接由Colab讀取出。
```Python
from google.colab import drive
drive.mount('/content/gdrive')
```

透過了2次的Convolution，並透過relu來進行activation
MaxPolling的PoolSize為2x2
Fully Connected則使用了雙層128個神經元
最終透過Softmax作為兩種輸出
優化器使用adam
```python
classifier = Sequential()
conv = Conv2D(32,(3,3),input_shape = (50,50,3) , activation = 'relu')
classifier.add(conv)

mp = MaxPooling2D(pool_size = (2,2))
classifier.add(mp)

conv1 = Conv2D(32,(3,3),activation = 'relu') 
classifier.add(conv1)

mp1 = MaxPooling2D(pool_size = (2,2))
classifier.add(mp1)

classifier.add(Flatten())

classifier.add(Dense(units = 128 , activation = 'relu'))
classifier.add(Dense(units = 128 , activation = 'relu'))
classifier.add(Dense(units = 2 , activation = 'softmax'))

classifier.compile(optimizer='adam',
    loss = 'categorical_crossentropy',
    metrics = ['accuracy'])

```
運用Colab平台訓練1000次，約使用了30分鐘，以下為訓練結果。
- acc
    ![](https://i.imgur.com/CrvKIHa.png)

- loss
    ![](https://i.imgur.com/gqrzuxI.png)

- val_acc
    ![](https://i.imgur.com/0Vt7EJO.png)

- val_loss
     ![](https://i.imgur.com/rHFixzO.png)
訓練結果不太完美，但是勉強可以用ㄌQQ

將訓練的模型下載回本地端，最方便施作的方式是透過Python的套件pickle包裝，pickle為一款可將python內部變數、物件等資訊做serialization，並以binary的方式儲存為檔案

```python
import pickle
data = {
    'classifier':classifier,
    'history':history
}
with open('pickle.data','wb') as f:
    pickle.dump(data, f)
```

### 判斷
現階段的classifier為輸入圖片，則可產生判斷結果，我們將其搭配上Python的套件Requests，改以爬蟲方式，輸入Youtube網址，則自動下載封面圖片放入判斷

```python
import requests
import cv2
import pickle
import numpy as np
import keras
from urllib.parse import urlparse,parse_qs

with open('pikle.data','rb') as f:
    data = pickle.load(f)
global classifier 
classifier = data['classifier']   

def video_id(value):
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
        
def chk_is_elsagate(url):
    global classifier
    vid = video_id(url)
    imgurl = "https://i.ytimg.com/vi/{}/hqdefault.jpg"
    res = requests.get(imgurl.format(vid))
    img = np.asarray(bytearray(res.content), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    img = cv2.resize(img,(50,50))
    img = img.reshape(1,50,50,3)
    classifier = data['classifier']
    res = classifier.predict_classes(img)[0]
    return res

def print_result(res):
    if res:
        print("是Elsa Gate 趕快關掉")
    else:
        print("因該ㄅ4ㄅ.....因該啦")
```

Ref:
[1][How can I extract video ID from YouTube's link in Python?](https://stackoverflow.com/questions/4356538/how-can-i-extract-video-id-from-youtubes-link-in-python)


### API Server
透過flask實作一個http的api Server，接收到http post的資料，即可執行判斷。這邊遇到一個雷，Keras的BUG，程式執行時，若直接call function會報錯，最簡單的處理方法為，在程式啟動時先做一次判斷，接下來就會正常了[1]。

```python

from flask import Flask,request
from get_and_predURL import init,chk_is_elsagate


def init():
    img = cv2.resize(cv2.imread("t.jpg"),(50,50)).reshape(1,50,50,3)
    res = classifier.predict_classes(img)[0]

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello Word</h1>"

@app.route("/api", methods=['POST'])
def api():
    if 'url' in request.form.keys():
        url = request.form['url']
        print(url)
        if chk_is_elsagate(url):
            print('is elsa gate')
            return '1'
        else:
            print('not elsa gate')
            return '0'
    else:
        return 'err'

if __name__ == "__main__":
    init()
    app.run(debug=True)
```
透過Postman驗證
![](https://i.imgur.com/HXzUnqC.jpg)



Ref:
[1][记录深度学习踩过的坑](https://zhuanlan.zhihu.com/p/32455451)

### Chrome Extension
希望可以透過Google Chrome的套件，使用AJAX來達成自動上傳網址到API Server上確認，並透過複寫html的方法防堵影片。
```json
   "permissions": [
    "activeTab",
    "storage",
    "tabs",
    "http://127.0.0.1:5000/"
  ],

 "content_scripts": [{
    "js": ["contentscript.js","jquery.js"],
    "matches": [
      "https://youtu.be/",
      "https://www.youtube.com/*",
      "https://youtube.com/*"
    ],
    "run_at": "document_start"
  }
  ]
  
```

```javascript
window.addEventListener("spfdone", process); // old youtube design
window.addEventListener("yt-navigate-start", process); // new youtube design
document.addEventListener("DOMContentLoaded", process); // one-time early processing
// window.addEventListener("load", process); // one-time late postprocessing 


function process() {
    // console.log("into porcess!");
    $.post("http://127.0.0.1:5000/api",{
        url:document.URL
    },function(data,status){
        var d = data;
        console.log(d);
        if (d == '1'){
            document.body.innerHTML = "<h1>Elsa Gate Detect!</h1>";   
        }
    });
}
```

Ref:
[How to detect page navigation on Youtube and modify HTML before page is rendered?](https://stackoverflow.com/questions/34077641/how-to-detect-page-navigation-on-youtube-and-modify-html-before-page-is-rendered)

## 結論
大概應該或許可能做出來ㄌ！
- Demo影片：
    - [連結](https://www.youtube.com/watch?v=uOqclDofASM)

### 未來展望及繼續研究方向
- 提高準確率
    - 目前的深度學習算法，基本上Elsa Gate影片過濾率可以達到>90%的程度，但是對於正常影片而言的誤判率有一點高，可能可以研究增加準確率。
    - 或是設法進行影片內容的辨識

- 增加其他平台的解決方案
    - Chrome套件的方式是當前最容易實作的方式，但是小朋友現在大多數都使用移動裝置觀看，可能需要設法增加移動裝置的過濾方法。
    - 已知Youtube沒有開放API，Android平台也沒有開放相應的介接方法，iOS更沒有QQQQ。
        - 採用Root過的Android手機做螢幕擷取來判斷
        - 直接自幹一個安全板的Youtube播放器，但4很累很難QQQQQQQQQ。
- 過濾其他有害內容
    - 血腥、暴力......
    - ~~小玉、放火、聖結石ㄉ影片~~
## 結束ㄌ
87+1