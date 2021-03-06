import re, json


class LogReader:
  def __init__(self, path="./output.txt"):
    self.path = path
  
  def getLines(self):
    stack = [""]
    data = []
    
    f = open(self.path, "r")
    
    for line in f.readlines():
      line = re.sub("^[ |]+", "", line)
      if line.startswith("->"):  # counter
        tmp = re.split("[\[\]]", line)
        data.append(stack[-1] + " " + tmp[1] + ": " + float(tmp[4].strip()))
      else:
        name = re.split("[\[\]]", line)[1]
        
        if line.startswith('+'):
          stack.append(stack[-1] + " " + name)
        elif line.startswith('-'):
          us = line[line.rfind(" ") + 1: -3]
          us = int(us)
          data.append(stack[-1] + ": " + us)
          stack.pop()
    
    f.close()
    
    return data
  
  def getData(self):
    stack = []
    data = None
    
    f = open(self.path, "r")
    
    for line in f.readlines():
      line = re.sub("^[ |]+", "", line)
      if line.startswith("->"):
        tmp = re.split("[\[\]]", line)
        counter = {
          "l1": tmp[1],
          "count": float(tmp[4].strip())
        }
        try:
          counter["l2"] = tmp[3]
        except:
          pass
        
        stack[-1]["counters"].append(counter)
      else:
        name = re.split("[\[\]]", line)[1]
        
        if line.startswith('+'):
          new = {"name": name, "time": -1, "children": [], "counters": []}
          if len(stack):
            stack[-1]["children"].append(new)
          stack.append(new)
        elif line.startswith('-'):
          us = line[line.rfind(" ") + 1: -3]
          us = int(us)
          stack[-1]["time"] = us
          if len(stack[-1]["counters"]) == 0:
            del stack[-1]["counters"]
          if len(stack[-1]["children"]) == 0:
            del stack[-1]["children"]
          data = stack.pop()
    
    f.close()
    
    return data
