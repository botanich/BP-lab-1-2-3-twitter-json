import json
import twitter2
import copy


def directory(container):
    """
    (dict(str, value)) -> list(str)
    (list(value)) -> list(str)
    Returns all keys and types of values of given dictionary.
    """

    lst = []
    if type(container) is dict:
        for key in container:
            num_spaces = len('key: ' + key)
            lst.append('key: ' + key + (60 - num_spaces)*' ' +
                       'value type: ' + str(type(container[key])))
        return '\n'.join(lst)
    elif type(container) is list:
        for i in range(len(container)):
            num_spaces = len('index: ' + str(i))
            lst.append('index: ' + str(i) + (60 - num_spaces)*' ' +
                       'value type: ' + str(type(container[i])))
        return '\n'.join(lst)
    else:
        return str(container)


def change_directory(container, path, key):
    """
    (dict, str) -> (dict/list/None)
    (list, int) -> (dict/list/None)

    Returns container which is subcontainer of given one.
    """

    try:
        tmp = container[key]
        path.append(key)
        return tmp
    except (TypeError, ValueError):
        return None


def navigate(container):
    """
    (dict, str, str) -> None
    (list, int, str) -> None
    Recursive function which allows to navigate in dictionary.
    Returns current path in it each time.
    """

    ancestor = copy.deepcopy(container)
    path = []
    while True:
        try:
            str_path = '/' + '/'.join(list(map(str, path)))
            key = input(str_path + '\n')
            if key == 'exit':
                break
            elif key == 'dir':
                print(directory(container))
            elif key.startswith('cd'):
                if key == 'cd..' or key == 'cd ..':
                    if not path:
                        continue
                    else:
                        del path[-1]
                        container = copy.deepcopy(ancestor)
                        for item in path:
                            container = container[item]
                else:
                    if key[2] == ' ':
                        key = key[3:]
                        if type(container) is list:
                            key = int(key)
                        container = change_directory(container, path, key)
            else:
                raise ValueError
        except:
            print('Wrong command. Try again.')
            continue


def main():
    nickname = input('Input account nickname to get data from: ')
    json_dict = twitter2.get_info_by_nickname(nickname)

    print('\nNavigate on the dictionary! [cd <key>] to go into value by key;' +
          '\n[cd ..] to go back; [dir] to see keys and types of values;\n' +
          '[exit] to leave dictionary and stop program.')
    navigate(json_dict)


if __name__ == '__main__':
    main()
