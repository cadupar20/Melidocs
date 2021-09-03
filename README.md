# [Proyecto Frecuencia de Palabras y Proceso *.txt en Mongo]

**El proyecto** esta basado en codigo python, utilizando diversas librerias y en el framework Flask .

Se utilizó el framework de **[Bootstrap](https://getbootstrap.com/)** para el uso amigable de las URLs.

El proyecto consta de varias URLS a mencionar:
- / (home o root): acceso al home del sitio
- /importtxt: pre-proceso de importación de archivos de text (extension .txt)
- /api/docs/: API para contar la frecuencia de 1 palabra de acuerdo a los parametro.
- /login: URL para autenticación, genera un token para el manejo de seguridad de la sesión.

Cabe mencionar que la interface /api/docs maneja 2 parametros:
```bash
term = debe tener como valor una palabra o numero a buscar ( no debe incluir espacios)
doc_name = nombre del documento donde se desea buscar/contar la palabra. El nombre ingresado puede o no incluir la extensión .txt al final del parametro.
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
|import_txt|inicia el proceso de lectura de archivos .txt del directorio ..\downloads |[app.py]| Principal |
|importfiles_toDB|realizar la lectura los archivos .txt, invocando a funciones secundarias como listfiles, InsertFilestoMongo |[importtxt.py]| Principal|
|listfiles|lectura de todo el contenido del directorio \downloads|[importtxt.py]|Secundaria|
|InsertFilestoMongo|recibe el listado de archivos .txt , abre el contenido, llava a la funcion get_database e inserta / actualiza la bse de datos con los los archivos .txt |[importtxt.py]|Secundaria|
|get_database|parametriza e instancia la conexión con la base de datos|[model.py]|Secundaria|
|count_words|inicia la URL /api/docs, toma los parametros recibidos en el query string, valida lo recibo y separa los parametros term y doc_name. Tambien invoca a la funcion querymongo |[app.py]| Principal |
|querymongo|mediante los parametros term y doc_name, solicita la collation, valida que exista el .txt en MongoDB. Luego trae el campo contents con el texto y finalmente busca en el string el "term" cuantas veces aparece (frecuencia) |[getdata.py]|Secundaria|
|string_cleanup|elimina del string caracteres especiales .#¡!¿?()/@%$;  |[getdata.py]|Secundaria|


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
Descargar la versión Community del sitio oficial [MongoDB](https://www.mongodb.com/try/download/community).

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

Se debe crear una cuenta de MongoDB, como admin la cual es el root del motor, se debe resguardar de forma segura:
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

## Database-drivers
*Librarias para conectar y gestionar bases de datos.*
* NoSQL Databases
	* [pymongo](https://github.com/mongodb/mongo-python-driver) - Cliente Python oficial para MongoDB.

## Web-Frameworks
*Librarias para la gestion del framework.*
- [Flask](http://flask.pocoo.org/) - A microframework for Python.
- `jsonify, request, render_template, flash, url_for`
### Librerias-estandar
- `datetime`
- `re`
- `os`
- `unicodedata`
- `jwt`
- `functools import wraps`

Archivos Python y librarias:
- `app.py` es el root  de la aplicación, es la que genera todas las URLs que utiliza la aplicación.
- `.gitignore` directorios ignorados a sincronizar en github
- `.README.md` documentación del proyecto
- `model.py` posee la conexión con MongoDB, incluye el string de conexión con la base.
- `requirements.txt` contiene todos los paquetes Pyhton dependencias para instalar con `pip`


### Comando para descargar el proyecto, en Github (dentro de la carpeta c:\git o en su directorio seleccionado)
```bash
git clone https://github.com/cadupar20/melidocs.git
```
## Browser soportado

| [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/edge/edge_48x48.png" alt="IE / Edge" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)<br/>Edge | 
| --------- |
| last version Edge| 

## Licencia

Este proyecto es open source, puede ser utilizado y compartido libremente.

## Referencias
- [Python](https://www.python.org/)
- [Flask](http://flask.pocoo.org)
- [Pymongo](https://github.com/mongodb/mongo-python-driver)
- [MongoDB](https://www.mongodb.com/try/download/community)

## Implementación en servicio Cloud

La arquitectura del proyecto en la nube está diseñada en base a servicios de Azure, pero puede ser deplegada en AWS o GC.

![](https://raw.githubusercontent.com/cadupar20/melidocs/main/2021-09-02_233347.png)

### Componentes para Alta Disponibilidad y Escalabilidad del proyecto

|Componente|Ubicación|Descripción|Resource Group|Alta Disponibilidad|Escalabilidad|
| ------------ | ------------ |------------ |------------ |------------ |------------ |
|Resource Group A|Región A|Ubicación lógica de los objetos a crear|NA|NA|NA|
|Resource Group B|Región B|Ubicación lógica de los objetos a crear|NA|NA|NA|
|Azure Front Door|Región A|Balanceador de trafico HTTPS activo/pasivo, 	A|NA|NA|
|Service Plan A|Región A|Hardware donde consume procesador/cpu		el Web app.|A|NA|Vertical		Horizontal|
|Service Plan B|Región B|Hardware donde consume procesador/cpu		el Web app.|B|NA|Vertical		Horizontal|
|Web App Service A|Región A|Web app basada en linux e interprete Python, donde se despliega el código Python, se instalan las librerías requerimients.txt|A|Web App A|Depende del Service Plan|
|Web App Service B|Región B|Web app basada en linux e interprete Python, donde se despliegael código Python, se instalan las librerías requerimients.txt|B|Web App B|Depende del Service Plan|
|Atlas DB (Mongo)|SaaS|Es el servicio de Mongo DB para Cloud, tipo Saas ofrece replica en mltiples regiones|Database|Mínimo 3 nodos|SI|

	• Regiones: Son las ubicaciones de los servicios Cloud. La propuesta está pensada en al menos 2 regiones (donde debe tenerse presente la latencia entre los clientes y los servicios HTTPS/MongoDB. En este caso región "A" puede ser EAST US y región "B" EAST US 2.
	https://www.azurespeed.com/Information/AzureRegions (regiones posibles a seleccionar)
	También puede evaluarse las availavility zone de cada región (en el caso de que las tenga), algunas regiones lo tienen e  implica que tiene varios Datacenter como un servicio mayor alta disponibilidad para los servicios de Azure.
	• Azure Front Door: es la propuesta como balanceador de carga para enturar el tráfico HTTPS, definiendo región prioritaria A y región secundaria B. También maneja métodos de afinidad por sesión y prioridad de lista de servidores. Este servicio de Azure también nos brinda Application Gateway y Applicacion Firewall para garantizar vulnerabilidades conocidas. El componente front end de acceso a los usuarios y detrás tendrá los 2 Web Apps brindando un servicio balanceado HTTPS.
	• Service Plans: Es el componente que nos da los recursos de memoria y cpu necesario para ejecutar nuestra aplicación Python, se puede basar en Windows o en Linux. En este caso se definieron tener (2) Service Plans, en regiones distintas. Tenemos 2 formas de escalar cada uno de ellos, verticalmente y horizontalmente. Verticalmente es mediante modelos serie P, serie S o serie PxV. En el caso de entornos no critico podemos usar los modelos F1, D1 o B1.  El otro modo de escalar es horizontalmente, donde en este caso se definen la cantidad de instancias (manual o automático). El escalar horizontalmente en forma automático tiene variantes como ser mínimo, máximo, predeterminado y de qué modo se escala basándose en métricas de carga por uso de CPU o basado en número de instancias.
	• Web App: Tiene el código de mi aplicación, el intérprete Python y sus requerimientos. Soporta PHP, Java, .NET, Python, Ruby, etc.![image](https://user-images.githubusercontent.com/83100373/131996881-16455c4d-7dfd-4647-84ef-0656226a079a.png)
	• Atlas DB (SaaS): es el servicio de MongoDB en la nube, puede ser contratado a traves de los distintos provedores (AWS, Azure, GC o directo a Mongo). Soportado en Cluster Multi-Region y tambien Multi-Cloud, en este caso de piensa en Azure distribuyendo los 2 nodos en una región y 1 nodo en una región distinta. ![cluster-multi-region](https://docs.atlas.mongodb.com/cluster-config/multi-cloud-distribution/#std-label-create-cluster-multi-region)
