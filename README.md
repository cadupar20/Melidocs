# [Proyecto Frecuencia de Palabras y Proceso *.txt en Mongo]

**El proyecto** esta basado en codigo python, utilizando diversas librerias y en el framework Flask .

Se utilizó el framework de **[Bootstrap](https://getbootstrap.com/)** para el uso amigable de las URLs.

El proyecto consta de varias URLS a mencionar:
- / (home o root): acceso al home del sitio
- /importtxt: pre-proceso de importacion de archivos de text (extension .txt)
- /api/docs/: API para contar la frecuencia de 1 palabra de acuerdo a los parametro.
- /login: URL para autenticacion, genera un token para el manejo de seguridad de la sesión.

Cabe mencionar que la interface /api/docs maneja 2 parametros:
```bash
term = debe tener como valor una palabra o numero a buscar ( no debe incluir espacios)
doc_name = nombre del documento donde se desea buscar/contar la palabra. El nombre ingresado puede o no incluir la extension .txt al final del parametro.
```
Ejemplo: http://127.0.0.1:5000/api/docs?term=pero&doc_name=10825-8.txt

```bash
{
  "texto": [
    "10825-8.txt", 
    "pero", 
    87
  ]
}
```
## Funciones Principales Python
A continuacion describimos las funciones.

|Funciones|Descripción|Archivo|Nivel|
|----|-----|-----|-----|
|import_txt|inicia la URL /importtxt junto con el proceso de lectura de archivos .txt del directorio ..\downloads |[app.py]| Principal |
|importfiles_toDB|realizar la lectura los archivos .txt, invocando a funciones secundarias como listfiles, InsertFilestoMongo |[importtxt.py]| Principal|
|listfiles|lectura de todo el contenido del directorio \downloads|[importtxt.py]|Secundaria|
|InsertFilestoMongo|recibe el listado de archivos .txt , abre el contenido, llava a la funcion get_database e inserta / actualiza la bse de datos con los los archivos .txt |[importtxt.py]|Secundaria|
|get_database|parametriza e instancia la conexion con la base de datos|[model.py]|Secundaria|
|count_words|inicia la URL /api/docs, toma los parametros recibidos en el query string, valida lo recibo y separa los parametros term y doc_name. Tambien invoca a la funcion querymongo |[app.py]| Principal |
|querymongo|mediante los parametros term y doc_name, solicita la collation, valida que exista el .txt en MongoDB. Luego trae el campo contents con el texto y finalmente busca en el string el "term" cuantas veces aparece (frecuencia) |[getdata.py]|Secundaria|
|string_cleanup|elimina del string caracteres especiales .#¡!¿?()/@%$; del campo contents del find_one de pymongo  |[getdata.py]|Secundaria|


## Instalación
A continuacion describimos los pasos de instalación.

1. `Phyton version 3.6.9` (Descargar [Python](https://www.python.org/) del sitio oficial.)
2. `Instalar Python` (se recomienda seleccionar la opción "Customize installation", **quitar** td/tk and idle, Python test suite y en opciones avanzadas **"Add path Python to  environment variables"**)
3. `mkdir c:\Git\melidocs` crear un directorio donde se va a trabajar con el proyecto.
4. `cd c:\Git\melidocs` ingresar al directorio vacio del proyecto (abrir linea de comando luego de la instalación de Python)
5. `pip install virtualenv` instalacion del entorno virtual
6. `virtualenv venv` Se configura el entorno virtual en el directorio del proyecto
7. `.\venv\Scripts\activate` Activar el modo virtual
8. `c:\Git\melidocs\requirements.txt` descargar el archivo **requirements.txt** en el directorio raiz del proyecto. El mismo contiene todas las librerias necesarias para realizar la implementación.
8. `c:\Git\melidocs>pip install -r requirements.txt` Instalamos en el entorno virtual las librerias a utilizar (flask y pymongo)
9. Para iniciar el servicio, setear las variables de entorno: 
		a. Ingresar al directorio del proyecto c:\Git\melidocs
		b. $env:FLASK_APP = "app"
		c. $env:FLASK_ENV = "development"
		d. flask run
(FLASK_APP="app" FLASK_ENV="development"solo para Windows)

### Instalación de MongoDB
Descargar la version Community del sitio oficial [MongoDB](https://www.mongodb.com/try/download/community).

			a. version 4.4.8
			b. zip
			c. windows
Crear un directorio donde se va a dejar el motor MongoDB, ejemplo `c:\mongodb\4.4\bin`. Crear directorios por default donde se crearan las bases de datos `c:\data\db\`

Crear y configurar archivo `mongod.cfg` en el directorio de instalación de MongoDB  `c:\mongodb\4.4\bin`:
```bash
#network interfaces
net:
port: 27017
bindIp: 127.0.0.1

security:
authorization: enabled
```
- **port** 27017 es el puerto por defecto de MongoDB.
- **bindIP** es la direccion IP por la que atendera las peticiones el demonio MongoDB.
- **security authorization** indica que esta activa la configuracion de seguridad basica.

Se debe crear una cuenta de MongoDB, como admin. Es el root del motor, se debe resguardar de forma segura:
```bash
	C:\mongodb\4.4\bin>mongo --eval "db.createUser({user:'mongoadmin',pwd:'Xi467234.QRTexv1',roles:[{db:'admin',role:'root'}]})" admin
	
	MongoDB shell version v4.4.8
	connecting to: mongodb://127.0.0.1:27017/admin?compressors=disabled&gssapiServiceName=mongodb
	Implicit session: session { "id" : UUID("7982804d-9d13-4d12-bc7a-2ca27805290a") }
	MongoDB server version: 4.4.8
	Successfully added user: {
	        "user" : "mongoadmin",
	        "roles" : [
	                {
	                        "db" : "admin",
	                        "role" : "root"
	                }
	        ]
}
```
Iniciar el motor mongodb, desde una linea de comando: 
`C:\mongodb\4.4\bin>mongod.exe`

## Librerias utilizadas
Lista de frameworks, librarias Python utilizado:
- [Database Drivers](#database-drivers)
- [Web Frameworks](#Web-Frameworks)

## Database-drivers
*Librarias para conectar y gestionar bases de datos.*
* NoSQL Databases
	* [pymongo](https://github.com/mongodb/mongo-python-driver) - Cliente Python oficial para MongoDB.

## Web-Frameworks
*Librarias para la gestion del framework.*
- [Flask](http://flask.pocoo.org/) - A microframework for Python.

### Comando para descargar el proyecto
#### Git (dentro de la carpeta c:\git o en su directorio seleccionado)
```bash
git clone https://github.com/cadupar20/melidocs.git
```
## Browsers soportados

| [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/edge/edge_48x48.png" alt="IE / Edge" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)<br/>IE / Edge | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/firefox/firefox_48x48.png" alt="Firefox" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)<br/>Firefox | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/chrome/chrome_48x48.png" alt="Chrome" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)<br/>Chrome 
| --------- | --------- | --------- |
| last version Edge| last version| last version| 

## Licencia

Este proyecto es open source, puede ser utilizado y compartido libremente.

## Referencias
- [Python](https://www.python.org/)
- [Flask](http://flask.pocoo.org)
- [Pymongo](https://github.com/mongodb/mongo-python-driver)
- [MongoDB](https://www.mongodb.com/try/download/community)
