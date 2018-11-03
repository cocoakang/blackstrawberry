import chardet
import zlib
import re

if __name__ == "__main__":
    f = open("data/348961700_300_1.z","rb")
    a = f.read()
    f.close()
    res = zlib.decompress(a)
    # f = open("res.txt","w",encoding="utf-8")
    # data = bytes.decode(res,encoding = "utf-8")
    res = re.findall(b"<content>.+</content>",res)[1]
    print(bytes.decode(res,encoding = "utf-8"))
    # f.write()
    # f.close()
    