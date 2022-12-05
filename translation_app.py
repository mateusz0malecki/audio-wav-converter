import os
from google.cloud import speech
from google.cloud import storage
from functools import lru_cache

STORAGE_CREDENTIALS_FILE = "scrapper-system-storage-sa.json"
BUCKET_NAME = "recording-app"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'scrapper-system-stt-sa.json'
speech_client = speech.SpeechClient()


class StorageClient:
    """
    Class creates a client that connects to Cloud Storage Bucket and uploads new files.
    """
    def __init__(self, credentials_file, bucket_name):
        self._credentials_file = credentials_file
        self._bucket_name = bucket_name
        self._client = storage.Client.from_service_account_json(self._credentials_file)
        self._bucket = self._client.get_bucket(self._bucket_name)

    def upload(self, blob_name, path_to_file):
        blob = self._bucket.blob(blob_name)
        blob.upload_from_filename(path_to_file)


@lru_cache
def get_client():
    return StorageClient(STORAGE_CREDENTIALS_FILE, BUCKET_NAME)


def translate_small_local_file_gcp(media_file_name):
    """
    Uses Google speech-to-text to transcript local file that is shorter than 60 sec and weights less than 10MB.
    :param: media_file_name: path to local file
    :return: transcript text and Google total billed time
    """
    with open(media_file_name, 'rb') as f1:
        byte_data_wav = f1.read()

    details_audio = dict(content=byte_data_wav)
    audio = speech.RecognitionAudio(details_audio)

    details_config = dict(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="pl-PL",
        enable_automatic_punctuation=True,
        model='default'
    )
    config = speech.RecognitionConfig(details_config)
    response = speech_client.recognize(config=config, audio=audio)
    return response.results, response.total_billed_time


def translate_big_bucket_file_gcp(media_uri):
    """
    Uses Google speech-to-text to transcript file that is longer than 60 sec or weights more than 10MB.
    File has to be uploaded to Cloud Storage bucket.
    :param: media_uri: URI to file sored in Cloud Storage Bucket
    :return: transcript text and Google total billed time
    """
    audio = speech.RecognitionAudio(uri=media_uri)
    detail_config = dict(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="pl-PL",
        enable_automatic_punctuation=True,
        use_enhanced=True,
        model='latest_long',
        audio_channel_count=2
    )
    config = speech.RecognitionConfig(detail_config)
    operation = speech_client.long_running_recognize(config=config, audio=audio)
    response = operation.result()
    return response.results, response.total_billed_time
