import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from django.shortcuts import render
from .forms import CSVUploadForm

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            
            uploaded_file = request.FILES['csv_file']
            
            df = pd.read_csv(uploaded_file)

            
            data_summary = df.describe()  
            missing_values = df.isnull().sum()  

            
            numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            histograms = []
            for column in numerical_columns:
                plt.figure()
                sns.histplot(df[column].dropna(), kde=True)
                plt.title(f'Histogram of {column}')
                plt.xlabel(column)
                plt.ylabel('Frequency')
                plt.tight_layout()
                histogram_img = get_img_from_plt()
                histograms.append(histogram_img)

            
            context = {
                'form': form,
                'data_summary': data_summary,
                'missing_values': missing_values,
                'histograms': histograms
            }
            return render(request, 'analysis_results.html', context)
    else:
        form = CSVUploadForm()
    return render(request, 'upload_form.html', {'form': form})

def get_img_from_plt():
    """Helper function to convert matplotlib plot to image."""
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()
