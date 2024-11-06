import os
import subprocess

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from .models import ActorFeature  # Import model ActorFeature Anda


def UseCaseDiagram(request):
    # Ambil semua fitur unik dari model ActorFeature
    features = list(ActorFeature.objects.values_list('feature_name', flat=True).distinct())
    print("Features available:", features)  # Log untuk debugging

    context = {
        'features': features,
        'nama': 'hello world',
    }

    # Cetak untuk memeriksa apakah 'context' memiliki data yang benar
    print("Context features:", context['features'])  # Log untuk debugging

    return render(request, 'use case diagram page/UseCaseDiagram.html', context)

def use_case_result(request):
    if request.method == 'POST':
        actor_data = []
        for key, value in request.POST.items():
            if 'actor' in key and value:
                actor_id = key.replace('actor', '')
                features = [
                    request.POST.get(f'feature{actor_id}_{i}') 
                    for i in range(1, 10)
                    if request.POST.get(f'feature{actor_id}_{i}')
                ]
                for feature in features:
                    ActorFeature.objects.create(actor_name=value, feature_name=feature)
                    actor_data.append((value, feature))

        # Menghasilkan diagram PlantUML
        diagram_path = generate_use_case_diagram(actor_data)

        # Mengambil fitur terbaru
        features = list(ActorFeature.objects.values_list('feature_name', flat=True).distinct())

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Data berhasil disimpan!', 'features': features, 'diagram_path': diagram_path})

        context = {
            'actor_data': actor_data,
            'diagram_path': diagram_path,
            'nama': 'hello world',
        }
        return render(request, 'use case diagram page/use_case_result.html', context)

    return render(request, 'use case diagram page/use_case_result.html', {'nama': 'hello world'})

def generate_use_case_diagram(actor_data):
    # Menghasilkan kode PlantUML berdasarkan actor_data
    uml_code = '@startuml\n'
    for actor, feature in actor_data:
        uml_code += f'actor "{actor}" as {actor}\n'
        uml_code += f'{actor} --> "{feature}"\n'
    uml_code += '@enduml'

    # Path dinamis untuk file PlantUML dan output diagram
    plantuml_file_path = settings.BASE_DIR / 'tools' / 'use_case_diagram.puml'
    diagram_output_path = settings.BASE_DIR / 'tools' / 'use_case_diagram.png'

    # Simpan file PlantUML
    with open(plantuml_file_path, 'w') as f:
        f.write(uml_code)

    print(f"PlantUML file created at: {plantuml_file_path}")

    # Jalankan PlantUML untuk menghasilkan diagram
    try:
        result = subprocess.run(['java', '-jar', 'D:/SEMESTER 5/PPL Prak/MINGGU 7/Generate/Generate/webapp/tools/plantuml.jar', str(plantuml_file_path)],
                                check=True, capture_output=True, text=True)
        print("PlantUML executed successfully.")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error generating diagram:", e)
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return None

    # Periksa apakah file output ada
    if diagram_output_path.exists():
        print("Diagram generated successfully:", diagram_output_path)
        return diagram_output_path
    else:
        print("Diagram generation failed: PNG file not found.")
        return None


def Specification(request):
    context = {
        'nama': 'hello world',
    }
    return render(request, 'use case specification page/Specification.html', context)

def output_activity(request):
    return render(request, 'output-activity.html')

def input_class(request):
    return render(request, 'class diagram page/inputClass.html')

def input_sequence(request):
    return render(request, 'sequence diagram page/inputsequence.html')

def output_class(request):
    return render(request, 'class diagram page/outputclass.html')

def output_sequence(request):
    return render(request, 'sequence diagram page/outputsequence.html')
