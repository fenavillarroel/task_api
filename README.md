## Simple API manejador de tareas

Simple API para administrar tareas
Escrito en Python utilizando el Framework FastAPI

### Dependencias

- Python 3.10+
- PostgreSQL Client
- Docker Engine

Docker Engine no es una dependencia excluyente si es que ya cuentas con PostgreSQL instalado o corriendo en algún host local o de tu red LAN.
La menciono ya que es la forma más simple de levantar un servidor de base de datos local de manera rapida.

### Configuracion de la Base de Datos

En mi caso levante una instancia de PostgreSQL versión 14.9 usando Docker

```
docker pull postgres:14.9
```

Luego levantamos una instancia de Postrgres desde docker

```
docker run --name some-postgres -e POSTGRES_HOST_AUTH_METHOD=trust -p 5432:5432 -d postgres:14.9
```

Luego creamos la base de datos tasks conectandonos al contenedor docker usando postgres client (Si tienes un administrador grafico como PgAdmin genial)

```
psql -h 127.0.0.1 -p 5432 -U postgres
```

Una ves en la cli de Postgres creamos la base de datos y nos desconectamos del motor Postgres

```
create database tasks;
\q
```

### Configuracion de la APP FastAPI

Nos descargamos la APP desde Github

```
git clone https://github.com/fenavillarroel/task_api.git
```

Luego nos movemos al directorio task_api y ejecutamos los siguientes comandos

```
cd task_api
pip install -r requirements.txt
mv env.example .env
```

Finalmente levantamos la APP ejecutando el siguiente comando

```
uvicorn app:app --reload --host 0.0.0.0
```

Si no ves ningún ya tendras la APP ejecutadose en tu localhost y podrás acceder a su documentación visitando la siguiente URL:

```
http://127.0.0.1:8000/docs
```

![api](./images/api.png)


### Probando la API

Lo primero que se debe hacer es crear un usuario, para ello se debe usar el endpoint Create User

![user](./images/create_user.png)

Luego para consumir los distintos endpoints de tareas te debes autentificar con el usuario recien creado.

Existen dos alternativas para ello:

La primera es usar el endpoint Auth, pasandole solo el username y password.
Este endpoint te servira para autentificar usando un cliente externo como alguna APP Front End, curl, Postman, etc.
Este endpoint te retornará un Token que debes usar desde alguno de los clientes externos antes mencionados.

![auth](./images/auth.png)

![auth](./images/token.png)

![auth](./images/get_tasks.png)

La segunda alternativa para autentificar es haciendo click sobre cualquiera de los candados que aparecen en el costado derecho como abiertos lo que desplegara un formulario para que ingreses tu usuario y contraseña recien creados.
Esta opción te permitira usar esta documentación para probar directamente los endponits.
Observaras que luego de autentificar exitosamente desde el formulario (pinchando en alguno de los candados) los candados aparecerán como cerrados lo que indica que ya estas autentificado y listo para probar los endpoints directamente

![auth](./images/candados.png)

![auth](./images/form.png)

![auth](./images/cerrados.png)


Y eso es todo ya puedes consumir la API Tareas.

Se proporciona un Dockerfile en caso que necesites hacer un despligue en un cluster de Kubernetes.