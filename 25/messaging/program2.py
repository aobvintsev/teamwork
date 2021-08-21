import time


class Recepient:
    def f1(self, s1, s2):
        print(s1, s2)

    def f2(self, s1, s2, s3):
        print(s1, s2, s3)


def new_meth(params_num):
    def f(*args):
        if len(args) != params_num:
            raise TypeError("Waited for {} params, but got {}"
                            .format(params_num, len(args)))
        print(*args)

    return f


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


def process_message(msg, rc):
    if not msg:
        raise ValueError("Empty message")

    parts = msg.split(',')
    if len(parts) < 3:
        raise ValueError(
            "Message must have at least 3 parts: "
            "(command, name, param(s))")

    command = parts[0]
    meth_name = parts[1]
    params = parts[2:]
    if command == 'call':
        meth = getattr(rc, meth_name, None)
        if not meth:
            raise AttributeError(
                "No method with name {}".format(meth_name))

        meth(*params)
    elif command == 'add_method':
        setattr(rc, meth_name, new_meth(int(params[0])))
    else:
        raise ValueError(
            "Invalid message command {}".format(command))


def process(msg_file, out_file, rc, num):
    print('program 2: processing {} messages'.format(num))
    with open(msg_file, 'r') as f:
        for i in range(num):
            s = f.readline()
            if not s:
                raise ValueError("Invalid meassages number")

            msg = s.strip()
            print('program 2: got message: {}'.format(msg))
            try:
                process_message(msg, rc)
            except Exception as e:
                print(e)

    with open(out_file, 'w') as g:
        g.write('{}\n'.format(num))


if __name__ == '__main__':
    print('Program 2 starting')
    rc = Recepient()
    while True:
        num = wait("1.txt")
        try:
            process("msg.txt", "2.txt", rc, num)
        except Exception as e:
            print(e)

