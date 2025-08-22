import tkinter as tk

from CONSTANTES import PATH_TESTE_SLIDE
from scripts.correlacionador import match_voice_json
from scripts.gravacao_slides import write_data_in_json_file
from scripts.leitor_slide import get_data_from_files_pptx
from scripts.open_slides import open_file
from scripts.transcricao_audio import get_string_from_audio


def init_win(title, area):

    win = tk.Tk()
    win.title(title)
    win.geometry(area)

    return win


def get_slide_from_phrase(phrase):

    path = match_voice_json(phrase)
    open_file(path)


def get_slide_from_audio():

    try:
        get_slide_from_phrase(get_string_from_audio())
    except Exception as e:
        print(f'ERRO: {e}')



def app():

    # Inicializar janela principal
    win = init_win('Sistema de Reconhecimento de Fala Mintre', '500x500')

    # Adicionar campos de texto de entrada
    phrase_input = tk.Entry(win, width=200)
    phrase_input.pack(padx=30, pady=30)

    # Adicionar botão de buscar música por frase
    button = tk.Button(win, text='Buscar música', command= lambda : get_slide_from_phrase(phrase_input.get()))
    button.pack()

    # Adicionar botão de buscar música por aúdio
    button_buscar_por_audio = tk.Button(win, text='Buscar música por aúdio', command=get_slide_from_audio)
    button_buscar_por_audio.pack()

    # Adicionar botão de atualizar repertório
    button_update_repertorio = tk.Button(win, text='Atualizar repertório', command= lambda : write_data_in_json_file(
                                                get_data_from_files_pptx(PATH_TESTE_SLIDE)))
    button_update_repertorio.pack()

    win.mainloop()

app()