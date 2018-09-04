import googletrans


class GoogleTranslationHelper:
# MARK: Singleton stuff
    _sharedInstance = None

    @staticmethod
    def getInstance():
        if (GoogleTranslationHelper._sharedInstance is None):
            _sharedInstance = GoogleTranslationHelper()

        return _sharedInstance


# MARK: Constructors and destructors
    def __init__(self):
        self.translator = googletrans.Translator(service_urls = ["translate.google.cn"], user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0")    # Sadly google.com is blocked in China. Please change this link to ".com" (or your country's suffix) if necessary.

    def __del__(self):
        # super.__del__(self)
        if (hasattr(self, "translator")):
            del self.translator


# MARK: Translation stuff
    def translateAString(self, stringToTranslate, sourceLanguage="auto", destinationLanguage="en"):
        """Translate a single string.

        Note:
            Please use the `translateStrings` method for faster batch operations.

        Returns:
            str: The translated string.
        """
        return self.translator.translate(stringToTranslate, dest=destinationLanguage, src=sourceLanguage).text

    def translateStringsInTheSameLanguage(self, stringsToTranslate, sourceLanguage="auto", destinationLanguage="en"):
        """Translate an array (list) of strings in the same language to another language.

        Args:
            stringsToTranslate (list): The list of strings to translate. They must be in the same language. Each string may NOT contain the '\n' character.

        Returns:
            dict: A dictionary containing both the source strings and their corresponding translated strings.
        """
        # 1. If `stringsToTranslate` contains too many strings (more than 10), then try to combine them into larger strings before translating them. This is to minimize the number of requests to Google Translate servers.
        processedStringsToTranslate = None

        if (len(stringsToTranslate) > 10):
            processedStringsToTranslate = []

            currentCombinedString = ""    # The current combined string.
            currentCombinedStringLength = 0     # The number of strings combined.

            for aStringToTranslate in stringsToTranslate:
                currentCombinedString += aStringToTranslate
                currentCombinedStringLength += 1

                if (currentCombinedStringLength >= 20):
                    processedStringsToTranslate.append(currentCombinedString)

                    currentCombinedString = ""
                    currentCombinedStringLength = 0
                else:
                    currentCombinedString += '\n'

            processedStringsToTranslate.append(currentCombinedString)

        else:
            processedStringsToTranslate = stringsToTranslate

        # 2. Translate the combined strings.
        # TODO: Separate strings by '\n'.
        translations = self.translator.translate(processedStringsToTranslate, dest=destinationLanguage, src=sourceLanguage)
        translationsArray = []
        for aTranslation in translations:
            sourceString = aTranslation.origin
            translatedString = aTranslation.text

            # Split strings by '\n'.
            splittedSourceStrings = sourceString.split('\n')
            splittedTranslatedStrings = translatedString.split('\n')

            for (aSourceString, aTranslatedString) in zip(splittedSourceStrings, splittedTranslatedStrings):
                translationsArray.append({
                    "sourceString": aSourceString,
                    "translatedString": aTranslatedString
                })

        return translationsArray




# MARK: For testing 😂
# print(GoogleTranslationHelper.getInstance().translateAString("你好世界", destinationLanguage="ko"))
# print(GoogleTranslationHelper.getInstance().translateAString(123))    # Failure

# stringsToTranslate = ["你好世界", "이 문장은 한글로 쓰여졌습니다.", "この文章は日本語で書かれました。"]
# for aStringToTranslate in stringsToTranslate:
#     print(GoogleTranslationHelper.getInstance().translateAString(aStringToTranslate))

# translations = GoogleTranslationHelper.getInstance().translateStrings(["你好\n世界", "이 문장은 한글로 쓰여졌습니다.", "この文章は日本語で書かれました。"])    # '\n' characters will get preserved in the translated string.
# for aTranslation in translations:
#     # print(aTranslation)
#     # print(aTranslation.text)
#     print(aTranslation["sourceString"], "->", aTranslation["translatedString"])

# stringsToTranslate = ["你好世界", "你好世界", "你好世界", "你好世界", "你好世界", "你好世界", "你好世界", "你好世界", "你好世界", "你好世界", "你好世界", "你好世界", "你好世界", "你好世界", "你好世界", "你好世界", "你好世界", "你好世界", "你好世界", "天呐！", "不要耍猴！", "毛脸雷公嘴的和尚", "长嘴大耳的和尚", "青面獠牙的和尚", "我是用来\n测试的", "唐三藏", "《西游记》"]
# print(GoogleTranslationHelper.getInstance().translateStringsInTheSameLanguage(stringsToTranslate))