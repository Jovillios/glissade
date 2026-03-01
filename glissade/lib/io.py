def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def write_file(content: str, path: str) -> None:
    with open(path, "w") as f:
        f.write(content)
