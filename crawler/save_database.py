from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd

class SaveDB:


    def save_data(self,
                  bq_json: str=None,
                  db: str=None,
                  table: str=None, 
                  file: str=None):
        
        credentials = service_account.Credentials.from_service_account_file(bq_json)
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        dataset_id = db
        table_id = table
        table_ref = f"{credentials.project_id}.{dataset_id}.{table_id}"
        df = pd.read_csv(file)
        job = client.load_table_from_dataframe(df, table_ref)
        job.result()

        print("Data has been uploaded successfully.")
