from django.shortcuts import render
from langchain_community.document_loaders import NewsURLLoader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langdetect import detect
from langchain_community.document_loaders import NewsURLLoader
import requests
import json
import nltk
nltk.download('punkt')
# Create your views here.

url = "https://pl0sc4vmuuw5x1-5000.proxy.runpod.net/v1/completions"


def detect_language(text):
        language = detect(text)
        if language == "hi":
           language = "Hindi"
           return language
        if language == "ta":
           language = "Tamil"   
           return language
        if language == "bn":
           language = "Bengali"
           return language  
        if language == "gu":
           language = "Gujarati"
           return language
        language = "English"
        return language    

@csrf_exempt
def get_news_summary(request):
    if request.method == 'POST':
        try:
            news_url = request.POST.get('url')
        
            print(f"This is a URL {news_url}")
            loader = NewsURLLoader(urls=[news_url], nlp=True)
            data = loader.load()
            print(f"This is a Data {data}")

            if data and data[0].page_content:
                content = data[0].page_content
                language = detect_language(content)
                prompt = f"""  
                   
                    {content}</s>
                   
                    1.tell the summary of the context in 100 words. tell with appropriate hashtags.tell with emojis.
                    2.Give three type of opinions(in one line) about the context with emojis:- 1.positive 2.neutral 3.negative.
                    3.tell the news category it belongs to.
                    4.detect appropriate sentiments:
                       1. Positive (Uplifting/Optimistic)
                       2. Outrage (Outrage-Inducing)
                       3. Info (Informative)
                       4. Debate (Controversial)
                       5. Sad (Sorrowful)
                       6. Alert (Fearful)
                       7. LOL (Amusing)
                       8. Retro (Nostalgic)
                       9. Insight (Analytical)
                       10.Balanced (Neutral)
                       11.Negative (Pessimistic)
                    5.tell the language of the context.
                    6.tell the country and place news belongs to.
                    7.Main persons in the news: </s>
                   
                   
                         """
                if language == "English":
                    prompt = f"""  
                        <|system|>
                            {content}</s>
                        <|user|>
                        1.tell the summary of the context in 100 words. tell with appropriate hashtags.tell with emojis.
                        2.Give three type of opinions(in one line) about the context with emojis:- 1.positive 2.neutral 3.negative.
                        3.tell the news category it belongs to.
                        4.detect appropriate sentiments:
                            1. Positive (Uplifting/Optimistic)
                            2. Outrage (Outrage-Inducing)
                            3. Info (Informative)
                            4. Debate (Controversial)
                            5. Sad (Sorrowful)
                            6. Alert (Fearful)
                            7. LOL (Amusing)
                            8. Retro (Nostalgic)
                            9. Insight (Analytical)
                            10.Balanced (Neutral)
                            11.Negative (Pessimistic)
                        5.tell the language of the context.
                        6.tell the country and place news belongs to.
                        7.Main persons in the news: </s>
                        <|assistant|>
                        
                                """
                else:
                      print("please give link of english news.")
                      
                data = {
                    "prompt": prompt,
                    "max_tokens": 350,
                    "temperature": 0.5,
                    "top_p": 0.9,
                    "guidance_scale" : 1,
                    "repetition_penalty" : 1.15,
                    "top_k": 15
                }

                print(data)

                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.post(url, headers=headers, json=data, verify=False)

                # Check if response is successful
                if response.status_code == 200:
                    try:
                        # Extracting the specific part of the JSON response
                        assistant_message = response.json()['choices'][0]['text']
                        print(assistant_message)
                        return JsonResponse({'response': assistant_message})
                    
                    except KeyError as e:
                        print(f"Key error: {e}")
                    except IndexError as e:
                        print(f"Index error: {e}")
                else:
                    print(f"Failed to get a successful response. Status code: {response.status_code}")

        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method'})


