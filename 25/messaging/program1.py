import time


def wait(in_file):
    while True:
        try:
            with open(in_file, 'r') as f:
                s = f.read()
            if s:
                break
        except IOError:
            pass
        time.sleep(1)
    with open(in_file, 'w') as g:
        pass
    return int(s)


def generate(msg_file, out_file):
    print('program 1: generating messages')
    with open(msg_file, 'w') as f:
        num = 0
        while True:
            msg = input('program1: message:')
            if not msg:
                break
            msg = msg.replace(' ', '')
            f.write(msg + '\n')
            num += 1

    with open(out_file, 'w') as g:
        g.write('{}\n'.format(num))


if __name__ == '__main__':
    print('Program 1 starting')
    while True:
        generate("msg.txt", "1.txt")
        wait("2.txt")
