
FROM --platform=x86_64 public.ecr.aws/docker/library/python:3.12.0-slim-bullseye
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.3 /lambda-adapter /opt/extensions/lambda-adapter

# Copy the model file
COPY .models/Phi-3-mini-4k-instruct-q4.gguf /var/task/.models/Phi-3-mini-4k-instruct-q4.gguf

# install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY model_lambda/requirements.txt /var/task/requirements.txt

RUN python3 -m pip install --no-cache -r /var/task/requirements.txt

# Copy the lambda function
COPY model_lambda /var/task/model_lambda

WORKDIR /var/task/

CMD [ "python", "-m", "uvicorn", "model_lambda.index:app", "--host", "0.0.0.0", "--port", "8080"]