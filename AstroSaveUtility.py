# Python 3 code that will read, decompress, and then recompress the UE4 game
# save file that Astroneer uses.

# .savegame         unmodded savefile
# .savegame.json    decompressed savefile
# .savegame-mod     loadable modded savefile

# usage
# copy your savefile into the folder where this script is located and rename it for ease of use (e.g. test.savegame)
# 
# $ python saveutil.py test load

import sys
import base64
import json

import cogs.Compression as Compression

print()
filename = sys.argv[1]

if sys.argv[2] == "load":
    print("decompressing...")

    save = {
        "data": ""
    }

    with open(filename + '.savegame', 'rb') as compressedFile:

        decompressed = Compression.decompress(compressedFile.read())
        b64encoded = base64.b64encode(decompressed).decode("utf-8")
        save["data"] = b64encoded
        
        with open(filename + '.savegame.json', 'wb') as decompressedFile:

            x = json.dumps(save)
            decompressedFile.write(bytes(x, "utf-8"))
                

elif sys.argv[2] == "save":
    print("compressing...")

    # load modded file
    with open(filename + '.savegame.json', 'rb') as decompressedFile:

        save = json.loads(decompressedFile.read())

        # save
        with open(filename + '.savegame-mod', 'wb') as compressedFile:
            
            compressed = Compression.compress(base64.b64decode(save["data"]))

            # write
            compressedFile.write(compressed)
            #sz_in  = len(data_decompressed1)
            #sz_out = len(data_compressed2)
            #print("Deflated from {:d} (0x{:0x}) to {:d} (0x{:0x}) bytes".format(sz_in,sz_in,sz_out,sz_out))


"""

    # recompress
    with open(filename + '-z', 'wb') as deflated:
        data_compressed2 = bytearray()
        compress = zlib.compressobj(
            6, # Compression level
            zlib.DEFLATED, # default
            (4+8), # Window size
            zlib.DEF_MEM_LEVEL, # default
            0 # Z_DEFAULT_STRATEGY
        )
        #compress = zlib.compressobj()
        data_compressed2 += compress.compress(data_decompressed1)
        data_compressed2 += compress.flush()
        #deflated.write(header1)
        #deflated.write(data_compressed2)
        sz_in  = len(data_decompressed1)
        sz_out = len(data_compressed2)
        print("Deflated from {:d} (0x{:0x}) to {:d} (0x{:0x}) bytes".format(sz_in,sz_in,sz_out,sz_out))
        
    with open(filename + '-z', 'rb') as compressed:
        header2 = compressed.read(16)
        data_decompressed2 = zlib.decompress(compressed.read())

    print()
    if data_compressed1 == data_compressed2:
        print("Compressed data matches!")
    else:
        print("Compressed data differs (but that may be ok)")

    if data_decompressed1 == data_decompressed2:
        print("Decompressed data matches!")
    else:
        print("Decompressed data differs (NOT GOOD)")
"""
