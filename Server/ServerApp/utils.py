from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import timedelta

def crear_evento_google_calendar(reunion):
    creds = Credentials.from_authorized_user_file('credentials.json')  # Ruta al archivo de credenciales
    service = build('calendar', 'v3', credentials=creds)
    evento = {
        'summary': reunion.titulo,
        'description': reunion.descripcion,
        'start': {
            'dateTime': reunion.fecha.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': (reunion.fecha + timedelta(hours=1)).isoformat(),
            'timeZone': 'UTC',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': f"{reunion.id}-meet",
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                },
            },
        },
    }
    evento_creado = service.events().insert(calendarId='primary', body=evento, conferenceDataVersion=1).execute()
    reunion.enlace = evento_creado['hangoutLink']
    reunion.save()