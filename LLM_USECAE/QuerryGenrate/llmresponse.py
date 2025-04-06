import json
import boto3
import openai
import os

# Initialize S3 client and OpenAI API key from environment variables
s3 = boto3.client("s3")
openai.api_key = os.getenv('OPENAI_API_KEY')  # Fetch API key securely from environment variables

def get_text_from_s3(object_key, bucket_name):
    """Fetch the extracted text from the S3 bucket."""
    try:
        # Fetch the extracted text from S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        extracted_text = response['Body'].read().decode('utf-8')
        return extracted_text
    except Exception as e:
        print(f"Error fetching file from S3 (Key: {object_key}): {e}")
        raise Exception(f"Error fetching file from S3: {e}")

def query_llm(extracted_text, query):
    """Call the LLM (e.g., OpenAI) to generate a response based on extracted text and query."""
    try:
        # Create a prompt combining the extracted text and the user query
        prompt = f"Here is some extracted text:\n\n{extracted_text}\n\nQuestion: {query}\nAnswer:"
        
        # Query the LLM using OpenAI's new API method `ChatCompletion.create`
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Choose the appropriate model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7,
        )
        
        # Extract the response from the LLM
        answer = response['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        print(f"Error querying LLM: {e}")
        raise Exception(f"Error querying LLM: {e}")

def lambda_handler(event, context):
    """AWS Lambda function triggered by API Gateway."""
    try:
        # Parse the incoming request
        body = json.loads(event['body'])
        query = body.get("query", "")  # The query the user asked
        object_key = body.get("object_key", "")  # S3 key for the extracted text file
        
        if not query or not object_key:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Missing 'query' or 'object_key' in the request."
                })
            }
        
        # Define the S3 bucket name where extracted text is stored
        bucket_name = "data-processing-bucket-llm"  # Replace with your bucket name
        
        # Fetch the extracted text from S3
        extracted_text = get_text_from_s3(object_key, bucket_name)
        
        if not extracted_text:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "message": "Failed to fetch extracted text from S3."
                })
            }
        
        # Query the LLM using the extracted text and the user's query
        llm_response = query_llm(extracted_text, query)
        
        if not llm_response:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "message": "Failed to generate a response from the LLM."
                })
            }
        
        # Return the LLM's response to the user
        return {
            "statusCode": 200,
            "body": json.dumps({
                "query": query,
                "response": llm_response
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }
    
    except Exception as e:
        # Handle unexpected errors
        print(f"Error processing the request: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "An error occurred.",
                "error": str(e)
            })
        }
