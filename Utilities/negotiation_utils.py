from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
os.environ['OPENAI_API_KEY'] = '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'


function_json = {
  "name": "get_vendor_quotation",
  "parameters": {
    "type": "object",
    "properties": {
      "requirements_satisfied": {
        "type": "boolean",
        "description": "Can the requirements be satisfied by the vendor? Make it true even if some requirements can be satisfied."
      },
      "unfullfiled_requirements": {
        "type": "string",
        "description": "What requirements cannot be satisfied by the vendor? Separate requirements with ';'. NA if there are no missing requirements."
      },
      "quotation": {
        "type": "number",
        "description": "Price per unit of the product. Only set to NA if the requirements cannot be satisfied at all. Otherwise ask the user for the exact price."
      },
      "procurement_days": {
        "type": "number",
        "description": "Number of days to fullfil the requirements. Only set to NA if the requirements cannot be satisfied at all. Otherwise ask the user for the days"
      }
    },
    "required": [
      "requirements_satisfied",
      "unfullfiled_requirements",
      "quotation",
      "procurement_days"
    ]
  },
  "description": "Check if the vendor can fullfil the requirements and get the vendor quotation and procurement days from the mail."
}

def gpt_draft_mail(specification, vendor_name):
    # Create a GPT prompt
    pormpt = f"Write a mail to a vendor named '{vendor_name}' on behalf of Vishwa Mohan Singh (salutations), asking for a quotation for the following specifications:\nSpecifications: {specification['specifications']}\nQuantity: {specification['quantity']}\nOur Price: {specification['price']} Euros\nNumber of days Required: {specification['num_days']}\nNeed logo: {specification['need_logo']}\n\nMail:"

    mail_assistant = ChatOpenAI()
    messages = [
        SystemMessage(
            content="You are an AI assistant that is supposed to write a mail to the vendor asking for a quotation and time of delivery. Specify our required price and days as well."
        ),
        HumanMessage(content=pormpt),
    ]
    response = mail_assistant(messages)

    return response.content


def get_new_assistant(specification):
    proc_assistant = OpenAIAssistantRunnable.create_assistant(
    name="Procurement_Bot_Vishwa",
    instructions=f"You are an AI assistant who is supposed to get the quotation and time of delivery from the vendor. These are the requirements:{specification}. You are supposed to collect the three main information: Can the requirements be met, what is the price and how long will it take to deliver (in days). All these requirements need to be provided by the vendor in chat. Do not invoke the function until you have all the information or if the vendor has rejected it. Always write your responses in form of a mail on behalf of Vishwa Singh.",
    tools=[{"type": "function", "function": function_json, "name": "get_specifications"}],
    model="gpt-4-1106-preview",)

    return proc_assistant