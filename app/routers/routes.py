from flask import g, render_template

from app.models.routers import Archivo
from .funciones import generar_nombre_html

from . import routers

@routers.route("/CodigoRoot")
def ClaveRoot():
    
    return render_template("routers/coderoot.html", title=" Clave Root para tu Router AX")


@routers.route('/ax1800')
def ax1800():
   
    archivos = Archivo.query.all()
    return render_template("routers/ax1800.html", archivos=archivos, title=" Manuales para el Ax1800",  generar_nombre_html=generar_nombre_html)

@routers.route('/Explicacionax1800')
def Explicacionax1800():
    archivos = Archivo.query.all()
    return render_template("routers/caracteristicas/Explicacionax1800.html", archivos=archivos, title=" Explicacion Ax1800") 

@routers.route('/Explicacionax1800_en')
def Explicacionax1800_en():
    archivos = Archivo.query.all()
    return render_template("routers/caracteristicas/Explicacionax1800_en.html", archivos=archivos, title=" Explicacion Ax1800") 


@routers.route('/ax3000')
def ax3000():
   
    archivos = Archivo.query.all()
    return render_template("routers/ax3000.html", archivos=archivos, title=" Manuales para el Ax3000",  generar_nombre_html=generar_nombre_html)


@routers.route('/Explicacionax3000')
def Explicacionax3000():
    archivos = Archivo.query.all()
    return render_template("routers/caracteristicas/Explicacionax3000.html", archivos=archivos, title=" Explicacion Ax3000")

@routers.route('/Explicacionax3000_en')
def Explicacionax3000_en():
    archivos = Archivo.query.all()
    return render_template("routers/caracteristicas/Explicacionax3000_en.html", archivos=archivos, title=" Explicacion Ax3000")



@routers.route('/ax3600')
def ax3600():
   
    archivos = Archivo.query.all()
    return render_template("routers/ax3600.html", archivos=archivos, title=" Manuales para el Ax3600",  generar_nombre_html=generar_nombre_html)


@routers.route('/Explicacionax3600')
def Explicacionax3600():
    archivos = Archivo.query.all()
    return render_template("routers/caracteristicas/Explicacionax3600.html", archivos=archivos, title=" Explicacion Ax3600")
    
@routers.route('/Explicacionax3600_en')
def Explicacionax3600_en():
    archivos = Archivo.query.all()
    return render_template("routers/caracteristicas/Explicacionax3600_en.html", archivos=archivos, title=" Explicacion Ax3600")
    

@routers.route('/ax9000')
def ax9000():
   
    archivos = Archivo.query.all()
    return render_template("routers/ax9000.html", archivos=archivos, title=" Manuales para el Ax9000",  generar_nombre_html=generar_nombre_html)


@routers.route('/Explicacionax9000')
def Explicacionax9000():
    archivos = Archivo.query.all()
    return render_template("routers/caracteristicas/Explicacionax9000.html", archivos=archivos, title=" Explicacion Ax9000")

@routers.route('/Explicacionax9000_en')
def Explicacionax9000_en():
    archivos = Archivo.query.all()
    return render_template("routers/caracteristicas/Explicacionax9000_en.html", archivos=archivos, title=" Explicacion Ax9000")


@routers.route('/Manuales/<filename>')
def manuales(filename):
    return render_template(f"routers/manuales/{filename}")
