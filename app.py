import requests
import json
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
    else:
        ticker = "SNAP"
    r = requests.get("http://localhost:5000/news?ticker=%s" %ticker)
    listOfLinks = r.json()

    for link in listOfLinks:
        print "====== %s =======" %link
        q = requests.get("http://localhost:5001/scrape?url=%s" %link)
        content = q.content.decode('unicode_escape').encode('ascii','ignore')
        print "\t CONTENT:"
        print content
        print "\t ANALYSIS:"
        payload = {"text": content}
        headers = {'Content-Type': 'application/json'}
        z = requests.post("http://localhost:5002/analyze", json=json.dumps(payload), headers=headers)
        #z = requests.get("http://localhost:5002/analyze?text=happy")
        jsoninfo = z.json()
        for tonecat in jsoninfo['document_tone']['tone_categories'][0]['tones']:
            print "%s - %s" %(tonecat['tone_name'], tonecat['score'])

        # print z.json()
