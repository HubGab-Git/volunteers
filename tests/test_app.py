import os
import mimetypes
from datetime import datetime
from lambda_code.app import handler

def test_root_path():
    event = {'path': '/'}
    context = {}
    response = handler(event, context)

    assert response['statusCode'] == 200
    assert 'Dynamic content' in response['body']
    assert response['headers']['Content-Type'] == 'text/html'

def test_static_file():
    static_file_path = os.path.join(os.path.dirname(__file__), '..', 'lambda_code', 'website', 'styles.css')
    event = {'path': '/styles.css'}
    context = {}
    response = handler(event, context)

    assert response['statusCode'] == 200
    assert response['headers']['Content-Type'] == 'text/css'
    assert response['isBase64Encoded'] == True

def test_non_existent_file():
    event = {'path': '/non-existent.txt'}
    context = {}
    response = handler(event, context)

    assert response['statusCode'] == 404
    assert response['body'] == 'File not found'
