def format_date_to_locale( date : str) -> str:
    splitted_date = date.split('-')

    return '/'.join(splitted_date[::-1])