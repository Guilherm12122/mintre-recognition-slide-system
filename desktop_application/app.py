import tkinter as tk
from tkinter import ttk
import os
from dotenv import load_dotenv, set_key
from tkinter import messagebox
from threading import Thread
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

def get_slide_from_phrase(phrase, var_notification):

    try:
        path = match_voice_json(phrase, os.getenv('PATH_TESTE_WRITE_JSON'))
        open_file(path)
    except Exception as e:
        messagebox.showerror('ERRO', f'{e}')

    if var_notification is not None:
        var_notification.destroy()

def search_from_audio(var_notification):

    phrase = ''

    try:
        phrase = get_string_from_audio()
        create_thread_search(phrase)
    except Exception as e:
        messagebox.showerror('ERRO', f'{e}')

    var_notification.destroy()

    return phrase

def config_param_envs(main_window):

    config_win = tk.Toplevel(main_window)
    config_win.title('Configuração')
    config_win.geometry("500x500")

    ttk.Label(config_win, text="Caminho do repertório:").pack(expand=True)
    repertorio_path = tk.Entry(config_win, width=100)
    repertorio_path.pack()

    ttk.Label(config_win, text="Caminho de escrita dos dados:").pack(expand=True)
    escrita_path = tk.Entry(config_win, width=100)
    escrita_path.pack()

    button_save_envs = tk.Button(config_win,
                                 text='Salvar alterações',
                                 command= lambda : modify_env_args(
                                     repertorio_path.get(),
                                     escrita_path.get(),
                                     config_win
                                 ))
    button_save_envs.pack()

    button_cancel_envs = tk.Button(config_win,
                                   text='Descartar alterações',
                                   command=config_win.destroy)
    button_cancel_envs.pack()

def modify_env_args(repertorio_path: str,
                    escrita_path: str,
                    top_level_win):

    set_key(".env", "PATH_TESTE_SLIDE", repertorio_path)
    set_key(".env", "PATH_TESTE_WRITE_JSON", escrita_path)
    load_dotenv(override=True)
    messagebox.showinfo('Aviso', 'As alterações foram salvas.',
                        parent=top_level_win)

def notification_alert(alert_msg, main_window):
    main_window.after(0, lambda: messagebox.showinfo('Notificação', alert_msg))

def get_slide_from_audio(main_window):

    notif = create_win_notification(main_window, 'Escutando')
    create_thread_get_phrase_from_audio(notif)


def create_thread_get_phrase_from_audio(notif):

    thread_search = Thread(target=search_from_audio, args=(notif,))
    thread_search.start()


def execute_threads(phrase, alert_msg, main_window):

    # Cria janela box de notificação
    notif = create_win_notification(main_window, alert_msg)

    # Cria thread de busca
    create_thread_search(phrase, notif)


def create_thread_search(phrase, notif = None):
    thread_search = Thread(target=get_slide_from_phrase, args=(phrase, notif))
    thread_search.start()


def create_win_notification(main_window, alert_msg):

    notif = tk.Toplevel(main_window)
    notif.title(f"Processando...")
    notif.geometry("250x100")
    ttk.Label(notif, text=f"{alert_msg}...").pack(expand=True, pady=20)
    notif.transient(main_window)  # fica em cima da principal
    notif.grab_set()

    return notif


def app():

    # Inicializar janela principal
    win = init_win('Sistema de Reconhecimento de Fala Mintre', '500x500')

    # Adicionar campos de texto de entrada
    phrase_input = tk.Entry(win, width=200)
    phrase_input.pack(padx=30, pady=30)

    # Adicionar botão de buscar música por frase
    button = tk.Button(win, text='Buscar música', command= lambda : execute_threads(phrase_input.get(), 'Procurando', win))
    button.pack()

    # Adicionar botão de buscar música por aúdio
    button_buscar_por_audio = tk.Button(win, text='Buscar música por aúdio', command= lambda : get_slide_from_audio(win))
    button_buscar_por_audio.pack()

    # Adicionar botão de atualizar repertório
    button_update_repertorio = tk.Button(win, text='Atualizar repertório', command= lambda : write_data_in_json_file(
                                                get_data_from_files_pptx(
                                                    os.getenv('PATH_TESTE_SLIDE')),
                                                    os.getenv('PATH_TESTE_WRITE_JSON')))
    button_update_repertorio.pack()

    # Adicionar botão de configurar as variáveis de ambiente
    buttom_update_envs = tk.Button(
        win, text='Definir diretório de leitura e escrita dos dados',
        command= lambda : config_param_envs(win)
    )

    buttom_update_envs.pack()

    win.mainloop()

load_dotenv()
app()