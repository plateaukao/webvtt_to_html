import webvtt
import sys
import argparse
import re
from os import listdir
from os.path import isfile, join

parser = argparse.ArgumentParser()
parser.add_argument('-o', dest="output", metavar="OUTPUT.html", type=argparse.FileType('w', encoding='UTF-8'), default=sys.stdout, help="write to output file")
parser.add_argument("-d", dest="dir", metavar="Directory", type=str, help="/path/to/vtt/dir")

args = parser.parse_args()

files = [f for f in listdir(args.dir) if isfile(join(args.dir, f))]
vtt_files_name = [f for f in files if re.match('.*\.vtt$', f)]
cc_vtt_files_name = [f for f in files if re.match('.*\[cc\]\.vtt$', f)]
cc_vtt_files_name.sort()
langs = map(lambda name: re.search('.*\.(.+?)\.vtt', name).group(1) ,vtt_files_name)
langs = list(set(langs)) # uniq
langs.sort()

for index, lang in enumerate(langs):
  print('[{idx:d}] {title:s}'.format(idx=index, title=lang))

main_lang_idx = int(input("select main lang: "))
sub_lang_idx = int(input("select sub lang: "))

def write(str):
    args.output.write(str)
    args.output.write("\n")

def rreplace(s, old, new):
  li = s.rsplit(old, 1)
  return new.join(li)

def convert_file(file_name, main_lang, sub_lang):
  file_name_sub = rreplace(file_name, main_lang, sub_lang)
  #write(file_name + '\n' + file_name_sub)
  #return
  vtt_main = webvtt.read(file_name)
  vtt_sub = webvtt.read(file_name_sub)

  # while loop all korean time captions
  index_main = 0
  index_sub = 0
  while index_main < len(vtt_main):
    while index_sub < len(vtt_sub):
      caption_main = vtt_main[index_main]
      caption_sub = vtt_sub[index_sub]

      if (caption_main.start <= caption_sub.start):
        #write("##### " + caption_main.text.replace("&lrm;","").replace("\n","\n##### "))
        write("<h3>" + caption_main.text.replace("&lrm;","") + "</h3>")
        break
      else:
        write("<p>" + caption_sub.text.replace("&lrm;", ""))
        write("<p>")
        index_sub += 1
    index_main += 1

  # finish final z index
  while index_sub < len(vtt_sub):
    write(caption_sub.text)
    index_sub += 1

  #write('end of ' + file_name)

# main
write("<html>")
for idx, vtt_file_name in enumerate(cc_vtt_files_name):
  vtt_file = join(args.dir, vtt_file_name)
  write('<title>Episode' + str(idx + 1) + '</title>')
  write('<p>======================')
  write('<p>Episode ' + str(idx + 1))
  write('<p>======================')
  write('')
  convert_file(vtt_file, langs[main_lang_idx], langs[sub_lang_idx])

write("</html>")
