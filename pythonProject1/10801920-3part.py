from moviepy.editor import *
import ffmpeg
import os
import math


def process_video(input, output):
    """Parameter input should be a string with the full path for a video"""
    clip = VideoFileClip(input)
    duration_main = clip.duration

    durations = math.ceil((duration_main / 3))
    duration01 = durations
    duration02 = 2*durations
    
    width_a = clip.w - 10
    height_a = clip.h - 20
    print(clip.w,clip.h, clip.fps,duration01,duration02, duration_main)
    input_stream = ffmpeg.input(input)

    v1 = (input_stream.video.filter('trim', start=0, end=duration01)
          .filter('setpts', expr='PTS-STARTPTS').filter('setpts', expr='0.97*PTS')
          .filter('eq', contrast=0.96, brightness=0.020, saturation=1.10)
          .filter('rotate', a=-0.003))   
    a1 = (input_stream.audio.filter('atrim', start=0, end=duration01)
          .filter('asetpts', expr='PTS-STARTPTS').filter('atempo', 1.03).filter('volume', 0.85))
    
    v2 = (input_stream.video.filter('trim', start=duration01, end=duration02)
          .filter('setpts', expr='PTS-STARTPTS').filter('setpts', expr='0.99*PTS')
          .filter('eq', contrast=0.95, brightness=0.021, saturation=1.09).filter('rotate', a=-0.002))
    a2 = (input_stream.audio.filter('atrim', start=duration01, end=duration02)
          .filter('asetpts', expr='PTS-STARTPTS').filter('atempo', 1.01).filter('volume', 0.9))
    v6 = (input_stream.video.filter('trim', start=duration02, end=duration_main)
          .filter('setpts', expr='PTS-STARTPTS').filter('setpts', expr='0.99*PTS')
          .filter('eq', contrast=0.92, brightness=0.024, saturation=1.06).filter('rotate', a=0.001))
    a6 = (input_stream.audio.filter('atrim', start=duration02, end=duration_main)
          .filter('asetpts', expr='PTS-STARTPTS').filter('atempo', 1.01))
    joined = ffmpeg.concat( v1, a1, v2, a2,v6,a6, v=1, a=1).node
    v8 = joined[0].filter('crop',width_a, height_a).filter('lut', a=155 * 0.5)
    a8 = joined[1].filter("highpass",f=1375.4).filter('volume','12.3dB').filter('atrim',start=1, end=duration_main).filter('asetpts', expr='PTS-STARTPTS')

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
            final_name_list.append(folder_path + "w3part_" + name)
    return path_name_list, final_name_list


if __name__ == "__main__":
    video_folder = input("What folder would you like to process? ")
    path_list, final_name_list = get_video_paths(video_folder)
    for path, name in zip(path_list, final_name_list):
        process_video(path, name)
    print("Finished")
