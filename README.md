# Care4U Hub

Care4U Hub is an innovative IoT system designed to ensure the safety, well-being, and connection of elderly individuals living independently. With features such as fall detection, activity monitoring, and seamless communication, it allows families and caregivers to provide proactive and comprehensive care.

## Features
- **Easy Communication**: Facilitates video calls to strengthen connection with loved ones.
- **Safe Home Environment**: Monitors environmental factors like temperature and smoke levels.
- **Interactive Dashboard**: Centralizes key system information with customizable widgets.
- **Light exposure**: Monitors how much light the person is exposed to.
  
## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Django (with FullCalendar integration)
- **Programming Language**: Python
- **Database**: PostgreSQL
- **Third-Party Libraries**: 
  - FullCalendar.js for event and schedule management.
    
## Installation
Follow these steps to install and run the project locally:

1. Clone this repository:
   ```bash
   https://github.com/MiguelAchaD/IoT
   cd care4u-hub
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database:
   ```bash
   python manage.py migrate
   ```
4. Start the development server:  
   ```bash
   python manage.py runserver
   ```
5. Access the application at http://127.0.0.1:8000.

## Usage
- **Calendar Management**: Schedule and manage patient-related events from the calendar page.
- **Patient Management**: View, edit, and manage patient details from the respective page.
- **Home Panel**: Access an overview of the system's functionalities with user-friendly navigation.
- **Dashboard**: Displays the following
                **Patient Information**: Shows details like patient name and age, with the option to update data via an interactive icon.
                **Customizable Widgets**:
                  **Current Weather**: Provides real-time weather information.
                  **Weather Forecast**: Offers weather predictions to help plan activities.
                **Notifications**: Indicates when no data is available on the dashboard, maintaining a clear user experience.
-**Navbar**: Defines the main navigation bar with links to home, patients, and profile pages. Linked to its corresponding CSS file.

-**Contact**: Template for the contact page that includes a form for inquiries and feedback with success or error messages.

-**Profile**: Allows users to manage their profile, including personal information updates and logging out.

## Contribution
Contributions are welcome. Please submit a pull request or create an issue to share your ideas or feedback.

## License
[License MIT](LICENSE)
