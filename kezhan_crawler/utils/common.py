import hashlib


def get_md5(url):  # UTF_8
    if isinstance(url, str):
        url = url.encode('utf8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == "__main__":
    print(get_md5('testing'.encode('utf8')))
    print(get_md5('yabnglingyushiqiangdeyipi'))
