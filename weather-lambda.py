import json
import os
import urllib.request
import boto3

API_KEY = os.environ['API_KEY']
ARN = os.environ['SNS_ARN']
client = boto3.client('sns')
def lambda_handler(event, context):
  api_url = "https://api.openweathermap.org/data/2.5/weather?"
  lat = "35.10"
  lon = "81.04"
  unit = "imperial"
  api_url = f"{api_url}lat={lat}&lon={lon}&units={unit}&appid={API_KEY}"
  print(api_url.replace(API_KEY, "My_key"))

  req = urllib.request.Request(
    url=api_url,
    headers={"Accept": "application/json"},
    method="GET"
  )

  with urllib.request.urlopen(req) as res:
    # print(res.status)

    response_body = res.read()
    data = json.loads(response_body)

    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']

    return_body = {
      'weather_description': json.dumps(weather_description),
      'temperature': temperature,
      'humidity': humidity
    }

    sent_message = json.dumps(return_body)

    response = client.publish(
      TopicArn=ARN,
      Message=sent_message
    )

    return response

