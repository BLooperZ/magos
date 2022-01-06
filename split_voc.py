import errno
import os
import struct
import sys


def create_directory(name):
    try:
        os.makedirs(name)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def get_sound(num, offset):
    name = 'tempfile{:04}.voc'.format(num)
    size = 0
    vocFile.seek(offset[0], 0)
    with open(ext +'/' + name.format(num), 'wb') as tempFile:
        tempFile.write(vocFile.read(27))
        size = vocFile.read(3)
        tempFile.write(size)
        size = struct.unpack('<I', size + b'\x00')
        tempFile.write(vocFile.read(size[0] + 1))
        size= tempFile.tell()
    return size

def get_offsets(maxcount):
    for i in range(maxcount):
        buf = vocFile.read(8)
        if buf == b'Creative' or buf == b'RIFF':
            return i
        vocFile.seek(-8, 1)
        offsets.append(struct.unpack('<I', vocFile.read(4)))

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print('Usage:\n' + 'python split-voc.py SIMON.VOC')
        exit(1)
    filename = sys.argv[1]
    if not os.path.exists(filename):
        print('Error: file \'{}\' does not exists.'.format(filename))
        exit(1)

    ext = filename.split('.')[-1]
    create_directory(ext)

    vocFile = open(filename, 'rb')
    datFile = open('TEMP_DAT', 'wb')
    idxFile = open('TEMP_IDX', 'wb')
    offsets = []

    num = get_offsets(32768)
    offsets.append(0)
    size = num * 4
    idxFile.write(struct.pack('<I', 0))
    idxFile.write(struct.pack('<I', size))

    j = 0
    for i in range(1, num):
        if offsets[i] == offsets[i + 1]:
            idxFile.write(struct.pack('<I', size))
            continue

        if offsets[i] != 0:
            size += get_sound(j, offsets[i])
        if i < num - 1:
            idxFile.write(struct.pack('<I', size))
            j += 1

    vocFile.close()
    datFile.close()
    idxFile.close()
