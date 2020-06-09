import boto3
import csv

class ImporterExporter:

    # Imports
    def local_import(self):
        pass

    def s3_import(self):
        pass

    # Exports #
    def local_export(self, filename: str, header=[], data=[]):
        with open (filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            if len(header) > 0: 
                writer.writerow(header) 
            for row in data:
                writer.writerow(row)

        print('Local upload successful')

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

        print('S3 upload successful')
