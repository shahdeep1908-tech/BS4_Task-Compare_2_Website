import re


def check_extra_dots(blog):
    num_of_dots = {'dot_count_2': 0, 'dot_count_3': 0, 'dot_count_4': 0}
    for dots in blog:
        if type(dots) == list:
            dots = ''.join(dots)
        regex = re.split(r'(\.+)', dots)
        num_of_dots['dot_count_2'] += regex.count('..')
        num_of_dots['dot_count_3'] += regex.count('...')
        num_of_dots['dot_count_4'] += regex.count('....')
    print('*' * 50)
    print('dot_count_2 :', num_of_dots['dot_count_2'])
    print('dot_count_3 :', num_of_dots['dot_count_3'])
    print('dot_count_4 :', num_of_dots['dot_count_4'])
    print('*' * 50)
    return num_of_dots
