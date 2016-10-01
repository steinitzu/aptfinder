def yes_no_bool(val):
    if val.lower() == 'yes':
        return True
    elif val.lower() == 'no':
        return False
    else:
        raise ValueError(
            'Cannot translate "{}" to bool'.format(val))
