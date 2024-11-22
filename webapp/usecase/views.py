import json
import os
import subprocess
from pathlib import Path
from typing import Sequence

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
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

def use_case_output(request):
    # Ambil semua fitur unik dari database
    features = ActorFeature.objects.values_list('feature_name', flat=True).distinct()

    context = {
        'features': features,
    }

    return render(request, 'use_case_diagram_page/use_case_result.html', context)

# ---------------------specification------------------------

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


@csrf_exempt
def input_sequence(request):
    if request.method == 'POST':
        # Ambil ID actor dari POST data
        actor_id = request.POST.get('actor_id')

        if not actor_id:
            return JsonResponse({'status': 'fail', 'message': 'actor_id tidak ditemukan dalam request.'})

        # Cek apakah actor_id ada di database
        try:
            actor = ActorFeature.objects.get(id=actor_id)
            actor_name = actor.actor_name  # Mengambil nama aktor dari data yang diambil
        except ActorFeature.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': f'Aktor dengan id {actor_id} tidak ditemukan.'})

        # Ambil data lain dari POST request
        boundary_name = request.POST.get('boundary')
        controller_name = request.POST.get('controller')
        entity_name = request.POST.get('entity')
        basic_path = request.POST.get('basic_path')
        alternative_path = request.POST.get('alternative_path')

        # Simpan data ke SequenceStuff jika belum ada
        sequence_stuff, created = SequenceStuff.objects.get_or_create(name=actor_name)

        # Simpan data ke Sequence
        if boundary_name and controller_name and entity_name:
            sequence = Sequence.objects.create(
                sequence_stuff=sequence_stuff,  # Hubungkan dengan SequenceStuff
                boundary=boundary_name,
                controller=controller_name,
                entity=entity_name,
                basic_path=basic_path,
                alternative_path=alternative_path
            )

        # Bangun konten untuk diagram PlantUML
        uml_content = f"""@startuml
        actor {actor_name}
        boundary {boundary_name}
        controller {controller_name}
        entity {entity_name}
        """

        # Menambahkan basic path jika ada
        if basic_path:
            uml_content += f"{actor_name} -> {boundary_name} : {basic_path}\n"
            uml_content += f"{boundary_name} -> {controller_name} : Langkah 2\n"
            uml_content += f"{controller_name} -> {entity_name} : Langkah 3\n"

        # Menambahkan alternative path jika ada
        if alternative_path:
            uml_content += f"alt {alternative_path}\n"
            uml_content += f"{controller_name} -> {actor_name} : {alternative_path}\n"
            uml_content += "end\n"

        # Menutup diagram
        uml_content += "@enduml"

        # Tentukan path untuk menyimpan file UML di folder txt di static
        txt_folder_path = os.path.join(settings.BASE_DIR, 'static', 'txt')
        os.makedirs(txt_folder_path, exist_ok=True)
        uml_file_path = os.path.join(txt_folder_path, 'uml_sequence.txt')

        # Simpan file UML
        with open(uml_file_path, 'w') as f:
            f.write(uml_content)

        # Proses generate diagram menggunakan PlantUML
        try:
            plantuml_path = os.path.join(settings.BASE_DIR, 'tools', 'plantuml-mit-1.2024.7.jar')
            output_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'generated_sequence_diagram.png')
            subprocess.run(['java', '-jar', plantuml_path, uml_file_path, '-o', os.path.dirname(output_path)], check=True)

            # Gambar berhasil dihasilkan
            diagram_url = f'/static/images/generated_sequence_diagram.png'

            return JsonResponse({
                'status': 'success',
                'message': 'Sequence diagram berhasil dihasilkan!',
                'diagram_url': diagram_url
            })

        except Exception as e:
            return JsonResponse({
                'status': 'fail',
                'message': f'Gagal menghasilkan diagram: {str(e)}'
            })

    return render(request, 'sequence_diagram/input_sequence_diagram.html')


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


def output_activity(request):
    return render(request, 'output-activity.html')


def input_class_diagram(request):
    return render(request, 'class_diagram_page/input_class_diagram.html')

def input_sequence(request):
    return render(request, 'sequence_diagram/input_sequence_diagram.html')

def output_class(request):
    return render(request, 'class_diagram_page/outputclass.html')


def output_sequence(request):
    return render(request, 'sequence_diagram_page/outputsequence.html')
