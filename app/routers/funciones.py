from flask import session


def generar_nombre_html(nombre_archivo):
    # Obtener el idioma actual. Este código puede variar dependiendo de cómo manejas la sesión o la configuración del idioma
    idioma_actual = session.get('language', 'es')  # 'es' es el idioma por defecto

    nombre_sin_extension = nombre_archivo.replace("Manual_", "").replace(".pdf", "")
    
    # Agregar el sufijo del idioma antes de la extensión .html
    sufijo_idioma = "_en" if idioma_actual == 'en' else ""
    nombre_html = nombre_sin_extension + sufijo_idioma + ".html"

    #print("Ruta generada:", nombre_html)
    return nombre_html