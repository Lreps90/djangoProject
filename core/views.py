from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
import subprocess
import os
from django.http import JsonResponse

# Home view to render index.html
def home(request):
    return render(request, 'index.html')

# Code editor view to render code_editor.html
def code_editor(request):
    return render(request, 'code_editor.html')




def save_data(request):
    if request.method == 'POST':
        message = request.POST.get('message')  # Get the message from the request
        with open('saved_messages.txt', 'a') as file:
            file.write(message + "\n")
        return JsonResponse({'response': 'Message saved successfully!'})
    return JsonResponse({'response': 'Invalid request'}, status=400)



# Download the file with saved messages
def download_file(request):
    file_path = 'saved_messages.txt'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=saved_messages.txt'
            return response
    return HttpResponse('No file found to download', status=404)

# Stream code execution output
def run_code_stream(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        user_inputs = request.POST.getlist('user_inputs[]')

        # Replace occurrences of input() with provided user inputs
        input_counter = 0
        while 'input(' in code and input_counter < len(user_inputs):
            code = code.replace('input(', f'"{user_inputs[input_counter]}" # input ', 1)
            input_counter += 1

        # Save the user code to a temporary file
        with open('temp_code.py', 'w') as f:
            f.write(code)

        def generate_output():
            try:
                process = subprocess.Popen(['python', 'temp_code.py'],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           text=True)
                # Stream output line by line
                for line in iter(process.stdout.readline, ''):
                    yield f"data: {line.strip()}\n\n"

                # Capture any error output
                error_output = process.stderr.read()
                if error_output:
                    yield f"data: Error:\n{error_output}\n\n"
            except Exception as e:
                yield f"data: Error: {str(e)}\n\n"

            if os.path.exists("temp_code.py"):
                os.remove("temp_code.py")

        return StreamingHttpResponse(generate_output(), content_type='text/event-stream')

