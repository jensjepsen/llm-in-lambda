import typer, json

import requests

import botocore.session
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

app = typer.Typer()

session = botocore.session.Session()

@app.command()
def invoke_lambda(function_url: str):
    sigv4 = SigV4Auth(session.get_credentials(),
                  service_name="lambda",
                  region_name="eu-central-1")

    data = json.dumps([
            {
                "content": "You're a really nice assistant.",
                "role": "system"
            },
            {
                "content": "Write some cool python code",
                "role": "user"
            }
        ])
    
    request = AWSRequest(method="POST", url=function_url + "chat", data=data)
    
    sigv4.add_auth(request)
    signed = request.prepare()
    response = requests.post(signed.url, headers=signed.headers, data=signed.body, stream=True)
    print(response.status_code)
    for line in response.iter_lines():
        line = line.decode("utf-8")
        if line.startswith("data: "):
            print(json.loads(line[6:])['choices'][0]['text'], end="", flush=True)

if __name__ == "__main__":
    app()


