#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by svsd_val
# jabber : svsd_val@jabber.ru
# mail to: svsdval@gmail.com

import os
import datetime
import time
import re
import sys

from PIL import Image , ImageDraw

if len(sys.argv) > 1:
 path = sys.argv[1]
if not os.path.exists('layers'):
 os.mkdir('layers');

f = open(path, "r");
n =0;

# setup image resolution
img_width=1440;
img_height=2560;
# get pixels in mm
pw=img_height/120.96;
# setup line width
LW = 2;

#
img = Image.new('RGB', [img_width,img_height], 0)
draw = ImageDraw.Draw(img)
data = img.load()

#
lb=[0,0];
le=(0,0);
seg=[];

currentLayerIdx = 0
currentLayerZ = 0

# first time prev command is empty
prev= {
	"C":"-",
	"X":0.0,
	"Y":0.0,
	"Z":0.0,
	"F":0.0,
	"E":0.0,
	"T":0,
        "L":0 };


def parse(l):
 global prev;
 global currentLayerIdx
 global currentLayerZ

 scmd = re.sub("\([^)]*\)", "", l.upper())
 ## then semicolons
 symidx = scmd.find(';')
 if symidx >= 0:
  scmd = scmd[0:symidx].strip()

 symidx = scmd.find('(')
 if symidx >= 0:
  scmd = scmd[0:symidx].strip();

 cmd= {
	"C":"-",
	"X":0.0,
	"Y":0.0,
	"Z":0.0,
	"F":0.0,
	"E":0.0,
	"T":0,
        "L":0 };

# if scmd == "": 
#  cmd["C"] = "-"
#  return cmd;

 array = scmd.split(" ");

 cmd["C"] = array[0];
 for i in range(1,len(array)):
  x=array[i];
  if len(x) < 1:
   continue;

  cmd[x[:1]] = float(x[1:]);

 cmdtype = "move"
 if ( (cmd["X"] == prev["X"]) and (cmd["Y"] == prev["Y"]) and (cmd["E"] != prev["E"]) ):
   cmdtype = "retract" if (cmd["E"] < prev["E"]) else "restore"

 if ( ( (cmd["X"] != prev["X"]) or (cmd["Y"] != prev["Y"]) ) and (cmd["E"] > prev["E"]) ):
   cmdtype = "extrude"

 if ( (cmd["Z"] > prev["Z"]) ):
   currentLayerZ = cmd["Z"]
   currentLayerIdx += 1
   print("currentLayerZ",currentLayerZ, " currentLayerIdx=",currentLayerIdx);

 # set cmdtype and layer index for command
 cmd["T"] = cmdtype
 cmd["L"] = currentLayerIdx;
 # save as last command, to combare with new command after...
 prev = cmd

 #print (cmd);
 return cmd;

def seg2vec(seg):
 return [ int(seg["X"] * pw ), int(seg["Y"]* pw )];


old_z=0;
layer_idx=0;

for l in f:
 cmd = parse(l);
 seg.append(cmd);

 #if cmd["C"] == "-":
 # continue;

 #print(cmd);

 if old_z != cmd["L"]:
  #
  print("Z", old_z)
  old_z = cmd["L"];
  #
  # check if we have segments to draw..
  empty=1;
  for i in range(len(seg)):
    if seg[i]["T"] == "extrude":
      empty=0;
  # if not, then
  if empty:
   print("skip.." , old_z)
   continue

  layer_idx+=1;
  # Create new image with black fill
  img = Image.new('RGB', [img_width,img_height], 0)
  draw = ImageDraw.Draw(img)
  lb= seg2vec(seg[0]);
  # Draw segments:
  for i in range(len(seg)):
    if seg[i]["T"] != "extrude":
     continue;
    if (i >0):
      lb=seg2vec(seg[i-1]);
    le=seg2vec(seg[i]);
    if lb[0] == 0 and lb[1] == 0 :
     lb=le;
    if le[0] == 0 and le[1] == 0 :
     le=lb;

    draw.line([ lb[0], lb[1], le[0],le[1] ], width=LW, fill="#FFFFFF");
  # generate image id
  si=str(layer_idx);
  while len(si) < 7:
    si="0"+si;
  s="layers/layer_"+si+".png"
  # save to file
  print("save layer to file:"+s);
  img.save(s);
  # and print we got a new layer
  print("New Layer");
  # remove all old not needed layer segments
  seg[:] = [];

f.close();
