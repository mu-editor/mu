# -*- coding: utf-8 -*-
import codecs
import locale

test_text = "£"
encodings = {
  "UTF16LE" : ("UTF-16-LE", codecs.BOM_UTF16_LE),
  "UTF16BE" : ("UTF-16-BE", codecs.BOM_UTF16_BE),
  "UTF8BOM" : ("UTF-8", codecs.BOM_UTF8),
  "LATIN" : ("iso-8859-1", None),
  "UTF8" : ("utf-8", None),
  "cp1252" : ("cp1252", None),
  "default" : (None, None),
}

for name, (encoding, bom) in encodings.items():
    print(name)
    with open("%s.txt" % name, "wb") as f:
        if bom:
            f.write(bom)
        elif encoding:
            f.write(("# -*- coding: %s -*-\n" % encoding).encode(encoding))
        f.write(test_text.encode(encoding or locale.getpreferredencoding()))
