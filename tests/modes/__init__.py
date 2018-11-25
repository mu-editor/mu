BYTES_TEST_STRING = bytes(range(0x20, 0x80)) + bytes(range(0xa0, 0xff))
UNICODE_TEST_STRING = BYTES_TEST_STRING.decode("iso-8859-1")
