import boto3
import csv
import datetime
import os
import pandas as pd


class ImporterExporter:

    # Imports
    def do_import(self, local: bool):
        if local:
            return self.local_import()
        else:
            return self.s3_import()

    def local_import(self):
        tweets = pd.read_csv(os.getenv('LOCAL_FILENAME'))
        now = datetime.datetime.now().time()
        print(f"{now}: Local read successful")
        return tweets

    def s3_import(self):
        s3 = boto3.client('s3')
        bucket = os.getenv('BUCKET_NAME')
        key = os.getenv('BUCKET_KEY')
        obj = s3.get_object(Bucket=bucket, Key=key)
        tweets = pd.read_csv(obj['Body'])
        now = datetime.datetime.now().time()
        print(f"{now}: S3 read successful")
        return tweets

    # Exports #
    def local_export(self, filename: str, header=[], data=[]):
        with open (filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            if len(header) > 0: 
                writer.writerow(header) 
            for row in data:
                writer.writerow(row)
        now = datetime.datetime.now().time()
        print(f"{now}: Local upload successful")

    def s3_export(self, filename: str, bucket_name: str, bucket_key:str, header=[], data=[]):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)

        with open (filename, 'w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            if len(header) > 0: 
                writer.writerow(header) 
            for row in data:
                writer.writerow(row)
        bucket.upload_file(filename, bucket_key)
        now = datetime.datetime.now().time()
        print(f"{now}: S3 upload successful")
