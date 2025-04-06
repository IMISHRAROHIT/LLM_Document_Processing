# LLM_Document_Processing/LLM_Document_Processing/README.md

# LLM Document Processing

This project is designed to extract text from PDF files stored in an S3 bucket using an AWS Lambda function. The extracted text is then uploaded to another S3 bucket.

## Project Structure

```
LLM_Document_Processing
├── Dockerfile
├── requirements.txt
├── LLM_Document_Processing
│   ├── __init__.py
│   └── lambda_extract.py
└── README.md
```

## Files

- **Dockerfile**: Contains instructions to build a Docker image for the application.
- **requirements.txt**: Lists the Python dependencies required for the project.
- **LLM_Document_Processing/lambda_extract.py**: Contains the main logic for the AWS Lambda function.

## Getting Started

### Prerequisites

- Docker
- AWS CLI
- An AWS account with permissions to use ECR and Lambda

### Building the Docker Image

1. Navigate to the project directory:
   ```
   cd LLM_Document_Processing
   ```

2. Build the Docker image:
   ```
   docker build -t your-image-name .
   ```

### Pushing the Image to ECR

1. Authenticate Docker to your ECR registry:
   ```
   aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin your-account-id.dkr.ecr.your-region.amazonaws.com
   ```

2. Tag the Docker image:
   ```
   docker tag your-image-name:latest your-account-id.dkr.ecr.your-region.amazonaws.com/your-repo-name:latest
   ```

3. Push the Docker image to ECR:
   ```
   docker push your-account-id.dkr.ecr.your-region.amazonaws.com/your-repo-name:latest
   ```

### Deploying the Lambda Function

After pushing the Docker image to ECR, you can create or update your AWS Lambda function to use the image from ECR.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.