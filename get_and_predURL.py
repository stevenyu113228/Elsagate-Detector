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
    #from https://stackoverflow.com/questions/4356538/how-can-i-extract-video-id-from-youtubes-link-in-python
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
    # cv2.imwrite("t.jpg",img)
    img = cv2.resize(img,(50,50))
    img = img.reshape(1,50,50,3)
    # res = classifier.predict_classes(img)[0]
    res = classifier.predict_classes(img)[0]
    return res

def print_result(res):
    if res:
        print("是Elsa Gate 趕快關掉")
    else:
        print("因該ㄅ4ㄅ.....因該啦")



def init():
# 知乎@王岳王院长
# 也遇到此问题，他的解决办法最好。在次引用：
# 就是说，当你引用模型后，随后进行一次预测，后面再用到时，就不会报错。
# https://zhuanlan.zhihu.com/p/32455451
    img = cv2.resize(cv2.imread("t.jpg"),(50,50)).reshape(1,50,50,3)
    res = classifier.predict_classes(img)[0]