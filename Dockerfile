FROM public.ecr.aws/lambda/python:3.12

ARG FUNCTION_NAME
# Copy requirements.txt
COPY ./lambda-code/requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY ./lambda-code/${FUNCTION_NAME}/app.py ${LAMBDA_TASK_ROOT}

USER volunteer
# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD ["app.handler"]
