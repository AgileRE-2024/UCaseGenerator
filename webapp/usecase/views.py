import json
import os
import subprocess
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from pyexpat import features

from .models import (  # Pastikan model ActorFeature sudah ada di models.py
    ActorFeature, FeatureConnection, UseCase)


# View untuk menampilkan file PNG
def serve_use_case_diagram(request):
    diagram_path = settings.BASE_DIR / 'tools' / 'use_case_diagram.png'
    
    if os.path.exists(diagram_path):
        return FileResponse(open(diagram_path, 'rb'), content_type='image/png')
    else:
        raise Http404("Diagram not found.")


def UseCaseDiagram(request):
    # Kosongkan fitur saat GET request (awal membuka halaman)
    features = []

    # Jika ada POST request untuk menyimpan data, ambil fitur dari database
    if request.method == "POST":
        features = list(ActorFeature.objects.values_list('feature_name', flat=True).distinct())
        print("Features available after POST:", features)  # Log untuk debugging

    context = {
        'features': features,
        'nama': 'hello world',
    }
    print("Context features:", context['features'])  # Log untuk debugging
    return render(request, 'use_case_diagram_page/UseCaseDiagram.html', context)

def use_case_result(request):
    if request.method == 'POST':
        actor_data = []
        features = []
        feature_connections = []

        # Proses input aktor dan fitur
        for key, value in request.POST.items():
            if 'actor' in key and value:  # Ambil data aktor
                actor_id = key.replace('actor', '')
                current_features = [
                    request.POST.get(f'feature{actor_id}_{i}')
                    for i in range(1, 10)
                    if request.POST.get(f'feature{actor_id}_{i}')
                ]
                for feature in current_features:
                    ActorFeature.objects.create(actor_name=value, feature_name=feature)
                    actor_data.append((value, feature))
                    features.append(feature)

        # Proses relasi antar fitur
        feature_start_list = request.POST.getlist('feature-start[]')
        feature_end_list = request.POST.getlist('feature-end[]')
        relation_type_list = request.POST.getlist('relation-type[]')

        for start, end, relation in zip(feature_start_list, feature_end_list, relation_type_list):
            if start and end:
                connection = FeatureConnection.objects.create(
                    feature_start=start,
                    feature_end=end,
                    relation_type=relation
                )
                feature_connections.append({
                    'feature_start': connection.feature_start,
                    'feature_end': connection.feature_end,
                    'relation_type': connection.relation_type,
                })

        # Generate diagram dengan PlantUML
        diagram_path = generate_use_case_diagram(actor_data, feature_connections)

        # Menangani path diagram relatif
        if diagram_path:
            # Pastikan diagram_path adalah objek Path
            diagram_path = Path(diagram_path)
            # Pastikan settings.BASE_DIR adalah objek Path
            if isinstance(settings.BASE_DIR, str):
                settings.BASE_DIR = Path(settings.BASE_DIR)
            diagram_path = str(diagram_path.relative_to(settings.BASE_DIR))
        else:
            diagram_path = None

        # Menangani AJAX request (misalnya jika menggunakan JS untuk mengupdate tanpa reload)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Data Berhasil Disimpan!',
                'diagram_path': diagram_path,
                'features': features,
                'feature_connections': feature_connections,
            })

        # Render hasil diagram ke template
        context = {
            'actor_data': actor_data,
            'diagram_path': diagram_path,
            'features': features,
            'feature_connections': feature_connections,
        }
        return render(request, 'use_case_diagram_page/use_case_result.html', context)

    # Jika request bukan POST, tampilkan halaman default
    return render(request, 'use_case_diagram_page/use_case_result.html', {'nama': 'hello world'})

# Fungsi untuk menghasilkan diagram PlantUML
def generate_use_case_diagram(actor_data, feature_connections):
    uml_code = '@startuml\n'
    uml_code += 'left to right direction\n'
    uml_code += 'skinparam packageStyle rectangle\n\n'

    # Tambahkan aktor
    actors = {actor for actor, _ in actor_data}
    for actor in actors:
        uml_code += f'actor {actor}\n'

    # Tambahkan package untuk use case
    uml_code += 'rectangle usecase {\n'
    for _, feature in actor_data:
        uml_code += f'  ({feature})\n'
    uml_code += '}\n\n'

    # Relasi antara aktor dan use case
    for actor, feature in actor_data:
        uml_code += f'{actor} -- ({feature})\n'

    # Relasi antar fitur
    for connection in feature_connections:
        feature_start = connection['feature_start']
        feature_end = connection['feature_end']
        relation = connection['relation_type']
        if relation == 'include':
            uml_code += f'({feature_start}) .> ({feature_end}) : include\n'
        elif relation == 'extend':
            uml_code += f'({feature_start}) .> ({feature_end}) : extend\n'

    uml_code += '@enduml'

    # Simpan kode UML dan generate diagram
    plantuml_file_path = os.path.join(settings.BASE_DIR, 'tools', 'use_case_diagram.puml')
    diagram_output_path = os.path.join(settings.BASE_DIR, 'tools', 'use_case_diagram.png')

    try:
        # Tulis file .puml
        with open(plantuml_file_path, 'w', encoding='utf-8') as file:
            file.write(uml_code)

        # Generate file PNG menggunakan PlantUML
        command = [
            'java', '-jar', os.path.join(settings.BASE_DIR, 'tools', 'plantuml-mit-1.2024.7.jar'),
            plantuml_file_path
        ]
        subprocess.run(command, check=True)

        # Pastikan file PNG berhasil dibuat
        if os.path.exists(diagram_output_path):
            return diagram_output_path
        else:
            print("Diagram generation failed: output file not found.")
            return None

    except subprocess.CalledProcessError as e:
        print(f"Error during PlantUML execution: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    
def save_feature_connection(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        feature_starts = data.get('feature_starts', [])
        feature_ends = data.get('feature_ends', [])
        relation_types = data.get('relation_types', [])

        saved_connections = []
        for start, end, relation in zip(feature_starts, feature_ends, relation_types):
            if start and end:
                connection = FeatureConnection.objects.create(
                    feature_start=start,
                    feature_end=end,
                    relation_type=relation
                )
                saved_connections.append(connection)

        return JsonResponse({
            'status': 'success',
            'message': 'Feature connections saved successfully!',
            'connections': [{'start': c.feature_start, 'end': c.feature_end, 'relation_type': c.relation_type} for c in saved_connections]
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def Specification(request):
    context = {
        'nama': 'hello world',
    }
    return render(request, 'use_case_specification_page/Specification.html', context)


def use_case_output(request):
    # Ambil semua fitur unik dari database
    features = ActorFeature.objects.values_list('feature_name', flat=True).distinct()

    context = {
        'features': features,
    }

    return render(request, 'use_case_diagram_page/use_case_result.html', context)


def output_activity(request):
    return render(request, 'output-activity.html')


def input_class(request):
    return render(request, 'class_diagram_page/inputClass.html')


def input_sequence(request):
    return render(request, 'sequence_diagram_page/inputsequence.html')


def output_class(request):
    return render(request, 'class_diagram_page/outputclass.html')


def output_sequence(request):
    return render(request, 'sequence_diagram_page/outputsequence.html')
