import pickle
import os

def dump_info(id_="", mangas=[]):
    if os.stat('settings').st_size != 0:
        with open('settings', 'rb') as file:
            temp = pickle.load(file)
            email = temp[0]['email']
            pass_1 = temp[0]['password']
            login = temp[1]['login']
            pass_2 = temp[1]['password']
    else:
        get_info()
    with open('settings', 'wb') as f:
        mangalib = {"email": email,
                    "password": pass_1,
                    "id": id_}
        shikimori = {"login": login,
                     "password": pass_2}
        pickle.dump([mangalib, shikimori, mangas], f)


def get_info():
    global email, pass_1, login, pass_2
    email = input('Your mangalib login: ')
    pass_1 = input('Your mangalib password: ')
    login = input('Your shikimori login: ')
    pass_2 = input('Your shikimori password: ')

    dump_info()



class Manga:
    def __init__(self, name, topic, chapter):
        self.name = name
        self.topic = topic
        self.chapter = chapter


if __name__ == '__main__':
    get_info()