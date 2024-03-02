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
    # Configure CherryPy to use SSL for HTTPS
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': 'server.crt', # Path to your SSL certificate
        'server.ssl_private_key': 'server.key', # Path to your SSL private key
    })
    
    # Configure a second HTTP server (if necessary) on port 80
    from cherrypy._cpserver import Server
    def run_dual_http_https():
        # Configure server for HTTPS
        server1 = Server()
        server1.socket_host = '0.0.0.0'
        server1.socket_port = 443
        server1.ssl_module = 'builtin'
        server1.ssl_certificate = 'ssl/server.crt' # Path to your SSL certificate
        server1.ssl_private_key = 'ssl/server.key' # Path to your SSL private key
        
        # Configure server for HTTP
        server2 = Server()
        server2.socket_host = '0.0.0.0'
        server2.socket_port = 80
        server2.subscribe()

        # Start the server
        cherrypy.quickstart(SimpleWebServer())

    run_dual_http_https()
