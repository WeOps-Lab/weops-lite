
from django.conf import settings
from keycloak import KeycloakOpenID


def get_open_client():
    client = KeycloakOpenID(
        server_url=f'http://{settings.KEYCLOAK_SETTINGS["HOST"]}:{settings.KEYCLOAK_SETTINGS["PORT"]}/',
        client_id=f'{settings.KEYCLOAK_SETTINGS["CLIENT_ID"]}',
        realm_name=f'{settings.KEYCLOAK_SETTINGS["REALM_NAME"]}',
        client_secret_key=f'{settings.KEYCLOAK_SETTINGS["CLIENT_SECRET_KEY"]}')
    return client

