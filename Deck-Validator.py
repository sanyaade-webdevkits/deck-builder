#!/usr/bin/python

# This software is owned by Cooliris, Inc., copyright 2011, and licensed to you under the
# Software License Agreement for the Decks by Cooliris Template Files and Sample Code available at
# http://www.decksapp.com/sample-code-license/

import sys, os, subprocess
try:
  from Quartz import *
  USE_QUARTZ = True
except ImportError:
  USE_QUARTZ = False

MAX_IMAGE_SIZE = 1024 * 1024
MAX_IMAGE_WIDTH = 2048
MAX_IMAGE_HEIGHT = 2048

def _ValidateXMLFile(path):
  success = True
  status = subprocess.call('xmllint "%s" > /dev/null' % path, shell=True)
  if status != 0:
    print "[%s] Invalid XML" % path
    success = False
  return success

def _ValidatePageKitFile(path, fonts):
  success = _ValidateXMLFile(path)
  if success == True and fonts != None:
    fd = open(path, "r")
    content = fd.read()
    if content.find("<name>@") >= 0:
      print '[%s] Contains "<name>@" sequence' % path
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
          print '[%s] Unknown font "%s"' % (path, font)
          success = False
        start = end + 7
    fd.close()
  return success

def _ValidateImageFile(path):
  success = True
  size = os.path.getsize(path)
  if size > 0 and size <= MAX_IMAGE_SIZE:
    format = None
    width = None
    height = None
    if USE_QUARTZ: # Use Quartz bindings if avaliable
      source = CGImageSourceCreateWithURL(CFURLCreateWithFileSystemPath(None, path, kCFURLPOSIXPathStyle, False), None)
      if source != None:
        format = CGImageSourceGetType(source)
        if format == "public.png":
          format = "PNG"
        elif format == "public.jpeg":
          format = "JPEG"
        properties = CGImageSourceCopyPropertiesAtIndex(source, 0, None)
        if properties != None:
          width = int(properties[kCGImagePropertyPixelWidth])
          height = int(properties[kCGImagePropertyPixelHeight])
    else:  # Otherwise, use ImageMagick
      format = subprocess.Popen(["identify", "-format", "%m", path], stdout=subprocess.PIPE).communicate()[0].rstrip('\n')
      width = int(subprocess.Popen(["identify", "-format", "%w", path], stdout=subprocess.PIPE).communicate()[0].rstrip('\n'))
      height = int(subprocess.Popen(["identify", "-format", "%h", path], stdout=subprocess.PIPE).communicate()[0].rstrip('\n'))
    if format == "JPEG" or format == "PNG":
      if width < 1 or width > MAX_IMAGE_WIDTH or height < 1 and height > MAX_IMAGE_HEIGHT:
        print "[%s] Invalid dimensions of %i X %i pixels" % (path, width, height)
        success = False
    else:
      print "[%s] Unknown format '%s'" % (path, format)
      success = False
  else:
    print "[%s] Unsupported size of %i bytes" % (path, size)
    success = False
  return success

def _ValidateMovieFile(path):
  # TODO
  return True

def _ValidateFiles(dir, fonts):
  success = True
  basedir = dir
  for item in os.listdir(dir):
    if not item.startswith("."):
      path = os.path.join(basedir, item)
      if os.path.isfile(path):
        extension = os.path.splitext(path)[1]
        if extension == ".include" or extension == ".page":
          if not _ValidatePageKitFile(path, fonts):
            success = False
        elif extension == ".jpg" or extension == ".png":
          if not _ValidateImageFile(path):
            success = False
        elif extension == ".xml" or extension == ".plist":
          if not _ValidateXMLFile(path):
            success = False
        elif extension == ".mov":
          if not _ValidateMovieFile(path):
            success = False
        elif len(extension) > 0:
          print "[%s] Unsupported file extension '%s'" % (path, extension)
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
