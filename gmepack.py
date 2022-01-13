from itertools import chain

from stream import read_uint16be, readcstr


def read_subroutines(stream):
    while True:
        min_sub = read_uint16be(stream)
        if min_sub == 0:
            break
        max_sub = read_uint16be(stream)
        yield min_sub, max_sub


def index_table_files(tbllist_path: str):
    with open(tbllist_path, 'rb') as stream:
        while True:
            fname = readcstr(stream)
            if not fname:
                break
            subroutines = tuple(read_subroutines(stream))
            yield fname.decode(), subroutines


def index_text_files(stripped_path: str):
    with open(stripped_path, 'rb') as stream:
        while True:
            name = stream.read(7)
            if not name:
                break
            base_max = read_uint16be(stream)
            yield name.rstrip(b'\0').decode(), base_max


def get_packed_filenames(game: str):
    if game == 'simon1':
        # Simon the Sorcerer
        yield from chain.from_iterable((f'{vga:03d}1.VGA', f'{vga:03d}2.VGA') for vga in range(164))
        yield from ['UNKNOWN.BIN'] # unknown file
        yield from ['MOD{:d}.MUS'.format(idx) for idx in range(36)]
        yield 'EMPTYFILE'
        yield from (fname for fname, _ in index_text_files('STRIPPED.TXT'))
        yield from (fname for fname, _ in index_table_files('TBLLIST'))
        yield 'EMPTYFILE'
        return

    if game == 'simon2':
        # Simon the Sorcerer 2
        yield from chain.from_iterable((f'{vga:03d}1.VGA', f'{vga:03d}2.VGA') for vga in range(140))
        yield from ['UNKNOWN1.BIN', 'UNKNOWN2.BIN'] # unknown files but might be vga as well
        yield from ['HI{:d}.XMI'.format(idx) for idx in range(1, 94)]
        yield 'EMPTYFILE'
        yield from (fname for fname, _ in index_text_files('STRIPPED.TXT'))
        yield from (fname for fname, _ in index_table_files('TBLLIST'))
        yield from ['SFX{:d}.VOC'.format(idx) for idx in range(1,20)]
        yield from ['LO{:d}.XMI'.format(idx) for idx in range(1, 94)]
        yield 'EMPTYFILE'
        return  

    raise NotImplementedError(game)