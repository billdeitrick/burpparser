import base64
import urllib
import urlparse
import json
import os
import sys
import xml.etree.ElementTree as ET
from HTTPRequest import *
from Utils import write_dict_list

def parse(src, img_dir, srch_csv, docs_csv):

    tree = ET.parse(src)
    root = tree.getroot()

    searches = []
    docs_strokes =[]

    # Loop through requests
    for item in root.getchildren():

        # Get request method
        method = item.find('method').text

        # Get request url
        url = item.find('url').text

        # Parse the request
        req = item.find('request').text
        req_obj = HTTPRequest(base64.b64decode(req))

        # Decode the request body
        raw_body = req_obj.rfile.read(int(req_obj.headers.getheader('content-length', 0)))
        body = urllib.unquote(raw_body)
        
        # Parse request fields
        fields = urlparse.parse_qs(body)

        # Parse request url params
        urlparams = urlparse.parse_qs(item.find('path').text)

        # Parse the response
        resp = item.find('response').text

        try:
            resp_obj = HTTPResponse(base64.b64decode(resp))
            resp_body = resp_obj.content
        except Exception as e:
            resp_obj = None

        # Process POST requests
        if method == 'POST':
            if 'q' in fields:
                searches.append({
                    'value':fields['q'][0],
                    'comment':'picker',
                    'timestamp': item.find('time').text

                })

            if 'picker/v2/query' in url:
                body_js = json.loads(body)

                if body_js[0] == 'qreq':
                    searches.append({
                        'value': body_js[-1][-1][-1][0],
                        'comment': 'picker',
                        'timestamp': item.find('time').text
                    })

            if 'bundles' in fields:
                try:
                    bundle = json.loads(fields['bundles'][0])[0]
                except Exception as e:
                    pass
                
                for command in bundle['commands']:
                        try:
                            docs_strokes.append({
                                'value': command['s'],
                                'comment': 'Probable Text POST to Docs',
                                'timestamp': item.find('time').text
                            })
                        except:
                            continue
        
        # Process GET requests
        if method == 'GET':
            if 'q' in urlparams:
                searches.append({
                    'value':urlparams['q'][0],
                    'comment':'Probable address bar autocomplete',
                    'timestamp': item.find('time').text
                })

            if resp_obj is not None and 'image' in resp_obj.getheader("Content-Type",""):
                xtn = resp_obj.getheader("Content-Type").split("/")[1]
                with open('{0}/IMG-{1}.{2}'.format(img_dir, item.find('time').text.replace(":", ""), xtn), 'wb') as img_file:
                    img_file.write(resp_body)

    # Write output logs
    if len(searches) != 0:
        write_dict_list(searches, srch_csv)

    if len(docs_strokes) != 0:
        write_dict_list(docs_strokes, docs_csv)

if __name__ == '__main__':
    # Input file
    src = "input.xml"

    # Image output dir
    img_dir = "./images"

    # Search csv
    srch_csv = "searches.csv"

    # Docs csv
    docs_csv = "docs_strokes.csv"

    parse(src, img_dir, srch_csv, docs_csv)