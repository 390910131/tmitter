#!/usr/bin/env python
import md5

# md5 encode
def md5_encode(str):
    return md5.new(str).hexdigest()
