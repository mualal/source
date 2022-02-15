import cv2
import glob
import os

from PIL import Image


def convert_video_to_frames(path: str):
    video_capture = cv2.VideoCapture(path)
    still_reading, image = video_capture.read()
    frame_count = 0
    while still_reading:
        if frame_count % 30 == 0:
            cv2.imwrite(os.path.join('frames', f'frame_{frame_count:04d}.jpg'), image)
        still_reading, image = video_capture.read()
        frame_count += 1


def create_gif(frames_folder, name: str):
    images = glob.glob(os.path.join(f'{frames_folder}', '*.jpg'))
    images.sort()
    frames = [Image.open(image) for image in images]
    frame_one = frames[0]
    frame_one.save(os.path.join('output', name + '.gif'), format='GIF', append_images=frames, save_all=True,
                   duration=1000, loop=0)


if __name__ == '__main__':
    convert_video_to_frames(os.path.join('input', 'Screen Recording 2022-02-16 at 02.10.29.mov'))
    create_gif('frames', 'liquid_rate')
