# [Proyecto Frecuencia de Palabras y Proceso *.txt en Mongo]

**El proyecto** esta basado en codigo python, utilizando diversas librerias y en el framework Flask .

Se utilizó el framework de **[Bootstrap](https://getbootstrap.com/)** para el uso amigable de las URLs.

El proyecto consta de varias URLS a mencionar:
- / (home o root): acceso al home del sitio
- /importtxt: pre-proceso de importacion de archivos de text (extension .txt)
- /api/docs/: API para contar la frecuencia de 1 palabra de acuerdo a los parametro.

Cabe mencionar que la interface /api/docs maneja 2 parametros:
```bash
term = debe tener como valor una palabra o numero a buscar ( no debe incluir espacios)
doc_name = nombre del documento donde se desea buscar/contar la palabra. El nombre ingresado puede o no incluir la extension .txt al final del parametro.
```
