# EstiloAgenda — Sistema de Gestión de Citas para Salón / Barbería

Prototipo web desarrollado en **Python**, **SQLite** y **Django** para la gestión integral de citas de un salón de belleza o barbería. Permite registrar clientes, agendar citas asociadas a un catálogo de servicios, controlar el flujo de estados de atención (*Pendiente*, *Confirmada*, *Completada* y *Cancelada*), filtrar registros y eliminar citas.

---

## Requisitos previos

Para ejecutar este proyecto en una computadora local necesitas tener instalado:

1. **Python 3.10 o superior** (incluye `sqlite3` de forma nativa).
   - En Windows, asegúrate de marcar la opción **"Add Python to PATH"** durante la instalación.
2. **Git** (opcional, para clonar el repositorio; también se puede descargar como archivo `.zip` desde GitHub).
3. **Navegador web** moderno (Chrome, Edge, Firefox, etc.).

---

## Instalación y ejecución paso a paso

### 1. Clonar el repositorio

Abre una terminal (PowerShell, CMD o terminal de VS Code) y ejecuta:

```bash

1. Obtener el código fuente
Clona el repositorio desde GitHub y entra a la carpeta del proyecto:
git clone https://github.com/FrxKxxL/Agenda-Barberia

(Si descargaste el repositorio en formato ZIP, descomprímelo y abre una terminal dentro de la carpeta raíz donde se encuentra manage.py).
2. Crear y activar un entorno virtual
En Windows (PowerShell):
python -m venv .venv
.venv\Scripts\activate

(Si PowerShell bloquea la ejecución de scripts por políticas locales, ejecuta primero Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned y vuelve a activar .venv\Scripts\activate).

En Linux / macOS:

python3 -m venv .venv
source .venv/bin/activate

3. Instalar Django

Con el entorno virtual activado, instala Django:
pip install django

4. Ejecutar el servidor de desarrollo
Inicia el servidor local de Django:

python manage.py runserver

5. Abrir la aplicación en el navegador
Ingresa a la siguiente dirección en tu navegador web:

http://127.0.0.1:8000/



utilizando estrictamente y obligatoriamente este formato
