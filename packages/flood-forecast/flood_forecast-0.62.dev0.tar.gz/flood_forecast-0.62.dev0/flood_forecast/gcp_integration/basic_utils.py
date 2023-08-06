from google.cloud import storage
import os


def get_storage_client() -> storage.Client:
    """
    Utility function to return a properly authenticated GCS
    storage client whether working in Colab, CircleCI, or other environment.
    """
    try:
        # GOOGLE_APPLICATION_CREDENTIALS must be set
        return storage.Client()
    except BaseException:
        if os.environ["ENVIRONMENT_GCP"] == "CircleCI":
            creds = create_file_environ()
            return storage.Client(credentials=creds, project=os.environ["GCP_PROJECT"])
        elif os.environ["ENVIRONMENT_GCP"] == "Colab":
            return storage.Client(project=os.environ["GCP_PROJECT"])


def upload_file(bucket_name: str, file_name: str, upload_name: str, client: storage.Client):
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_filename(upload_name)


def create_file_environ():
    # TODO FIX
    from oauthlib.service_account import ServiceAccountCredentials
    credentials_dict = {
        'type': 'service_account',
        'client_id': os.environ['BACKUP_CLIENT_ID'],
        'client_email': os.environ['BACKUP_CLIENT_EMAIL'],
        'private_key_id': os.environ['BACKUP_PRIVATE_KEY_ID'],
        'private_key': os.environ['BACKUP_PRIVATE_KEY'],
    }
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        credentials_dict
    )
    return credentials
