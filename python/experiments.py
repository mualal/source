class BeginWithA:
    __match_args__ = ('value', )
    def __init__(self, value):
        self.value = value


class BeginWithNotA:
    __match_args__ = ('value', )
    def __init__(self, value):
        self.value = value


Result = BeginWithA | BeginWithNotA


def check(value: str) -> Result:
    if value.startswith(('a', 'A')):
        return BeginWithA(value)
    return BeginWithNotA(f'{value} starts with not A or a')


def define_string(value: str):
    match check(value=value):
        case BeginWithA(value):
            print(f'Starts with A or a! Value is {value}')
        case BeginWithNotA(value):
            print(f'Error! Message is \"{value}\"')


def main1():
    texts = ['25', '25A', 'A25', 'a25', 'b1']
    for text in texts:
        define_string(value=text)


if __name__ == '__main__':
    main1()
