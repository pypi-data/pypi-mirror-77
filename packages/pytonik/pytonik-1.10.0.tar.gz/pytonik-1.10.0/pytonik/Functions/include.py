# Author : BetaCodings
# Author : info@betacodings.com
# Maintainer By: Emmanuel Martins
# Maintainer Email: emmamartinscm@gmail.com
# Created by BetaCodings on 08/11/2019.

from pytonik.Editor import Template
from pytonik.Log import Log
from pytonik.App import App
import os
log_msg = Log()


class include(App):


    def __getattr__(self, item):

        return item

    def __call__(self, *args, **kwargs):

        return None

    def __init__(self, *args,  **kwargs):
        if len(args) > 0 or len(kwargs) > 0:
            if all(args) is not False:
                self.ex = self.include(*args,  **kwargs)
            else:
                self.ex = self.include(**kwargs)
        return None

    def __str__(self):

        return self.ex


    def include(self, path = "", is_temp=False):
        tempath = ""
        DS = str("/")
        if bool(is_temp) == True:
            tempath = DS+str(self.envrin('tempath'))
        if os.path.isdir(os.getcwd() + '/public'):
            host = str(os.getcwd()).replace("\\", "/")  # os.path.dirname(os.getcwd())

        else:
            host = str(os.path.dirname(os.getcwd())).replace("\\", "/")

       
        pth = path

        split = pth.split('.')


        fileExists = []
        for x in split:
            fileExists.append(x)

        try:

            dirF =  list(filter(None, fileExists))
            lf = ""
            for v in dirF:
                lf +="/"+v

            template_dir = host + DS + 'views' + str(tempath)+ str(lf)
            engine  = template_dir.rsplit('/', 1)[-1]
            direct = str(template_dir.rsplit('/', 1)[-2])
            
            if os.path.isdir(direct) == True:

                if 'views.html' not in template_dir+".html":

                    if os.path.isfile(template_dir+".html") == True:

                        loadm0 = self.loadmodule()
                        return self.read_html(direct, engine, loadm0)
                    else:
                      log_msg.error("The File '{filepath}' does not exists.".format(filepath=template_dir+".html"))
                      return "The File '{filepath}' does not exists.".format(filepath=template_dir+".html" )

            else:
              log_msg.error("The Folder '{filepath}' does not exists.".format(filepath=direct))
              return "The Folder '{filepath}' does not exists.".format(filepath=direct)

        except Exception as err:
                log_msg.error(err)
                return  err