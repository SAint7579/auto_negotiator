from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
os.environ['OPENAI_API_KEY'] = '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'


def gpt_draft_mail(specification, vendor_name):
    # Create a GPT prompt
    pormpt = f"Write a mail to a vendor named '{vendor_name}' on behalf of Vishwa Mohan Singh (salutations), asking for a quotation for the following specifications:\nSpecifications: {specification['specifications']}\nQuantity: {specification['quantity']}\nPrice: {specification['price']}\nNumber of days: {specification['num_days']}\nNeed logo: {specification['need_logo']}\n\nMail:"

    mail_assistant = ChatOpenAI()
    messages = [
        SystemMessage(
            content="You are an AI assistant that is supposed to write a mail to the vendor asking for a quotation and time of delivery."
        ),
        HumanMessage(content=pormpt),
    ]
    response = mail_assistant(messages)

    return response.content