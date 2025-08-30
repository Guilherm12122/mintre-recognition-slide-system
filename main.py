from CONSTANTES import PATH_TESTE_SLIDE
from scripts.leitor_slide import get_data_from_files_pptx
from scripts.gravacao_slides import write_data_in_json_file
from scripts.correlacionador import match_voice_json
from scripts.open_slides import open_file
from scripts.transcricao_audio import get_string_from_audio

def app():
    print('''BEM VINDO AO SISTEMA DE RECONHECIMENTO DE SLIDES DA MINTRE
        VOCÊ DESEJA:
            - 1: ATUALIZAR REPERTÓRIO DE MÚSICAS?
            - 2: BUSCAR UMA MÚSICA USANDO UMA FRASE?
    ''')
    option = input('Escolha: ')

    if option == '1':
        write_data_in_json_file(get_data_from_files_pptx(PATH_TESTE_SLIDE))
    elif option == '2':
        print('Fale uma frase da música !')
        frase = get_string_from_audio()
        caminho = match_voice_json(frase)
        open_file(caminho)
    else:
        raise Exception('Opção digitada é inválida !')

try:
    app()
except Exception as e:
    print(f'Erro: {e}')


