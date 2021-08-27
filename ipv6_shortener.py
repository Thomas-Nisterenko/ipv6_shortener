#ipv6 shortener by Thomas Cascais Nisterenko

ADDRESS_LENGTH = 39
HEX = "0123456789ABCDEFabcdef"
ZERO = 0
ONE = 1
TWO = 2
FIVE = 5


def is_valid_address(ip_address):
    chars_seen = ZERO
    if len(ip_address) != ADDRESS_LENGTH:
        return False

    for char in ip_address:
        chars_seen += ONE

        if not (chars_seen % FIVE):
            if char != ":":
                return False
        else:
            if char not in HEX:
                return False
    return True


def split_address(ip_address):
    ip_address_lst = ip_address.split(":")
    return ip_address_lst


def remove_leading_zeroes(ip_address_lst):
    i = ZERO
    while i < len(ip_address_lst):
        if ip_address_lst[i] == "0000":
            ip_address_lst[i] = "0"
        else:
            ip_address_lst[i] = ip_address_lst[i].lstrip("0")
        i += ONE

    return ip_address_lst


def zero_sequence(ip_address_lst_no_leading):
    seq_len = ZERO
    i = ZERO
    start, end = ZERO, ZERO
    longest = ONE
    sequences = []
    while i < len(ip_address_lst_no_leading):
        if ip_address_lst_no_leading[i] == "0":
            if not seq_len:
                start = i
            else:
                end = i
            seq_len += ONE
        else:
            seq_len = ZERO
            if end - start >= longest:
                longest = end - start
                sequences.append((start, end))
        i += ONE
    
    if end - start >= longest:
        longest = end - start
        sequences.append((start, end))
    
    seq_lengths = [end - start for (start, end) in sequences]

    if not sequences:
        return (-ONE, -ONE)
    return sequences[seq_lengths.index(max(seq_lengths))]


def remove_zero_sequence(ip_address_lst, zero_sequence):
    if zero_sequence == (-ONE, -ONE):
        return ip_address_lst
    else:
        start, end = zero_sequence
        ip_address_lst = ip_address_lst[:start] + [""] + ip_address_lst[end + ONE:]
        
    return ip_address_lst


def merge_address_lst(shortened_address_lst):
    short_address = ":".join(shortened_address_lst)
    if not short_address:
        return "::"
    if shortened_address_lst[ZERO] == "":
        short_address = ":" + short_address
    elif shortened_address_lst[-ONE] == "":
        short_address += ":"
    return short_address


def shorten_ip_address():
    valid = False
    while not valid:
        ip_address = input("Please provide a valid, full-length IPv6 address> ")
        valid = is_valid_address(ip_address)

    ip_address_lst = split_address(ip_address)
    no_leading = remove_leading_zeroes(ip_address_lst)
    sequence = zero_sequence(no_leading)
    short_lst = remove_zero_sequence(no_leading, sequence)
    shortened_address = merge_address_lst(short_lst)

    print()
    print("Full address>", ip_address)
    print("Shortened address>", shortened_address)
    print()


def main():
    print("Welcome to the IPv6 address shortener in python!\n")
    quit = False
    while not quit:
        shorten_ip_address()
        usr_choice = input("Press 'q' to quit, press any other key to run the shortener again> ")
        print()
        if usr_choice.lower() == "q":
            quit = True
    print("Goodbye!")


if __name__ == "__main__":
    main()
