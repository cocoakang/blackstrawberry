# -*-coding:utf-8-*-

import requests
import re
import random
import zlib
import time


def randomUn(n):
    s = pow(10,n-1)
    e = pow(10,n)-1
    res = random.random() *(e - s) + s
    return res

def getBulletScreen(url):
    r = requests.get(url)
    #get vid
    result = re.findall(r"param\[\'tvid\'\] = \"\d+\"",r.text)[0]
    tvId = re.findall(r"\d+",result)[0]#TODO check all result if they are same
    infoUrl = "http://mixer.video.iqiyi.com/jp/mixin/videos/" + tvId

    #get info and analysis
    r = requests.get(infoUrl)
    albumID = re.findall(r"\d+",re.findall(r"\"albumId\":\d+",r.text)[0])[0]
    channelId = re.findall(r"\d+",re.findall(r"\"channelId\":\d+",r.text)[0])[0]
    duration = re.findall(r"\d+",re.findall(r"\"duration\":\d+",r.text)[0])[0]
    # print(albumID,"\t",channelId,"\t",duration)

    #get the encoded bullet screen
    t = "0000" + tvId
    length = len(t)
    page = int(duration) // (60*5)+1
    bullets = []
    for i in range(1,page+1):
        first = t[length-4:length-2]
        second = t[length-2:]
        rn = "0.{}".format(randomUn(16)) 
        bulletUrl = "http://cmts.iqiyi.com/bullet/{}/{}/{}_300_{}.z?rn={}&business=danmu&is_iqiyi=true&is_video_page=true&tvid={}&albumid={}&categoryid={}&qypid=01010021010000000000".format(
            first,second,tvId,i,rn,tvId,albumID,channelId
        )
        # print(bulletUrl)
        r = requests.get(bulletUrl)
        if(len(r.text) != 0):
            res = zlib.decompress(r.content)
            res_c_t = re.findall(b"<content>.+</content>\n<showTime>\d+</showTime>",res)
            bullets.extend(res_c_t)
    #uncompress
    return bullets


    
if __name__ == "__main__":
    printf("I am here to destory again")
    pUrlsF = open("urls.txt","r")
    saveRoot = "bullets/"
    urls = pUrlsF.read().split("\n")
    for i,url in enumerate(urls):
        print("current video url:",i)
        bullets = getBulletScreen(url)
        f = open(saveRoot+"{}.txt".format(i+1),"w",encoding="utf-8")
        for no,bullet in enumerate(bullets):
            content = re.findall(b"<content>.+</content>",bullet)[0]
            time_stamp = re.findall(b"\d+",re.findall(b"<showTime>\d+</showTime>",bullet)[0])[0]
            f.write("{}: ".format(no+1))
            f.write("{}".format(time.strftime("%H:%M:%S", time.gmtime( float(time_stamp) ))))
            f.write(bytes.decode(content[9:-10],encoding = "utf-8"))
            f.write("\n")
        f.close()
