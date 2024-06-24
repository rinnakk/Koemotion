import argparse
import json
import sys

from .client import Koemotion
from .facemotion import visualize as vis_fn


def request():
    """Send request to Koemotion API."""
    parser = argparse.ArgumentParser()
    # fmt: off
    parser.add_argument("-d", "--data", type=str, required=True, help="JSON string of the request data.")
    parser.add_argument("-H", "--header", type=str, default="", help="JSON string of the optional request header. Content-Type and Ocp-Apim-Subscription-key are included by default.")
    parser.add_argument("-k", "--api-key", type=str, default=None, help="Koemotion API key. Taken from KOEMOTION_API_KEY environment variable if not specified.")
    parser.add_argument("-j", "--output-json", type=str, default="", help="Path to output json file. Ignored for streaming requests.")
    parser.add_argument("-a", "--output-audio", type=str, default="", help="Path to output audio.")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation prompt.")
    parser.add_argument("--autoplay", action="store_true", help="Play the audio file if True. Only valid for streaming requests.")
    # fmt: on
    args = parser.parse_args()

    if not args.yes:
        confirmation = input(
            f"API call may incur a cost. Do you want to continue? [y/N] "
        )
        if confirmation.lower() != "y":
            print("Request cancelled.")
            sys.exit()

    client = Koemotion(api_key=args.api_key)

    params = json.loads(args.data)
    streaming = params.get("streaming", False)

    response = client.request(params=params)

    if streaming:
        if args.autoplay:
            response.stream_audio()
        if not args.output_audio:
            args.output_audio = "result_streaming.wav"
        response.save_audio(args.output_audio)
    else:
        args.output_json = args.output_json or "result.json"
        response.save_json(args.output_json)
        if args.output_audio:
            response.save_audio(args.output_audio)


def visualize():
    """Visualize the facemotion data."""
    parser = argparse.ArgumentParser()
    # fmt: off
    parser.add_argument("-i", "--input", type=str, required=True, help="Path to input json file containing keypoints.")
    parser.add_argument("-a", "--audio", type=str, default="", help="Path to input audio file, combined with video if specified.")
    parser.add_argument("-o", "--output", type=str, default="", help="Path to output video file, inferred from --input if not specified.")
    parser.add_argument("--quiet", action="store_true", help="Suppress ffmpeg output if True.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite output file if True.")
    # fmt: on
    args = parser.parse_args()

    vis_fn(args.input, args.audio, args.output, args.quiet, args.overwrite)
