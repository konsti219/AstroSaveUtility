# this is responsible for dealing with the zlib comprssion and header of the save file

import zlib
import binascii


def compress(decompressed):

    dataCompressed = bytearray()
    
    compress = zlib.compressobj(
        6, # Compression level
        zlib.DEFLATED, # default
        (4+8), # Window size
        zlib.DEF_MEM_LEVEL, # default
        0 # Z_DEFAULT_STRATEGY
    )
    #compress = zlib.compressobj()

    dataCompressed += compress.compress(decompressed)
    dataCompressed += compress.flush()

    sz_in  = len(decompressed)
    sz_out = len(dataCompressed)
    print("Compressed from {:d} (0x{:0x}) to {:d} (0x{:0x}) bytes".format(sz_in,sz_in,sz_out,sz_out))

    # generate header

    header = binascii.unhexlify("BE40374AEE0B74A301000000")

    # format size as hex, then turn to binary string
    size = binascii.unhexlify('{:08x}'.format(sz_in))[::-1]
    header += size

    print("Header: " + str(binascii.hexlify(header)))

    dataCompressed = header + dataCompressed

    return dataCompressed


def decompress(compressed):
    compressed = compressed[16:len(compressed)]

    # decompress
    dataDecompressed = zlib.decompress(compressed)
    sz_in = len(compressed)
    sz_out = len(dataDecompressed)

    print("Decompressed from {:d} (0x{:0x}) to {:d} (0x{:0x}) bytes".format(
        sz_in, sz_in, sz_out, sz_out))

    return dataDecompressed
