import cherrypy
import requests

def get_ip_geolocation(ip_address, api_key):
    url = f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip_address}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

class SimpleWebServer(object):
    @cherrypy.expose
    def index(self):
        # Get client IP address
        client_ip = cherrypy.request.remote.ip
        
        # Assuming you have your API key
        api_key = 'YOUR_API_KEY_HERE'
        
        # Get geolocation data for the IP address
        geolocation_data = get_ip_geolocation(client_ip, api_key)
        
        # Log IP and geolocation data
        with open('visits.log', 'a') as log_file:
            log_file.write(f'IP: {client_ip}, Geolocation Data: {geolocation_data}\n')
        
        return """<!DOCTYPE html>
<html>
<head>
    <title>Embedded Page</title>
</head>
<body>
    <h1>Hello, CherryPy with Embedded HTML and Geolocation!</h1>
    <p>This is a simple page served by CherryPy with embedded HTML content.</p>
</body>
</html>"""

if __name__ == '__main__':
    # Update CherryPy configuration to listen on port 80 and bind to all network interfaces
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 80,
    })
    cherrypy.quickstart(SimpleWebServer())
