#!/usr/bin/env python3
"""
AWS Bedrock Vision Client for Invoice Extraction

This module provides a client for interacting with AWS Bedrock Claude Vision API
to extract structured data from invoice images.

Adapted from: /Users/Michael.Zhang/Documents/myob/repos/aws-bedrock-hello-world/bedrock_claude_4_5_hello_world.py
"""

import os
import json
import base64
import time
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv
from PIL import Image
import io

# Load environment variables from .env file if it exists
# Reason: Load AWS credentials and configuration from .env file for security
load_dotenv()


class BedrockVisionClient:
    """
    A client class for interacting with AWS Bedrock Claude Vision API.
    
    This class handles:
    - Authentication with AWS Bedrock
    - Image encoding to base64
    - Invoice data extraction using Claude Vision
    - Retry logic with exponential backoff
    """
    
    def __init__(self, model_id, region_name):
        """
        Initialize the Bedrock Vision client.
        
        Args:
            model_id (str): The Claude model ID to use for extraction
            region_name (str): AWS region name for Bedrock service
        """
        # Reason: Accept model_id and region as explicit parameters for configurability
        self.model_id = model_id
        self.region_name = region_name
        
        try:
            # Initialize the Bedrock client
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name=self.region_name
            )
            print(f"✅ Bedrock Vision client initialized successfully in region: {self.region_name}")
        except NoCredentialsError:
            raise Exception("❌ AWS credentials not found. Please configure your AWS credentials.")
        except Exception as error:
            raise Exception(f"❌ Failed to initialize Bedrock client: {str(error)}")
    
    def encode_image_to_base64(self, image_path):
        """
        Convert an image file to base64 encoding for API transmission.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            str: Base64-encoded image data
            
        Raises:
            Exception: If image cannot be loaded or encoded
        """
        try:
            # Reason: Load image with PIL to ensure proper format handling
            with Image.open(image_path) as img:
                # Convert to RGB if necessary (handles RGBA, grayscale, etc.)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Save to bytes buffer as PNG
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                buffer.seek(0)
                
                # Encode to base64
                image_bytes = buffer.read()
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                
                return base64_image
        except Exception as error:
            raise Exception(f"❌ Failed to encode image {image_path}: {str(error)}")
    
    def extract_invoice_data(self, image_path, max_tokens=2000, temperature=0.0, max_retries=3):
        """
        Extract invoice data from an image using Claude Vision API.
        
        Args:
            image_path (str): Path to the invoice image file
            max_tokens (int): Maximum tokens to generate (default: 2000)
            temperature (float): Temperature for generation (default: 0.0 for deterministic)
            max_retries (int): Number of retry attempts on failure (default: 3)
            
        Returns:
            dict: Extracted invoice data with fields:
                - invoice_no: Invoice number
                - invoice_date: Invoice date
                - total_gross_worth: Total gross amount
                - seller: Seller information
                - client: Client information
                
        Raises:
            Exception: If extraction fails after all retries
        """
        # Reason: Clear, structured prompt ensures consistent JSON output format
        extraction_prompt = """
        Analyze this invoice image and extract the following information exactly as it appears:

        1. invoice_no: The invoice number
        2. invoice_date: The invoice date
        3. total_gross_worth: The total gross worth/amount (final total with currency)
        4. seller: The seller's complete name and address
        5. client: The client's complete name and address

        Return ONLY a valid JSON object with these exact field names. Do not include any explanation or additional text.

        Example format:
        {
        "invoice_no": "12345678",
        "invoice_date": "01/15/2023",
        "total_gross_worth": "$ 1,234.56",
        "seller": "Company Name and Address",
        "client": "Client Name and Address"
        }"""
        
        # Encode the image
        image_base64 = self.encode_image_to_base64(image_path)
        
        # Prepare the request body with image and text
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_base64
                            }
                        },
                        {
                            "type": "text",
                            "text": extraction_prompt
                        }
                    ]
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        # Retry logic with exponential backoff
        # Reason: API calls can fail due to network issues or rate limits
        for attempt in range(max_retries):
            try:
                # Invoke the model
                response = self.bedrock_client.invoke_model(
                    modelId=self.model_id,
                    body=json.dumps(request_body),
                    contentType='application/json',
                    accept='application/json'
                )
                
                # Parse the response
                response_body = json.loads(response['body'].read())
                content_blocks = response_body.get('content', [])
                generated_text = "".join(
                    block.get('text', '') for block in content_blocks if block.get('type') == 'text'
                )
                
                # Parse the JSON response
                # Reason: Extract JSON from response, handling potential markdown code blocks
                generated_text = generated_text.strip()
                if generated_text.startswith('```json'):
                    generated_text = generated_text[7:]
                if generated_text.startswith('```'):
                    generated_text = generated_text[3:]
                if generated_text.endswith('```'):
                    generated_text = generated_text[:-3]
                generated_text = generated_text.strip()
                
                extracted_data = json.loads(generated_text)
                
                # Validate that all required fields are present
                required_fields = ['invoice_no', 'invoice_date', 'total_gross_worth', 'seller', 'client']
                for field in required_fields:
                    if field not in extracted_data:
                        raise ValueError(f"Missing required field: {field}")
                
                return extracted_data
                
            except ClientError as error:
                error_code = error.response['Error']['Code']
                error_message = error.response['Error']['Message']
                
                # Reason: Log the attempt and retry with exponential backoff
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    print(f"⚠️  Bedrock API error (attempt {attempt + 1}/{max_retries}): {error_code}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"❌ Bedrock API error after {max_retries} attempts ({error_code}): {error_message}")
                    
            except (json.JSONDecodeError, ValueError) as error:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"⚠️  JSON parsing error (attempt {attempt + 1}/{max_retries}): {str(error)}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"❌ Failed to parse response after {max_retries} attempts: {str(error)}")
                    
            except Exception as error:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"⚠️  Extraction error (attempt {attempt + 1}/{max_retries}): {str(error)}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"❌ Extraction failed after {max_retries} attempts: {str(error)}")
    
    def test_connection(self):
        """
        Test the connection to AWS Bedrock and verify model access.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            # Simple test prompt to verify model access
            test_prompt = "Hello, respond with 'Connection successful'"
            
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": test_prompt}
                        ]
                    }
                ],
                "max_tokens": 50,
                "temperature": 0.0,
            }
            
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body),
                contentType='application/json',
                accept='application/json'
            )
            
            print(f"✅ Connection test successful")
            return True
        except Exception as error:
            print(f"❌ Connection test failed: {str(error)}")
            return False


if __name__ == "__main__":
    # Test the client
    print("🧪 Testing Bedrock Vision Client")
    print("=" * 50)
    
    try:
        # Reason: Use default Claude 4.5 model for testing
        test_model_id = 'au.anthropic.claude-sonnet-4-5-20250929-v1:0'
        test_region = 'ap-southeast-2'
        
        client = BedrockVisionClient(model_id=test_model_id, region_name=test_region)
        
        if client.test_connection():
            print("\n✅ Client is ready for invoice extraction")
        else:
            print("\n❌ Client connection failed")
            
    except Exception as error:
        print(f"\n❌ Error: {str(error)}")


