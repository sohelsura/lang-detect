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

url = "https://mzxwykgsxnf33g-5000.proxy.runpod.net/v1/completions"


def home(request):
    return render(request, 'home.html')


def output(text):
        language = detect(text)
        if language == "en": ##hindi
           prompt = []
           prompts1 = f"""
                 <|system|>
                       {text}</s>
                 <|user|>
                        -> try to end in one line.
                        ->Tell the summary of the above context in 50 words. End with three hashtags.include one emoji. now this is the end, don't tell anything extra. </s>
                 <|assistant|>
                """
           prompt.append(prompts1)
           prompts2 = f"""
                 <|system|>
                       {text}</s>
                 <|user|>
                        ->Give three type of opinions(in one line) about the context with emojis in one points:- 1.positive 2.neutral 3.negative </s>
                 <|assistant|>
                """
           prompt.append(prompts2)
           prompts3 = f"""
                 <|system|>
                       {text}</s>
                 <|user|>
                        ->tell the news category it belongs to.
                        ->detect appropriate sentiments:
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
                        ->tell the language of the context.
                        ->tell the country and place news belongs to. </s>
                 <|assistant|>
                """
           prompt.append(prompts3)
           prompts4 = f"""
                 <|system|>
                       {text}</s>
                 <|user|>
                        ->Give Main persons in the news.
                        ->Ask a thinkable question in one line. </s>
                 <|assistant|>
                """
           prompt.append(prompts4)
           return prompt
        if language == "ta":
           language = "Tamil"
           return language
        if language == "bn":
           language = "Bengali"
           return language
        if language == "gu":
           language = "Gujarati"
           return language


def get_summary(request):
    if request.method == 'GET':
        try:
            news_url = request.GET.get('url')
            
            loader = NewsURLLoader(urls=[news_url])
            data = loader.load()
            hi = data[0].page_content
            text_to_detect = f"""{hi}"""
            # print(text_to_detect)
            prompts = output(text_to_detect)
            # print(prompts)
            # print(prompts[1])
            data = {
                "prompt": prompts[0],
                "max_tokens": 200,
                "temperature": 0.5,
                "top_p": 0.9,
                "guidance_scale" : 1,
                "repetition_penalty" : 1.15,
                "top_k": 15
            }

            headers = {
                'Content-Type': 'application/json'
            }

            # Making the POST request
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


def get_opinions(request):
    if request.method == 'GET':
        try:
            news_url = request.GET.get('url')
            
            loader = NewsURLLoader(urls=[news_url])
            data = loader.load()
            hi = data[0].page_content
            text_to_detect = f"""{hi}"""
            # print(text_to_detect)
            prompts = output(text_to_detect)
            # print(prompts)
            # print(prompts[1])
            data = {
                "prompt": prompts[1],
                "max_tokens": 200,
                "temperature": 0.5,
                "top_p": 0.9,
                "guidance_scale" : 1,
                "repetition_penalty" : 1.15,
                "top_k": 15
            }

            headers = {
                'Content-Type': 'application/json'
            }

            # Making the POST request
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

def get_info(request):
    if request.method == 'GET':
        try:
            news_url = request.GET.get('url')
            
            loader = NewsURLLoader(urls=[news_url])
            data = loader.load()
            hi = data[0].page_content
            text_to_detect = f"""{hi}"""
            # print(text_to_detect)
            prompts = output(text_to_detect)
            # print(prompts)
            # print(prompts[1])
            data = {
                "prompt": prompts[2],
                "max_tokens": 200,
                "temperature": 0.5,
                "top_p": 0.9,
                "guidance_scale" : 1,
                "repetition_penalty" : 1.15,
                "top_k": 15
            }

            headers = {
                'Content-Type': 'application/json'
            }

            # Making the POST request
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


def get_question(request):
    if request.method == 'GET':
        try:
            news_url = request.GET.get('url')
            
            loader = NewsURLLoader(urls=[news_url])
            data = loader.load()
            hi = data[0].page_content
            text_to_detect = f"""{hi}"""
            # print(text_to_detect)
            prompts = output(text_to_detect)
            # print(prompts)
            # print(prompts[1])
            data = {
                "prompt": prompts[3],
                "max_tokens": 200,
                "temperature": 0.5,
                "top_p": 0.9,
                "guidance_scale" : 1,
                "repetition_penalty" : 1.15,
                "top_k": 15
            }

            headers = {
                'Content-Type': 'application/json'
            }

            # Making the POST request
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


