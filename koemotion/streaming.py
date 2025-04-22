import ctypes
import os
import platform
import struct
import wave

import pyaudio


def alsa_error_handler(filename, line, function, err, fmt):
    pass


def is_wsl():
    if "microsoft" in platform.uname().release.lower():
        return True
    if os.path.exists("/proc/version"):
        with open("/proc/version") as f:
            if "microsoft" in f.read().lower():
                return True
    return False


def parse_wav_header(header):
    n_channels = struct.unpack("<H", header[22:24])[0]
    sample_rate = struct.unpack("<I", header[24:28])[0]
    bit_depth = struct.unpack("<H", header[34:36])[0]
    sample_width = bit_depth // 8
    return n_channels, sample_width, sample_rate


def save_audio(audio_data, output_path, output_format="wav"):
    """
    Save the audio stream from the response object to a WAV file.
    Note that this function waits for the entire audio stream to be downloaded before saving.

    Args:
        audio_data (bytes): Binary audio data.
        output_path (str): Path to save the audio file.
        output_format (str): Audio format, one of ["wav", "raw"].
    """
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    if output_format == "wav":
        header, audio = audio_data[:44], audio_data[44:]
        n_channels, sample_width, sample_rate = parse_wav_header(header)

        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(n_channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(sample_rate)
            wf.writeframes(audio)
    elif output_format == "raw":
        with open(output_path, "wb") as f:
            f.write(audio_data)
    else:
        raise ValueError(f"Invalid output format: {output_format}")


def stream_audio(response, output_format="wav", chunk_size=1024):
    """
    Play the audio stream from the response object.

    Args:
        response (httpx.Response): Response object from Koemotion API.
        output_format (str): Audio format, one of ["wav", "raw"].
        chunk_size (int): Size of the audio chunk to stream.
    """
    if is_wsl():
        # suppress ALSA errors
        try:
            alsa = ctypes.cdll.LoadLibrary("libasound.so")
            ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(
                None,
                ctypes.c_char_p,
                ctypes.c_int,
                ctypes.c_char_p,
                ctypes.c_int,
                ctypes.c_char_p,
            )
            c_error_handler = ERROR_HANDLER_FUNC(alsa_error_handler)
            alsa.snd_lib_error_set_handler(c_error_handler)
        except Exception as e:
            print(f"Error setting ALSA error handler: {e}")

    data = b""
    prev = b""
    for i, chunk in enumerate(response.iter_bytes(chunk_size=chunk_size)):
        if chunk:
            data += chunk

            # skip WAV header
            if i == 0:
                if output_format == "wav":
                    header, chunk = chunk[:44], chunk[44:]
                    n_channels, _, sample_rate = parse_wav_header(header)
                elif output_format == "raw":
                    n_channels, sample_rate = 1, 24000
                else:
                    raise ValueError(f"Invalid output format: {output_format}")
                p = pyaudio.PyAudio()
                stream = p.open(
                    format=pyaudio.paInt16,
                    channels=n_channels,
                    rate=sample_rate,
                    output=True,
                )
            # prepend previous chunk
            if prev != b"":
                chunk = prev + chunk
                prev = b""
            # avoid chunk with odd length
            if len(chunk) % 2 != 0:
                chunk = chunk[:-1]
                prev = chunk[-1:]

            stream.write(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()

    return data
