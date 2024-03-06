from moviepy.editor import *
import ffmpeg
import os
import math
import subprocess

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
    height_a = clip.h - 40
    print(clip.w,clip.h, clip.fps,duration01,duration02,duration03,duration04,duration05,duration06,duration07, duration_main)
    overlaypng = ffmpeg.input("C:/Users/dinhh/Desktop/MainProjectDinhho/pythonProject/srt/dtiff.tiff")
    input_stream = ffmpeg.input(input)
    
    
    v0 = (input_stream.video.filter('trim', start=0, end=duration01)
          .filter('setpts', expr='PTS-STARTPTS').filter('setpts', expr='0.97*PTS')
          .filter('eq', contrast=0.96, brightness=0.020, saturation=1.10)
          .filter('rotate', a=-0.003)).filter('scale',)
    a0 = (input_stream.audio.filter('atrim', start=0, end=duration01)
          .filter('asetpts', expr='PTS-STARTPTS').filter('atempo', 1.03).filter('volume', 0.85))

    v1 = (input_stream.video.filter('trim', start=duration01, end=duration02)
          .filter('setpts', expr='PTS-STARTPTS').filter('setpts', expr='0.99*PTS')
          .filter('eq', contrast=0.95, brightness=0.021, saturation=1.09).filter('rotate', a=-0.002))
    a1 = (input_stream.audio.filter('atrim', start=duration01, end=duration02)
          .filter('asetpts', expr='PTS-STARTPTS').filter('atempo', 1.01).filter('volume', 0.9))

    v2 = (input_stream.video.filter('trim', start=duration02, end=duration03)
          .filter('setpts', expr='PTS-STARTPTS').filter('setpts', expr='0.98*PTS')
          .filter('eq', contrast=0.94, brightness=0.022, saturation=1.08).filter('rotate', a=-0.001))
    a2 = (input_stream.audio.filter('atrim', start=duration02, end=duration03)
          .filter('asetpts', expr='PTS-STARTPTS').filter('atempo', 1.02).filter('volume', 0.95))

    v3 = (input_stream.video.filter('trim', start=duration03, end=duration04)
          .filter('setpts', expr='PTS-STARTPTS').filter('setpts', expr='0.99*PTS')
          .filter('eq', contrast=0.93, brightness=0.023, saturation=1.07).filter('rotate', a=0.00))
    a3 = (input_stream.audio.filter('atrim', start=duration03, end=duration04)
        .filter('asetpts', expr='PTS-STARTPTS').filter('atempo', 1.01).filter('volume', 1))

    v4 = (input_stream.video.filter('trim', start=duration04, end=duration05)
         .filter('setpts', expr='PTS-STARTPTS').filter('setpts', expr='0.98*PTS')
          .filter('eq', contrast=0.92, brightness=0.024, saturation=1.06).filter('rotate', a=0.002))
    a4 = (input_stream.audio.filter('atrim', start=duration04, end=duration05)
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

    v7 = (input_stream.video.filter('trim', start=duration07, end=duration_main-1)
          .filter('setpts', expr='PTS-STARTPTS').filter('setpts', expr='0.99*PTS')
          .filter('eq', contrast=0.89, brightness=0.028, saturation=0.95).filter('rotate', a=0.008))
    a7 = (input_stream.audio.filter('atrim', start=duration07, end=duration_main-1)
          .filter('asetpts', expr='PTS-STARTPTS').filter('atempo', 1.01).filter('volume',0.98))
    joined = ffmpeg.concat(v0, a0, v1, a1, v2, a2, v3, a3, v4, a4, v5, a5, v6, a6, v7, a7, v=1, a=1).node

    v8 = joined[0]
    a8 = joined[1].filter("highpass",f=1375.4).filter('volume','12.3dB').filter('atrim',start=1, end=duration_main).filter('asetpts', expr='PTS-STARTPTS')
    #.filter('zoompan',z=f'if(lte(mod(it*30,300),90),min(max(zoom,pzoom)+0.02,1.7),min(max(zoom,pzoom)-0.015,1.7))', x='iw/2-(iw/zoom/2)', y='ih/2-(ih/zoom/2)', d=1,s=f'{width_a}x{height_a}', fps=30)
    input_stream = ffmpeg.output(v8, a8, output, vcodec='libx264', map_metadata=-1,
                                 **{'metadata:g:0': f'title=dinhho', 'metadata:g:1': f'date=2024'})
    input_stream.run()
    #'if(lte(mod(it*30,330),90),min(max(zoom,pzoom)+0.02,2.0),min(max(zoom,pzoom)-0.015,2.0))' edit_
    #.filter('zoompan',z=f'if(lte(mod(it*30,180),70),min(max(zoom,pzoom)+0.07,2.0),min(max(zoom,pzoom)-0.07,2.0))', x='iw/2-(iw/zoom/2)', y='ih/2-(ih/zoom/2)', d=1,s=f'{width_a}x{height_a}', fps=30)
    #subprocess.call(["ffmpeg","-i",input, "-filter_complex", f"zoompan=z='if(lte(mod(time,10),3),2,1)':d=1:x=iw/3.5-(iw/zoom/3.5)+50:y=ih/3.5-(ih/zoom/3.5)-40:s={clip.w}x{clip.h}:fps=29.97",output,])
    #.filter('zoompan',z=f'if(lte(mod(it*30,300),90),min(max(zoom,pzoom)+0.02,1.8),min(max(zoom,pzoom)-0.015,1.8))', x='iw/2-(iw/zoom/2)', y='ih/2-(ih/zoom/2)', d=1,s=f'{width_a}x{height_a}', fps=30)
    #.filter('zoompan',z=f'if(lte(mod(it*30,300),90),min(max(zoom,pzoom)+0.02,1.7),min(max(zoom,pzoom)-0.015,1.7))', x='iw/2-(iw/zoom/2)', y='ih/2-(ih/zoom/2)', d=1,s=f'{width_a}x{height_a}', fps=30)***
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
            final_name_list.append(folder_path + "edit_" + name)
    return path_name_list, final_name_list


if __name__ == "__main__":
    video_folder = input("What folder would you like to process? ")
    path_list, final_name_list = get_video_paths(video_folder)
    for path, name in zip(path_list, final_name_list):
        process_video(path, name)
    print("Finished")
#ffmpeg -i VIDEO.mp4 -vf "zoompan=z='if(lte(mod(time,10),3),2,1)':d=1:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):fps=29.97" video_result.mp4
#.filter('zoompan',z=f'if(lte(mod(it*30,180),30),min(max(zoom,pzoom)+0.008,1.5),min(max(zoom,pzoom)-0.008,1.5))', x='iw/2-(iw/zoom/2)', y='ih/2-(ih/zoom/2)', d=1,s=f'{width_a}x{height_a}', fps=30)
#ffmpeg -i "test.mp4" -filter_complex " zoompan=z='if(lte(mod(it*30,180),30),min(max(zoom,pzoom)+0.018,1.5),min(max(zoom,pzoom)-0.008,1.5))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30" output.mp4 -y