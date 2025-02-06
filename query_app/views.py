from django.shortcuts import render

# query_app/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .query import ask_question_from_pdf  # Import the function

@csrf_exempt
def ask_question(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request
            data = json.loads(request.body)
            question = data.get('question')
            pdf_path = "Sixd Details.pdf"  # Path to your PDF file

            # Call the function to get the answer from LLaMA
            answer = ask_question_from_pdf(pdf_path, question)

            # Return the answer as a JSON response
            return JsonResponse({'answer': answer})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)