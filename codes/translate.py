from googletrans import Translator
import openai
import re
from PyQt5 import QtWidgets, uic

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('test_gui.ui', self)
        # UI 요소 사용하기

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())



x= input("입력받을 문장: ")

# Google Translate API를 사용하여 번역을 가져옵니다.
translator = Translator()
detected= translator.detect(x) #입력받은 문장의 언어 감지
src_lang= detected.lang

dest_lang='ko'   #위젯 기능 추가 예정

if x is not None:
  translated_text = translator.translate(x, src=src_lang, dest=dest_lang).text

# openai의 GPT 모델을 사용하여 문장을 교정합니다.
openai.api_key = ""
model_engine = "text-davinci-003"
corrected_text = openai.Completion.create(
    engine=model_engine,
    prompt=(f"Please polish and correct following setences in {dest_lang}: {translated_text}"),
    temperature=0.5,
    max_tokens=1000,
    n = 1,
    stop=None,
    )
# 교정된 문장을 추출합니다.
corrected_text = corrected_text.choices[0].text
# 필요한 경우 문장 끝의 공백 및 줄바꿈 문자를 제거합니다.
corrected_text = re.sub(r'[\n\s]+', ' ', corrected_text.strip())

print("\n")
print(f"원본 문장: {x}")
print(f"번역된 문장: {translated_text}")
print(f"교정된 문장: {corrected_text}")