from codeSpeaker import CodeSpeaker
import string
class MorseCode(object):
    def __init__(self):
        self.__MorseCharCode = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..',
            'J': '.---',
            'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...',
            'T': '-',
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
        }
        self.__MorseNumCode = {
            '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.', '0': '-----',
        }
        #'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

        self.__MorsePunctuationCode = {
            '?': '..--..', '/': '-..-.', '-': '-....-', '.': '.-.-.-',
        }
        self.__codeSpeaker = CodeSpeaker()
    def __ismorsecode(self,code):
        for i in code:
            if i  not in ['.','-',' ']:
               return False
        return True
    def __isEnglish(self,str):
        str = str.replace(' ','')
        for i in str:
            if i in string.punctuation:
                str = str.replace(i,'')
        return str.isalnum()
    def MorseEncode(self,str):
        if not self.__isEnglish(str):
            raise AttributeError(str + ' is not English')
        UpStr = str.upper()
        strList = UpStr.split()
        MorseStr = ''
        for word in strList:
            MorseWord = ''
            for char in word:
                if char.isdigit():
                    try:
                        MorseWord += self.__MorseNumCode[char]+' '
                    except:
                        return None
                elif char.isalpha():
                    try:
                        MorseWord += self.__MorseCharCode[char]+' '
                    except:
                        return None
                else:
                    try:
                        MorseWord += self.__MorsePunctuationCode[char]+' '
                    except:
                        return None
            MorseStr += MorseWord+'  '
        return MorseStr
    def MorseCodeDecode(self,code):
        if not self.__ismorsecode(code):
            raise AttributeError(code + ' is not MorseCode')
        code = code.strip()
        wordList = code.split('  ')
        returnstr = ''
        for morseWord in wordList:
            morseWord = morseWord.strip()
            charList = morseWord.split(' ')
            word= []
            realWord = ''
            for char in charList:
                if len(char) <= 4 and char in self.__MorseCharCode.values():
                    word.append(list(self.__MorseCharCode.keys())[list(self.__MorseCharCode.values()).index(char)])
                elif len(char) == 5 and char in self.__MorseNumCode.values():
                    word.append(list(self.__MorseNumCode.keys())[list(self.__MorseNumCode.values()).index(char)])
                else:
                    word.append(list(self.__MorsePunctuationCode.keys())[list(self.__MorsePunctuationCode.values()).index(char)])
            realWord += ''.join(word)
            returnstr += (realWord+' ')

        return  returnstr.capitalize()

    def beepMorseCodeSound(self,str1):
        if not self.__ismorsecode(str1):
            raise AttributeError(str1 + 'is not MorseCode')
        str = str1.strip()
        self.__codeSpeaker.playMorseCode(str)

    def playString(self,str):
        self.__codeSpeaker.play(str)
    def __saveMorseCodeAudio(self,code,fileName):
        self.__codeSpeaker.saveCodeAudio(code,fileName)
    def __saveStringAudio(self,str,fileName):
        self.__codeSpeaker.save(str,fileName)
    def save(self,str,fileName):
        if  self.__ismorsecode(str):
            self.__saveMorseCodeAudio(str,fileName)
        elif self.__isEnglish(str):
            self.__saveStringAudio(str,fileName)
        else:
            return False
        return True

if __name__ == '__main__':
    mc = MorseCode()
    code = mc.MorseEncode('i always want to see Twice')
    print(code)
    mc.beepMorseCodeSound(code)
    mc.save(code,'MorseCode.wav')
    str = mc.MorseCodeDecode(code)
    print(str)
    mc.playString(str)
    # mc.save(str,'./test.mp3')
