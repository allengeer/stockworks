import requests
import json
import sys
import numpy as np
import time
import threading
from threading import Lock
import hashlib
import redis
lock = Lock()
redisCache = redis.StrictRedis(host='localhost', port=6379, db=0)

def scrapeAnalyze(ticker, link):
    sha = hashlib.md5(link).hexdigest()
    content = redisCache.get(sha)
    if content is None:
        q = requests.get("http://localhost:5001/scrape?url=%s" % link)
        content = q.content.decode('unicode_escape').encode('ascii', 'ignore')
        redisCache.set(sha,content)
    redisCache.set("%s:%s:CONTENT" %(ticker, link), content)

    payload = {"text": content}
    headers = {'Content-Type': 'application/json'}
    #print "%s Start\t" %link
    z = requests.post("http://localhost:5002/analyze", json=json.dumps(payload), headers=headers)
    redisCache.set("%s:%s:TONE" %(ticker, link), z.content)
    #print "STOP %s Stop" %link
    jsoninfo = z.json()

    if 'document_tone' in jsoninfo:
        lock.acquire()
        for tonesuper in jsoninfo['document_tone']['tone_categories']:
            for tonecat in tonesuper['tones']:
                if (emotions.get(tonecat['tone_name']) is None):
                    emotions[tonecat['tone_name']] = []
                emotions.get(tonecat['tone_name']).append(float(tonecat['score']))
        lock.release()


if __name__ == '__main__':
    start = time.time()

    if len(sys.argv) > 1:
        for idx in range(1,len(sys.argv)):
            ticker = sys.argv[idx]

            r = requests.get("http://localhost:5000/news?ticker=%s" %ticker)
            listOfLinks = r.json()

            emotions = dict()
            pricing = requests.get("http://localhost:5003/stock/%s" % ticker)
            pricing = pricing.json()
            #print "============ %s =============" %time.strftime("%c")
            #print pricing['symbol'], pricing["price"], pricing["name"]
            #print "======= Running analysis on %d links =======" %len(listOfLinks)

            threads = []
            for link in listOfLinks:
                t = threading.Thread(target=scrapeAnalyze, args=(ticker, link,))
                threads.append(t)
                t.start()
                # t.join()

            for t in threads:
                t.join()

            emotions["Normal"] = np.random.normal(0.5, 0.341, len(listOfLinks))

            # print "%s %s (%s)" %pricing["price"], pricing["name"], pricing["symbol"]
            # print "%sMean\tVar\t\tStd\t\t\t(%s samples)" %('{0: <20}'.format('Emotion'),len(emotions.get("Anger")))
            # for key,value in emotions.iteritems():
            #     u = np.mean(value)
            #     var = np.var(value)
            #     std = np.std(value)
            #     print "%s%.4f\t%.4f\t%.4f" %('{0: <20}'.format(key), u, var, std)

            print "%s\t%s\t%s\t" %(ticker, time.strftime("%c"), pricing["price"]),
            for key, value in emotions.iteritems():
                u = np.mean(value)
                std = np.std(value)
                if key is not "Normal":
                    print "%.4f\t%.4f\t" %(u, std),
            print ""

            end = time.time()

            elapsed = end - start
            #print ""
            #print "%s ELAPSED TIME %s" %(ticker, elapsed)