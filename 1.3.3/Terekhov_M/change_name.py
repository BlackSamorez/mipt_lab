import sys
ARG_NUMBER = 4
assert len(sys.argv) == ARG_NUMBER, "Usage: script.py <Name> <Surname> <group>"
with open("1_3_3.tex", "r") as f:
    text = f.read()
sp = text.split("rhead{")
text = sp[0] + "rhead{" + sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3]
for i in sp[1].split("\\")[1:]:
        text += "\\" + i
print(text)
