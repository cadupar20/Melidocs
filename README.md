# [Proyecto Frecuencia de Palabras y Proceso *.txt en Mongo]

**El proyecto** está basado en código python, utilizando diversas librerías y en el framework Flask.

Se utilizó el framework de **[Bootstrap](https://getbootstrap.com/)** para el uso amigable de las URLs.

El proyecto consta de varias URLS a mencionar:
- `/` (home o root): acceso al home del sitio
- `/import_txt`: pre-proceso de importación de archivos de texto (extensión .txt)
- `/api/docs`: API para contar la frecuencia de 1 palabra de acuerdo a los parámetros.
- `/login`: URL para autenticación, genera un token para el manejo de seguridad de la sesión.

**Actualización**
(2) nuevas URLs agregadas, mejoras a la función de Contar de Frecuencia de término:
- `/api/docsV2?`: API versión 2 de frecuencia de 1 palabra de acuerdo a los parámetros, utilizando Aggregation como contador de frecuencia y regex para omitir caracteres especiales **¡¿([,")%'\',;'$?!:#;:'#._-**
- `/api/docsV3?`: API versión 2 de frecuencia de 1 palabra de acuerdo a los parámetros, utilizando translate para eliminar caracteres especiales.

**MongoDB*
Se crea 1 indice dentro de MongoDB para mejorar la performance de busqueda del documento:
![](https://raw.githubusercontent.com/cadupar20/melidocs/main/Index_docname.jpg)
![](https://raw.githubusercontent.com/cadupar20/melidocs/main/Index_properties.jpg)

Cabe mencionar que la interfaz /api/docs maneja 2 parámetros:
+ term = debe tener como valor una palabra o número a buscar (no debe incluir espacios)
+ doc_name = nombre del documento donde se desea buscar/contar la palabra. El nombre ingresado puede o no incluir la extensión .txt al final del parámetro.

Ejemplo: http://127.0.0.1:5000/api/docs?term=pero&doc_name=10825-8.txt

Ejemplo versión 2: http://127.0.0.1:5000/api/docsV2?term=pero&doc_name=10825-8.txt

Ejemplo versión 3: http://127.0.0.1:5000/api/docsV3?term=pero&doc_name=10825-8.txt

```bash
{
"texto": [
"10825-8.txt",
"pero",
87
]
}
```

El path posee seguridad de Token, deben incluirse en el Header con método Get:

```bash
GET /api/docs?term=habia&amp;doc_name=10825-8.txt HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjMwNzIwMzAyLCJqdGkiOiJjNTM4OTIwOC1lZjEzLTQxZGQtOGM3MS1iMjVhYWYyYTQ3OTMiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoidGVzdCIsIm5iZiI6MTYzMDcyMDMwMiwiZXhwIjoxNjMwNzIxMjAyfQ.iXip9s7hJJ_MLBvJ3Hd63pp2kIHdl_VF73lWF0KxOd0
Cache-Control: no-cache
Postman-Token: e54f1b32-924d-61a1-88c1-9d0e54aa5cb5
```
**Actualización**
```bash
GET /api/docsV2?term=había&amp;doc_name=10825-8.txt HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjMwNzIwMzAyLCJqdGkiOiJjNTM4OTIwOC1lZjEzLTQxZGQtOGM3MS1iMjVhYWYyYTQ3OTMiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoidGVzdCIsIm5iZiI6MTYzMDcyMDMwMiwiZXhwIjoxNjMwNzIxMjAyfQ.iXip9s7hJJ_MLBvJ3Hd63pp2kIHdl_VF73lWF0KxOd0
Cache-Control: no-cache
Postman-Token: e54f1b32-924d-61a1-88c1-9d0e54aa5cb5
```
```bash
GET /api/docsV3?term=había&amp;doc_name=10825-8.txt HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjMwNzIwMzAyLCJqdGkiOiJjNTM4OTIwOC1lZjEzLTQxZGQtOGM3MS1iMjVhYWYyYTQ3OTMiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoidGVzdCIsIm5iZiI6MTYzMDcyMDMwMiwiZXhwIjoxNjMwNzIxMjAyfQ.iXip9s7hJJ_MLBvJ3Hd63pp2kIHdl_VF73lWF0KxOd0
Cache-Control: no-cache
Postman-Token: e54f1b32-924d-61a1-88c1-9d0e54aa5cb5
```

La URL /login es la que nos brinda el token necesario para poder utilizar el sitio.
Se accede mediante la URL http://127.0.0.1:5000/login, se deben utilizar el método POST, pasándole los parámetros username y password.
```bash
POST /login HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json
Cache-Control: no-cache
Postman-Token: c0f80b5f-88f6-2ca9-090a-807aef99615a

{
"username": "test",
"password": "test"
}
```
La URL de Importar TXT http://127.0.0.1:5000/import_txt también posee seguridad mediante Token.
(debe obtenerse un Token activo para ejecutar dicho proceso)
```bash
GET /import_txt HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjMwNzIwMzAyLCJqdGkiOiJjNTM4OTIwOC1lZjEzLTQxZGQtOGM3MS1iMjVhYWYyYTQ3OTMiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoidGVzdCIsIm5iZiI6MTYzMDcyMDMwMiwiZXhwIjoxNjMwNzIxMjAyfQ.iXip9s7hJJ_MLBvJ3Hd63pp2kIHdl_VF73lWF0KxOd0
Cache-Control: no-cache
Postman-Token: b447299c-0f3b-4bfa-4608-32f569f07eae
```
Todas estas URLs se puede testear con [postman.com](https://www.postman.com/downloads/)

## Funciones Principales Python
A continuación describimos las funciones.

|Funciones|Descripción|Archivo|Nivel|
|----|-----|-----|-----|
|import_txt|inicia el proceso de lectura de archivos .txt del directorio ..\downloads |[app.py]| Principal |
|importfiles_toDB|realizar la lectura los archivos .txt, invocando a funciones secundarias como listfiles, InsertFilestoMongo |[importtxt.py]| Principal|
|listfiles|lectura de todo el contenido del directorio \downloads|[importtxt.py]|Secundaria|
|InsertFilestoMongo|recibe el listado de archivos .txt , abre el contenido, llava a la función get_database e inserta / actualiza la base de datos con los archivos .txt |[importtxt.py]|Secundaria|
|get_database|parametriza e instancia la conexión con la base de datos|[model.py]|Secundaria|
|count_words|inicia la URL /api/docs, toma los parámetros recibidos en el query string, valida lo recibo y separa los parametros term y doc_name. También invoca a la función querymongo |[app.py]| Principal |
|querymongo|mediante los parámetros term y doc_name, solicita la collation, valida que exista el nombre .txt en MongoDB. Luego trae el campo contents con el texto y finalmente busca en el string el "term" cuantas veces aparece (frecuencia) |[getdata.py]|Secundaria|
|string_cleanup|elimina del string caracteres especiales .#¡!¿?()/@%$; |[getdata.py]|Secundaria|

### Actualización
|Funciones|Descripción|Archivo|Nivel|
|----|-----|-----|-----|
|Frecuency_Words_MongoDB|mediante los parámetros term y doc_name, se conecta a MongoDB, con la la opción Aggregation MongoDB para contar término dentro del documento parámetro (doc_name). También hace un de Regex (expresiones regulares) para omitir caracteres especiales, acentos, comillas y guiones|[getdata.py]|Secundaria|
|contar_palabra|mediante los parámetros term y doc_name, valida que exista el nombre .txt en MongoDB. Al buscar el término dentro del campo contents lo hace mediante translate (para quitar caracteres especiales y re.findall para encontrar el término parámetro|[getdata.py]|Secundaria|

## Instalación
A continuación describimos los pasos de instalación.

1. `Phyton version 3.6.9` (Descargar [Python](https://www.python.org/) del sitio oficial.)
2. `Instalar Python` (se recomienda seleccionar la opción "Customize installation", **quitar** td/tk and idle, Python test suite y en opciones avanzadas **"Add path Python to environment variables"**)
3. `mkdir c:\Git\melidocs` crear un directorio donde se va a trabajar con el proyecto.
4. `cd c:\Git\melidocs` ingresar al directorio vacio del proyecto (abrir línea de comando luego de la instalación de Python)
5. `pip install virtualenv` instalación del entorno virtual
6. `virtualenv venv` Se configura el entorno virtual en el directorio del proyecto
7. `.\venv\Scripts\activate` Activar el modo virtual
8. `c:\Git\melidocs\requirements.txt` descargar el archivo **requirements.txt** en el directorio raíz del proyecto. El mismo contiene todas las librerías necesarias para realizar la implementación.
8. `c:\Git\melidocs&gt;pip install -r requirements.txt` Instalamos en el entorno virtual las librerías a utilizar (flask y pymongo)
9. Para iniciar el servicio, setear las variables de entorno:
+ Ingresar al directorio del proyecto c:\Git\melidocs
+ $env:FLASK_APP = "app"
+ $env:FLASK_ENV = "development"
+ flask run

(FLASK_APP="app" FLASK_ENV="development"solo para Windows)

### Instalación de MongoDB
Descargar la versión Community del sitio oficial [MongoDB](https://www.mongodb.com/try/download/community).

+ a. version 4.4.8
+ b. zip
+ c. windows

Crear un directorio donde se va a dejar el motor MongoDB, ejemplo `c:\mongodb\4.4\bin`. Crear directorios por default donde se crearan las bases de datos `c:\data\db\`
Crear y configurar archivo `mongod.cfg` en el directorio de instalación de MongoDB `c:\mongodb\4.4\bin`:
```bash
#network interfaces
net:
port: 27017
bindIp: 127.0.0.1

security:
authorization: enabled
```
- **port** 27017 es el puerto por defecto de MongoDB.
- **bindIP** es la dirección IP por la que atenderá las peticiones el demonio MongoDB.
- **security authorization** indica que está activa la configuración de seguridad básica.

Se debe crear una cuenta de MongoDB, como admin la cual es el root del motor, se debe resguardar de forma segura:
```bash
C:\mongodb\4.4\bin&gt;mongo --eval "db.createUser({user:'mongoadmin',pwd:'Xi467234.QRTexv1',roles:[{db:'admin',role:'root'}]})" admin

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
Iniciar el motor mongodb, desde una línea de comando:
```bash 
C:\mongodb\4.4\bin&gt;mongod.exe
```

## Database-drivers
*Librarías para conectar y gestionar bases de datos.*
* NoSQL Databases
* [pymongo](https://github.com/mongodb/mongo-python-driver) - Cliente Python oficial para MongoDB.

## Web-Frameworks
*Librarías para la gestión del framework.*
- [Flask](http://flask.pocoo.org/) - microframework de Python.
- `jsonify, request, render_template, flash, url_for`
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/installation/) - librería Python para manejo de Json Web Token.
### Librerías-estándar
- `datetime`
- `re`
- `os`
- `unicodedata`
- `jwt`
- `functools import wraps`

Archivos Python y librarías:
- `app.py' es el root de la aplicación, es la que genera todas las URLs que utiliza la aplicación.
- `getdata.py` contiene las funciones para contar la frecuencia de los términos.
- `getdata.py` contiene las funciones para importar los archivos .txt del directorio downloads.
- `.gitignore` directorios ignorados a sincronizar en github.
- `.README.md` documentación del proyecto
- `model.py` posee la conexión con MongoDB, incluye el string de conexión con la base.
- `requirements.txt` contiene todos los paquetes Pyhton dependencias para instalar con `pip`

### Seguridad implementada
Se hizo uso de la librería Pyhton Flask-JWT-Extended para la generación de Token, a laa URL /login (modo prueba username=test, password=test). Dicho Token es requerido para acceder a las URLs de la aplicación /import_txt y /api/docs.
![](https://github.com/cadupar20/melidocs/blob/main/2021-09-06_125003.jpg)

El cliente hace una petición POST enviando en mensaje Json el usuario y contraseña, y realiza el proceso de autenticación. Se comprueba usuario y contraseña, de ser válidos, generar el token JWT para devolverlo al usuario access_token dentro de un mensaje Json.

A partir de ahí utilizando ese token, accede a las URLs de la aplicación, siempre que ese token JWT dentro de un encabezado, Authorization: Bearer XXXXXXX, siendo Bearer el tipo de prefijo seguido de todo el contenido del token.

Para este prototipo no se usó una autenticación externa (identity) sino que dentro del código de la función tokenlogin_access se validan los datos recibidos en el mensaje Json request.json.get("username", None) / password = request.json.get("password", None).

Cada URL que se quiere proteger, se hizo uso de la función @jwt_required(), la cual invoca a la librería mencionada de Python y le solicita el Token generdo durante la autenticación. Si el request no lo posee dentro del header del mensaje, no se podrá seguir ejecutando el resto de la función (ya sea lectura de datos o importación de archivos).

### Comando para descargar el proyecto, en Github (dentro de la carpeta c:\git o en su directorio seleccionado)
```bash
git clone https://github.com/cadupar20/melidocs.git
```
## Licencia

Este proyecto es open source, puede ser utilizado y compartido libremente.

## Referencias
- [Python](https://www.python.org/)
- [Flask](http://flask.pocoo.org)
- [Pymongo](https://github.com/mongodb/mongo-python-driver)
- [MongoDB](https://www.mongodb.com/try/download/community)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/installation/)
- [JWT](https://openwebinars.net/blog/que-es-json-web-token-y-como-funciona/)
- [Re](https://docs.python.org/3/library/re.html/)
- [Pymongo Aggregation with BSON](https://pymongo.readthedocs.io/en/stable/examples/aggregation.html)

## Implementación en servicio Cloud

La arquitectura del proyecto en la nube está diseñada basándose en servicios de Azure, pero puede ser desplegada en AWS o GC.

![](https://raw.githubusercontent.com/cadupar20/melidocs/main/2021-09-02_233347.png)

### Componentes para Alta Disponibilidad y Escalabilidad del proyecto

|Componente|Ubicación|Descripción|Resource Group|Alta Disponibilidad|Escalabilidad|
| ------------ | ------------ |------------ |------------ |------------ |------------ |
|Resource Group A|Región A|Ubicación lógica de los objetos a crear|NA|NA|NA|
|Resource Group B|Región B|Ubicación lógica de los objetos a crear|NA|NA|NA|
|Azure Front Door|Región A|Balanceador de tráfico HTTPS activo/pasivo, A|NA|NA|
|Service Plan A|Región A|Hardware donde consume procesador/cpu el Web app.|A|NA|Vertical Horizontal|
|Service Plan B|Región B|Hardware donde consume procesador/cpu el Web app.|B|NA|Vertical Horizontal|
|Web App Service A|Región A|Web app basada en linux e, interprete Python, donde se despliega el código Python, se instalan las librerías requerimients.txt|A|Web App A|Depende del Service Plan|
|Web App Service B|Región B|Web app basada en linux e interprete Python, donde se despliega el código Python, se instalan las librerías requerimients.txt|B|Web App B|Depende del Service Plan|
|Atlas DB (Mongo)|SaaS|Es el servicio de Mongo DB para Cloud, tipo Saas ofrece réplica en mltiples regiones|Database|Mínimo 3 nodos|SI|

+ Regiones: Son las ubicaciones de los servicios Cloud. La propuesta está pensada en al menos 2 regiones (donde debe tenerse presente la latencia entre los clientes y los servicios HTTPS/MongoDB. En este caso región "A" puede ser EAST US y región "B" EAST US 2.
https://www.azurespeed.com/Information/AzureRegions (regiones posibles a seleccionar)
También puede evaluarse las availavility zone de cada región (en el caso de que las tenga), algunas regiones lo tienen e implica que tiene varios Datacenter como un servicio mayor alta disponibilidad para los servicios de Azure.
+ Azure Front Door: es la propuesta como balanceador de carga para enrutar el tráfico HTTPS, definiendo región prioritaria A y región secundaria B. También maneja métodos de afinidad por sesión y prioridad de lista de servidores. Este servicio de Azure también nos brinda Application Gateway y Applicacion Firewall para garantizar vulnerabilidades conocidas. El componente front end de acceso a los usuarios y detrás tendrá los 2 Web Apps brindando un servicio balanceado HTTPS.
+ Service Plans: Es el componente que nos da los recursos de memoria y cpu necesario para ejecutar nuestra aplicación Python, se puede basar en Windows o en Linux. En este caso se definieron tener (2) Service Plans, en regiones distintas. Tenemos 2 formas de escalar cada uno de ellos, verticalmente y horizontalmente. Verticalmente es mediante modelos serie P, serie S o serie PxV. En el caso de entornos no crítico podemos usar los modelos F1, D1 o B1. El otro modo de escalar es horizontalmente, donde en este caso se definen la cantidad de instancias (manual o automático). El escalar horizontalmente en forma automático tiene variantes como ser mínimo, máximo, predeterminado y de qué modo se escala basándose en métricas de carga por uso de CPU o basado en número de instancias.
+ Web App: Tiene el código de mi aplicación, el intérprete Python y sus requerimientos. Soporta PHP, Java, .NET, Python, Ruby, etc.!
+ Atlas DB (SaaS): es el servicio de MongoDB en la nube, puede ser contratado a traves de los distintos provedores (AWS, Azure, GC o directo a Mongo). Soportado en Cluster Multi-Región y también Multi-Cloud, en este caso se piensa en Azure distribuyendo los 2 nodos en una región y 1 nodo en una región distinta. [cluster-multi-región](https://docs.atlas.mongodb.com/cluster-config/multi-cloud-distribution/#std-label-create-cluster-multi-region)
