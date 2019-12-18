from .worker import CelerySingleton
from src.utils.errors.custom_errors import NoResultsFoundInDatabase, DatabaseCommitFailed
from src.utils.errors.messages import DATABASE_COMMIT_FAILED
from google.auth.exceptions import DefaultCredentialsError
from google.api_core.exceptions import GoogleAPICallError


celery_app = CelerySingleton().get_celery()


@celery_app.task(name="add_two_numbers")
def add_two_numbers(x, y):
    return x + y


@celery_app.task(
    bind = True, 
    autoretry_for = (GoogleAPICallError, DatabaseCommitFailed), 
    retry_kwargs = {"max_retries": 5, "countdown": 1},
    name="calculate_sentiment_for_response"
)
def calculate_sentiment_for_response(response_uuid):
    from google.cloud import language
    from google.cloud.language import enums 
    from google.cloud.language import types

    from src.database.db import get_db
    

    client = language.LanguageServiceClient()

    from src.database.crud.response_crud import SurveyResponseCRUD
    response = SurveyResponseCRUD().read_response_by_uuid(uuid = response_uuid) # pylint: disable=no-value-for-parameter

    if not response.processed:
        response_json: dict = dict(response.response) 
        key_list = list(response_json.keys())

        for key in key_list:
            if key.startswith("textarea"):
                document = language.types.Document( #pylint: disable=no-member
                    content = response_json[key],
                    type = "PLAIN_TEXT"
                )

                response = client.analyze_sentiment(
                    document = document,
                    encoding_type="UTF8"
                )
                sentiment = response.document_sentiment

                response_json[key + "_sentimentScore"] = sentiment.score
                response_json[key + "_magnitudeScore"] = sentiment.magnitude
                response_json[key + "_language"] = sentiment.language
        
        response.processed = True
        response.response = response_json

        session = get_db()

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise DatabaseCommitFailed(
                DATABASE_COMMIT_FAILED.format(
                    e = repr(e)
                )
            )





    


    