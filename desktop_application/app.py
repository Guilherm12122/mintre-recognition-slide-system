import os
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
from dotenv import load_dotenv, set_key
from threading import Thread

# Imports locais
from scripts.correlacionador import match_voice_json
from scripts.gravacao_slides import write_data_in_json_file
from scripts.leitor_slide import get_data_from_files_pptx
from scripts.open_slides import open_file
from scripts.transcricao_audio import get_string_from_audio


# ==========================
# INICIALIZAÇÃO DA JANELA
# ==========================
def init_win(title, area):
    win = tb.Window(themename="superhero")
    win.title(title)
    win.geometry(area)
    win.resizable(True, True)
    win.place_window_center()
    win.configure(padx=20, pady=20)
    return win


# ==========================
# FUNÇÕES AUXILIARES
# ==========================
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


def search_path_explore_files(entry_widget):
    path_selected = filedialog.askdirectory(title='Seleciona uma pasta.')
    if path_selected:
        entry_widget.delete(0, "end")
        entry_widget.insert(0, path_selected)


# ==========================
# CONFIGURAÇÕES DE DIRETÓRIOS
# ==========================
def config_param_envs(main_window):
    config_win = tb.Toplevel(main_window)
    config_win.title('Configuração')
    config_win.geometry("500x400")
    config_win.configure(padx=20, pady=20)

    tb.Label(config_win, text="Caminho do repertório:", font=('Segoe UI', 10, 'bold')).pack(anchor=W, pady=(0, 5))
    repertorio_path = tb.Entry(config_win, width=70)
    repertorio_path.pack(pady=(0, 10))

    tb.Button(config_win, text='Selecionar pasta de músicas', bootstyle=INFO,
              command=lambda: search_path_explore_files(repertorio_path)).pack(pady=(0, 15))

    tb.Label(config_win, text="Caminho de escrita dos dados:", font=('Segoe UI', 10, 'bold')).pack(anchor=W, pady=(0, 5))
    escrita_path = tb.Entry(config_win, width=70)
    escrita_path.pack(pady=(0, 10))

    tb.Button(config_win, text='Selecionar pasta de escrita', bootstyle=INFO,
              command=lambda: search_path_explore_files(escrita_path)).pack(pady=(0, 20))

    frame_buttons = tb.Frame(config_win)
    frame_buttons.pack(fill=X, pady=(10, 0))

    tb.Button(frame_buttons, text='Salvar alterações', bootstyle=SUCCESS,
              command=lambda: modify_env_args(
                  repertorio_path.get(),
                  escrita_path.get(),
                  config_win)).pack(side=LEFT, expand=True, fill=X, padx=5)

    tb.Button(frame_buttons, text='Descartar alterações', bootstyle=DANGER,
              command=config_win.destroy).pack(side=LEFT, expand=True, fill=X, padx=5)


def modify_env_args(repertorio_path: str, escrita_path: str, top_level_win):
    try:
        if not ((repertorio_path != '') or (escrita_path != '')):
            raise Exception('Deve-se preencher ao menos um desses campos.')

        if repertorio_path != '':
            set_env_path("CAMINHO_REPERTORIO", repertorio_path)
        if escrita_path != '':
            set_env_path("ESCRITA_DADOS", escrita_path)

        load_dotenv(override=True)
        messagebox.showinfo('Aviso', 'As alterações foram salvas.', parent=top_level_win)
        top_level_win.destroy()

    except Exception as e:
        messagebox.showerror('ERRO', f'{e}', parent=top_level_win)


# ==========================
# NOTIFICAÇÕES E THREADS
# ==========================
def notification_alert(alert_msg, main_window):
    main_window.after(0, lambda: messagebox.showinfo('Notificação', alert_msg))


def get_slide_from_audio(main_window):
    notif = create_win_notification(main_window, 'Escutando')
    create_thread_get_phrase_from_audio(notif)


def create_thread_get_phrase_from_audio(notif):
    thread_search = Thread(target=search_from_audio, args=(notif,))
    thread_search.start()


def execute_threads(phrase, alert_msg, main_window):
    notif = create_win_notification(main_window, alert_msg)
    create_thread_search(phrase, notif)


def create_thread_search(phrase, notif=None):
    thread_search = Thread(target=get_slide_from_phrase, args=(phrase, notif))
    thread_search.start()


def create_win_notification(main_window, alert_msg):
    notif = tb.Toplevel(main_window)
    notif.title("Processando...")
    notif.geometry("300x120")
    notif.configure(padx=20, pady=20)
    tb.Label(notif, text=f"{alert_msg}...", font=('Segoe UI', 11)).pack(expand=True, pady=10)
    notif.transient(main_window)
    notif.grab_set()
    return notif


# ==========================
# ATUALIZAÇÃO DE REPERTÓRIO
# ==========================
def update_repertorio(main_window):
    try:
        write_data_in_json_file(
            get_data_from_files_pptx(os.getenv('CAMINHO_REPERTORIO')),
            os.getenv('ESCRITA_DADOS'))
        messagebox.showinfo('Aviso', 'Repertório atualizado', parent=main_window)
    except Exception as e:
        messagebox.showerror('ERRO', f'{e}', parent=main_window)


# ==========================
# APLICAÇÃO PRINCIPAL
# ==========================
def app():
    win = init_win('Sistema de Reconhecimento de Fala Mintre', '500x500')

    tb.Label(win, text="Digite a frase para buscar música:",
             font=('Segoe UI', 11, 'bold')).pack(pady=(10, 5))

    phrase_input = tb.Entry(win, width=80)
    phrase_input.pack(pady=(0, 20))

    tb.Button(win, text='Buscar música', bootstyle=PRIMARY,
              command=lambda: execute_threads(phrase_input.get(), 'Procurando', win)).pack(pady=5, fill=X)

    tb.Button(win, text='Buscar música por áudio', bootstyle=INFO,
              command=lambda: get_slide_from_audio(win)).pack(pady=5, fill=X)

    tb.Button(win, text='Atualizar repertório', bootstyle=SECONDARY,
              command=lambda: update_repertorio(win)).pack(pady=5, fill=X)

    tb.Button(win, text='Definir diretórios de leitura e escrita', bootstyle=WARNING,
              command=lambda: config_param_envs(win)).pack(pady=(15, 0), fill=X)

    tb.Label(win, text="Mintre © 2025", font=('Segoe UI', 9, 'italic')).pack(side=BOTTOM, pady=10)

    win.mainloop()


# ==========================
# EXECUÇÃO
# ==========================
load_dotenv()
app()
