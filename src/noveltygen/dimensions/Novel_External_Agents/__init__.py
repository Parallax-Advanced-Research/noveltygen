import sys
import os
p = os.path.dirname(os.path.abspath(__file__))
sys.path.append(p)
f = sys._getframe()  # Get the parent frame, so we can inject variables into it.
for fi in os.listdir(p):
    if fi[0] == "_":
        continue
    if fi[-3:] != ".py" and not os.path.isdir(p+"/"+fi):
        continue
    if os.path.isdir(p+"/"+fi):
        f.f_locals[fi] = __import__(fi)
    else:
        f.f_locals[fi[:-3]] = __import__(fi[:-3])  # inject import into namespace
