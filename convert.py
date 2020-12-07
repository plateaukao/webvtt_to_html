import webvtt
import sys

if len(sys.argv) < 4:
  print("need file names")
  sys.exit(1)

def rreplace(s, old, new):
  li = s.rsplit(old, 1)
  return new.join(li)

def convert_file(file_name, main_lang, sub_lang):
  file_name_sub = rreplace(file_name, main_lang, sub_lang)
  #print(file_name + '\n' + file_name_sub)
  #return
  vtt_main = webvtt.read(file_name)
  vtt_sub = webvtt.read(file_name_sub)

  # while loop all korean time captions
  index_main = 0
  index_sub = 0
  while index_main < len(vtt_main):
    while index_sub < len(vtt_sub):
      caption_k = vtt_main[index_main]
      caption_z = vtt_sub[index_sub]

      if (caption_k.start < caption_z.start):
        print(caption_k.text)
        break
      else:
        print(caption_z.text)
        print("")
        index_sub += 1
    index_main += 1

  # finish final z index
  while index_sub < len(vtt_sub):
    print(caption_z.text)
    index_sub += 1


  print('end of ' + file_name)

# main
lang_main = sys.argv[1]
lang_sub = sys.argv[2]
for i in range(3, len(sys.argv)):
  print('<title>Episode' + str(i - 2) + '</title>')
  print('======================')
  print('Episode ' + str(i - 2))
  print('======================')
  print('')
  convert_file(sys.argv[i], lang_main, lang_sub)
