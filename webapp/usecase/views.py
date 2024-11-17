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
    # Ambil semua fitur unik dari model ActorFeature
    features = list(ActorFeature.objects.values_list('feature_name', flat=True).distinct())
    print("Features available:", features)  # Log untuk debugging

    context = {
        'features': features,
        'nama': 'hello world',
    }
    print("Context features:", context['features'])  # Log untuk debugging
    return render(request, 'use_case_diagram_page/UseCaseDiagram.html', context)


# def use_case_result(request):
#     if request.method == 'POST':
#         actor_data = []
#         features = []  # Menyimpan fitur yang baru diinputkan
#         feature_connections = []  # Menyimpan koneksi antar fitur

#         # Tangani data aktor dan fitur
#         for key, value in request.POST.items():
#             if 'actor' in key and value:
#                 actor_id = key.replace('actor', '')
#                 current_features = [
#                     request.POST.get(f'feature{actor_id}_{i}')
#                     for i in range(1, 10)
#                     if request.POST.get(f'feature{actor_id}_{i}')
#                 ]

#                 for feature in current_features:
#                     ActorFeature.objects.create(actor_name=value, feature_name=feature)
#                     actor_data.append((value, feature))
#                     features.append(feature)  # Menambahkan fitur baru ke list

#         # Tangani koneksi fitur (feature connections)
#         feature_start_list = request.POST.getlist('feature-start[]')
#         feature_end_list = request.POST.getlist('feature-end[]')

#         for start, end in zip(feature_start_list, feature_end_list):
#             if start and end:
#                 FeatureConnection.objects.create(feature_start=start, feature_end=end)
#                 feature_connections.append(FeatureConnection(feature_start=start, feature_end=end))

#         # Generate diagram
#         diagram_path = generate_use_case_diagram(actor_data, feature_connections)

#         # Pastikan diagram_path menjadi objek Path
#         if diagram_path:
#             diagram_path = Path(diagram_path)

#         # Mengembalikan JSON response jika ini adalah AJAX request
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#             return JsonResponse({
#                 'status': 'success',
#                 'message': 'Data berhasil disimpan!',
#                 'features': features,
#                 'feature_connections': feature_connections,
#                 'diagram_path': str(diagram_path.relative_to(settings.BASE_DIR)) if diagram_path else None
#             })

#         context = {
#             'actor_data': actor_data,
#             'diagram_path': str(diagram_path.relative_to(settings.BASE_DIR)) if diagram_path else None,
#             'features': features,
#             'feature_connections': feature_connections,
#         }
#         return render(request, 'use_case_diagram_page/use_case_result.html', context)

#     return render(request, 'use_case_diagram_page/use_case_result.html', {'nama': 'hello world'})

def use_case_result(request):
    if request.method == 'POST':
        actor_data = []
        features = []  # Menyimpan fitur yang baru diinputkan
        feature_connections = []  # Menyimpan koneksi antar fitur

        # Tangani data aktor dan fitur
        for key, value in request.POST.items():
            if 'actor' in key and value:
                actor_id = key.replace('actor', '')
                current_features = [
                    request.POST.get(f'feature{actor_id}_{i}')
                    for i in range(1, 10)
                    if request.POST.get(f'feature{actor_id}_{i}')
                ]

                for feature in current_features:
                    ActorFeature.objects.create(actor_name=value, feature_name=feature)
                    actor_data.append((value, feature))
                    features.append(feature)  # Menambahkan fitur baru ke list

        # Tangani koneksi fitur (feature connections)
        feature_start_list = request.POST.getlist('feature-start[]')
        feature_end_list = request.POST.getlist('feature-end[]')

        for start, end in zip(feature_start_list, feature_end_list):
            if start and end:
                connection = FeatureConnection.objects.create(feature_start=start, feature_end=end)
                feature_connections.append({
                    'feature_start': connection.feature_start,
                    'feature_end': connection.feature_end,
                })

        # Generate diagram
        diagram_path = generate_use_case_diagram(actor_data, feature_connections)

        # Pastikan diagram_path menjadi objek Path
        if diagram_path:
            diagram_path = Path(diagram_path)

        # Mengembalikan JSON response jika ini adalah AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Data berhasil disimpan!',
                'features': features,
                'feature_connections': feature_connections,
                'diagram_path': str(diagram_path.relative_to(settings.BASE_DIR)) if diagram_path else None
            })

        context = {
            'actor_data': actor_data,
            'diagram_path': str(diagram_path.relative_to(settings.BASE_DIR)) if diagram_path else None,
            'features': features,
            'feature_connections': feature_connections,
        }
        return render(request, 'use_case_diagram_page/use_case_result.html', context)

    return render(request, 'use_case_diagram_page/use_case_result.html', {'nama': 'hello world'})



