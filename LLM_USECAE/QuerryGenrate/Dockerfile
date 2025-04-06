FROM public.ecr.aws/lambda/python:3.8

# Set the working directory
WORKDIR /var/task

# Copy the application code
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the Lambda function handler
CMD ["llmresponse.lambda_handler"]