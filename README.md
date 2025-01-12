# Care4U Hub

Care4U Hub es un innovador sistema IoT diseñado para garantizar la seguridad, el bienestar y la conexión de los adultos mayores que viven de forma independiente. Con funciones como detección de caídas, monitoreo de actividades y comunicación fluida, permite a las familias y cuidadores brindar una atención proactiva y completa.

## Características
- **Detección de Caídas**: Detecta caídas al instante y envía alertas a cuidadores y servicios de emergencia.
- **Monitoreo de Actividades**: Realiza un seguimiento de las rutinas diarias y detecta irregularidades.
- **Fácil Comunicación**: Facilita videollamadas para fortalecer la conexión con los seres queridos.
- **Entorno Seguro en el Hogar**: Supervisa factores ambientales como temperatura y niveles de humo.
- **Dashboard Interactivo**: Centraliza la información clave del sistema con widgets personalizables.
  
## Tecnologías Utilizadas
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Django (con integración de FullCalendar)
- **Lenguaje de Programación**: Python
- **Base de Datos**: PostgreSQL
- **Librerías de Terceros**: 
  - FullCalendar.js para gestión de eventos y horarios.

## Instalación
Sigue estos pasos para instalar y ejecutar el proyecto localmente:

1. Clona este repositorio:
   ```bash
   https://github.com/MiguelAchaD/IoT
   cd care4u-hub
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura la base de datos:
   ```bash
   python manage.py migrate
   ```
4. Inicia el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```
5. Accede a la aplicación en `http://127.0.0.1:8000`.

## Uso
- **Gestión del Calendario**: Programa y administra eventos relacionados con pacientes desde la página de calendario.
- **Gestión de Pacientes**: Visualiza, edita y administra los detalles de los pacientes desde la página correspondiente.
- **Panel de Inicio**: Accede a una vista general de las funcionalidades del sistema con una navegación amigable.
- **Dashboard**: Se ve lo siguiente
                **Información del Paciente**: Muestra detalles del paciente como nombre y edad, con la opción de actualizar datos mediante un ícono interactivo.
                **Widgets Personalizables**:
                  **Clima Actual**: Proporciona información en tiempo real sobre el clima.
                  **Pronóstico del Clima**: Ofrece previsiones meteorológicas para ayudar en la planificación de actividades.
                **Notificaciones**: Indica cuando no hay datos disponibles en el dashboard, manteniendo una experiencia clara para el usuario.
-**Navbar**: Define la barra de navegación principal con enlaces a las páginas de inicio, pacientes y perfil. Ligado a su archivo CSS correspondiente.

-**Contact**: Plantilla para la página de contacto que incluye un formulario para consultas y retroalimentación con mensajes de éxito o error.

-**Profile**: Permite gestionar el perfil del usuario, incluyendo cambios en información personal y cierre de sesión.

## Contribución
Las contribuciones son bienvenidas. Por favor, envía un pull request o crea un issue para compartir tus ideas o feedback.

## Licencia
[Licencia MIT](LICENSE)
