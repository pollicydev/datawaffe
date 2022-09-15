MIME_TO_CATEGORY = {
    "application/msword": "word",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "word",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.template": "word",
    "application/vnd.ms-word.document.macroEnabled.12": "word",
    "application/vnd.ms-word.template.macroEnabled.12": "excel",
    "application/vnd.ms-excel": "excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.template": "excel",
    "application/vnd.ms-excel.sheet.macroEnabled.12": "excel",
    "application/vnd.ms-excel.template.macroEnabled.12": "excel",
    "application/vnd.ms-excel.addin.macroEnabled.12": "excel",
    "application/vnd.ms-excel.sheet.binary.macroEnabled.12": "excel",
    "application/vnd.ms-powerpoint": "powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.template": "powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.slideshow": "powerpoint",
    "application/vnd.ms-powerpoint.addin.macroEnabled.12": "powerpoint",
    "application/vnd.ms-powerpoint.presentation.macroEnabled.12": "powerpoint",
    "application/vnd.ms-powerpoint.template.macroEnabled.12": "powerpoint",
    "application/vnd.ms-powerpoint.slideshow.macroEnabled.12": "powerpoint",
    "application/zip": "zip",
    "image/bmp": "image",
    "image/gif": "image",
    "image/jpeg": "image",
    "image/png": "image",
    "image/tiff": "image",
    "application/pdf": "pdf",
    "text/plain": "word",
    "image/svg+xml": "vector graphic",
    "video/x-ms-wmv": "video",
    "video/quicktime": "video",
    "video/x-msvideo": "video",
    "video/mp4": "video",
    "video/mpeg": "video",
    "text/html": "html",
}

CATEGORY_TO_FILE = {
    "word": "microsoftword.png",
    "excel": "microsoftexcel.png",
    "powerpoint": "microsoftpowerpoint.png",
    "zip": "rar.png",
    "image": "image.png",
    "pdf": "adobereader.png",
    "vector graphic": "photoshop.png",
    "video": "vlc.png",
    "html": "chrome.png",
}


def get_alt_for_mime(mime):
    try:
        return MIME_TO_CATEGORY[mime] + " file"
    except KeyError:
        return "Unknown file"


def get_categories():
    lst = sorted(set(MIME_TO_CATEGORY.values()))
    lst = [(item, item) for item in lst]
    lst.insert(0, ("", "-----"))
    return lst


def get_categories_for_mimes(mimes):
    categories = []
    for mime in mimes:
        try:
            categories.append(MIME_TO_CATEGORY[mime[0]])
        except KeyError:
            categories.append("unknown")
    lst = sorted(set(categories))
    lst = [(item, item) for item in lst]
    lst.insert(0, ("", "-----"))
    return lst


def get_mimes_for_category(category):
    return [keys for keys, value in MIME_TO_CATEGORY.items() if value == category]


def get_icon_for_mime(mime):
    try:
        file = CATEGORY_TO_FILE[MIME_TO_CATEGORY[mime]]
        return "images/icons/%s" % file
    except KeyError:
        return "images/icons/filemanager.png"
