# Python 3 code that will read, decompress, and then recompress the UE4 game
# save file that Astroneer uses.

# .savegame         unmodded savefile
# .savegame.json    decompressed savefile
# .savegame-mod     loadable recomprssed savefile

# usage
# copy your savefile into the folder where this script is located and rename it for ease of use (e.g. test.savegame)
# 
# $ python AstroSaveUtility.py -m unpack -f test1.savegame

import sys
import base64
import json
import argparse

import cogs.Compression as Compression


argParser = argparse.ArgumentParser(description='Work with Astroneer Savefiles')
argParser.add_argument('-f', '--file', type=str, help='the path to file')
argParser.add_argument('-m', '--mode', type=str, help='Mode: unpack/pack')

args = argParser.parse_args()

if args.mode == "unpack":
    print("decompressing...")

    save = {
        "data": ""
    }

    with open(args.file, 'rb') as compressedFile:

        decompressed = Compression.decompress(compressedFile.read())
        b64encoded = base64.b64encode(decompressed).decode("utf-8")
        save["data"] = b64encoded
        
        with open(args.file.split('.')[0] + '.savegame.json', 'wb') as decompressedFile:

            x = json.dumps(save)
            decompressedFile.write(bytes(x, "utf-8"))
                

elif args.mode == "pack":
    print("compressing...")

    # load modded file
    with open(args.file, 'rb') as decompressedFile:

        save = json.loads(decompressedFile.read())

        # save
        with open(args.file.split('.')[0] + '.savegame-mod', 'wb') as compressedFile:
            
            compressed = Compression.compress(base64.b64decode(save["data"]))

            # write
            compressedFile.write(compressed)
            #sz_in  = len(data_decompressed1)
            #sz_out = len(data_compressed2)
            #print("Deflated from {:d} (0x{:0x}) to {:d} (0x{:0x}) bytes".format(sz_in,sz_in,sz_out,sz_out))


