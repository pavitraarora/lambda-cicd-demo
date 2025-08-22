{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "572c7f41-50e8-4c73-9aa1-975001fbe73c",
   "metadata": {},
   "outputs": [],
   "source": [
    "from langchain_community.chat_models import BedrockChat\n",
    "from langchain.prompts.chat import (\n",
    "    HumanMessagePromptTemplate,\n",
    "    ChatPromptTemplate,\n",
    "    SystemMessagePromptTemplate,\n",
    ")\n",
    "\n",
    "def lambda_handler(event, context):\n",
    "    # Bedrock Model\n",
    "    model_id = \"anthropic.claude-3-5-sonnet-20240620-v1:0\"\n",
    "    chat_model = BedrockChat(model_id=model_id, region_name=\"us-east-1\")\n",
    "\n",
    "    # System message\n",
    "    system_template = \"You are an expert in the AWS\"\n",
    "    system1 = SystemMessagePromptTemplate.from_template(system_template)\n",
    "\n",
    "    # Human message with dynamic input\n",
    "    service = event.get(\"service\", \"EKS\")  # comes from API Gateway or test event\n",
    "    human_template = (\n",
    "        \"Write a short summary on the AWS service {service} in no more than 100 words\"\n",
    "    )\n",
    "    human1 = HumanMessagePromptTemplate.from_template(human_template)\n",
    "\n",
    "    # Chat Prompt\n",
    "    chat_prompt = ChatPromptTemplate.from_messages([system1, human1])\n",
    "    input_prompt = chat_prompt.format_prompt(service=service)\n",
    "\n",
    "    # Run Bedrock\n",
    "    results = chat_model(input_prompt.to_messages())\n",
    "\n",
    "    return {\"summary\": results.content}\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "LLM Env",
   "language": "python",
   "name": "llm_env"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
