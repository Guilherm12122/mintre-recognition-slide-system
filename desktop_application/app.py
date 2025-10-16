import tkinter as tk
from tkinter import ttk
import os
from dotenv import load_dotenv, set_key
from tkinter import messagebox, filedialog
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

def set_env_path(env_name, value):

    if os.path.exists(value):
        set_key("../.env", env_name, value)
    else:
        raise Exception(f'O caminho informado para {env_name} é inválido')

def get_slide_from_phrase(phrase, var_notification):

    try:

        if phrase == '':
            raise Exception('Deve-se informar um valor de entrada')

        path = match_voice_json(phrase, os.getenv('ESCRITA_DADOS'))
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


def search_path_explore_files(input):

    path_selected = filedialog.askdirectory(title='Seleciona uma pasta.')

    if path_selected:

        input.delete(0, tk.END)
        input.insert(0, path_selected)


def config_param_envs(main_window):

    config_win = tk.Toplevel(main_window)
    config_win.title('Configuração')
    config_win.geometry("500x500")

    ttk.Label(config_win, text="Caminho do repertório:").pack(expand=True)
    repertorio_path = tk.Entry(config_win, width=100)
    repertorio_path.pack()

    bt_select_path_repertorio = tk.Button(config_win, text='Selecionar pasta para buscar músicas.',
                                          command= lambda : search_path_explore_files(repertorio_path))
    bt_select_path_repertorio.pack()

    ttk.Label(config_win, text="Caminho de escrita dos dados:").pack(expand=True)
    escrita_path = tk.Entry(config_win, width=100)
    escrita_path.pack()

    bt_select_path_escrita = tk.Button(config_win, text='Selecionar pasta para escrever dados das músicas.',
                                       command= lambda : search_path_explore_files(escrita_path))
    bt_select_path_escrita.pack()


    button_save_envs = tk.Button(config_win,
                                 text='Salvar alterações',
                                 command= lambda : modify_env_args(
                                     repertorio_path.get(),
                                     escrita_path.get(),
                                     config_win))

    button_save_envs.pack()

    button_cancel_envs = tk.Button(config_win,
                                   text='Descartar alterações',
                                   command=config_win.destroy)
    button_cancel_envs.pack()

def modify_env_args(repertorio_path: str,
                    escrita_path: str,
                    top_level_win):

    try:
        if not ((repertorio_path != '') or (escrita_path != '')):
            raise Exception('Deve-se preencher ao menos um desses campos.')

        if repertorio_path != '':
            set_env_path("CAMINHO_REPERTORIO", repertorio_path)

        if escrita_path != '':
            set_env_path("ESCRITA_DADOS", escrita_path)

        load_dotenv(override=True)
        messagebox.showinfo('Aviso', 'As alterações foram salvas.',
                            parent=top_level_win)

        top_level_win.destroy()

    except Exception as e:
        messagebox.showerror('ERRO', f'{e}', parent=top_level_win)

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

def update_repertorio(main_window):

    try:
        write_data_in_json_file(
            get_data_from_files_pptx(
                os.getenv('CAMINHO_REPERTORIO')),
                os.getenv('ESCRITA_DADOS'))

        messagebox.showinfo('Aviso', 'Repertório atualizado',
                            parent=main_window)
    except Exception as e:
        messagebox.showerror('ERRO', f'{e}', parent=main_window)

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
    button_update_repertorio = tk.Button(win, text='Atualizar repertório', command= lambda :
                                         update_repertorio(win))
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