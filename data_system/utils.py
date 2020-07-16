from google.cloud import bigquery
from google.cloud import storage
from data_system.config import CAR_INFO_TABLE

from flask import request, current_app
import jwt
from flask_jwt_extended.view_decorators import _decode_jwt_from_headers
from flask_jwt_extended.config import config
from http import HTTPStatus

import pdb

def check_username_query(unique_id):
    client = bigquery.Client()

    query = """
        SELECT *
        FROM `{}`
        WHERE unique_id = @unique_id
    """.format(CAR_INFO_TABLE)

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('unique_id', 'STRING', unique_id)
        ]
    )
    query_job = client.query(query, job_config=job_config)
    return query_job

def check_jwt_payload(func):
    def wrapper(*args, **kwargs):
        encoded_token, csrf_token = _decode_jwt_from_headers()
        unverified_claims = jwt.decode(encoded_token, verify=False, algorithms=config.decode_algorithms)
        try:
            query_job = check_username_query(unverified_claims['identity'])
            for row in query_job:
    #           current_app.config['JWT_PRIVATE_KEY'] = row.jwt_private_key
                current_app.config['JWT_PUBLIC_KEY'] = row.jwt_public_key
                break
        except:
            return {"message": "Invalid Request"}, HTTPStatus.UNAUTHORIZED
        return func(*args, **kwargs)
    return wrapper

def upload_blob(bucket_name, source_file, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(source_file)
   #blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file.filename, destination_blob_name
        )
    )
