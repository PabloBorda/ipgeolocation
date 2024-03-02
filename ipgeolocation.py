import json
import logging
import requests

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_ip_geolocation(ip_address, api_key='27f48d1d022b425a88542cfde5d25b67'):
    url = f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip_address}'
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def lambda_handler(event, context):
    # Extract the source IP from the event object
    source_ip = event['requestContext']['identity']['sourceIp']
    
    # Get geolocation data for the IP address
    geolocation_data = get_ip_geolocation(source_ip)
    
    # Log geolocation data to CloudWatch
    logger.info(f'Geolocation data for {source_ip}: {json.dumps(geolocation_data)}')
    
    # Return basic HTML content
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Simple Page</title>
</head>
<body>
    <h1>Hello from Lambda!</h1>
    <p>This is a simple HTML page.</p>
</body>
</html>"""

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": html_content
    }
