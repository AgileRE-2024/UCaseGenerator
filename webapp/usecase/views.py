from ast import Attribute
from datetime import datetime
from io import StringIO
import json
import logging
import os
from pyclbr import Class
from sqlite3 import Connection
import subprocess
from pathlib import Path
from typing import OrderedDict, Sequence

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from pyexpat import features

from .models import *
# View untuk menampilkan file PNG
def serve_use_case_diagram(request):
    diagram_path = settings.BASE_DIR / 'tools' / 'use_case_diagram.png'
    
    if os.path.exists(diagram_path):
        return FileResponse(open(diagram_path, 'rb'), content_type='image/png')
    else:
        raise Http404("Diagram not found.")

def use_case_result(request):
    if request.method == 'POST':
        actor_data = []
        features = []
        feature_connections = []

        try:
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

            # Hilangkan duplikat fitur sambil menjaga urutan
            unique_features = list(OrderedDict.fromkeys(features))

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
                diagram_path = Path(diagram_path)
                if isinstance(settings.BASE_DIR, str):
                    settings.BASE_DIR = Path(settings.BASE_DIR)
                diagram_path = str(diagram_path.relative_to(settings.BASE_DIR))
            else:
                diagram_path = None

            # Menangani AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Data Berhasil Disimpan!',
                    'diagram_path': diagram_path,
                    'features': unique_features,
                    'feature_connections': feature_connections,
                })

            # Render hasil diagram ke template
            context = {
                'actor_data': actor_data,
                'diagram_path': diagram_path,
                'features': unique_features,
                'feature_connections': feature_connections,
            }
            return render(request, 'use_case_diagram_page/use_case_result.html', context)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

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


