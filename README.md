# Gigarama Downloader
## Утилита для загрузки панорамы из gigarama.ru

Утилита сделана для загрузки панорамной фотографии велофестиваля `velofest2023`.
Для загрузки панорамы другого события необходимо поменять значение константы `EVENT_NAME`.
В `PANORAMAS_IDS` указываются идентификаторы панорам. Например:
```
PANORAMAS_IDS = ["P0016831", "P0016860"]
```

Предварительно необходимо установить зависимости из `requirements.txt`.
Запуск скрипта обычный - `python main.py`

Если нужна не только панорама, но и ее отдельные части, можно выключить их удаление:
```
DO_PIECES_DELETION_AFTER_SCRIPT_END = False
```