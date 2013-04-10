"""
Created on Jul 31, 2012

@author: Administrator
"""
from distutils.core import setup
import py2exe

setup( windows = [
                  {
                   "script": "main.py",
                   "icon_resources": [( 0, ".\\images\\odmedia.ico" )],
                   "dest_base": "AVSProcessor_1.2.3"
                  }
                 ],
       options = {
                  "py2exe":{
                            "dist_dir": r"C:\Users\alexandros\Desktop\AVSProcessor 1.2.3",
                            "packages": "pubsub"
                            }
                 }
      )
