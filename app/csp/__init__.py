

csp = {
    'default-src': '\'self\'',
    'connect-src': [
        '\'self\'',
        # Agregar otras fuentes de conexión según sea necesario
    ],
    'script-src': [
        '\'self\'',
        'https://code.jquery.com',
        'https://cdn.jsdelivr.net',
        # Agregar otras fuentes de scripts según sea necesario
    ],
    'style-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
        # Agregar otras fuentes de fuentes según sea necesario
    ],
    'font-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
        # Agregar otras fuentes de fuentes según sea necesario
    ],
    'img-src': [
        '\'self\'',
        # Agregar otras fuentes de imágenes según sea necesario
    ],
    'frame-src': [
        '\'self\'',
        # Agregar otros dominios de iframes si es necesario
    ],
    # Agregar más directivas según sea necesario
}

