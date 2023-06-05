import re
import openai
from googletrans import Translator
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Trans:
    def __init__(self):
        self.translated_text = ""
        self.detected = ""
        self.src_lang = ""
        self.dest_lang = ""
        self.corrected_text = ""
        self.key_val = ""


    def translate_text(self):
        try:
            x = self.input_text.get("1.0", "end-1c")

            if not x.strip():  # 입력값이 없거나 공백인 경우 예외 처리
                messagebox.showerror("Translation Error", "Please enter a sentence to translate.")
                return
            
            if len(x) > 5000:  # 메시지가 5000자를 초과하는 경우 예외 처리
                messagebox.showerror("Translation Error", "Please enter a message with a maximum of 5000 characters.")
                return

            translator = Translator()
            self.detected = translator.detect(x)  # 입력받은 문장의 언어 감지
            self.src_lang = self.detected.lang


            # 번역 중에 다른 버튼 비활성화
            self.translate_button.config(state="disable")
            self.copy_button.config(state="disable")
            self.lang_combobox.config(state="disable")


            # 번역 중입니다... 메시지 표시
            self.translated_output.delete("1.0", tk.END)
            self.translated_output.insert(tk.END, "Translating...")

            self.corrected_output.delete("1.0", tk.END)
            self.corrected_output.insert(tk.END, "Translating...")

            self.root.update_idletasks()  # 화면 업데이트

            #번역
            if x is not None:
                self.translated_text = translator.translate(x, src=self.src_lang, dest=self.dest_lang).text

            
            # openai의 GPT 모델을 사용하여 문장을 교정합니다.
            openai.api_key = self.key_val
            model_engine = "text-davinci-003"
            self.corrected_text = openai.Completion.create(
                engine=model_engine,
                prompt=(f"Please polish and correct following these sentences in {self.dest_lang}: {self.translated_text}"),
                temperature=0.5,
                max_tokens=2048,
                n=1,
                stop=None,
            )


            # 교정된 문장을 추출합니다.
            self.corrected_text = self.corrected_text.choices[0].text
            # 필요한 경우 문장 끝의 공백 및 줄바꿈 문자를 제거합니다.
            self.corrected_text = re.sub(r'[\n\s]+', ' ', self.corrected_text.strip())

            # 출력
            self.translated_output.delete("1.0", tk.END)
            self.translated_output.insert(tk.END, self.translated_text)

            self.corrected_output.delete("1.0", tk.END)
            self.corrected_output.insert(tk.END, self.corrected_text)

            # 번역이 끝나면 다른 버튼 다시 활성화
            self.translate_button.config(state="normal")
            self.copy_button.config(state="normal")
            self.lang_combobox.config(state="readonly")

            # 번역 중입니다... 메시지 박스 닫기
            messagebox.showinfo("Translation", "Translation completed.")

        except Exception as e:
            # 번역 오류가 발생했을 때 "번역 에러" 팝업 표시
            messagebox.showerror("Translation Error", "An error occurred during translation: " + str(e))

            # 번역 오류로 인해 다른 버튼 다시 활성화
            self.translate_button.config(state="normal")
            self.copy_button.config(state="normal")
            self.lang_combobox.config(state="readonly")
            self.key_btn.config(state="normal")
            
    def select_lang(self, event):
        lang = self.lang_combobox.get()
        self.dest_lang = lang

        if self.dest_lang is not None:
            self.translate_button.config(state="normal")
            self.lang_label.config(text=f"Selected Language: {self.dest_lang}")
            

    def key_insert(self):
        key_val = ""
        key_val = self.input_key.get()

        if not key_val.strip():  # API 키가 입력되지 않은 경우 예외 처리
            messagebox.showerror("Key Error", "Please enter a valid API key.")
            return

        self.key_val = str(key_val)

        # 성공 메시지 출력
        success_label = tk.Label(self.root, text="API Key inserted successfully!")
        success_label.pack()

        # 일정 시간(예: 3초) 후에 메시지를 삭제
        self.root.after(3000, lambda: success_label.pack_forget())

        # Check 버튼 비활성화
        self.key_btn.config(state="disabled")
        

    def copy_translated(self):
        translated_text = self.translated_output.get("1.0", "end-1c")

        # 클립보드에 복사
        self.root.clipboard_clear()
        self.root.clipboard_append(translated_text)

        # 팝업 메시지 표시
        messagebox.showinfo("Copy", "Text copied to clipboard successfully.")

    def copy_corrected(self):
        corrected_text = self.corrected_output.get("1.0", "end-1c")

        # 클립보드에 복사
        self.root.clipboard_clear()
        self.root.clipboard_append(corrected_text)

        # 팝업 메시지 표시
        messagebox.showinfo("Copy", "Text copied to clipboard successfully.")

        
    def exit_program(self):
        self.root.destroy()
        

    def run(self):
        self.root = tk.Tk()
        self.root.title("Improved Translater")
        self.root.geometry("600x650")
        self.root.protocol("WM_DELETE_WINDOW", self.exit_program)  # 프로그램 종료 시 자원 정리

        key_label = tk.Label(self.root, text="Insert OpenAI API key")
        key_label.pack()

        self.input_key = tk.Entry(self.root, width=30, border=1, relief='solid')
        self.input_key.pack()
        self.input_key.bind("<Return>", lambda event: self.key_insert())

        self.key_btn = tk.Button(self.root, text='Insert Key', command=self.key_insert)
        self.key_btn.pack()

        input_label = tk.Label(self.root, text="(Auto Language Detection)")
        input_label.pack()

        self.input_text = tk.Text(self.root, height=8)
        self.input_text.pack()

        self.translate_button = tk.Button(self.root, text="Translate", command=self.translate_text, state="disabled")
        self.translate_button.pack()

        translated_label = tk.Label(self.root, text="Before Correction")
        translated_label.pack()

        self.translated_output = tk.Text(self.root, height=8)
        self.translated_output.pack()

        self.copy_button = tk.Button(self.root, text="Copy", command=self.copy_translated)
        self.copy_button.pack()

        corrected_label = tk.Label(self.root, text="After Correction")
        corrected_label.pack()

        self.corrected_output = tk.Text(self.root, height=8)
        self.corrected_output.pack()

        self.copy_button = tk.Button(self.root, text="Copy", command=self.copy_corrected)
        self.copy_button.pack()

        lang_label = tk.Label(self.root, text="Select Language")
        lang_label.pack()

        #language list
        langs= {
                'af': 'afrikaans',
                'sq': 'albanian',
                'am': 'amharic',
                'ar': 'arabic',
                'hy': 'armenian',
                'az': 'azerbaijani',
                'eu': 'basque',
                'be': 'belarusian',
                'bn': 'bengali',
                'bs': 'bosnian',
                'bg': 'bulgarian',
                'ca': 'catalan',
                'ceb': 'cebuano',
                'ny': 'chichewa',
                'zh-cn': 'chinese (simplified)',
                'zh-tw': 'chinese (traditional)',
                'co': 'corsican',
                'hr': 'croatian',
                'cs': 'czech',
                'da': 'danish',
                'nl': 'dutch',
                'en': 'english',
                'eo': 'esperanto',
                'et': 'estonian',
                'tl': 'filipino',
                'fi': 'finnish',
                'fr': 'french',
                'fy': 'frisian',
                'gl': 'galician',
                'ka': 'georgian',
                'de': 'german',
                'el': 'greek',
                'gu': 'gujarati',
                'ht': 'haitian creole',
                'ha': 'hausa',
                'haw': 'hawaiian',
                'iw': 'hebrew',
                'he': 'hebrew',
                'hi': 'hindi',
                'hmn': 'hmong',
                'hu': 'hungarian',
                'is': 'icelandic',
                'ig': 'igbo',
                'id': 'indonesian',
                'ga': 'irish',
                'it': 'italian',
                'ja': 'japanese',
                'jw': 'javanese',
                'kn': 'kannada',
                'kk': 'kazakh',
                'km': 'khmer',
                'ko': 'korean',
                'ku': 'kurdish (kurmanji)',
                'ky': 'kyrgyz',
                'lo': 'lao',
                'la': 'latin',
                'lv': 'latvian',
                'lt': 'lithuanian',
                'lb': 'luxembourgish',
                'mk': 'macedonian',
                'mg': 'malagasy',
                'ms': 'malay',
                'ml': 'malayalam',
                'mt': 'maltese',
                'mi': 'maori',
                'mr': 'marathi',
                'mn': 'mongolian',
                'my': 'myanmar (burmese)',
                'ne': 'nepali',
                'no': 'norwegian',
                'or': 'odia',
                'ps': 'pashto',
                'fa': 'persian',
                'pl': 'polish',
                'pt': 'portuguese',
                'pa': 'punjabi',
                'ro': 'romanian',
                'ru': 'russian',
                'sm': 'samoan',
                'gd': 'scots gaelic',
                'sr': 'serbian',
                'st': 'sesotho',
                'sn': 'shona',
                'sd': 'sindhi',
                'si': 'sinhala',
                'sk': 'slovak',
                'sl': 'slovenian',
                'so': 'somali',
                'es': 'spanish',
                'su': 'sundanese',
                'sw': 'swahili',
                'sv': 'swedish',
                'tg': 'tajik',
                'ta': 'tamil',
                'te': 'telugu',
                'th': 'thai',
                'tr': 'turkish',
                'uk': 'ukrainian',
                'ur': 'urdu',
                'ug': 'uyghur',
                'uz': 'uzbek',
                'vi': 'vietnamese',
                'cy': 'welsh',
                'xh': 'xhosa',
                'yi': 'yiddish',
                'yo': 'yoruba',
                'zu': 'zulu',
        }
        #lang_list= langs.keys()
        
        self.lang_combobox = ttk.Combobox(self.root, values=list(langs.values()), state="readonly")
        self.lang_combobox.set("Select Language")
        self.lang_combobox.pack()
        self.lang_combobox.bind("<<ComboboxSelected>>", self.select_lang)

        self.root.mainloop()
        

# Trans 클래스 인스턴스 생성 및 실행
translator = Trans()
translator.run()
