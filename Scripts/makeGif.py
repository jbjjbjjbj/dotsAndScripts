#!/usr/bin/env python
import sys
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--start',
                    required=False,
                    type=int,
                    default=0, 
                    dest="start",
                    help="Time to start gif at. [0]" )
parser.add_argument('-l', '--lenght',
                    required=True,
                    type=int,
                    dest="lenght",
                    help="Lenght of gif in seconds" )
parser.add_argument('-i', '--infile',
                    required=True,
                    type=str,
                    dest="infile",
                    help="Movie to convert" )
parser.add_argument('-o', '--outfile',
                    required=False,
                    type=str,
                    default="output.gif",
                    dest="outfile",
                    help="Output gif name. [output.gif]")
parser.add_argument('-f', '--fps',
                    required=False,
                    type=int,
                    default=10,
                    dest="fps",
                    help="Frames per second. [10]")
parser.add_argument('-r', '--resolution',
                    required=False,
                    type=int,
                    default=320,
                    dest="res",
                    help="Resolution. [320]")
args = parser.parse_args()


os.system("ffmpeg -y -ss " + str(args.start) + " -t " + str(args.lenght) + " -i '" + args.infile + "' -vf fps=" + str(args.fps) + ",scale=" + str(args.res) + ":-1:flags=lanczos,palettegen palette.png")

string = 'fps=' + str(args.fps) + ',scale=' + str(args.res) + ':-1:flags=lanczos[x];[x][1:v]paletteuse'

os.system('ffmpeg -ss ' + str(args.start) + ' -t ' + str(args.lenght) + ' -i "' + args.infile + '" -i palette.png -filter_complex "' + string + '" "' + args.outfile + '"')

os.remove("palette.png")

print("\n\nDONE - your file " + args.outfile + " is ready. Have a nice day :-D")
