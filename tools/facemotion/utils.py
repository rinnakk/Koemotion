import json
import os

import cv2
import ffmpeg
import numpy as np


def load_keypoints(kpath):
    """
    Args:
        kpath (str): path to input json file containing keypoints.
    Returns:
        keypoints (np.array): numpy array of keypoints with shape (num_frames, dim).
    """
    keypoints_json = json.load(open(kpath))
    keypoints = np.array([x for x in keypoints_json["face_keypoints_3d"].values()])
    return keypoints


def create_video(keypoints, C=3, H=720, W=1280):
    """
    Args:
        keypoints (np.array): numpy array of keypoints with shape (num_frames, dim).
        C (int): number of channels of output video.
        H (int): height of output video.
        W (int): width of output video.
    Returns:
        video (np.array): output video array with shape (num_frames, H, W, C).
    """
    T = len(keypoints)

    keypoints = keypoints.reshape(T, -1, 3)  # (num_frames, num_keypoints, 3)
    keypoints = keypoints[..., :2]  # discard z value

    video = np.zeros((T, H, W, C), np.uint8)
    for i, frame_keypoints in enumerate(keypoints):
        img = np.zeros((H, W, C), np.uint8)
        for x, y in frame_keypoints:
            cv2.circle(img, (int(x), int(y)), 3, (255, 255, 255), -1)
        video[i] = img

    return video


def save_video(vpath, video, fps=30):
    """
    Args:
        vpath (str): path to save video.
        video (np.array): video array with shape (num_frames, H, W, C).
        fps (int): frames per second.
    """
    _, height, width, _ = video.shape
    fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
    writer = cv2.VideoWriter(vpath, fourcc, fps, (width, height))
    for v in video:
        writer.write(v)
    cv2.destroyAllWindows()
    writer.release()


def combine_video_audio(vpath, apath, opath, remove_vpath=False, remove_apath=False):
    """
    Args:
        vpath (str): path to input video.
        apath (str): path to input audio.
        opath (str): path to output video.
        remove_vpath (bool): remove input video file if True.
        remove_apath (bool): remove input audio file if True.
    """
    video = ffmpeg.input(vpath)
    audio = ffmpeg.input(apath)
    out = ffmpeg.output(video, audio, opath)
    out.run()
    if remove_vpath:
        os.remove(vpath)
    if remove_apath:
        os.remove(apath)
