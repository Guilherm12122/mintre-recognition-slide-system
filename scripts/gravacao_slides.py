from typing import List
from pathlib import Path
import json


def write_data_in_json_file(data_from_files_pptx: List[dict], write_json_path: str):

    for data_pptx in data_from_files_pptx:

        pptx_name = Path(data_pptx['path_slide']).stem

        with open(f'{write_json_path}/{pptx_name}.json', 'w', encoding='utf-8') as f:

            json.dump(data_pptx, f, ensure_ascii=False, indent=4)

#write_data_in_json_file(get_data_from_files_pptx(PATH_TESTE_SLIDE))


