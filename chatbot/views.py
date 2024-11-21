from django.shortcuts import render
from django.http import JsonResponse
import openai
from django.utils import timezone
import random
from .models import Chats
import requests

# Set OpenAI API key
openai.api_key = "3887c25909msheabfa8ed70bf98ep14f9b8jsn0f24d3cd6aa3"

def askOpenAI(message):
    url = "https://chatgpt-42.p.rapidapi.com/conversationgpt4-2"
    
    payload = {
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ],
        "system_prompt": "",
        "temperature": 0.9,
        "top_k": 5,
        "top_p": 0.9,
        "max_tokens": 256,
        "web_access": False
    }
    headers = {
        "x-rapidapi-key": "3887c25909msheabfa8ed70bf98ep14f9b8jsn0f24d3cd6aa3",
        "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        answer = response.json()
        return answer['result']
    except Exception as e:
        print(f"Error: {e}")
        return "I'm sorry, but I'm having trouble responding right now."

def index(request):
    return render(request, 'chat.html')

def chat(request):
    all_chats = Chats.objects.all().order_by("-created_time")
    return render(request, 'chat.html', {"chats": all_chats[:3][::-1]})

def chatbot(request):
    return render(request, 'chat.html')

def chatbot_response(request):
    if request.method == "POST":
        message = request.POST.get("message", "")
        if not message:
            return JsonResponse({"error": "No message provided"}, status=400)

        response_text = askOpenAI(message)
        
        # Save chat history to database
        chat = Chats(message=message, response=response_text, created_time=timezone.now())
        chat.save()
        
       
        
        return JsonResponse({
            "message": message,
            "response": response_text,
        })
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
