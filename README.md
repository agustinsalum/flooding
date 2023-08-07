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

1. Instalar bases de datos: instalar mysql server y mysql workbench.

1. Crea el archivo: En la raíz de tu proyecto, crea un archivo llamado '.env'.

2. Define las variables de entorno: Dentro del archivo '.env', define las variables de entorno necesarias para tu proyecto. Cada variable se define en una línea separada y sigue el formato NOMBRE=VALOR. En este caso:

```
DB_HOST=mi_host
DB_PORT=mi_port
DB_USER=mi_user
DB_PASS=mi_pass
DB_NAME=mi_name_db
FLASK_ENV=development
FLASK_DEBUG=1
```

## Entorno virtual: virtualenv

Virtualenv es una herramienta para manejar versiones. La idea de usar este tipo de herramientas son:

* Instalar prácticamente cualquier versión de Python (o del lenguaje que sea)
* Permitir tener instaladas múltiples versiones

Como paso previo, debemos instalar las dependencias necesarias:

Actualizamos e instalamos dependencias necesarias:

```
sudo apt-get update;
```

```
sudo apt-get install make build-essential libssl-dev zlib1g-dev \ libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \ libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

Instalamos pyenv:

```
mkdir $HOME/.pyenv
```

```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
```

```
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
```

```
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
```

Por último:

```
exec “$SHELL”
```

```
pyenv install --list // nos muestra la lista de versiones para instalar
```

```
pyenv install 3.x.x // version preferida
```

```
pyenv versions // nos muestra las versiones instaladas y la del sistema
```

```
pyenv global 3.x.x
```

Verificamos:

```
python
```

## Crear un entorno virtual

Nos tenemos que asegurar que pip apunta a pyenv y ver que pip pertenece a la versión de Python que acabas de seleccionar como global:

```
pyenv global 3.x.x
```

Nos paramos en nuestro proyecto y tecleamos python --version. Debería aparecer la versión de python elegida. Ahora vamos a crear un directorio virtual llamado venv para la versión de Python que hayamos configurado como global:

```
pip install virtualenv
```

```
virtualenv -p python venv
```

## Como usar el entorno virtual

Para activar el entorno ejecutamos:

```
source venv/bin/activate
```

Es necesario desactivar si queremos volver a usar el Python que instalamos
globalmente:

```
deactivate
```

## Pasos para usar el proyecto


1. Clonamos el repositorio

```
git clone git@github.com:agustinsalum/flooding.git
```

2. Acceder a la carpeta clonada

```
cd flooding
```

3. Instalar las dependencias

```
pip install -r requirements.txt
```

Asegurese de activar el entorno virtual antes de instalar las dependencias. En caso de error en la dependencia "psycopg2" se soluciona con "sudo apt install libpq-dev build-essential"


## Iniciar el proyecto

Una vez realizada la configuracion e instalado el entorno virtual podemos iniciar el proyecto. Para iniciar el proyecto solamente debe ingresar en la terminal:

```
flask run
```

Le debera aparecer el mensaje 'Debug mode: on' y una advertencia de produccion. Tenga en cuenta que la primera vez puede tardar, ya que se esta creando la base de datos, las tablas y los atributos correspondientes. 


