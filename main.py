import os
from PIL import Image
import requests


EVENT_NAME = "velofest2023"

PANORAMAS_IDS = []

ROWS_COUNT = 21
COLUMNS_COUNT = 28

PIECE_WIDTH = 512
PIECE_HEIGHT = 512

RESULT_FOLDER = "result"

DO_PIECES_DELETION_AFTER_SCRIPT_END = True


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'}


def get_photo_pieces(panorama_id):
    main_link = f"https://gigarama.ru/{EVENT_NAME}/xml/panos/{panorama_id}.tiles/"
    for row_number in range(1, ROWS_COUNT + 1):
        for column_number in range(1, COLUMNS_COUNT + 1):
            yield (row_number, column_number,
                   main_link + "l5/{:02d}/l5_{:02d}_{:02d}.jpg".format(row_number, row_number, column_number))


def download_picture(panorama_id, row_number, column_number, url):
    if not os.path.exists(panorama_id):
        os.mkdir(panorama_id)

    img_data = requests.get(url, headers=headers).content
    with open(os.path.join(panorama_id, "{:02d}_{:02d}.jpg".format(row_number, column_number)), 'wb') as handler:
        handler.write(img_data)


def merge_photos(panorama_id):
    result = Image.new('RGB', (PIECE_WIDTH * COLUMNS_COUNT, PIECE_HEIGHT * ROWS_COUNT))

    for row_number in range(1, ROWS_COUNT + 1):
        for column_number in range(1, COLUMNS_COUNT + 1):
            piece = Image.open(os.path.join(panorama_id, "{:02d}_{:02d}.jpg".format(row_number, column_number)))
            result.paste(piece, (PIECE_WIDTH * (column_number - 1), PIECE_HEIGHT * (row_number - 1)))

    if not os.path.exists(RESULT_FOLDER):
        os.mkdir(RESULT_FOLDER)

    result.save(os.path.join(RESULT_FOLDER, f'{panorama_id}.jpg'))


if __name__ == "__main__":
    for p_id in PANORAMAS_IDS:
        print(f"downloading {p_id}")
        for r_number, c_number, picture_url in get_photo_pieces(p_id):
            download_picture(p_id, r_number, c_number, picture_url)
        print(f"end of downloading {p_id}")

    for p_id in PANORAMAS_IDS:
        print(f"merge {p_id}")
        merge_photos(p_id)
        print(f"end of merging {p_id}")

    if DO_PIECES_DELETION_AFTER_SCRIPT_END:
        for p_id in PANORAMAS_IDS:
            os.remove(p_id)
