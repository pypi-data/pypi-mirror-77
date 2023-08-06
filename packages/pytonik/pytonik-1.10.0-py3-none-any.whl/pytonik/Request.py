###
# Author : Betacodings
# Author : info@betacodings.com
# Maintainer By: Emmanuel Martins
# Maintainer Email: emmamartinscm@gmail.com
# Created by Betacodings on 2019.
###


import os
import cgi
from pytonik.Controllers import Controllers
from pytonik.util.Variable import Variable
from pytonik.Version import *
from pytonik.Log import Log


class Request(Variable):

    def __getattr__(self, item):
        return item

    def __init__(self, prform=None):
        self.Controllers = Controllers()
        self.para_vv ={} 
        if self.out("SERVER_SOFTWARE") == AUTHOR:
             self.attr = prform
        else:
            self.attr = cgi.FieldStorage()
        self.method = self.out('REQUEST_METHOD', '')

    def get(self, key=0, error=0):
        
        try:
            if 'GET' in self.out('REQUEST_METHOD'):

                if key != 0:
                    if (key in self.attr):
                        if self.attr.getvalue(key) != "":
                            return self.attr.getvalue(key)
                        else:
                            return self.params(key)
                    elif error == 1:
                        return self.attr
                    else:
                        return self.params(key)
                else:
                    return ""
            else:
                
                Log('').warning("advise use POST instead of GET")
                return False
        except Exception as err:
            Log('').warning(err)
            return err

    def post(self, key=0, error=0):
        try:
            if 'POST' in self.out('REQUEST_METHOD'):
                if key != 0:
                    if (key in self.attr):
                        if self.attr.getvalue(key) != "":
                            return self.attr.getvalue(key)
                        else:
                            return self.params(key)
                    elif error == 1:
                        return self.attr
                    else:
                        return self.params(key)
                else:
                    return ""
            else:
                Log('').warning("advise use GET instead of POST")
                return False
        except Exception as err:
            Log('').warning(err)
            return err

    def file(self, key=0, error=0):
        try:
            if key != 0:
                if (key in self.attr):
                    self.attr.getvalue(key)
                    return self.attr[key]
                elif error == 1:
                    return self.attr
                else:
                    return ""
            else:
                return ""

        except Exception as err:
            Log('').warning(err)
            return err

    def all(self):
        if None is not self.attr.keys():
            return self.attr.keys()

    def params(self, key=""):
        self.para_vv = self.Controllers._getParams()
        if key == "" or key == None:
            result = self.para_vv  
        else:
            result =  self.para_vv.get(key, '') 
        return result       
       
        
