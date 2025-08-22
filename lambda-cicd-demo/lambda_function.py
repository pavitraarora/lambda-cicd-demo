from langchain_community.chat_models import BedrockChat
from langchain.prompts.chat import HumanMessagePromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate,AIMessagePromptTemplate
model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
chat_model = BedrockChat(
    model_id=model_id,
    region_name="us-east-1"
)
system_template = "You are an expert in the AWS"
system1 = SystemMessagePromptTemplate.from_template(system_template)

human_template = "Write a short summary on the AWS service {service} in no more then 100 words"
human1 = HumanMessagePromptTemplate.from_template(human_template)

# Chat Prompt
chat_prompt = ChatPromptTemplate.from_messages([system1,human1])

#pass input data
Input_Chat_Prompt =chat_prompt.format_prompt(service="EKS")
#Passing the Input_Chat_Prompt to ChatModel
results  = chat_model(Input_Chat_Prompt.to_messages())
results.content