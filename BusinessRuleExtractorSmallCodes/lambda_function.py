#Above Code as Lambda Funciton
import boto3
import os
from datetime import datetime
from langchain_community.chat_models import BedrockChat
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)

# Initialize S3 client
s3 = boto3.client("s3")

# Bedrock Claude Sonnet
model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
chat_model = BedrockChat(
    model_id=model_id,
    region_name="us-east-1"
)

def process_file(bucket_name, object_key):
    # --- Get COBOL file from S3 ---
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    file_content = response["Body"].read().decode("utf-8")  # change if EBCDIC

    # --- Build LangChain prompt ---
    system_template = (
        "You are an expert legacy mainframe modernization analyst. "
        "Analyze the COBOL code provided from the S3 file and prepare a detailed document. "
        "Focus on explaining business logic, data access, and modernization recommendations."
    )
    system_msg = SystemMessagePromptTemplate.from_template(system_template)

    human_template = "Here is the COBOL code:\n{input_text}"
    human_msg = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_msg, human_msg])
    formatted_prompt = chat_prompt.format_prompt(input_text=file_content)

    # --- Call Bedrock Claude Sonnet ---
    result = chat_model(formatted_prompt.to_messages())

    # Extract output text safely
    output_text = getattr(result, "content", str(result))

    # --- Prepare output key ---
    base_name, ext = os.path.splitext(object_key)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_key = f"{base_name}_analysis_{timestamp}.txt"

    # --- Save analysis back to S3 ---
    s3.put_object(
        Bucket=bucket_name,
        Key=output_key,
        Body=output_text.encode("utf-8")
    )

    return output_key

# Lambda Handler
def lambda_handler(event, context):
    """
    Expected event format:
    {
        "bucket": "pa-agentic-output1",
        "key": "CBACT03C.cbl"
    }
    """
    try:
        bucket = event["bucket"]
        key = event["key"]

        output_key = process_file(bucket, key)

        return {
            "statusCode": 200,
            "body": f"✅ Processed {key}, results saved as {output_key}"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
