from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .forms import FileUploadForm

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            with open('myapp/uploads/' + file.name, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            return render(request, 'upload_success.html')
    else:
        form = FileUploadForm()
        return render(request, 'upload_file.html', {'form': form})