import BurpParse
import os
import re

for path,dirs,files in os.walk('input'):
    for file in files:
        if re.match('.*Traffic\.xml', file):
            print file

            src = "{0}{1}{2}".format(path, os.sep, file)

            img_dir = "output\images\{0}".format(file[:-4])
            os.mkdir(img_dir)

            srch_csv = "output\searches\{0}.csv".format(file[:-4])

            docs_csv = "output\docs\{0}.csv".format(file[:-4])

            BurpParse.parse(src, img_dir, srch_csv, docs_csv)
