from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")
# Get the input language from environment variables.
InputLanguage = env_vars.get("InputLanguage")

# Define the HTML code template for the speech-to-text interface.
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Replace the language placeholder in the HTML code with the actual input language.
HtmlCode = str(HtmlCode).replace("recognition.lang = '';",f"recognition.lang = '{InputLanguage}';")


with open(r"Data\Voice.html","w") as f:
    f.write(HtmlCode)


current_dir = os.getcwd()

Link = f"{current_dir}\\Data\\Voice.html"


chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

Service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=Service, options=chrome_options)


TempDirPath = rf"{current_dir}\Frontend\Files"


def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}/Status.data', 'w', encoding='utf-8') as file:
        file.write(Status)


def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["what", "when", "where", "who", "whom", "which", "whose", "why", "how"]

    if any(word in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    
    return new_query.capitalize()


def UniversalTranslator(Text):
    try:
        print(f"[DEBUG] Translating from {InputLanguage} to English: {Text}")
        english_translation = mt.translate(Text, "en", InputLanguage)
        print(f"[DEBUG] Translation result: {english_translation}")
        if english_translation and english_translation.strip():
            return english_translation.capitalize()
        else:
            # Fallback: if translation is empty, return original text
            print(f"[DEBUG] Translation failed, returning original text")
            return Text.capitalize()
    except Exception as e:
        print(f"[DEBUG] Translation error: {type(e).__name__}: {str(e)}")
        return Text.capitalize()


def SpeechRecognition():

    driver.get("file:///" + Link)

    driver.find_element(by=By.ID, value="start").click()

    while True:
        try:

            Text = driver.find_element(by=By.ID, value="output").text

            if Text:

                driver.find_element(by=By.ID, value="end").click()

                print(f"[DEBUG] Recognized text: {Text}")
                print(f"[DEBUG] InputLanguage: {InputLanguage}")
                
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    print(f"[DEBUG] Language is English, not translating")
                    return QueryModifier(Text)
                else:
                    print(f"[DEBUG] Language is not English, translating...")
                    SetAssistantStatus("Translating ...")
                    translated = UniversalTranslator(Text)
                    print(f"[DEBUG] Final translated text: {translated}")
                    return QueryModifier(translated)

        except Exception as e:
            print(f"[DEBUG] Exception in SpeechRecognition: {type(e).__name__}: {str(e)}")
            pass


if __name__ == "__main__":
    while True:

        Text = SpeechRecognition()
        print(Text)

