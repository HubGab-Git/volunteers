import os
import mimetypes
from datetime import datetime

def handler(event, context):
    requested_path = event.get('path', '/') or '/'
    resource_path = os.path.join(os.path.dirname(__file__), 'website', requested_path.lstrip('/'))

    try:
        if requested_path == '/':
            # Render the index.html with dynamic content
            index_html_path = os.path.join(os.path.dirname(__file__), 'website', 'index.html')
            with open(index_html_path, 'r') as f:
                index_html = f.read()
            modified_html = index_html.replace('<p id="dynamic-content">This content will be updated dynamically.</p>',
                                               f'<p id="dynamic-content">Dynamic content: {datetime.now().isoformat()}</p>')

            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/html',
                },
                'body': modified_html,
            }
        else:
            # Serve static files
            with open(resource_path, 'rb') as f:
                file_content = f.read()

            content_type = mimetypes.guess_type(resource_path)[0] or 'application/octet-stream'

            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': content_type,
                },
                'body': file_content,
                'isBase64Encoded': True,
            }
    except FileNotFoundError:
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'text/plain',
            },
            'body': 'File not found',
        }
