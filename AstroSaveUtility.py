# Python 3 code that will read, decompress, and then recompress the UE4 game
# save file that Astroneer uses.

# .savegame         unmodded savefile
# .savegame-raw     decompressed savefile
# .savegame-rawmod  modified savefile
# .savegame-z       recompressed savefile for itegrity check
# .savegame-mod     loadable modded savefile

# usage
# copy your savefile into the folder where this script is located and rename it for ease of use (e.g. test.savegame)
# 
# $ python saveutil.py test.savegame save

import zlib
import sys
import binascii

print()
filename = sys.argv[1]

if sys.argv[2] == "load":
    print("decompressing...")

    with open(filename, 'rb') as compressed:
        header = compressed.read(16)
        #print("Header: " + binascii.hexlify(header))
        data_compressed = compressed.read()

        # decompress
        data_decompressed = zlib.decompress(data_compressed)
        sz_in  = len(data_compressed)
        sz_out = len(data_decompressed)

        #write
        with open(filename + '-raw', 'wb') as inflated:
            inflated.write(data_decompressed)
        
        print("Decompressed from {:d} (0x{:0x}) to {:d} (0x{:0x}) bytes".format(sz_in, sz_in, sz_out, sz_out))

elif sys.argv[2] == "save":
    print("compressing...")

    # load modded file
    with open(filename + '-rawmod', 'rb') as decompressed:
        data_compressed = bytearray()
        compress = zlib.compressobj(
            6, # Compression level
            zlib.DEFLATED, # default
            (4+8), # Window size
            zlib.DEF_MEM_LEVEL, # default
            0 # Z_DEFAULT_STRATEGY
        )
        #compress = zlib.compressobj()

        # compress
        data_decompressed = decompressed.read()

        data_compressed += compress.compress(data_decompressed)
        data_compressed += compress.flush()

        sz_in  = len(data_decompressed)
        sz_out = len(data_compressed)
        print("Compressed from {:d} (0x{:0x}) to {:d} (0x{:0x}) bytes".format(sz_in,sz_in,sz_out,sz_out))

        # save
        
        with open(filename + '-mod', 'wb') as modded:

            # generate header
            
            header = binascii.unhexlify("BE40374AEE0B74A301000000")
            
            # format size as hex, then turn to binary string and reverse (dunno why reverse)
            size = binascii.unhexlify('{:08x}'.format(sz_in))[::-1]
            header += size

            print("Header: " + binascii.hexlify(header))

            # write
            modded.write(header)
            modded.write(data_compressed)
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
