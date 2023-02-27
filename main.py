import pickle

from MoMem.MoNode.monode_pickle import *
from MoMem.MoNode import monode
from MoMem.MoNode.monode_basic import file_to_monode

# Create a MoNode object for toffu.png
toffu = file_to_monode("toffu.png", open("image\\toffu.png", "rb").read(), "A picture of the glorious Toffu", note=[], tags=["toffu", "picture"])

p = dump(toffu)
print(f"lens {len(p)}")
print(f"header {p[:2]}")
print(f"length {int.from_bytes(p[2:10], 'big')}")
print(f"next object {p[10:12]}")
print(f"size {int.from_bytes(p[12:20], 'big')}")
n = int.from_bytes(p[20:28], 'big')
print(f"n ele in the list {n}")

for i in range(n):
    print(f"key {i} {int.from_bytes(p[28 + i * 8: 36 + i * 8], 'big')}")

print(f"next object {p[92: 94]}")
size = int.from_bytes(p[94:102], 'big')
print(f"size {size}")
print(f"object {p[102:102+size]}")
print()

print(f"Object 6 {p[205:207]}")
print(f"Object 6 size {int.from_bytes(p[207:215], 'big')}")
n = int.from_bytes(p[215:223], 'big')
print(f"Object 6 n ele in the list {n}")
curpos = 223
for i in range(n):
    print(f"Object 6 key {i} {int.from_bytes(p[curpos:curpos+8], 'big')}")
    curpos += 8

print()

for i in range(n):
    print(f"Object {i} type {p[curpos:curpos+2]}")
    curpos += 2
    size = int.from_bytes(p[curpos:curpos+8], 'big')
    print(f"Object {i} size {size}")
    curpos += 8
    print(f"Object {i} data {p[curpos:curpos+size]}")
    curpos += size
    print()