def save_feature_connection(request):
    if request.method == 'POST':
        # Parse JSON request body
        data = json.loads(request.body)

        feature_starts = data.get('feature_starts', [])
        feature_ends = data.get('feature_ends', [])
        relation_types = data.get('relation_types', [])  # Ambil relasi baru

        # Proses untuk menyimpan koneksi fitur
        saved_connections = []
        for start, end, relation in zip(feature_starts, feature_ends, relation_types):
            if start and end:
                connection = FeatureConnection.objects.create(
                    feature_start=start,
                    feature_end=end,
                    relation_type=relation  # Simpan relasi di database
                )
                saved_connections.append({
                    'start': connection.feature_start,
                    'end': connection.feature_end,
                    'relation': connection.relation_type
                })

        return JsonResponse({
            'status': 'success',
            'message': 'Feature connections saved successfully!',
            'connections': saved_connections
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


def use_case_output(request):
    # Ambil semua fitur unik dari database
    features = ActorFeature.objects.values_list('feature_name', flat=True).distinct()

    context = {
        'features': features,
    }

    return render(request, 'use_case_diagram_page/use_case_result.html', context)


# --------------------------------------------------------------------------------------SPECIFICATION-------------------------------------------------------------------------------------------------

def save_specification(request):
    if request.method == "POST":
        # Ambil data dari form
        use_case_name = request.POST.get('use_case_name')
        actor = request.POST.get('actor')
        summary_description = request.POST.get('summary_description')
        pre_conditions = request.POST.get('pre_conditions')
        post_conditions = request.POST.get('post_conditions')

        # Ambil langkah-langkah yang ada
        basic_actor_steps = request.POST.getlist('basic_actor_step[]')
        basic_system_steps = request.POST.getlist('basic_system_step[]')

        alternative_actor_steps = request.POST.getlist('alternative_actor_step[]')
        alternative_system_steps = request.POST.getlist('alternative_system_step[]')

        exception_actor_steps = request.POST.getlist('exception_actor_step[]')
        exception_system_steps = request.POST.getlist('exception_system_step[]')

        # Simpan data ke UseCaseSpecification
        specification = UseCaseSpecification(
            use_case_name=use_case_name,
            actor=actor,
            summary_description=summary_description,
            pre_conditions=pre_conditions,
            post_conditions=post_conditions
        )
        specification.save()

        # Menyimpan Basic Path steps
        for actor_step, system_step in zip(basic_actor_steps, basic_system_steps):
            BasicPath.objects.create(
                use_case_specification=specification,
                basic_actor_step=actor_step,
                basic_system_step=system_step
            )

        # Menyimpan Alternative Path steps
        for actor_step, system_step in zip(alternative_actor_steps, alternative_system_steps):
            AlternativePath.objects.create(
                use_case_specification=specification,
                alternative_actor_step=actor_step,
                alternative_system_step=system_step
            )

        # Menyimpan Exception Path steps
        for actor_step, system_step in zip(exception_actor_steps, exception_system_steps):
            ExceptionPath.objects.create(
                use_case_specification=specification,
                exception_actor_step=actor_step,
                exception_system_step=system_step
            )

        # Redirect setelah berhasil
        return redirect('output_activity', specification_id=specification.specification_id)



    # Menambahkan template_name yang hilang
    return render(request, 'use_case_specification/Specification.html')  # Tampilkan form jika GET request


def generate_activity_diagram(specification_id):
    # Ambil data dari BasicPath dan AlternativePath
    basic_paths = BasicPath.objects.filter(use_case_specification_id=specification_id)
    alternative_paths = AlternativePath.objects.filter(use_case_specification_id=specification_id)

    # Menentukan Loop Start dan Loop End
    loop_start = None
    loop_end = None

    # Cari Loop Start
    for alternative_path in alternative_paths:
        if any(
            (alternative_path.alternative_actor_step.strip() == basic_path.basic_actor_step.strip() and alternative_path.alternative_actor_step.strip())
            or (alternative_path.alternative_system_step.strip() == basic_path.basic_system_step.strip() and alternative_path.alternative_system_step.strip())
            for basic_path in basic_paths
        ):
            loop_start = alternative_path
            break

    # Loop End: Langkah terakhir dari Alternative Path
    if alternative_paths.exists():
        loop_end = alternative_paths.last()

    # Log untuk debugging
    print(f"Basic Path steps:")
    for basic_path in basic_paths:
        print(f"- {basic_path.basic_actor_step} | {basic_path.basic_system_step}")

    print(f"Alternative Path steps:")
    for alternative_path in alternative_paths:
        print(f"- {alternative_path.alternative_actor_step} | {alternative_path.alternative_system_step}")

    if loop_start:
        print(f"Loop start found: {loop_start.alternative_actor_step or loop_start.alternative_system_step}")
    else:
        print("Warning: Loop start not found.")

    if loop_end:
        print(f"Loop end found: {loop_end.alternative_actor_step or loop_end.alternative_system_step}")
    else:
        print("Warning: Loop end not found.")

    # Membuat UML string
    uml_code = "@startuml\n"
    uml_code += "|Aktor|\n"
    uml_code += "start\n\n"

    # Tambahkan langkah BasicPath sebelum loop_start
    for basic_path in basic_paths:
        if basic_path.basic_actor_step:
            uml_code += "|Aktor|\n"
            uml_code += f":{basic_path.basic_actor_step};\n"
        if basic_path.basic_system_step:
            uml_code += "|Sistem|\n"
            uml_code += f":{basic_path.basic_system_step};\n"

        # Ketika mencapai loop_end, tambahkan blok repeat
        if loop_end and (
            basic_path.basic_actor_step == loop_end.alternative_actor_step or
            basic_path.basic_system_step == loop_end.alternative_system_step
        ):
            # Tentukan swimlane berdasarkan langkah loop_end
            if loop_end.alternative_actor_step == basic_path.basic_actor_step:
                uml_code += "|Aktor|\n"  # Jika loop_end di aktor
            elif loop_end.alternative_system_step == basic_path.basic_system_step:
                uml_code += "|Sistem|\n"  # Jika loop_end di sistem

            # Tambahkan langkah loop_end di swimlane yang sesuai
            loop_end_step = loop_end.alternative_actor_step or loop_end.alternative_system_step
            uml_code += "|Aktor|\n"

            # Tambahkan blok repeat
            uml_code += f"repeat :{loop_end_step};\n"
            break


   # Tambahkan langkah-langkah AlternativePath untuk backward
    if alternative_paths.exists():
        for i, alternative_path in enumerate(alternative_paths):
            # Langkah kedua sampai sebelum terakhir (tidak pertama dan tidak terakhir)
            uml_code += "|Sistem|\n"
            if i > 0 and i < len(alternative_paths) - 1:
                if alternative_path.alternative_actor_step:
                    uml_code += f"backward :{alternative_path.alternative_actor_step};\n"
                if alternative_path.alternative_system_step:
                    uml_code += f"backward :{alternative_path.alternative_system_step};\n"
        
        # Tambahkan pernyataan repeat while jika loop_start ada
        if loop_start:
            loop_step = (
                loop_start.alternative_actor_step
                or loop_start.alternative_system_step
            )
            
            uml_code += "|Sistem|\n"
            uml_code += f"repeat while ({loop_step}) is (no)\n\n"


    # Tambahkan langkah BasicPath setelah loop_start hingga akhir
    after_loop = False  # Flag untuk menandai langkah setelah loop_start
    for basic_path in basic_paths:
        # Tambahkan langkah setelah loop_start
        if after_loop:
            if basic_path.basic_actor_step:
                uml_code += "|Aktor|\n"
                uml_code += f":{basic_path.basic_actor_step};\n"
            if basic_path.basic_system_step:
                uml_code += "|Sistem|\n"
                uml_code += f":{basic_path.basic_system_step};\n"
        # Periksa jika sudah mencapai loop_start
        if (
            loop_start
            and (basic_path.basic_actor_step == loop_start.alternative_actor_step
                or basic_path.basic_system_step == loop_start.alternative_system_step)
        ):
            after_loop = True

    # Akhiri diagram
    uml_code += "stop\n"
    uml_code += "@enduml"

    # Path file untuk PlantUML dan output diagram
    plantuml_file_path = Path(settings.BASE_DIR) / 'tools' / 'activity_diagram.puml'
    diagram_output_path = Path(settings.BASE_DIR) / 'tools' / 'activity_diagram.png'

    try:
        # Simpan kode UML ke file .puml
        with open(plantuml_file_path, 'w', encoding='utf-8') as file:
            file.write(uml_code)

        # Jalankan perintah PlantUML untuk membuat file PNG
        command = [
            'java', '-jar', str(Path(settings.BASE_DIR) / 'tools' / 'plantuml-mit-1.2024.7.jar'),
            str(plantuml_file_path)
        ]
        subprocess.run(command, check=True)

        # Periksa apakah file PNG berhasil dibuat
        if diagram_output_path.exists():
            return str(diagram_output_path)
        else:
            print("Diagram generation failed: output file not found.")
            return None

    except subprocess.CalledProcessError as e:
        print(f"Error occurred during PlantUML execution: {e}")
        return None
    except IOError as e:
        print(f"Error writing to file: {e}")
        return None
    
    # View untuk menampilkan file PNG
def serve_activity_diagram(request):
    diagram_path = settings.BASE_DIR / 'tools' / 'activity_diagram.png'
    
    if os.path.exists(diagram_path):
        return FileResponse(open(diagram_path, 'rb'), content_type='image/png')
    else:
        raise Http404("Diagram not found.")


def Specification(request):
    context = {
        'nama': 'hello world',
    }
    return render(request, 'use_case_specification_page/Specification.html', context)


def use_case_output(request):
    # Ambil semua fitur unik dari database
    features = ActorFeature.objects.values_list('feature_name', flat=True).distinct()

def save_feature_connection(request):
    if request.method == 'POST':
        # Parse JSON request body
        data = json.loads(request.body)

        feature_starts = data.get('feature_starts', [])
        feature_ends = data.get('feature_ends', [])
        relation_types = data.get('relation_types', [])  # Ambil relasi baru

        # Proses untuk menyimpan koneksi fitur
        saved_connections = []
        for start, end, relation in zip(feature_starts, feature_ends, relation_types):
            if start and end:
                connection = FeatureConnection.objects.create(
                    feature_start=start,
                    feature_end=end,
                    relation_type=relation  # Simpan relasi di database
                )
                saved_connections.append({
                    'start': connection.feature_start,
                    'end': connection.feature_end,
                    'relation': connection.relation_type
                })

        return JsonResponse({
            'status': 'success',
            'message': 'Feature connections saved successfully!',
            'connections': saved_connections
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


# -----------------------------------------------------------------ACTIVITY DIAGRAM----------------------------------------------------------

def output_activity(request, specification_id):
    # Generate diagram berdasarkan specification_id
    diagram_path = generate_activity_diagram(specification_id)

    if diagram_path:
        # Tampilkan diagram yang dihasilkan
        context = {'diagram_path': str(Path(diagram_path).relative_to(settings.BASE_DIR))}
        return render(request, 'output-activity.html', context)
    else:
        # Jika gagal, tampilkan pesan error
        return HttpResponse("Failed to generate activity diagram.")


import os
import subprocess
from pathlib import Path
from django.http import JsonResponse, Http404, FileResponse
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

import os
import subprocess
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

def input_sequence(request):
    if request.method == "POST":
        actors = request.POST.getlist('actor')
        boundaries = request.POST.getlist('boundary')
        controllers = request.POST.getlist('controller')
        entities = request.POST.getlist('entity')
        
        # Proses basic path
        basic_path_inputs = request.POST.getlist('basic_path_input')
        basic_paths = []
        
        # Daftar semua elemen yang bisa digunakan
        all_elements = actors + boundaries + controllers + entities
        
        # Proses basic path dengan urutan logis
        for i, basic_path in enumerate(basic_path_inputs):
            if basic_path.strip():  # Abaikan input kosong
                try:
                    if i == 0:
                        # Jalur pertama: actor -> boundary
                        start_element = actors[0] if actors else "Unknown"
                        end_element = boundaries[0] if boundaries else "Unknown"
                    elif i == 1:
                        # Jalur kedua: boundary -> control
                        start_element = boundaries[0] if boundaries else "Unknown"
                        end_element = controllers[0] if controllers else "Unknown"
                    elif i == 2:
                        # Jalur ketiga: control -> entity
                        start_element = controllers[0] if controllers else "Unknown"
                        end_element = entities[0] if entities else "Unknown"
                    else:
                        # Jalur selanjutnya mengulang dari entity -> control atau boundary
                        start_element = entities[min(i-3, len(entities)-1)] if entities else "Unknown"
                        end_element = controllers[min(i-3, len(controllers)-1)] if controllers else "Unknown"

                    # Tambahkan jalur ke daftar basic paths
                    basic_paths.append(f"{start_element} -> {end_element} : {basic_path}")
                except IndexError:
                    # Fallback jika elemen tidak mencukupi
                    basic_paths.append(f"Unknown -> Unknown : {basic_path}")

        # Proses alternative paths
        alternative_path_labels = request.POST.getlist('alternative_path_label')
        alternative_path_inputs = request.POST.getlist('alternative_path_input')
        alternative_paths = []

        # Proses else paths
        else_path_labels = request.POST.getlist('else_path_label')
        else_path_inputs = request.POST.getlist('else_path_input')

        for i in range(len(alternative_path_labels)):
            if alternative_path_labels[i] and alternative_path_inputs[i]:
                start_element = entities[0] if entities else "Unknown"
                end_element = controllers[0] if controllers else "Unknown"

                alt_path = {
                    'title': alternative_path_labels[i],
                    'path': f"{start_element} -> {end_element} : {alternative_path_inputs[i]}",
                    'else_conditions': []
                }

                # Tambahkan else paths
                for j in range(len(else_path_labels)):
                    if else_path_labels[j] and else_path_inputs[j]:
                        else_start = controllers[0] if controllers else "Unknown"
                        else_end = boundaries[0] if boundaries else "Unknown"

                        alt_path['else_conditions'].append({
                            'title': else_path_labels[j],
                            'condition': else_path_inputs[j],
                            'path': f"{else_start} -> {else_end} : {else_path_inputs[j]}"
                        })

                alternative_paths.append(alt_path)



        # Generate script PlantUML
        plantUmlScript = "@startuml\n"

        # Tambahkan elemen hanya sekali
        plantUmlScript += "\n".join([f"actor {actor}" for actor in actors if actor]) + "\n"
        plantUmlScript += "\n".join([f"boundary {boundary}" for boundary in boundaries if boundary]) + "\n"
        plantUmlScript += "\n".join([f"control {controller}" for controller in controllers if controller]) + "\n"
        plantUmlScript += "\n".join([f"entity {entity}" for entity in entities if entity]) + "\n"

        # Tambahkan basic paths
        plantUmlScript += "\n".join(basic_paths) + "\n"

        # Tambahkan alternative paths
        for alt_path in alternative_paths:
            plantUmlScript += f"alt {alt_path['title']}\n"
            plantUmlScript += f"{alt_path['path']}\n"
            for else_condition in alt_path['else_conditions']:
                plantUmlScript += f"else {else_condition['title']}\n"
                plantUmlScript += f"{else_condition['path']}\n"
            plantUmlScript += "end\n"

        plantUmlScript += "@enduml\n"


        # Path file di folder tools
        plantUmlFilePath = os.path.join(settings.BASE_DIR, 'tools', 'sequence_diagram.puml')
        outputPngPath = os.path.join(settings.BASE_DIR, 'tools', 'sequence_diagram.png')

        # Simpan file .puml
        with open(plantUmlFilePath, 'w', encoding='utf-8') as file:
            file.write(plantUmlScript)

        try:
            # Jalankan PlantUML untuk mengenerate PNG
            command = [
                'java', '-jar', str(Path(settings.BASE_DIR) / 'tools' / 'plantuml-mit-1.2024.7.jar'),
                '-tpng', '-overwrite', plantUmlFilePath
            ]
            subprocess.run(command, check=True)

            # Cek apakah file PNG berhasil dibuat
            if os.path.exists(outputPngPath):
                # Simpan URL ke session dan redirect ke halaman output
                request.session['image_url'] = reverse('serve_sequence_diagram')
                return redirect('output_sequence')
            else:
                return JsonResponse({
                    "success": False,
                    "error": "Generated PNG file not found."
                }, status=500)

        except subprocess.CalledProcessError as e:
            logger.error("PlantUML execution error: %s", e)
            return JsonResponse({"success": False, "error": f"PlantUML execution error: {e}"}, status=500)
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return JsonResponse({"success": False, "error": f"Unexpected error: {e}"}, status=500)

    elif request.method == "GET":
        return render(request, 'sequence_diagram/input_sequence_diagram.html')

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)

from django.http import FileResponse, Http404
import os
from django.conf import settings

def serve_sequence_diagram(request):
    # Path ke file dalam direktori tools
    diagram_path = os.path.join(settings.BASE_DIR, 'tools', 'sequence_diagram.png')

    # Cek apakah file ada
    if os.path.exists(diagram_path):
        return FileResponse(open(diagram_path, 'rb'), content_type='image/png')
    else:
        raise Http404("Diagram not found.")



def output_sequence(request):
    # Ambil URL gambar dari session
    image_url = request.session.get('image_url', None)
    return render(request, 'sequence_diagram/output_sequence_diagram.html', {
        'image_url': image_url
    })

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------CLASS DIAGRAM------------------------------------------------------------------

def create_connection(request):
    if request.method == 'POST':
        path_name = request.POST.get('path_name')
        relation = request.POST.get('relation')
        relation_reverse = request.POST.get('relation_reverse')
        class_start_id = request.POST.get('class_start_id')
        class_end_id = request.POST.get('class_end_id')

        # Validasi pilihan relasi
        valid_choices = [choice[0] for choice in Connection.RELATION_CHOICES]
        if relation not in valid_choices or relation_reverse not in valid_choices:
            return JsonResponse({'error': 'Invalid value for relation or relation_reverse'}, status=400)

        # Simpan data ke database
        connection = Connection.objects.create(
            path_name=path_name,
            relation=relation,
            relation_reverse=relation_reverse,
            class_start_id=class_start_id,
            class_end_id=class_end_id,
        )
        return JsonResponse({'message': 'Connection created successfully', 'id': connection.id})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)





from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from pathlib import Path
import subprocess

def input_class_diagram(request):
    if request.method == 'POST':
        logger.info("Received POST request on /inputclass/")  # Log info ketika POST diterima
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received.")  # Log error jika JSON tidak valid
            return JsonResponse({"success": False, "message": "Invalid JSON data."}, status=400)

        connections_data = data.get('connections', [])
        if not connections_data:
            logger.warning("No connections data provided.")  # Log jika data kosong
            return JsonResponse({"success": False, "message": "No connections data provided."}, status=400)

        for connection_data in connections_data:
            path_name = connection_data.get('path_name')
            relation = connection_data.get('relation')
            class_start_id = connection_data.get('class_start_id')
            class_end_id = connection_data.get('class_end_id')
            relation_reverse = connection_data.get('relation_reverse', '')

            # Validasi data sebelum disimpan
            if not path_name or not relation or not class_start_id or not class_end_id:
                logger.warning("Missing required fields.")  # Log jika ada field yang hilang
                return JsonResponse({"success": False, "message": "All fields are required."}, status=400)

            valid_relations = ["0..1", "1..", "0..", "1"]
            if relation not in valid_relations:
                logger.warning(f"Invalid relation: {relation}")  # Log jika relasi tidak valid
                return JsonResponse({"success": False, "message": f"Invalid relation: {relation}"}, status=400)
            if relation_reverse and relation_reverse not in valid_relations:
                logger.warning(f"Invalid reverse relation: {relation_reverse}")  # Log jika relasi balik tidak valid
                return JsonResponse({"success": False, "message": f"Invalid reverse relation: {relation_reverse}"}, status=400)

            try:
                # Mendapatkan objek kelas dari ID
                class_start = Class.objects.get(id=class_start_id)
                class_end = Class.objects.get(id=class_end_id)

                # Simpan data koneksi ke dalam database
                connection = Connection.objects.create(
                    path_name=path_name,
                    relation=relation,
                    class_start=class_start,
                    class_end=class_end,
                    relation_reverse=relation_reverse
                )
                logger.info(f"Connection {connection.id} saved successfully.")  # Log jika berhasil disimpan
            except Class.DoesNotExist:
                logger.error(f"Class not found with id {class_start_id} or {class_end_id}.")  # Log jika kelas tidak ditemukan
                return JsonResponse({"success": False, "message": "One or both classes not found."}, status=404)
            except Exception as e:
                logger.error(f"Error occurred while saving connection: {str(e)}")  # Log jika terjadi error
                return JsonResponse({"success": False, "message": f"Error occurred: {str(e)}"}, status=500)

        # Generate class diagram setelah data koneksi disimpan
        try:
            # Mulai membuat kode UML berdasarkan data di database
            uml_code = '@startuml\n'
            uml_code += 'skinparam classAttributeIconSize 16\n\n'

            # Ambil semua kelas dan koneksi untuk diagram
            classes = Class.objects.all()
            connections = Connection.objects.all()

            # Menambahkan kelas dan atribut/operasi
            for cls in classes:
                uml_code += f'class {cls.name} {{\n'
                attributes = cls.attributes.all()
                operations = cls.operations.all()

                for attr in attributes:
                    uml_code += f'  {attr.name}\n'

                for op in operations:
                    uml_code += f'  {op.name}()\n'

                uml_code += '}\n'

            # Menambahkan hubungan antar kelas
            for conn in connections:
                uml_code += f'{conn.class_start.name} "{conn.relation}" -- "{conn.relation_reverse}" {conn.class_end.name}\n'

            uml_code += '@enduml'

            # Simpan kode UML ke file .puml
            plantuml_file_path = Path(settings.BASE_DIR) / 'tools' / 'class_diagram.puml'
            diagram_output_path = Path(settings.BASE_DIR) / 'tools' / 'class_diagram.png'

            with open(plantuml_file_path, 'w', encoding='utf-8') as file:
                file.write(uml_code)

            # Generate diagram PNG menggunakan PlantUML
            command = [
                'java', '-jar', str(Path(settings.BASE_DIR) / 'tools' / 'plantuml-mit-1.2024.7.jar'),
                str(plantuml_file_path)
            ]
            subprocess.run(command, check=True)

             # Cek apakah file diagram berhasil dibuat
            if diagram_output_path.exists():
                logger.info("Diagram generated successfully.")
                # Arahkan ke halaman outputclass
                return HttpResponseRedirect(reverse('output_class_view'))
            else:
                logger.error("Failed to generate the diagram.")
                return render(request, 'error_page.html', {'message': 'Diagram generation failed.'})


        except Exception as e:
            logger.error(f"Error while generating diagram: {str(e)}")  # Log error jika terjadi kesalahan saat generate diagram
            return JsonResponse({"success": False, "message": f"Error occurred: {str(e)}"}, status=500)

    return render(request, 'class_diagram_page/input_class_diagram.html')

logger = logging.getLogger(__name__)

def get_classes(request):
    try:
        # Ambil semua kelas yang ada
        classes = Class.objects.all()
        if not classes.exists():
            return JsonResponse({"classes": []})  # Kembalikan array kosong jika tidak ada kelas
        
        class_data = [{"id": cls.id, "name": cls.name} for cls in classes]
        return JsonResponse({"classes": class_data})
    except Exception as e:
        logger.error(f"Error fetching classes: {str(e)}")
        return JsonResponse({"status": "error", "message": "An error occurred while fetching classes"}, status=500)


@csrf_exempt  # Menonaktifkan CSRF sementara untuk pengujian, pastikan menggunakan CSRF token di frontend
def save_data(request):
    if request.method == "POST":
        try:
            # Log request body untuk debugging
            logger.info(f"Request Body: {request.body.decode('utf-8')}")

            # Mengambil data dari body request
            data = json.loads(request.body)

            # Validasi data
            if not isinstance(data, dict):
                return JsonResponse({"status": "error", "message": "Expected JSON object"}, status=400)

            # Menyimpan data kelas dan atribut
            for class_data in data.get("classes", []):
                class_name = class_data.get("name")
                if not class_name:
                    return JsonResponse({"status": "error", "message": "Class name missing"}, status=400)

                # Membuat instance kelas
                class_instance = Class.objects.create(name=class_name)

                # Menyimpan atribut untuk setiap kelas
                for attribute_name in class_data.get("attributes", []):
                    if attribute_name:
                        Attribute.objects.create(class_ref=class_instance, name=attribute_name)

                # Menyimpan operasi untuk setiap kelas
                for operation_name in class_data.get("operations", []):
                    if operation_name:
                        Operation.objects.create(class_ref=class_instance, name=operation_name)

            # Menyimpan data koneksi
            for connection_data in data.get("connections", []):
                path_name = connection_data.get("path_name")
                relation = connection_data.get("relation")
                class_start = connection_data.get("class_start")
                class_end = connection_data.get("class_end")
                reverse_relation = connection_data.get("reverse_relation")

                if not all([path_name, relation, class_start, class_end, reverse_relation]):
                    return JsonResponse({"status": "error", "message": "Incomplete connection data"}, status=400)

                try:
                    class_start_instance = Class.objects.get(name=class_start)
                    class_end_instance = Class.objects.get(name=class_end)
                except Class.DoesNotExist as e:
                    logger.error(f"Class does not exist: {str(e)}")
                    return JsonResponse({"status": "error", "message": "One or more classes not found"}, status=400)

                Connection.objects.create(
                    path_name=path_name,
                    relation=relation,
                    class_start=class_start_instance,
                    class_end=class_end_instance,
                    reverse_relation=reverse_relation
                )

            # Setelah semua data disimpan, ambil daftar kelas terbaru
            classes = Class.objects.values("id", "name")  # Mengambil id dan nama kelas

            return JsonResponse({"status": "success", "classes": list(classes)})

        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {str(e)}")
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)

        except Exception as e:
            logger.error(f"Exception occurred: {str(e)}")
            return JsonResponse({"status": "error", "message": "Internal server error"}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

def output_class_view(request):
    # URL ke view yang menyajikan file diagram
    diagram_url = reverse('serve_class_diagram')  # Pastikan view ini ada di urls.py
    
    # Kirim URL ke template
    return render(request, 'class_diagram_page/outputclass.html', {
        'diagram_url': diagram_url
    })

from django.http import FileResponse, Http404
from pathlib import Path

def serve_class_diagram(request):
    # Path ke file diagram kelas
    diagram_path = Path(settings.BASE_DIR) / 'tools' / 'class_diagram.png'

    # Cek apakah file ada
    if diagram_path.exists():
        return FileResponse(open(diagram_path, 'rb'), content_type='image/png')
    else:
        raise Http404("Class diagram not found.")
