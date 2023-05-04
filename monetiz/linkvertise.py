import random
import base64

def linkvertise(userid, link):
    base_url = f"https://link-to.net/{userid}/{random.random() * 1000}/dynamic"
    href = f"{base_url}?r={base64.b64encode(link.encode('utf-8')).decode('utf-8')}"
    return href

#print(linkvertise(674349, "https://www.youtube.com/watch?v=dQw4w9WgXcQ"))