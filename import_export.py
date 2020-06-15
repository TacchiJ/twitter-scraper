import boto3
import csv
import datetime
import os
import pandas as pd


class ImporterExporter:
    '''A class that allows for easy importing and exporting of data locally as well as to S3'''

    #TODO: Rewrite imports so that they take parameters similarly to the exports
    #TODO: Add a do_export() method

    # Imports
    def do_import(self, local: bool):
        '''Imports data using locations and authorizations from .env file
        
        :param local: imports local data if set to True, else imports from S3
        '''
        if local:
            return self.local_import()
        else:
            return self.s3_import()

    def local_import(self):
        '''Imports local data'''
        tweets = pd.read_csv(os.getenv('LOCAL_FILENAME'))
        now = datetime.datetime.now().time()
        print(f"{now}: Local read successful")
        return tweets

    def s3_import(self):
        '''Imports data from S3'''
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
        '''Exports data locally as a csv file

        :param filename: the name of the file to be output
        :param header: optional header for the file
        :param data: the data to be output
        '''
        with open (filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            if len(header) > 0: 
                writer.writerow(header) 
            for row in data:
                writer.writerow(row)
        now = datetime.datetime.now().time()
        print(f"{now}: Local upload successful")

    def s3_export(self, filename: str, bucket_name: str, bucket_key:str, header=[], data=[]):
        '''Exports data as a csv file to an S3 bucket

        :param filename: the name of the file to be output
        :param bucket_name: name of the destination bucket
        :param bucket_key: key for the destination bucket
        :param header: optional header for the file
        :param data: the data to be output
        '''
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
