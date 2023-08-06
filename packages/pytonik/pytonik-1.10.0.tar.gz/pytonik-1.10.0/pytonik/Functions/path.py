# Author : BetaCodings
# Author : info@betacodings.com
# Maintainer By: Emmanuel Martins
# Maintainer Email: emmamartinscm@gmail.com
# Created by BetaCodings on 05/11/2019.
import os

from pytonik.Functions.url import url
from pytonik.util.Variable import Variable
from pytonik import Version

if os.path.isdir(os.getcwd() + '/public'):
    host_public = str(os.getcwd()).replace('\\', '/') + '/public'  # os.path.dirname(os.getcwd())
    host_app = str(os.path.dirname(os.getcwd())).replace("\\", "/") + '/app'
else:
    host_public = str(os.getcwd()).replace("\\", "/")
    host_app = str(os.path.dirname(os.getcwd())).replace("\\", "/")


class path(url, Variable):
    def __getattr__(self, item):
        return item

    def __call__(self, *args, **kwargs):

        return None

    def __init__(self, *args, **kwargs):

        if len(args) > 0 or len(kwargs) > 0:
            if all(args) is not False:
                self.pt = self.path(*args, **kwargs)
            else:
                self.pt = self.path(**kwargs)

        return None

    def __str__(self):

        return self.pt

    def path(self, path="", link=False):

        u = ""
        DS = "/"
        dev_path = ""
    
        if bool(link) == True:
            u = self.url()

        if path[:1] == DS or path[0] == DS:
            DS = ""
        else:
            DS = "/"
    
        return str(u)+str(DS)+str(path)

    def exist(self, newpath, defaultpath="", link=False):

        newpath = "" if newpath == None or newpath == "" else newpath
        path_res = ""

        try:
            if os.path.isfile(newpath) == True:

                path_res = self.path(path=newpath, link=link)

            elif os.path.isfile(str(host_app)+"/"+str(newpath)) == True:

                path_res = self.path(path=newpath, link=link)

            elif os.path.isfile(str(host_public)+"/" + str(newpath)) == True:

                path_res = self.path(path=str("/public/")+str(+newpath), link=link)
                
            elif os.path.isdir(newpath) == True:
                path_res = newpath

            elif os.path.isdir(self.public(path=newpath)) == True:
                path_res = self.public(path=newpath)

            else:

                if defaultpath != "":

                    if os.path.isfile(defaultpath) == True:
                        path_res = self.path(path=defaultpath, link=link)

                    elif os.path.isfile(str(host_app) + "/" + str(defaultpath)) == True:

                        path_res = self.path(path=defaultpath, link=link)

                    elif os.path.isfile(str(host_public)+"/"+str(defaultpath)) == True:

                        path_res = self.path(path=str("/public/")+str(defaultpath), link=link)

                    elif os.path.isdir(defaultpath) == True:
                        path_res = defaultpath

                    elif os.path.isdir(self.public(defaultpath)) == True:

                        path_res = self.public(path=defaultpath)
            return path_res

        except Exception as err:

            return err

    def public(self, path):
        DS = "/"
        if path[:1] == DS or path[:1] == DS:
            DS = ""
        else:
            DS = "/"

        return str(host_public) + DS + str(path)
