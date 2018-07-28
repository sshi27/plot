import re, json

stack = []
data = None

f = open("output.txt", "r")
for line in f.readlines():
  line = re.sub("^[ |]+", "", line)
  if line.startswith("->"):
    tmp = re.split("[\[\]]", line)
    counter = {
      "l1": tmp[1],
      "l2": tmp[3],
      "count": float(tmp[4].strip())
    }
    stack[-1]["counters"].append(counter)
  else:
    name = re.split("[\[\]]", line)[1]
  
    if line.startswith('+'):
      new = {"name": name, "time": -1, "children": [], "counters": []}
      if len(stack):
        stack[-1]["children"].append(new)
      stack.append(new)
    if line.startswith('-'):
      us = line[line.rfind(" ") + 1: -3]
      us = int(us)
      stack[-1]["time"] = us
      data = stack.pop()
    
f.close()

assert len(stack) == 0
print(json.dumps(data))
