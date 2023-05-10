'''
python .\split_mp4_tool.py r"C:\\  Users\\  hloma\\  Downloads\\123.mp4" -sp   240 
python .\split_mp4_tool.py r"C:\\  Users\\  hloma\\  Downloads\\123.mp4" -bt 0:39:34  0:46:41 
python .\split_mp4_tool.py r"C:\\  Users\\  hloma\\  Downloads\\123_nnn.mp4" -wav
python .\split_mp4_tool.py r"C:\\  Users\\  hloma\\  Downloads\\123_nnn.wav" -txtt
python .\mp4_tool.py r"C:\\Users\hloma\\Downloads\\【科管院talk】我的人_3600.mp4"  -louder
'''
import sys
from moviepy.editor import VideoFileClip
import time
  
# define the countdown func.
def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


# print(get_sec('1:23:45'))
def countdown(t):
    
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
      
    print('Fire in the hole!!')
def get_length(filename):
  clip = VideoFileClip(filename)
  return ( int(clip.duration) )

def convert_len_to_HHMM(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d:%02d:%02d" % (hour, minutes, seconds)
    

def to_split_mp4_by_times(in_mp4_name,times):
    
    print("-%s --"%(times))
    new_mp4_files = []
    if len(times)>1:
      times = [x[0].strip() for x in times]  
    else:
      times = times
      print("-%s --"%(times))
    
    # print("-%s --"%(x[0].strip()))
    print("proc   by time tables:%s" %times)
    for time in times:
      starttime = int(time.split("-")[0])
      endtime = int(float(time.split("-")[1]))
      print("in_mp4_name:%s" %in_mp4_name)
      import os
      loc_path = os.path.dirname(in_mp4_name)
      print("loc_path:%s" %loc_path)
      full_name = os.path.basename(in_mp4_name)
      out_pre_fix = (full_name[0:12])
      new_mp4  =  os.path.join(loc_path,out_pre_fix+"_"+ str(starttime)+ ".mp4")
      print("new_mp4:%s" %new_mp4)
      print("-----")
      
      print("out_pre_fix:%s" %out_pre_fix)
      new_mp4 = "%s_%s.mp4" % ( out_pre_fix, starttime) 
      #print(new_mp4)
      print("---save to new:----%s ----"% (new_mp4))
      #input()
      ffmpeg_extract_subclip(in_mp4_name, starttime, endtime, targetname=new_mp4)
      new_mp4_files = new_mp4_files + [new_mp4]
    print("---new_mp4_files----")
    print(new_mp4_files)
    return   new_mp4_files
         
    
def to_split_mp4_per_sec(in_mp4_name, split_sec=240):
    
    # print("-%s --"%(times)) to_split_mp4_by_times
    
    print(split_sec)
    print("----%s   sec per mp4---"% (split_sec))
    print(type(split_sec))
    mp4_len = get_length(required_video_file)
    print("影片長度:%s 秒" % (mp4_len) )
    mp4_HHMM = convert_len_to_HHMM(mp4_len)
    print("----proc file:%s---%s  %s"% (required_video_file,mp4_len, mp4_HHMM))
    times_table = gen_split_sec_table(int(mp4_len), int(split_sec))
    print(times_table)
    input("wait")
    to_split_mp4_by_times(in_mp4_name,times_table)

      
      #ffmpeg_extract_subclip(required_video_file, starttime, endtime, targetname=str(times.index(time)+1)+".mp4")
def gen_split_sec_table(mp4_len, split_sec=180):
        times = []
        times2 = ["0:0-0"]
        for i in range((int(int(mp4_len)/int(split_sec))+1)):
            
            st = 0
            ret = 0
            starttime = i*split_sec
            endtime = int((i+1)*split_sec)
            endtime2 = (i+2)*split_sec
              
              
            if endtime > mp4_len:
              endtime = mp4_len
            if endtime2 > mp4_len:
              endtime = mp4_len
              ret = 1
            ts ="%s:%s-%s\n" % (i, starttime, endtime  )
            ts ="%s-%s\n" % (  starttime, endtime  )
            # print("iiii====--%s====--00--" % (ts[0:-1]))
            uu = [ts[0:-1]]
            times = times +[uu]
            
            '''
            
            '''
            if ret == 1:         
              # print("====--dd%s %s====--kk" % (i, st)) 
              # print("==== time tables===--" )  
              # print(times)
              # print("==== time tables===--" )  
              # print("====--dd%s %s====--kk" % (i, st)) 
              for i in times:
                # print("____%s_____" % ( i )) 
                # print("lyy")
                # print(type(i))
                # print("lyy")
                starttime = int(i[0].split("-")[0])
                endtime = int(float(i[0].split("-")[1]))
                # print("2222")
                # print(starttime)
                # print("2222")
                # print(endtime)
                return   times

def do_mp4_recognize(filenames, lantype= 'zh-TW'):
   print("--- DO recognize in %s "% (lantype))
   #pip install SpeechRecognition
   #pip install pydub
   import speech_recognition as sr
   from pydub import AudioSegment
   # import os
   for filename in  filenames:
    # Load the video file
    # filename = r'C:\Users\hloma\Videos\m1.mp4'
    #lantype= 'zh-TW'
    #lantype= 'en-US'
    temp_audio_file = "audio.wav"
    # print("in getsound %s" % (filename))
    print("--- Proc file: %s "% (filename))
    print("--- lan type: %s "% (lantype))
    video = AudioSegment.from_file(filename, format="mp4")
    audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    audio.export(temp_audio_file, format="wav")
    print("out getsound %s" % (temp_audio_file))
    if 'txt' in sys.argv[4]:
      go_recognize = False
    else:
      go_recognize = True
    
      
    if go_recognize:
      print("not to Recognizer %s" % (1))
      sys.exit()
    else:
      if():
        pass
      else:
        print("wav <10mb ok to go ")
        folder = r".\\"
        file = temp_audio_file
        
        split_wav = SplitWavAudioMubin(folder, file)
        from_min = 0
        to_min = 3
        split_wav.single_split(self, from_min, to_min, r'.\\'+temp_audio_file)
      # print(audio)
      
      # Initialize recognizer class (for recognizing the speech)
      r = sr.Recognizer()
      
      # Open the audio file
      with sr.AudioFile(temp_audio_file) as source:
          audio_text = r.record(source)
      # Recognize the speech in the audio
      # text = r.recognize_google(audio_text, language='en-US')
      
      text = r.recognize_google(audio_text, language=lantype)
      text_file = filename[:-4]+"_逐字稿.txt"
      print("save to %s" % (text_file))
      with open(text_file, 'w') as tfp:
        tfp.write(text)
        
      
      print("saved")
      print(text)

def split(src_video_file, starttime, endtime, new_mp4_name):
  
  # if (len(sys.argv)>4) and (':' in sys.argv[2] and ':' in sys.argv[3])
  ffmpeg_extract_subclip(src_video_file, starttime, endtime, targetname=new_mp4_name)

def gen__mp4_s_wav(in_mp4_name):
  from pydub import AudioSegment
  import os
  loc_path = os.path.dirname(in_mp4_name)
  print("loc_path:%s" %loc_path)
  full_name = os.path.basename(in_mp4_name)
  # out_pre_fix = (full_name[0:12])
  temp_audio_file = full_name[0:-4]+'.wav'
  video = AudioSegment.from_file(in_mp4_name, format="mp4")
  audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
  audio.export(temp_audio_file, format="wav")
  print("saved wav:%s" % (temp_audio_file) )
  return temp_audio_file


                 
def get_file_size_in_bytes_3(file_path):
   """ Get size of file at given path in bytes"""
   # get file object
   from pathlib import Path
   file_obj = Path(file_path)
   # Get file size from stat object of file
   size = file_obj.stat().st_size
   return size  # 'File size in bytes

def get_wav_duration(file_path):
   # get file object
   import librosa
   wav_duration = librosa.get_duration(filename=file_path)
   print("wav_duration:: %s seconds" % (wav_duration))
   return wav_duration  ## 'File size in bytes
   
def split_wav_by_sec(file_path, st1, st2, new_file_path):
   from pydub import AudioSegment
   
   t1 = st1 * 1000 #Works in milliseconds
   t2 = st2 * 1000
   newAudio = AudioSegment.from_wav(file_path)
   newAudio = newAudio[t1:t2]
   newAudio.export(new_file_path, format="wav")
   print("save wav:: %s" % (new_file_path))


def do_wav_recognize4(wav_filename,  lantype= 'zh-TW'):
   gtext = ""
   text_0 = "   \n-294-------- %s ---------\n"% (wav_filename)
   print("----do_wav_recognize4 %s" % (wav_filename))
   import speech_recognition as sr
   
   r = sr.Recognizer()
   with sr.AudioFile(wav_filename) as source:
        audio_text = r.record(source)
   try:
     gtext = r.recognize_google(audio_text, language=lantype)
   except Exception as e:
     print(repr(e))
     
     text = text_0+repr(e)+gtext+"\n\n\n"
        
   # print("save to %s" % (save_text_file))
   text = text_0+gtext+"\n\n\n"
   return text



def do_wav_recognize5(wav_filename,  lantype= 'zh-TW'):
   gtext = ""
   text_0 = "   \n-294-------- %s ---------\n"% (wav_filename)
   print("----do_wav_recognize5 %s" % (wav_filename))
   import speech_recognition as sr
   
   r = sr.Recognizer()
   with sr.AudioFile(wav_filename) as source:
        audio_text = r.record(source)
   try: 
        gtext = r.recognize_google(audio_text, language=lantype)
        print("vvvvvv")
        print(gtext)
        print("^^^^^^")
   except Exception as e:
        gtext = "\n-334----------Exception \n["+ repr(e) +"]\n----------\n"
        print(repr(e))
        
   # print("save to %s" % (save_text_file))
   text = text_0+gtext+"\n\n\n"
   return text
def mp4_2_louder_wav(filename_mp4):
   
   o_audio = r"temp_audio.wav"
   o_temp_audio = "----"
   import os 
   from pydub import AudioSegment
   loc_path = os.path.dirname(filename_mp4)
   print("loc_path:%s" %loc_path)
   full_name = os.path.basename(filename_mp4)
   out_pre_fix = (full_name[0:-4])
   louder_audio_temp_file  =  os.path.join(loc_path,o_audio)
   new_louder_mp4_file  =  os.path.join(loc_path,out_pre_fix+"_louder.mp4")
   
   to_louder_video = AudioSegment.from_file(filename_mp4, format="mp4")
   # boost volume by 9dB
   louder_video = to_louder_video + 999
   # audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
   louder_video.export(louder_audio_temp_file, format='wav')
   to_louder_video.export(louder_audio_temp_file, format="wav")
   print("---out sound %s" % (louder_audio_temp_file))
   
   

def getsound_txt(wav_filename, lantype= 'zh-TW'):#en-US
   #pip install SpeechRecognition
   #pip install pydub
   wav_duration = get_wav_duration(wav_filename)
   size = get_file_size_in_bytes_3(wav_filename)
   wav_size_MB = float(size/1024/1024)
   text ="\n  "
   if wav_duration  >99:
      print("wav too big to recognize %s - to split small wav files" % (""))
      wav_split_interval = 25
      wav_split_interval_back = 3
      times_to_ask_google = 9
      wav_sp_table = []
      wav_file_table = []
      loop_times = int(wav_duration/wav_split_interval)
      print("to split wav to  %s:: files" % (loop_times))
      text ="\n  "
      # text_0 = "   \n\n\n-384-------- %s ---------\n"% (wav_filename)
      
      save_text_file = wav_filename[:-4]+"_逐字稿.txt"

      for i in range(loop_times):
        if i<2:
          start_time_sec = (wav_split_interval*(i))
          start_time_sec = 0
        else:
          start_time_sec = ((wav_split_interval*(i-1))-wav_split_interval_back)
        stop_time_sec = i*wav_split_interval
        # print("seq:: %s  start_time_sec:: %s  stop_time_sec:: %s" % ( i , start_time_sec , stop_time_sec))
        wav_sp_table.append([i , start_time_sec , stop_time_sec])
        
        #  new_wav_file_ = wav_filename[0:-4]+"_" + str(i) + "_temp.wav"
        st1 = start_time_sec
        st2 = stop_time_sec
        new_wav_file_ = wav_filename[0:-4]+"_"+str(i)+"_temp.wav"
        split_wav_by_sec(wav_filename, st1, st2, new_wav_file_)
        wav_file_table.append([new_wav_file_]) 
        # save_new_wav_text_file = new_wav_file_[:-4]+"_temp_逐字稿.txt"
        # #print("---%s  " % new_wav_file_)
        # save_new_wav_text_file = wav_filename[:-4]+"_temp_逐字稿.txt"
      for file in wav_file_table[2:times_to_ask_google]:
          print("file is : %s "% (file[0]) )
          # input("wait type %s"% (type(file[0])) )
          gtext = "test"
          
          gtext = do_wav_recognize5(file[0], lantype= 'zh-TW')
          # text_1 = "   \n\n--417--------- %s ---------\n\n"% (file[0])
          text = text+"\n\n"+gtext+"\n\n\n"
          # text += text
      with open(save_text_file, 'w') as tfp:
          tfp.write(text)
      print("saved : %s "% (save_text_file) )
      #from pprint import pprint 
      #pprint(wav_sp_table[:])
      #pprint(wav_file_table)
      #pprint(wav_file_table[:4])
      #pprint(wav_sp_table[:5])
      sys.exit()
   else:
     print(" ---direct recognize wav %s" % ("")) 
     #new_wav_file1 = wav_filename[0:-4]+"_temp"+".wav"
        
     #save_new_wav_text_file = wav_filename[:-4]+"_逐字稿.txt"
     txt = do_wav_recognize5(wav_filename, lantype= 'zh-TW')
     print(txt)
   
   
     
   sys.exit("done") 



#!/usr/bin/env python
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# Replace the filename below.
# required_video_file = "filename.mp4"
# a = len(sys.argv) if a>2 required_video_file = sys.argv[1]
# a = 1 if n < 10 else 2 if n > 10 else 0
argc = len(sys.argv)
required_video_file = sys.argv[1]  if  argc>1 else ""
MP4_src = required_video_file
# split_sec = sys.argv[2]
split_sec = ['path',4]
print("來源 mp4:   %s "% (MP4_src))
per_sec = sys.argv[-1]
print("num of arg:   %s "% (len(sys.argv)))
print("last arg:   %s "% (MP4_src))


if (len(sys.argv)<2):
  usage = '''
python .\split_mp4_tool.py "C:\\  Users\\  hloma\\  Downloads\\123.mp4" -sp   240 
python .\split_mp4_tool.py "C:\\  Users\\  hloma\\  Downloads\\123.mp4" -bt 0:39:34  0:46:41 
python .\split_mp4_tool.py "C:\\  Users\\  hloma\\  Downloads\\123_nnn.mp4" -wav
python .\split_mp4_tool.py "C:\\  Users\\  hloma\\  Downloads\\123_nnn.wav" -txtt
python .\mp4_tool.py "C:\\Users\\hloma\\Downloads\\【科管院talk】我的人_3600.mp4"  -louder
'''
  print(usage)


if '-sp' in sys.argv:
  
  print((sys.argv))
  print("依參數分多段:   %s "% (sys.argv[-1]))
  per_sec = sys.argv[-1]
  print("num of arg:   %s "% (len(sys.argv)))
  print("last arg:   %s "% (sys.argv[-1]))
  print("mp4:   %s "% (sys.argv[1]))
  new_mp4_files = to_split_mp4_per_sec(MP4_src,per_sec)
  sys.exit("exit")

if '-bt' in sys.argv:
  
  print((sys.argv))
  print("依參數取一段mp4:   %s "% (sys.argv[0]))
  if (len(sys.argv)>4) and (':' in sys.argv[-2] and ':' in sys.argv[-1]):
    # split(MP4_src, starttime, endtime, new_mp4_name)
    split_start_str = (sys.argv[-2])
    split_stop_str = (sys.argv[-1])
    split_start_sec =  get_sec( split_start_str )
    split_stop_sec =  get_sec( split_stop_str )
    time_str = "%s-%s" % ((split_start_sec), (int(split_stop_sec)))
    print((time_str))
  ado = to_split_mp4_by_times(MP4_src,[time_str,])
  sys.exit("exit")


if '-wav' in sys.argv:
  
  # print((sys.argv))
  print("產生mp4的wav:   %s "% ("GO"))
  gen__mp4_s_wav(MP4_src)
  sys.exit("exit")

wav_filename = MP4_src
if '-txt' in sys.argv:
  
  # print((sys.argv))
  print("產生 wav的文字:   %s "% (sys.argv[1]))
  getsound_txt(wav_filename, lantype= 'zh-TW')
  sys.exit("exit")

if '-txtt' in sys.argv:
  print("產生 wav的文字TT:   %s "% (sys.argv[1]))
  getsound_txt(wav_filename, lantype= 'zh-TW')
  
  sys.exit("exit")


if '-greco' in sys.argv:
  print("recognize:   %s "% (sys.argv[1]))
  file = sys.argv[1]
  gtext = do_wav_recognize4(file, lantype= 'zh-TW')
  print(gtext)
  sys.exit("exit")

if '-louder' in sys.argv:
  print("recognize:   %s "% (sys.argv[1]))
  filename_mp4 = sys.argv[1]
  print("generate wav from:   %s "% (sys.argv[1]))
  mp4_2_louder_wav(filename_mp4)
  # print(gtext)
  sys.exit("exit")

# print("split file:   %s "% (required_video_file))
if (len(sys.argv)>4) and (':' in sys.argv[2] and ':' in sys.argv[2]): 
  split_start_str = (sys.argv[2])
  split_stop_str = (sys.argv[3])
  split_start_sec =  get_sec( split_start_str )
  split_stop_sec =  get_sec( split_stop_str )
  time_str = "%s-%s" % ((split_start_sec), (int(split_stop_sec)))
  print((time_str))  
  print(type(time_str))
  # time_split_sec = int(sys.argv[2])
  # print("第2個參數是分割秒數如180是3分   %s "% (time_split_sec))
  # split_start_str = (sys.argv[3])
  # split_start_sec =  get_sec( split_start_str )
  # print("第3個參數是分割start秒數%s "% (split_start_sec) )
  # time_str = "%s-%s" % ((split_start_sec), (int(split_start_sec+time_split_sec)))
  # print((time_str))
  ado = to_split_mp4_by_times(required_video_file,[time_str,])
  do_mp4_recognize(ado, lantype= 'zh-TW')
  # print("第2個參數是分割秒數如180是3分: .. ： ")
  # print("第3個參數是分割start秒數如180是3分: .. ： ")
  sys.exit()

'''
if (len(sys.argv)==4): 
  time_split_sec = int(sys.argv[2])
  print("第2個參數是分割秒數如180是3分   %s "% (time_split_sec))
  split_start_str = (sys.argv[3])
  split_start_sec =  get_sec( split_start_str )
  print("第3個參數是分割start秒數%s "% (split_start_sec) )
  time_str = "%s-%s" % ((split_start_sec), (int(split_start_sec+time_split_sec)))
  print((time_str))
  print(type(time_str))
  ado = to_split_mp4_by_times(required_video_file,[time_str,])
  getsound(ado, lantype= 'zh-TW')
  # print("第2個參數是分割秒數如180是3分: .. ： ")
  # print("第3個參數是分割start秒數如180是3分: .. ： ")
  sys.exit()
print("每  %s 秒切成一個影片檔案 184" % (split_sec))
# countdown(6)
# # # input("Press Enter to continue...")
# split_sec = unicode(split_sec, 'utf-8')
# time_str_issec = get_sec(time_str)
# to_split_mp4_by_times
if (len(sys.argv)<3):
   print("第2個參數是分割秒數如180是3分: .. ： ")
   try:
    
      split_sec = int(input('秒數: .. ： '))
   except:
      split_sec = int(240)
   print("------")
   print("----%s--"% (split_sec))
   # split_sec = int(split_sec)
   
   # print(type(split_sec))
   print("第------")
   print(type(split_sec))
else :
   split_sec = int(sys.argv[2])
   print("每  %s 秒切成一個影片檔案 206" % (split_sec))
   countdown(6)
# # # input("Press Enter to continue...")
   # split_sec = unicode(split_sec, 'utf-8')

'''
'''
print(split_sec)
print(type(split_sec))
mp4_len = get_length(required_video_file)
print("影片長度:%s 秒" % (mp4_len) )
mp4_HHMM = convert_len_to_HHMM(mp4_len)
print("----proc file:%s---%s  %s"% (required_video_file,mp4_len, mp4_HHMM))
times = split_mp4_by_sec(int(mp4_len), split_sec)#360
print(times)
new_mp4_files = to_split_mp4_by_times(required_video_file,times)
# getsound(new_mp4_files, lantype= 'zh-TW') to_split_mp4_per_sec

print("33333")
print(times)
print("33333")
sys.exit()
input()
'''
