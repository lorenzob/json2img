'''
Created on May 2, 2018

@author: trz
'''
import logging
import sys
import json
import base64
import imghdr
import os

def is_base64(s):
  return type(s) is str and len(s) > 100

def b64_generator(dict_var):
  for k, v in dict_var.items():
    if v is str:
      print(len(v))
    if is_base64(v):
      #print("OK:", k, is_base64(v), type(v))
      yield v
    elif isinstance(v, dict):
        yield from b64_generator(v)
    elif isinstance(v, list):
        for item in v:
          yield from b64_generator(item)
                                       
def process_request(data):
  
  for i, c in enumerate(b64_generator(data)):
    data = base64.b64decode(c)
    
    save_name = "work/data{}.tmp".format(i)
    with open(save_name, "wb") as f:
      f.write(data)
    ext = imghdr.what(save_name)
    os.rename(save_name, save_name.replace(".tmp", "."+ext))

if __name__ == '__main__':

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    request = sys.argv[1]

    with open(request, 'r') as myfile:
      datas = myfile.read()
      datas = datas.replace('\n', '')
      datas = datas.replace('\r', '')
      data = json.loads(datas)
    
    res = process_request(data)

    #sprint(json.dumps(res, indent=4))
