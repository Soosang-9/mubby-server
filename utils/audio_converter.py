# -*- coding:utf-8 -*-

import os
import audioop


def convert(input_audio):
    # ================ Audio converter =================
    #   - mp3 to wav
    #   - sample rate(22050Hz to 44100Hz)
    #   - channel(mono to stereo)
    # ==================================================
    convert_audio = "output_tts.wav"
    cmd_convert = "ffmpeg -i {} -ar 44100 -ac 2 -y {}".format(input_audio, convert_audio)
    os.system(cmd_convert)
    print("Convert mp3 to wav")

    return convert_audio


def mono_to_stereo(data, width=1):
    lsample = audioop.tostereo(data, width, 1, 0)
    rsample = audioop.tostereo(data, width, 0, 1)
    return audioop.add(lsample, rsample, width)


def stereo_to_mono(data, width=2):
    # 2채널 스트레오를 모노로 바꾸는 함수
    # 1채널 모노 파일을 사용할 때는 사용하시지 않아도 됩니다.
    lsample = audioop.tomono(data, width, 1, 0)
    rsample = audioop.tomono(data, width, 0, 1)
    return audioop.add(lsample, rsample, width)