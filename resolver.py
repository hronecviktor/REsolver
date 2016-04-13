import re
from itertools import product
import string
import time


def re_matches(regex, len, chars):
    combinations = (''.join(letters) for letters in product(chars, repeat=len))
    matching = []
    for combination in combinations:
        if regex.match(combination):
            matching.append(combination)
    return matching


def field_print(lst):
    print("\"" * 30)
    for line in lst:
        print(''.join(line))
    print("\"" * 30)


def setfields(lst, choices):
    _cols = len(lst[0])
    cnt = 0
    for line in range(lines):
        lst[line][:_cols] = choices[cnt:cnt + _cols]
        cnt += _cols
    return lst


def check_regexes(lst, re_vertical):
    colx = lambda list, position: ''.join(line[position] for line in list)
    for cnt, re_column in enumerate(re_vertical):
        col_text = colx(lst, cnt)
        if not re_column.match(col_text):
            return False
    return True


def apply_anchors(regex):
    if not regex.endswith('$'):
        regex = regex + '$'
    if not regex.startswith('^'):
        regex = '^' + regex
    return regex


if __name__ == '__main__':
    # MOCKUP

    # WALKER
    # horizontal = ['[AWE]+',
    #               '[ALP]+K',
    #               'PR|ER|EP']
    #
    # vertical = ['[BQW](PR|LE)',
    #             '[RANK]+']

    # HELP
    # horizontal = ['HE|LL|O+',
    #           '[PLEASE]+']
    #
    # vertical = ['[^SPEAK]+',
    #         'EP|IP|EF']

    # DONTPANIC
    horizontal = ['[DEF][MNO]*',
                  '[^DJNU]P[ABC]',
                  '[ICAN]*']

    vertical = ['[JUNDT]*',
                'APA|OPI|OLK',
                '(NA|FE|HE)[CV]']

    # HAMLET #1
    # horizontal = [
    #     """[RA](A|E)[V\s]\1[NG]+\1""",
    #     """[SHI\s]+.{2}""",
    #     """(FO|UL|ED)*[DAN\s]+""",
    #     """[TORM]+ST(U|\s|N|K)*""",
    #     """(F|N)(.)[RUNT]+\2[CL]*""",
    #     """\s[URM]*[ERD]{3,}"""
    # ]
    #
    # vertical = [
    #     """[RQ\s]*(N|U|M|\s){3,}""",
    #     """(N|I|E)[HOLE]{2,}A(M|N)""",
    #     """[VIT]{2}[T\s]?(STU|PLO)+""",
    #     """(E|\s)(A|S|K)*.U?[FR]""",
    #     """(F|A|N)(\s)\1\2[RIF](K|D)+""",
    #     """(G|A|\s)(DU|F|SET)+[WAE]+""",
    #     """[ASK]?(LR|EO|\sN)+"""
    # ]

    horizontal = [apply_anchors(regex) for regex in horizontal]
    vertical = [apply_anchors(regex) for regex in vertical]

    horizontal = [re.compile(pat) for pat in horizontal]
    vertical = [re.compile(pat) for pat in vertical]

    lenh = lines = len(horizontal)
    lenv = cols = len(vertical)

    fields = [[' ' for option in range(cols)] for option in range(lines)]

    usable_chars = string.ascii_uppercase+'1234567890 .:/-$?!\\'

    print('Looking for horizontal match groups, please wait...')

    horizontal_matches = [re_matches(regex, cols, usable_chars)
                          for regex in horizontal]
    start_time = time.time()
    all_options = [''.join(letters) for letters in product(*horizontal_matches)]

    print('Trying {} combinations of horizontal matches, please wait...'.format(
            len(all_options)
    ))

    last_percent = 0
    for opt_number, option in enumerate(all_options):
        percent_done = int((opt_number / float(len(all_options))) * 100)
        if percent_done != last_percent:
            last_percent = percent_done
            print('{}% of options scanned ({}/{} - \'{}\')'.format(percent_done,
                                                          opt_number,
                                                          len(all_options), option))
        setfields(fields, option)
        matched = check_regexes(fields, vertical)
        if matched:
            field_print(fields)
            print(
            'Solution is \'{}\', guessed on try #{}'.format(option, opt_number))
            break
    time_took = time.time() - start_time
    print("Finished in {}s - {} attempts / second".format(time_took, int(
        opt_number / time_took)))
