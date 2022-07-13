from magos.stream import read_uint32be, write_uint32be


def read_gamepc(stream):
    total_item_count = read_uint32be(stream)
    version = read_uint32be(stream)
    assert version == 128, version
    item_count = read_uint32be(stream)
    string_table_count = read_uint32be(stream)

    total_item_count += 2
    item_count += 2

    text_size = read_uint32be(stream)
    texts = stream.read(text_size).split(b'\0')
    last_text = texts.pop()
    assert last_text == b''
    assert len(texts) == string_table_count, (len(texts), string_table_count)

    tables = stream.read()
    return total_item_count, version, item_count, texts, tables


def write_gamepc(total_item_count, version, item_count, texts, tables_data):
    texts_content = b'\0'.join(texts) + b'\0'
    return (
        write_uint32be(total_item_count - 2)
        + write_uint32be(version)
        + write_uint32be(item_count - 2)
        + write_uint32be(len(texts))
        + write_uint32be(len(texts_content))
        + texts_content
        + tables_data
    )
