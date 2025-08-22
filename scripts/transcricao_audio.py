# Obtém o aúdio de entrada do computador e converte em string.

import speech_recognition as sr

from CONSTANTES import TIME_LISTENING, DEVICE_INDEX


def get_string_from_audio():

    recognizer = sr.Recognizer()

    with sr.Microphone(device_index=DEVICE_INDEX) as source:

        audio = recognizer.listen(source, timeout=3, phrase_time_limit=TIME_LISTENING)

        try:
            string_audio = recognizer.recognize_google(audio, language="pt-BR")
            return string_audio
        except sr.UnknownValueError:
            print("Não entendi o que você falou")
        except sr.RequestError:
            print("Erro ao se conectar ao serviço de reconhecimento")
        except sr.WaitTimeoutError:
            print("Nada foi dito !")
        except Exception as e:
            print("Erro:", e)