import ntpath


def get_filename_from_path(path: str) -> str:
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

