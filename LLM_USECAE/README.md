# LLM_Document_Processing# LLM Query Response Generator

This project provides an AWS Lambda function that generates responses to user queries based on text extracted from PDF files stored in an S3 bucket. The function uses OpenAI's GPT model to process the extracted text and return meaningful answers.

---

## Features

- **S3 Integration**: Fetches extracted text from an S3 bucket.
- **LLM Query Response**: Uses OpenAI's GPT model (e.g., `gpt-3.5-turbo`) to generate responses to user queries.
- **API Gateway Integration**: Exposes the Lambda function as an API endpoint for querying the LLM.
- **Error Handling**: Handles missing inputs, S3 errors, and LLM query failures gracefully.

---

## How It Works

1. **Extracted Text in S3**:
   - Text extracted from PDF files is stored in an S3 bucket.

2. **Query the LLM**:
   - The user sends a query and the S3 key of the extracted text file to the API Gateway endpoint.
   - The Lambda function fetches the extracted text from the S3 bucket and queries the LLM to generate a response.

3. **Response**:
   - The Lambda function returns the LLM's response to the user.

---

## Prerequisites

- **AWS Services**:
  - S3 bucket for storing extracted text.
  - Lambda function with appropriate IAM permissions.
  - API Gateway for exposing the Lambda function as an API.

- **Environment Variables**:
  - `OPENAI_API_KEY`: Your OpenAI API key for querying the LLM.

- **Dependencies**:
  - Python 3.8 or higher
  - Required Python libraries (see `requirements.txt`):
    ```plaintext
    boto3
    openai
    ```

---

## Deployment

### 1. Build the Docker Image
Build the Docker image for the Lambda function:
```bash
docker build -t llm-query-response .
