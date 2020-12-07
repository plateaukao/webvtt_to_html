import webvtt
import sys

if len(sys.argv) < 2:
  print("need file names")
  sys.exit(1)

def convert_file(file_name):
  vtt_k = webvtt.read(file_name[1:])
  vtt_z = webvtt.read(file_name)

  # while loop all korean time captions
  index_k = 0
  index_z = 0
  while index_k < len(vtt_k):
    while index_z < len(vtt_z):
      caption_k = vtt_k[index_k]
      caption_z = vtt_z[index_z]

      if (caption_k.start < caption_z.start):
        print(caption_k.text)
        break
      else:
        print(caption_z.text)
        print("")
        index_z += 1
    index_k += 1

  # finish final z index
  while index_z < len(vtt_z):
    print(caption_z.text)
    index_z += 1


  print('end of ' + file_name)

for i in range(1, len(sys.argv)):
  print('<title>第' + str(i) + '集</title>')
  print('======================')
  print('第' + str(i) + '集')
  print('======================')
  print('')
  convert_file(sys.argv[i])
