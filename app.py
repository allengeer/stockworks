import requests
import json
import sys
import numpy as np

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
    else:
        ticker = "SNAP"

    r = requests.get("http://localhost:5000/news?ticker=%s" %ticker)
    listOfLinks = r.json()

    emotions = dict()
    pricing = requests.get("http://localhost:5003/stock/%s" % ticker)
    pricing = pricing.json()
    print "==================================================="
    print pricing['symbol'], pricing["price"], pricing["name"]
    print "===== Running analysis on %d links =====" %len(listOfLinks)
    for link in listOfLinks:
        q = requests.get("http://localhost:5001/scrape?url=%s" %link)
        content = q.content.decode('unicode_escape').encode('ascii','ignore')
        payload = {"text": content}
        headers = {'Content-Type': 'application/json'}
        z = requests.post("http://localhost:5002/analyze", json=json.dumps(payload), headers=headers)
        jsoninfo = z.json()
        if 'document_tone' in jsoninfo:
            for tonesuper in jsoninfo['document_tone']['tone_categories']:
                for tonecat in tonesuper['tones']:
                    if (emotions.get(tonecat['tone_name']) is None):
                        emotions[tonecat['tone_name']] = []
                    emotions.get(tonecat['tone_name']).append(float(tonecat['score']))



    # print "%s %s (%s)" %pricing["price"], pricing["name"], pricing["symbol"]
    print "%sMean\tVar\t\tStd\t\t\t(%s samples)" %('{0: <20}'.format('Emotion'),len(emotions.get("Anger")))
    for key,value in emotions.iteritems():
        u = np.mean(value)
        var = np.var(value)
        std = np.std(value)
        print "%s%.4f\t%.4f\t%.4f" %('{0: <20}'.format(key), u, var, std)