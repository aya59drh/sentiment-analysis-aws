import boto3
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client('s3')
athena = boto3.client('athena', region_name=os.getenv('AWS_DEFAULT_REGION'))

BUCKET = os.getenv('S3_BUCKET')
DATABASE = 'sentiment_db'
OUTPUT = f's3://{BUCKET}/athena-results/'

def write_result_to_s3(result: dict):
    """Écrit un résultat de sentiment dans S3"""
    key = f"results/event={result['event_name']}/date={datetime.now().strftime('%Y-%m-%d')}/{result['post_id']}.json"
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(result)
    )
    print(f"✅ Écrit dans S3 : {key}")

def run_athena_query(query: str):
    """Exécute une requête SQL sur Athena"""
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': DATABASE},
        ResultConfiguration={'OutputLocation': OUTPUT}
    )
    return response['QueryExecutionId']

def setup_athena():
    """Crée la base et la table Athena"""
    # Créer la base
    run_athena_query(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
    print("✅ Base sentiment_db créée")

    # Créer la table
    import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, 'schema.sql'), 'r') as f:
        schema = f.read()
        run_athena_query(schema)
        print("✅ Table sentiment_results créée")

if __name__ == '__main__':
    setup_athena()

    # Test : écrire un faux résultat
    test_result = {
        "post_id": "test_001",
        "event_name": "world_cup",
        "text": "This match is incredible!",
        "clean_text": "match incredible",
        "language": "en",
        "source": "simulated_twitter",
        "timestamp": datetime.now().isoformat(),
        "sentiment_label": "positive",
        "sentiment_score": 0.92,
        "model_name": "xlm-roberta",
        "processing_time": "0.45s"
    }
    write_result_to_s3(test_result)