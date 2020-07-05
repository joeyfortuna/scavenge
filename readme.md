## Scavenge
### QRCode-based Scavenger Hunt

All the web code can just be accessed here: https://s3.amazonaws.com/natterbot.com/qrcode/index.html

To create the codes, build a JSON file as an array, with one object per QRCode. An example file can be found in the python directory of this repo: "example_scvg.json"

Properties of the objects should be: 

* file_name - this is just to create a temporary single-code image
* clue_location - this will be readable text on the clue so you can tell where to hide it
* msg - this is the clue itself -- a hint leading to the next clue!

One high-level object should also be in the array:

* master_file - this is the name of the image with all of the clues packed together

To create the printable page full of clues, run "process_clues.py" in the same directory as your json file (note that the file name should end with "_scvg.json").

I've tried to include credit for all of the stuff I cargo-culted, but let me know if I missed anything or anyone!
