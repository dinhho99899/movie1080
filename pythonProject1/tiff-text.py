from moviepy.editor import *
import ffmpeg
import os
import subprocess
from moviepy.editor import *
def process_video(input, output,text):
    """Parameter input should be a string with the full path for a video"""
    print(input,output)
    clip = VideoFileClip(input)
    width_a = clip.w
    height_a = clip.h
    new_text,fonsize,split,numberword = split_txt_into_multi_lines(text,width_a,height_a)
    print(new_text,split,fonsize,numberword)
    subprocess.call(["ffmpeg","-i",input,"-i","C:/Users/dinhh/Desktop/MainProjectDinhho/pythonProject/srt/dtiff.tiff", "-filter_complex", rf"[0:v]drawtext=fontfile=Poppins-Bold.ttf:text={new_text}:fontcolor=white:fontsize={fonsize}:line_spacing=0.5:box=1:boxcolor=black@0.1:boxborderw=20:x=(w-text_w)/2:y=(h-text_h)/2:text_align=C:enable='between(t,0,2)'[video];[1:v]format=argb,geq=r='r(X,Y)':a='0.01*alpha(X,Y)'[zork];[video][zork]overlay","-codec:a","copy",output,])
def split_txt_into_multi_lines(input_str: str,width_a: int,height_a:int):
    x = input_str.replace(',','')
    x = input_str.replace("'",'')
    words = x.split(" ")
    numberword = len(words)
    print(numberword)
    line_length = 2
    fontsize = 0
    split =3
    line_count = 0
    
    if numberword <10:
     fontsize = 65
    if numberword >=10:
     fontsize = 57
    if numberword >=15:
     fontsize = 47
    if numberword >=20:
     fontsize = 45
    if numberword >=25:
     fontsize = 45
    if width_a <900:
       fontsize = fontsize -17
    if width_a >900 and width_a <=1300 and height_a<1000:
       fontsize = fontsize +3
    if width_a >900 and width_a <=1300 and height_a>1000:
       fontsize = fontsize +7
    if width_a >1300:
       fontsize = fontsize +7
    if width_a >1600:
       fontsize = fontsize+12
       
    # subprocess.call(["ffmpeg","-i",input,"-i","C:/Users/dinhh/Desktop/MainProjectDinhho/pythonProject/srt/dtiff.tiff", "-filter_complex", rf"[0:v]drawtext=fontfile=Poppins-Medium.ttf:text={new_text}:fontcolor=white:fontsize=85:box=1:boxcolor=black@0.3:boxborderw=12:line_spacing=1:x=(w-text_w)/2:y=(h-text_h)/1.3:text_align=C:enable='between(t,0,2)'[video];[1:v]format=argb,geq=r='r(X,Y)':a='0.01*alpha(X,Y)'[zork];[video][zork]overlay","-codec:a","copy",output,])
    split_input = ""
    for word in words:
        line_count += 1
        split_input += word
        split_input += " "
        if line_count > line_length:
            split_input += "\n"
            line_length +=split
           
    print(split_input)
    return split_input,fontsize,split,numberword
        

def get_video_paths(folder_path):
    """
    Parameter folder_path should look like "Users/documents/folder1/"
    Returns a list of complete paths
    """
    file_name_list = os.listdir(folder_path)

    path_name_list = []
    final_name_list = []
    text_list =[]
    for name in file_name_list:
        # Put any sanity checks here, e.g.:
        if name == ".DS_Store":
            pass
        else:
            text = name.replace('.mp4','')
            text_list.append(text)
            path_name_list.append(folder_path + name)
            final_name_list.append(folder_path + "ztiff_" + name)
    return path_name_list, final_name_list, text_list


if __name__ == "__main__":
    video_folder = input("What folder would you like to process? ")
    path_list, final_name_list,text_list  = get_video_paths(video_folder)
    for path, name,text in zip(path_list, final_name_list,text_list):
        process_video(path, name,text)
    print("Finished")
