import RPi.GPIO as GPIO
from rplidar import RPLidar
import sys
import json
import boto3

def detect_labels(photo):
    client = boto3.client('rekognition')
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image = {'Bytes': image.read()})
        
    data = {
        'source': photo,
        'data': response.get('Labels')
    }
    
    return json.dumps(data, indent = 4)
    
def main():
    script = sys.argv[0]
    if len(sys.argv) <= 1:
        print(f'Please supply a file.')
        exit(1)
    photo = sys.argv[1]
    print(detect_labels(photo))
    return none
    