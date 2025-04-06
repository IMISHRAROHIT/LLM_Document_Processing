import json
import boto3
import io
import PyPDF2
import urllib.parse
import openai  # For LLM-based query-response generation

# Initialize the S3 client
s3 = boto3.client("s3")

# Set your OpenAI API key (store securely in environment variables)
openai.api_key = "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"  # Replace with your OpenAI API key

def extract_text_from_pdf(pdf_bytes):
    """Extracts text from a PDF file using PyPDF2."""
    text = ""
    pdf_stream = io.BytesIO(pdf_bytes)
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_stream)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        raise e
    return text

def generate_response_from_text(extracted_text, query):
    """Generates a response to a query using the extracted text and an LLM."""
    try:
        # Use OpenAI's GPT model to generate a response
        response = openai.Completion.create(
            engine="text-davinci-003",  # Replace with the desired model
            prompt=f"Context: {extracted_text}\n\nQuery: {query}\n\nResponse:",
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        raise e

def lambda_handler(event, context):
    """AWS Lambda function triggered by an S3 event."""
    try:
        # Parse S3 event details
        print("Event:", json.dumps(event, indent=2))  # Debugging logs
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        object_key = event["Records"][0]["s3"]["object"]["key"]

        # Decode the object key in case it is URL-encoded
        object_key = urllib.parse.unquote(object_key)

        print(f"Bucket Name: {bucket_name}")
        print(f"Object Key: {object_key}")

        # Download PDF from S3
        try:
            pdf_file = s3.get_object(Bucket=bucket_name, Key=object_key)
            pdf_bytes = pdf_file["Body"].read()
        except s3.exceptions.NoSuchKey:
            print(f"Error: The object key '{object_key}' does not exist in bucket '{bucket_name}'.")
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "File not found", "object_key": object_key})
            }

        # Extract text from PDF
        extracted_text = extract_text_from_pdf(pdf_bytes)

        # Generate a response to a query using the extracted text
        query = "What is the main topic of the document?"  # Replace with your query
        response = generate_response_from_text(extracted_text, query)

        print(f"Generated Response: {response}")

        # Upload extracted text and response to another S3 bucket
        output_bucket = "data-processing-bucket-llm"  # Replace with actual output bucket name
        output_key = object_key.replace(".pdf", "_extracted.txt")
        response_key = object_key.replace(".pdf", "_response.txt")

        # Upload extracted text
        s3.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=extracted_text,
            ContentType="text/plain"
        )

        # Upload LLM response
        s3.put_object(
            Bucket=output_bucket,
            Key=response_key,
            Body=response,
            ContentType="text/plain"
        )

        print(f"Extracted text uploaded to {output_bucket}/{output_key}")
        print(f"Response uploaded to {output_bucket}/{response_key}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "PDF text extracted and response generated successfully",
                "output_file": output_key,
                "response_file": response_key
            })
        }

    except Exception as e:
        print(f"Error processing file: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "An error occurred", "error": str(e)})
        }