# flooding

## Introduccion

Se debe crear una aplicacion que permita conocer y gestionar zonas con peligro de inundación y las acciones a llevar a cabo. Se debe enfocar en el desarrollo de un prototipo que brinde información a los
y las habitantes de la ciudad de La Plata sobre:
- zonas inundables de la ciudad;
- puntos de encuentro en caso de una emergencia;
- recorridos de evacuación.

También se podrán realizar denuncias respecto a alcantarillas tapadas, basurales.

## Objetivo

Se implementarán dos aplicaciones que permitirán gestionar y brindar la información mencionada. Por un lado, se desarrollará una aplicación privada que potencialmente proveerá la siguiente funcionalidad:
- Gestión de usuarios del sistema.
- Mantener opciones de configuración del sistema
- Gestión de las zonas inundables.
- Gestión de puntos de encuentro establecidos por el municipio.
- Procesamiento de las denuncias realizadas.

También se desarrollará una aplicación pública, que permitirá visualizar la información de interés para los y las ciudadanos/as. A través de esta aplicación se podrá:
- Visualizar zonas inundables.
- Ubicar los puntos de encuentro, que son establecidos por el municipio, pudiendo mostrar los más próximos a la ubicación del usuario.
- Realizar denuncias sobre: alcantarillas tapadas y basurales. También se pueden pensar en otros tipos de denuncias que pueden ser de inteŕes para la aplicación.
- Visualizar recorrido de evacuación de acuerdo a la ubicación del usuario.

## Configuracion

El archivo '.env' es un archivo de configuración que se utiliza para almacenar variables de entorno en tu proyecto. Las variables de entorno son valores que se utilizan para configurar y personalizar la aplicación sin tener que codificar valores directamente en el código fuente. Esto proporciona una mayor seguridad y flexibilidad, ya que puedes cambiar la configuración sin necesidad de modificar el código. Los pasos son los siguentes:

1. Crea el archivo: En la raíz de tu proyecto, crea un archivo llamado .env.

2. Define las variables de entorno: Dentro del archivo .env, define las variables de entorno necesarias para tu proyecto. Cada variable se define en una línea separada y sigue el formato NOMBRE=VALOR. Por ejemplo:

```
DB_HOST=mi_host
DB_PORT=mi_port
DB_USER=mi_user
DB_PASS=mi_pass
DB_NAME=mi_name_db
FLASK_ENV=development
FLASK_DEBUG=1
```

## Iniciar el proyecto

Para iniciar el proyecto solamente debe ingresar en la terminal:

```
flask run
```

Le debera aparecer el mensaje 'Debug mode: on' y una advertencia de produccion. Tenga en cuenta que la primera vez puede tardar, ya que se esta creando la base de datos, las tablas y los atributos correspondientes. 