def generate_use_case_diagram(actor_data, feature_connections):
    # Generate PlantUML code based on actor_data and feature_connections
    uml_code = '@startuml\n'
    
    # Menentukan layout dari kiri ke kanan
    uml_code += 'left to right direction\n'

    # Menambahkan package untuk fitur (use case)
    uml_code += 'package "usecase" {\n'
    for actor, feature in actor_data:
        uml_code += f'usecase "{feature}" as UC_{feature.replace(" ", "_")}\n'
    uml_code += '}\n'

    # Menambahkan koneksi antara aktor dan use case
    for actor, feature in actor_data:
        uml_code += f'{actor} --> "UC_{feature.replace(" ", "_")}"\n'

    # Menambahkan koneksi antar fitur
    for connection in feature_connections:
        # Periksa apakah connection adalah instance model atau dictionary
        feature_start = (
            connection.feature_start if hasattr(connection, 'feature_start') else connection['feature_start']
        )
        feature_end = (
            connection.feature_end if hasattr(connection, 'feature_end') else connection['feature_end']
        )
        uml_code += f'"UC_{feature_start.replace(" ", "_")}" --> "UC_{feature_end.replace(" ", "_")}"\n'
    
    uml_code += '@enduml'

    # Path untuk file PlantUML dan output diagram
    plantuml_file_path = os.path.join(settings.BASE_DIR, 'tools', 'use_case_diagram.puml')
    diagram_output_path = os.path.join(settings.BASE_DIR, 'tools', 'use_case_diagram.png')

    try:
        # Simpan kode UML ke dalam file .puml
        with open(plantuml_file_path, 'w', encoding='utf-8') as file:
            file.write(uml_code)

        # Jalankan perintah PlantUML untuk membuat file PNG
        command = [
            'java', '-jar', os.path.join(settings.BASE_DIR, 'tools', 'plantuml-mit-1.2024.7.jar'),
            plantuml_file_path
        ]
        subprocess.run(command, check=True)

        # Pastikan diagram berhasil dibuat
        if os.path.exists(diagram_output_path):
            return diagram_output_path
        else:
            print("Diagram generation failed: output file not found.")
            return None

    except subprocess.CalledProcessError as e:
        print(f"Error occurred during PlantUML execution: {e}")
        return None
    except IOError as e:
        print(f"Error writing to file: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    
def save_feature_connection(request):
    if request.method == 'POST':
        # Parse JSON request body
        data = json.loads(request.body)

        feature_starts = data.get('feature_starts', [])
        feature_ends = data.get('feature_ends', [])

        # Proses untuk menyimpan koneksi fitur
        saved_connections = []
        for start, end in zip(feature_starts, feature_ends):
            if start and end:
                connection = FeatureConnection.objects.create(
                    feature_start=start,
                    feature_end=end
                )
                saved_connections.append(connection)

        return JsonResponse({
            'status': 'success',
            'message': 'Feature connections saved successfully!',
            'connections': [{'start': c.feature_start, 'end': c.feature_end} for c in saved_connections]
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
