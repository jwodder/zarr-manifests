import os
import json

def application(environ, start_response):
    # Get the base directory (where the WSGI script resides)
    base_dir = os.path.dirname(environ['SCRIPT_FILENAME'])
    
    # Get the path from the URL
    request_path = environ.get('PATH_INFO', '')
    
    # Safely construct the full path to avoid security issues
    full_path = os.path.normpath(os.path.join(base_dir, request_path.strip('/')))

    # Ensure the requested path is within the base_dir to prevent directory traversal attacks
    if not full_path.startswith(base_dir):
        status = '403 Forbidden'
        response = 'Access denied.'
        response_headers = [('Content-type', 'text/plain'),
                            ('Content-Length', str(len(response)))]
        start_response(status, response_headers)
        return [response.encode('utf-8')]
    
    # List directory contents
    files = []
    directories = []
    try:
        for item in os.listdir(full_path):
            if os.path.isfile(os.path.join(full_path, item)):
                files.append(item)
            else:
                directories.append(item)
        
        # Create JSON response
        response = json.dumps({
            'path': request_path,
            'files': files,
            'directories': directories
        })

        status = '200 OK'
        response_headers = [('Content-type', 'application/json'),
                            ('Content-Length', str(len(response)))]
        start_response(status, response_headers)
        
        return [response.encode('utf-8')]
    except OSError as e:
        # Handle error (e.g., directory does not exist)
        status = '404 Not Found'
        response = 'Directory not found.'
        response_headers = [('Content-type', 'text/plain'),
                            ('Content-Length', str(len(response)))]
        start_response(status, response_headers)
        return [response.encode('utf-8')]

