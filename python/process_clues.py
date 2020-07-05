import pyqrcode
import json
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import os
files = os.listdir("./")
for filename in files:
    print "Processing: %s" % filename
    if filename.find("_scvg.json")>-1:
        with open(filename,"r") as fin:
            data = json.loads(fin.read())
            master_file = None
            images = [];
            for barcode in data:
                try:
                    master_file = barcode["master_file"]
                    print "master file: %s" % master_file
                    continue
                except:
                    print "image processing"
                file_name = barcode["file_name"]
                msg = barcode["msg"]
                caption = barcode["clue_location"]
                qrcode = pyqrcode.create(msg)
                qrcode.png(file_name,scale=3)

                img=Image.open(file_name)
                h = img.height
                draw=ImageDraw.Draw(img)
                font = ImageFont.truetype("Arial.ttf", 14)
                draw.text((10,(h-14)),str(caption),font=font)
                barcode["image"] = img
                images.append(barcode)
                img.save(file_name)
            big_img = Image.new("RGB",(612,792),"#ffffff")
            row = 10
            col = 10
            max_height = -1
            for barcode in images:
                i = barcode["image"]
                if i.size[0] > max_height:
                    max_height = i.size[0]
                if (col+i.size[1]>600):
                    row+=max_height+10
                    col=10
                    max_height = 0
                big_img.paste(i,(col,row))
                col+=i.size[1]+10
                os.unlink(barcode["file_name"])
            big_img.save(master_file)