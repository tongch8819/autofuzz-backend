from django.db import models
import os

# Create your models here.

class PathItem:
    name = ""
    parent = ""
    url = ""
 
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.url = "folder/" + os.path.join(parent, name)
 
 
class FileItem:
    name = ""
    parent = ""
    url = ""
    canRead = False
 
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
