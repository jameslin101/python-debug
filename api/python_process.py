from http.server import BaseHTTPRequestHandler
import cv2
import numpy as np
import urllib
from urllib.parse import urlparse, parse_qs
from cgi import parse_header, parse_multipart
from collections import OrderedDict
class handler(BaseHTTPRequestHandler):

  def do_POST(self):

    length = int(self.headers['content-length'])
    params = parse_qs(self.rfile.read(length).decode(), keep_blank_values=1)
    try:
      self.process(params)
    except Exception as e:
      self.send_error(404)
      self.send_header('Content-type', 'text/plain')
      self.end_headers()
      self.wfile.write("Exception {0}".format(e))
    return

  def process(self, params):
    print(params)
    
    img_path = "https://pengulove.s3.amazonaws.com/imgs/faqs.png"
    req = urllib.request.urlopen(img_path)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    fg = cv2.imdecode(arr, -1)
    is_success, im_buf_arr = cv2.imencode(".png", fg)
    file_data = im_buf_arr.tobytes()
    file_data_len = len(file_data)        
    self.send_response(200)

    self.send_header("Accept-Ranges","bytes")
    self.send_header("Content-Disposition","attachment")
    self.send_header("Content-Length",file_data_len)
    self.send_header("Content-type", "image/png")
    self.end_headers()
    self.wfile.write(file_data)

    return

  