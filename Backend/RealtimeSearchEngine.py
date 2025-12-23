from googlesearch import search
from duckduckgo_search import DDGS
from groq import Groq               # Import the Groq library for AI interactions.
from json import load, dump         # Import JSON functions for reading and writing chat logs.
import datetime                     # Import datetime for real-time information.
from dotenv import dotenv_values    # Import dotenv to load environment from a .env file.
import sys                          # Import sys for command-line arguments.

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve necessary environment variables from the Chatbot.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Create a Groq client using the provided API key.
client = Groq(api_key=GroqAPIKey)

# Define the system instructions for the chatbot.
system = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet. 
*** Provide Answers In a Professional Manner, make sure to add Full stops, commas, question marks, and use proper grammar.***
*** just answer the question from the provided data in a professional way and precise manner, do not add any unnecessary information.***
"""

# Try to load existing chat logs; if not found, create a new log file.
try:
    with open(r"Data\ChatLog.json","r") as f:
        messages = load(f)
except:
    with open(r"Data\ChatLog.json","w") as f:
        dump([],f)

# Function to perform a search (DuckDuckGo primary, Google fallback) and return formatted results.
def GoogleSearch(query):
    """
    Perform a web search using DuckDuckGo (primary) or Google (fallback).
    Returns formatted search results for the AI to process.
    """
    try:
        print(f"[DEBUG] Searching for: {query}")
        results = []
        
        # Try DuckDuckGo first (more reliable)
        try:
            ddgs = DDGS()
            ddg_results = ddgs.text(query, max_results=5)
            results = ddg_results
            print(f"[DEBUG] DuckDuckGo found {len(results)} results")
        except Exception as e:
            print(f"[DEBUG] DuckDuckGo search failed: {str(e)}")
            # Fallback to Google
            try:
                google_results = list(search(query, advanced=True, num_results=5))
                results = [{"title": r.title, "body": r.description, "href": r.url} for r in google_results]
                print(f"[DEBUG] Google found {len(results)} results")
            except Exception as google_e:
                print(f"[DEBUG] Google search also failed: {str(google_e)}")
        
        if not results:
            return f"Search data for '{query}': Unable to retrieve live search results. Use your knowledge to provide helpful information about: {query}"
        
        Answer = f"Search Results for '{query}':\n[start]\n"
        for idx, result in enumerate(results, 1):
            title = result.get("title", "No title")
            body = result.get("body", result.get("description", "No description"))
            href = result.get("href", result.get("url", "No URL"))
            Answer += f"Result {idx}:\nTitle: {title}\nInfo: {body}\nSource: {href}\n\n"
        Answer += "[end]\n"
        return Answer
        
    except Exception as e:
        print(f"[DEBUG] Search exception: {type(e).__name__}: {str(e)}")
        return f"Real-time search for '{query}' encountered issues. Answer based on your training knowledge about: {query}"

# Function to clean up the AI's answer by removing empty lines.
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()] 
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer


SystemChatBot = [
    {"role": "system", "content": system},
    {"role": "user" , "content": "Hey"},
    {"role": "assistant" , "content": "Hey! How can I assist you today?"}
]

# Function to get real-time current date and time information.
def Information():
    data = ""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data





# Function to handle real-time search engine queries.
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    # Load existing chat logs.
    with open(r"Data\ChatLog.json","r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})


    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})


    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""


    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content


    Answer = Answer.strip().replace("</s>","")
    messages.append({"role": "assistant", "content": Answer})

    # Save the updated chat logs.
    with open(r"Data\ChatLog.json","w") as f:
        dump(messages,f, indent=4)


    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If arguments are provided, use them as the query
        prompt = " ".join(sys.argv[1:])
        print(RealtimeSearchEngine(prompt))
    else:
        # Otherwise, run in interactive mode
        while True:
            prompt = input("Enter your query: ")
            print(RealtimeSearchEngine(prompt))

