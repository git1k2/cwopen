import math
import random


def gen_random_serials(data=None, perc_cut=None):
    # generate random serial number

    # Cut numbers
    x = "09"
    y = "TN"

    serial_numbers = []
    for i in range(len(data)):
        serial_numbers.append(f'{random.randint(0, 999):03}')

    using_cut_nr = math.floor(perc_cut * len(serial_numbers) / 100)

    count = 0
    for item in serial_numbers[:using_cut_nr]:
        translate_table = item.maketrans(x, y)
        serial_numbers[count] = item.translate(translate_table)
        count += 1

    return serial_numbers


def read_file(filename=None):
    # parse call history file
    with open(filename, 'r') as file:
        uniqe_lines = list(set(file))

    output = []
    for line in uniqe_lines:
        stripped_line = line.strip()
        if not stripped_line.startswith("!!") and not stripped_line.startswith("#") and stripped_line:
            output.append(stripped_line)

    return(output)


def main():
    file = "CWOPS_2984-BBB.txt"

    # percentage of exchanges that use cut numbers, if there is a number to cut...
    percentage_using_cut_nr = 20

    # frequency range
    freq_min = 500
    freq_max = 650

    # wpm range
    wpm_min = 25
    wpm_max = 30

    file_output = read_file(filename=file)
    serial_nrs = gen_random_serials(data=file_output, perc_cut=percentage_using_cut_nr)

    exchange = []
    for idx, line in enumerate(file_output):
        call = line.split(',')[0]
        serial = serial_nrs[idx]
        name = line.split(',')[1]
        exchange.append(f''
                        f'|f{random.randint(freq_min, freq_max)} '
                        f'|w{random.randint(wpm_min, wpm_max)} '
                        f'{call} |S1000 '
                        f'{serial} '
                        f'{name} '
                        f'|S2000')

    # Shuffle exchanges
    random.shuffle(exchange)

    with open('output.txt', 'w') as file:
        for line in exchange:
            file.writelines(line + '\n')


if __name__ == '__main__':
    main()
