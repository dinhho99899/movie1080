from moviepy.editor import *
import ffmpeg
import os

def process_video(input, output):
    """Parameter input should be a string with the full path for a video"""
    clip = VideoFileClip(input)
    duration_main = clip.duration
    clip_duration = clip.duration / 2
 
    width_a = clip.w - 10
    height_a = clip.h - 100
    print(clip.h, clip.w, clip_duration, clip.fps,duration_main)
    input_stream = ffmpeg.input(input).filter('lut', a=155 * 0.5).filter('eq', contrast=0.95, brightness=0.021,saturation=1.09).filter('rotate', a=-0.01).filter('crop',width_a,height_a).filter('fade', t='in', s=5, n=15)
    audio_stream = ffmpeg.input('titikaudio.mp3').filter('atrim', start=0,end=duration_main)

    joined = ffmpeg.concat(input_stream, audio_stream, v=1, a=1).node
    v8 = joined[0]
    a8 = joined[1]  
 
    input_stream = ffmpeg.output(a8, v8, output, vcodec='libx264', map_metadata=-1,
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
            final_name_list.append(folder_path + "edited_" + name)
    return path_name_list, final_name_list


if __name__ == "__main__":
    video_folder = input("What folder would you like to process? ")
    path_list, final_name_list = get_video_paths(video_folder)
    for path, name in zip(path_list, final_name_list):
        process_video(path, name)
    print("Finished")
