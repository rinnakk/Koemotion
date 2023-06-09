import argparse
import os

import utils


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="path to input json file containing keypoints")
    parser.add_argument("-a", "--audio", type=str, default="", help="path to input audio file, combined with video if specified")
    parser.add_argument("-o", "--output", type=str, default="", help="path to output video file, inferred from --input if not specified")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_arguments()

    if args.output == "":
        args.output = args.input.replace(".json", ".mp4")
    output_tmp = args.output.replace(".mp4", "_no_audio.mp4")

    keypoints = utils.load_keypoints(args.input)
    video = utils.create_video(keypoints)
    utils.save_video(output_tmp, video)
    if args.audio != "":
        utils.combine_video_audio(output_tmp, args.audio, args.output, remove_vpath=True)
    else:
        os.rename(output_tmp, args.output)
