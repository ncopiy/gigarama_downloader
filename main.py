import os
import requests


EVENT_NAME = "velofest2023"

PANORAMAS_IDS = ["P0016828", "P0016829", "P0016830", "P0016831", "P0016832", "P0016833", "P0016834"]

ROWS_COUNT = 21
COLUMNS_COUNT = 28

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'}

def get_photo_pieces(panorama_id):
    main_link = f"https://gigarama.ru/{EVENT_NAME}/xml/panos/{panorama_id}.tiles/"
    for row_number in range(1, ROWS_COUNT + 1):
        for column_number in range(1, COLUMNS_COUNT + 1):
            yield (row_number, column_number, main_link + "l5/{:02d}/l5_{:02d}_{:02d}.jpg".format(row_number, row_number, column_number))


def download_picture(panorama_id, row_number, column_number, url):
    if not os.path.exists(panorama_id):
        os.mkdir(panorama_id)
    
    img_data = requests.get(url, headers=headers).content
    with open(os.path.join(panorama_id, f"{}_{}.jpg".format(row_number, column_number)), 'wb') as handler:
        handler.write(img_data)


def merge_photos(panorama_id):
    pass


if __name__ == "__main__":
    for p_id in PANORAMAS_IDS:
        print(f"downloading {p_id}")
        for row_number, column_number, url in get_photo_pieces(p_id):
            download_picture(p_id, row_number, column_number, url)
        print(f"end of downloading {p_id}")

    for p_id in PANORAMAS_IDS:
        print(f"merge {p_id}")
        merge_photos(p_id)
        print(f"end of merging {p_id}")
