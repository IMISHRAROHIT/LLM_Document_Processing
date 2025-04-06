FROM public.ecr.aws/lambda/python:3.8

# Set the working directory
WORKDIR /var/task

# Copy the application code
COPY LLM_Document_Processing/ .

# Install the dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Command to run the Lambda function
CMD ["lambda_extract.lambda_handler"]