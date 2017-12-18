import pyttsx3 as tt
from gtts import gTTS
import numpy as np
from enum import Enum,unique
import wave
import struct
import pyaudio
np.set_printoptions(threshold=np.nan)
@unique
class VoiceSound(Enum):
    shortBeep = 1
    longBeep = 3
    noBeep = -3
    longNoBeep = -7

class CodeSpeaker(object):
    def __init__(self,whatyousay=None,duration = None,volume=None,rate=None,gender=None,franeRate =None):
        self.whatyousay = whatyousay
        self.volume = 0.5 if volume is None else volume
        self.rate = rate
        self.gender = 0 if (gender is None or gender == 'female') else 1
        self.duration = 0.15 if duration is None else duration
        self.__engine = None
        self.__tt = None
        self.__stream = None
        self.__p = None
        self.fs = 44100 if franeRate is None else franeRate
        self.__frames =[]
        self.__codeAudioData=None
        self.__params=None
    def __createBeepSound(self,duration,isSilence = False):
        a = 1  # 振幅
        fs = self.fs
        f0 = 800.0
        sec = duration + 0.1  # 秒

        swav = []
        for n in np.arange(fs * sec):
            if not isSilence:
                if n >= fs*duration:
                    s = 0.0
                else:
                    s = a * np.sin(2.0 * np.pi * f0 * n / fs)
            else:
                if n > fs*sec-fs*0.1*2:
                    break
                s = 0.0
            swav.append(s)

        swav = [int(x * 32767.0) for x in swav]


        binwave = struct.pack("h" * len(swav), *swav)
        return binwave
    def __beep(self, Voice,duration=None):
        if type(Voice) is not VoiceSound:
            raise AttributeError(' the type of Voice is NOT VoiceSound')
        volume = self.volume  # range [0.0, 1.0]
        fs = self.fs  # sampling rate, Hz, must be integer
        duration = self.duration if duration is None else duration  # in seconds, may be float
        f = 800.0  # sine frequency, Hz, may be float
        # generate samples, note conversion to float32 array
        if Voice == VoiceSound(1):
            samples = self.__createBeepSound(duration)
            # samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs))
        elif Voice == VoiceSound(3):
            # samples = (np.sin(2 * np.pi * np.arange(fs * (duration*3) ) * f / fs))
            samples = self.__createBeepSound(duration*3)
        elif Voice == VoiceSound(-3):
            # samples = (np.arange(fs * (duration * 3)  * f / fs) * 0.0).astype(np.float32)
            # samples = (np.sin(2 * np.pi * np.arange(fs * (duration * 3)) * f / fs))
            samples = self.__createBeepSound(duration*3,isSilence=True)
        else:
            # samples = (np.arange(fs * (duration * 7) * f / fs) * 0.0).astype(np.float32)
            # samples = (np.sin(2 * np.pi * np.arange(fs * (duration * 3)) * f / fs))
            samples = self.__createBeepSound(duration*7,isSilence=True)
        # for paFloat32 sample values must be in range [-1.0, 1.0]
        # if self.__stream is None :
        #     self.__stream = self.__p.open(format=pyaudio.paFloat32,
        #                     channels=1,
        #                     rate=fs,
        #                     output=True)
        # play. May repeat with different volume values (if done interactively)
        self.__frames.append(samples)
        # self.__stream.stop_stream()
        # self.__stream.close()
        # self.__p.terminate()
    def __createCodeBinary(self,code):
        self.__frames = []
        for index, char in enumerate(code):
            if char == '.':
                self.__beep(VoiceSound.shortBeep)
                # times += self.duration * abs(VoiceSound.shortBeep.value)
                # exit()
            elif char == '-':
                self.__beep(VoiceSound.longBeep)
                # times += self.duration * abs(VoiceSound.longBeep.value)
            else:
                if char == " ":
                    try:
                        if code[index + 1] == ' ':
                            self.__beep(VoiceSound.longNoBeep)
                            # times += self.duration * abs(VoiceSound.longNoBeep.value)
                        else:
                            self.__beep(VoiceSound.noBeep)
                            # times += self.duration * abs(VoiceSound.noBeep.value)
                    except:
                        self.__beep(VoiceSound.noBeep)
                        # times += self.duration * abs(VoiceSound.noBeep.value)

        if len(self.__frames) == 0:
            return False
        data = self.__frames[0]
        print(len(self.__frames))
        for i in range(1, len(self.__frames)):
            data += self.__frames[i]
        self.__params =  (1, 2, self.fs, len(data), 'NONE', 'not compressed')
        self.__codeAudioData = data
        return data
    def saveCodeAudio(self,code,filePath):
        data = self.__createCodeBinary(code)
        w = wave.Wave_write(filePath)
        w.setparams(self.__params)
        w.writeframes(data)
        w.close()
    def playMorseCode(self,code):
        data = self.__createCodeBinary(code)
        if self.__p is None:
            self.__p = pyaudio.PyAudio()
        stream = self.__p.open(format = self.__p.get_format_from_width(self.__params[1]),
                channels = self.__params[0],
                rate = self.fs,
                output = True)
        stream.write(data)
        # stop stream
        stream.stop_stream()
        stream.close()
        # close PyAudio
        self.__p.terminate()
    def play(self,str=None):
        if str is  None and self.whatyousay is None:
            raise AttributeError('what do you want say? ')
        str = (str if str is not None else self.whatyousay).strip()
        self.__engine = tt.init()
        self.__engine.say(str)
        self.__engine.runAndWait()
    def save(self,str,fileName):
        str = str.strip()
        print(str)
        self.__tt = gTTS(text=str,lang='en',slow=True)
        self.__tt.save(fileName)


if __name__ == '__main__':
    # print(wavfile.read('output.wav'))
    # wavfile.write()

    # print(VoiceSound.longNoBeep.value)
    # print(VoiceSound(1))
    # exit()
    cs = CodeSpeaker()
    code = '.. -.-- -.-. ..--  -..'
    cs.playMorseCode(code)
    # -*- coding: utf-8 -*-






