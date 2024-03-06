from moviepy.editor import *
import ffmpeg
import os
import math


def process_video(input, output):
    """Parameter input should be a string with the full path for a video"""
    clip = VideoFileClip(input)
    duration_main = clip.duration

    durations = math.ceil((duration_main / 8))
    duration01 = durations
    duration02 = 2*durations
    duration03 = 3*durations
    duration04 = 4*durations
    duration05 = 5*durations
    duration06 = 6*durations
    duration07 = 7*durations
    
    width_a = clip.w - 10
    height_a = clip.h - 60
    print(clip.w,clip.h, clip.fps,duration01,duration02,duration03,duration04,duration05,duration06,duration07, duration_main)
    input_stream = ffmpeg.input(input)
    
    v4 = (input_stream.video.filter('trim', start=duration_main/2, end=duration05)
         .filter('setpts', expr='PTS-STARTPTS').filter('setpts', expr='0.98*PTS')
          .filter('eq', contrast=0.92, brightness=0.024, saturation=1.06).filter('rotate', a=0.002))
    a4 = (input_stream.audio.filter('atrim', start=duration_main/2, end=duration05)
         .filter('asetpts', expr='PTS-STARTPTS').filter('atempo', 1.02).filter('volume', 1.02))
    
    v5 = (input_stream.video.filter('trim', start=duration05, end=duration06)
          .filter('setpts', expr='PTS-STARTPTS').filter('setpts', expr='0.99*PTS')
          .filter('eq', contrast=0.91, brightness=0.026, saturation=1.05).filter('rotate', a=0.004))
    a5 = (input_stream.audio.filter('atrim', start=duration05, end=duration06)
          .filter('asetpts', expr='PTS-STARTPTS').filter('atempo', 1.01).filter('volume', 1.05))
    
    v6 = (input_stream.video.filter('trim', start=duration06, end=duration07)
          .filter('setpts', expr='PTS-STARTPTS').filter('setpts', expr='0.98*PTS')
          .filter('eq', contrast=0.90, brightness=0.027, saturation=1.06).filter('rotate', a=0.006))
    a6 = (input_stream.audio.filter('atrim', start=duration06, end=duration07)
          .filter('asetpts', expr='PTS-STARTPTS').filter('atempo', 1.02).filter('volume', 1.02))
    
    v7 = (input_stream.video.filter('trim', start=duration07, end=duration_main)
          .filter('setpts', expr='PTS-STARTPTS').filter('setpts', expr='0.99*PTS')
          .filter('eq', contrast=0.89, brightness=0.028, saturation=0.95).filter('rotate', a=0.008))
    a7 = (input_stream.audio.filter('atrim', start=duration07, end=duration_main)
          .filter('asetpts', expr='PTS-STARTPTS').filter('atempo', 1.01).filter('volume',0.98))  # Khúc 8/Zoom 105% , Xoay 5deg, Crop-Top 110px,Crop-Bottom-110px Contrast=0.89, Brightness=0.028,saturation=1.05,Audio Speed:1.05
    joined = ffmpeg.concat( v4, a4, v5, a5, v6, a6, v7, a7, v=1, a=1).node
    v8 = joined[0].filter('crop',width_a, height_a).filter('lut', a=155 * 0.5)
    a8 = joined[1]

    input_stream = ffmpeg.output(v8, a8, output, vcodec='libx264', map_metadata=-1,
                                 **{'metadata:g:0': f'title=dinhho', 'metadata:g:1': f'date=2024'})
    input_stream.run()


def get_video_paths(folder_path):
    """
    Parameter folder_path should look like "Users/documents/folder1/"
    Returns a list of complete paths
    """
    file_name_list = os.listdir(folder_path)

    path_name_list = []
    final_name_list = []
    for name in file_name_list:
        # Put any sanity checks here, e.g.:
        if name == ".DS_Store":
            pass
        else:
            path_name_list.append(folder_path + name)
            final_name_list.append(folder_path  + "part2_" + name)
    return path_name_list, final_name_list


if __name__ == "__main__":
    video_folder = input("What folder would you like to process? ")
    path_list, final_name_list = get_video_paths(video_folder)
    for path, name in zip(path_list, final_name_list):
        process_video(path, name)
    print("Finished")
