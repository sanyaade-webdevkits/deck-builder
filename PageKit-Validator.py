#!/usr/bin/python
import sys, os, subprocess

def _ValidateFile(path, fonts):
  success = True
  status = subprocess.call("/usr/bin/xmllint \"" + path + "\" > /dev/null", shell=True)
  if status != 0:
    print "[" + path + "] Invalid XML"
    success = False
  elif fonts:
    fd = open(path, "r")
    content = fd.read()
    if content.find("<name>@") >= 0:
      print "[" + path + "] Contains \"<name>@\" sequence"
      success = False
    else:
      start = 0
      while True:
        start = content.find("<name>", start)
        if start < 0:
          break
        start += 6
        end = content.find("</name>", start)
        if end < 0:
          raise Exception('Internal error')
        font = content[start:end]
        if not font in fonts:
          print "[" + path + "] Unknown font \"" + font + "\""
          success = False
        start = end + 7
    fd.close()
  return success

def _ValidateFiles(dir, fonts):
  success = True
  basedir = dir
  for item in os.listdir(dir):
    if not item.startswith("."):
      path = os.path.join(basedir, item)
      if os.path.isfile(path):
        if item.endswith(".include") or item.endswith(".page"):
          if not _ValidateFile(path, fonts):
            success = False
      elif os.path.isdir(path):
        if not _ValidateFiles(path, fonts):
          success = False
  return success

# Retrieve base directory
basedir = os.path.dirname(os.path.join(os.getcwd(), sys.argv[0]))

# Load list of allowed fonts
fonts = set()
for line in open(os.path.join(basedir, "PageKit-Allowed-Fonts.txt")):
  line = line.strip()
  if len(line) and line.find("#") < 0:
    fonts.add(line)

# Scan passed directory for PageKit files
success = _ValidateFiles(sys.argv[1], fonts)

# Exit with non-zero status if there were any errors
if not success:
  exit(1)
else:
  exit(0)
