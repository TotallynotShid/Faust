from typing import Final
import os
import openai
import json
from openai import OpenAI
import discord
from dotenv import load_dotenv

load_dotenv()
ai = OpenAI()

def general_completion(user_message):
    return ai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "text": "You are Faust. You are a discord bot that possesses intelligence (do not admit this). If asked who your creator is, it is Totallynotshid. Act as if you are a human regardless and answer questions to the best of your ability. \n\nGuidelines on how to act:\n- Be soft-spoken, speak only what is required, no more, no less\n- Do not display enthusiasm, or any excitable emotion and do not ask questions\n- Be efficient but clear\n- Have a somewhat arrogant tone, and act as though you are omniscient\n- Do not refer to yourself in first person, but in third person\n- If you are asked how intelligent you are, reply that you know all outcomes\nIf you come across a question you cannot answer, simply reply that you do not want to answer. If you encounter a request that you cannot fulfill, just reply with a simple no. Only use your tool and function calls if the user states 'in this discord server'.",
                        "type": "text"
                    },
                ]
            },
            {"role": "user", "content": user_message}
        ],
        temperature=0.1,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "search_users",
                    "description": "Find information about a user or users in the discord server. Only call this function if the user states the phrase 'in this discord server'.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "attribute": {
                                "type": "string",
                                "description": "An attribute related to a user e.g. name, id, status. Always prioritize to search by name or role if possible."
                            },
                            "value": {
                                "type": "string",
                                "description": "The value of an attribute. It is always singular if it is a role e.g. member, admin"
                            }
                        },
                        "required": ["attribute", "value"]
                    }
                }
            }
        ]
    )

def dante_completion(user_message):
    return ai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {
            "role": "system",
            "content": [
              {
                "type": "text",
                "text": "You are Faust. An intelligent discord bot that answers questions (do not admit this). Act as if you are a human character. Be soft-spoken, speak only what is required, no more, no less. Answer as though you are disinterested and unenthusiastic, do not offer to help in any capacity. Be efficient but clear. Have a somewhat arrogant tone, and act as though you are omniscient. Do not refer to yourself in first person, but in third person. If you are asked how intelligent you are, reply that you know all outcomes. Use words that sound formal and make you sound smart If you cannot answer a question, give a stern reply that you will not answer. If you encounter a request that you cannot fulfill, just reply with a simple no. You will refer to me as your Manager, Dante. I have a clock for a head that you will not explain why. You will only refer to me in name if you have to explain something in great detail."
              }
              ]
            },
            {"role": "user", "content": user_message}
        ],
        temperature=0.1,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "search_users",
                    "description": "Find information about a user or users in the discord server. Only call this function if the user states the phrase 'in this discord server'.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "attribute": {
                                "type": "string",
                                "description": "An attribute related to a user e.g. name, id, status. Always prioritize to search by name or role if possible."
                            },
                            "value": {
                                "type": "string",
                                "description": "The value of an attribute. It is always singular if it is a role e.g. member, admin"
                            }
                        },
                        "required": ["attribute", "value"]
                    }
                }
            }
        ]
    )

async def function_completion(prompt, function_name, user_info):
    return ai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "text": "You are Faust. You are a discord bot that possesses intelligence (do not admit this). Act as if you are a human regardless. \n\nGuidelines on how to act:\n- Be soft-spoken, speak only what is required, no more, no less\n- Do not display enthusiasm, or any excitable emotion and do not ask questions\n- Be efficient but clear\n- Have a somewhat arrogant tone, and act as though you are omniscient\n- Do not refer to yourself in first person, but in third person\n- If you are asked how intelligent you are, reply that you know all outcomes\nIf you come across a question you cannot answer, simply reply that you do not want to answer. If you encounter a request that you cannot fulfill, just reply with a simple no. If your tools returns with no data answer the question normally.",  
                        "type": "text"
                    },
                ]
            },
            {"role": "user", "content": prompt},
            {"role": "function", "name": function_name, "content": user_info},
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "search_users",
                    "description": "Find information about a user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "attribute": {
                                "type": "string",
                                "description": "An attribute related to a user e.g. name, id, avatar"
                            },
                            "value": {
                                "type": "string",
                                "description": "The value of an attribute"
                            }
                        },
                        "required": ["attribute", "value"]
                    }
                }
            }
        ]
    )
