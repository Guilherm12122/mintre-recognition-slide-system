# Esse script irá calcular a correlação do aúdio de entrada com o json, irá pegar o path
# dos dados de slide que possuir a maior correlação
import  glob
import json
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from CONSTANTES import PATH_READ_DATA_JSON


def extract_dict_from_json_file(file_json_path: str):

    return json.load(open(file_json_path))


def get_dicts_from_json_files(general_path_json: str):

    return [extract_dict_from_json_file(file_json_path)
            for file_json_path in glob.glob(general_path_json, recursive=True)]


def return_max_correlation(phrase: str, list_strs: List[str]):

    list_correlation = []

    for string in list_strs:

        vectorizer = TfidfVectorizer().fit_transform([phrase, string])

        list_correlation.append(float(cosine_similarity(vectorizer[0], vectorizer[1])[0][0]))

    return max(list_correlation)


def match_voice_json(phrase: str):

    data_slide = get_dicts_from_json_files(PATH_READ_DATA_JSON)

    list_dict_slides_correlation = []

    for info_slide in data_slide:

        list_content = [content['conteudo'] for content in info_slide['data']]

        correlation = return_max_correlation(phrase, list_content)

        list_dict_slides_correlation.append({'path': info_slide['path_slide'], 'correlation': correlation})

    max_dict_correlation = max(list_dict_slides_correlation, key=lambda obj: obj['correlation'])

    if max_dict_correlation['correlation'] > 0:
        return max_dict_correlation['path']
    else:
        raise Exception('O valor de entrada não corresponde a nenhum slide disponível...Tente atualizar o repertório !')
