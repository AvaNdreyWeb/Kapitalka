def generate_wallet_slug(ru_str):
    ru_str = ru_str.lower()
    ALPH = {
        'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'еёэ',
        'dz': 'ж', 'z': 'з', 'i': 'ийы', 'k': 'к', 'l': 'л', 'm': 'м',
        'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у',
        'f': 'ф', 'h': 'х', 'ts': 'ц', 'ch': 'ч', 'sh': 'шщ',
        'yu': 'ю', 'ya': 'я', '_': ' ([{-<', '': '.,+=~`?>!@#$%^&*}])|\\/ьъ\"\'',
    }
    slug = ''
    for char in ru_str:
        f = True
        for key, value in ALPH.items():
            if char in value:
                slug += key
                f = False
                break
        if f:
            slug += char
    return slug
