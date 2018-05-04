def format_sizeof(number, suffix='', divisor=1000):
    """
    Formats a number (greater than unity) with SI Order of Magnitude
    prefixes.
    Parameters
    ----------
    num  : float
        Number ( >= 1) to format.
    suffix  : str, optional
        Post-postfix [default: '']
    divisor  : float, optionl
        Divisor between prefixes [default: 1000].
    Returns
    -------
    out  : str
        Number with Order of Magnitude SI unit postfix.
    """
    for unit in ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(number) < 999.95:
            if abs(number) < 99.95:
                if abs(number) < 9.995:
                    return '{0:1.2f}'.format(number) + unit + suffix
                return '{0:2.1f}'.format(number) + unit + suffix
            return '{0:3.0f}'.format(number) + unit + suffix
        number /= divisor
    return '{0:3.1f}Y'.format(number) + suffix

a=format_sizeof(1000000000000)
print(a)