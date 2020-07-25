import pyqrcode
import json
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import os
import csv
import sys
import getopt
from os import path

def makeClues(cluedir):
    files = os.listdir(cluedir)
    for fname in files:
        filename = "%s/%s" % (cluedir,fname)
        indx = 1
        if (filename.find("_scvg.json")==-1):
            continue
        print ("Processing: %s" % filename)
        if filename.find("_scvg.json")>-1:
            master_file = fname.replace("_scvg.json","")
            print("\tmaster: %s" % master_file)
            with open(filename,"r") as fin:
                data = json.loads(fin.read())
                images = [];
                for barcode in data:
                    temp_image = "%s/%s%d.png" % (cluedir,master_file,indx) #barcode["file_name"]
                    print("\t%s" % temp_image)
                    msg = barcode["msg"]
                    caption = "%d. %s - %s" % (indx,master_file,barcode["clue_location"])
                    qrcode = pyqrcode.create(msg)
                    qrcode.png(temp_image,scale=3)
                    img=Image.open(temp_image)
                    h = img.height
                    draw=ImageDraw.Draw(img)
                    font = ImageFont.truetype("Arial.ttf", 14)
                    draw.text((10,(h-14)),str(caption),font=font)
                    barcode["image"] = img
                    images.append(barcode)
                    img.save(temp_image)
                    indx += 1
                big_img = Image.new("RGB",(612,792),"#ffffff")
                row = 10
                col = 10
                max_height = -1
                indx = 1
                for barcode in images:
                    temp_image = "%s/%s%d.png" % (cluedir,master_file,indx) #barcode["file_name"]
                    i = barcode["image"]
                    if i.size[0] > max_height:
                        max_height = i.size[0]
                    if (col+i.size[1]>600):
                        row+=max_height+10
                        col=10
                        max_height = 0
                    big_img.paste(i,(col,row))
                    col+=i.size[1]+10
                    os.unlink(temp_image)
                    indx += 1
                big_file = "%s/%s.png" % (cluedir, master_file)
                big_img.save(big_file)
                print("\tsaved: %s\n" % big_file)



if __name__ == "__main__":
  try:
    opts, args = getopt.getopt(sys.argv[1:],"hd:",["help","dir="])
  except getopt.GetoptError:
    print ('python scavenge.py -h')
    sys.exit(2)
  for opt, arg in opts:
    print ("%s %s" % (opt,arg))
    if opt in ("-d","--dir"):
        makeClues(arg)
    elif opt in ("-h","--help"):
        print("python scavenge.py -d [CLUE_DIRECTORY]")
    else:
        print ('python scavenge.py -h')
        sys.exit(2)


