#!/usr/bin/python3
import os
import random
import string
import http.server
import socketserver
import json
import signal
import sys
import shutil
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import getopt
import urllib.request
import requests
from time import time as timer
from multiprocessing.pool import ThreadPool

opts, args = getopt.getopt(sys.argv[1:], "s:", ['--source='])

server = True
for opt, arg in opts:
    if opt in ('-s', '--source'):
        server = False
        source = arg

def randomString(stringLength = 16):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength)) + ".tmp"

def mk_empty_dir(dir, rm_existing=True, chdir=True):
    dir_absolute_path = os.path.join(os.path.dirname(__file__), dir)
    if rm_existing and os.path.exists(dir_absolute_path):
        shutil.rmtree(dir_absolute_path)
    Path(dir_absolute_path).mkdir(parents=True, exist_ok=True)
    if chdir:
        os.chdir(dir_absolute_path)

def download_url(url):
    file_name_start_pos = url.rfind("/") + 1
    file_name = url[file_name_start_pos:]

    r = requests.get(url, stream=True)
    if r.status_code == requests.codes.ok:
        with open(file_name, 'wb') as f:
            for data in r:
                f.write(data)

if (server):
    public_dir = os.path.join(os.path.dirname(__file__), 'public')
    shutil.rmtree(public_dir)
    Path(public_dir).mkdir(parents=True, exist_ok=True)
    os.chdir(public_dir)

    files = []
    for x in range(4):
        rand = randomString()
        with open(rand, 'wb') as fout:
            fout.write(os.urandom(500000000))
        files.append(rand)

    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public')
            if self.path == '/':   
                parsed_path = urlparse(self.path)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(files).encode())
                return
            else:
                with open(root + self.path, 'rb') as fh:
                    file = fh.read()
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(file)
                    return
                    
        # def do_POST(self):
        #     content_len = int(self.headers.getheader('content-length'))
        #     post_body = self.rfile.read(content_len)
        #     data = json.loads(post_body)

        #     parsed_path = urlparse(self.path)
        #     self.send_response(200)
        #     self.end_headers()
        #     self.wfile.write(json.dumps({
        #         'method': self.command,
        #         'path': self.path,
        #         'real_path': parsed_path.query,
        #         'query': parsed_path.query,
        #         'request_version': self.request_version,
        #         'protocol_version': self.protocol_version,
        #         'body': data
        #     }).encode())
        #     return

    if __name__ == '__main__':
        server = HTTPServer(('', 8000), RequestHandler)
        print('Starting server at http://*:8000')
        server.serve_forever()
else:
    urls = []
    with urllib.request.urlopen(source) as url:
        data = json.loads(url.read().decode())
        for x in data:
            urls.append((source + "/" + x))
            print("Downloading " + source + "/" + x)

        mk_empty_dir('downloads', True, True)
        results = ThreadPool(len(urls)).imap_unordered(download_url, urls)
        i = 0
        for r in results:
            i += 1
            print("File #{} downloaded successfully".format(i))
