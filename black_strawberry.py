# -*-coding:utf-8-*-

import requests
import re
import random
import zlib
import base64

def decode_base64_and_inflate( b64string ):
    decoded_data = base64.b64decode( b64string )
    return zlib.decompress( decoded_data , -15)

def deflate_and_base64_encode( string_val ):
    zlibbed_str = zlib.compress( string_val )
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode( compressed_string )

def inflate(data):
    decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated

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
    print(albumID,"\t",channelId,"\t",duration)

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
        print(bulletUrl)
        r = requests.get(bulletUrl)
        if(len(r.text) != 0):
            res = zlib.decompress(r.content)
            res = re.findall(b"<content>.+</content>",res)
            bullets.extend(res)
    #uncompress
    return bullets


    
if __name__ == "__main__":
    url = "https://www.iqiyi.com/v_19rr2hvv68.html"
    results = getBulletScreen(url)
    f = open("res.txt","w",encoding="utf-8")
    for frame in results:
        f.write(bytes.decode(frame[9:-10],encoding = "utf-8"))
        f.write("\n")
    f.close()