#!/usr/bin/python
import sys

sys.stdout.reconfigure(encoding="utf-8")
from pwn import *

context.log_level = "DEBUG"

mapping = {
    b'\xe2\x87\xa9': b's',
    b'\xe2\x87\xa8': b'd',
    b'\xe2\x87\xa7': b'w',
    b'\xe2\x87\xa6': b'a',


}

def splitBytes(line, n):
    return [line[i:i+n] for i in range(0, len(line), n)]

p = remote('chal.2023.sunshinectf.games', 23200)
p.recvuntil(b'   -- Press ENTER To Start --   \r\n')
p.sendline(b'')

p.recvline() # receive code
byteString = (p.recvline().strip())

chars = splitBytes(byteString, 3)
chars = b''.join([mapping[c] for c in chars]) # send keys

p.sendline(chars)

for i in range(254):
    byteString = (p.recvline().strip())

    chars = splitBytes(byteString, 3)
    chars = b''.join([mapping[c] for c in chars]) # send keys

    p.sendline(chars)

p.interactive()