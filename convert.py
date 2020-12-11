import webvtt
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', dest="output", metavar="OUTPUT.html", type=argparse.FileType('w', encoding='UTF-8'), default=sys.stdout, help="write to output file")
parser.add_argument("main_lang", type=str, help="main language")
parser.add_argument("sub_lang", type=str, help="sub language")
parser.add_argument('input_files', nargs='*', type=str, help="/path/to/*\[cc\].vtt")

args = parser.parse_args()

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
for idx, vtt_file in enumerate(args.input_files):
  write('<title>Episode' + str(idx + 1) + '</title>')
  write('<p>======================')
  write('<p>Episode ' + str(idx + 1))
  write('<p>======================')
  write('')
  convert_file(vtt_file, args.main_lang, args.sub_lang)

write("</html>")
