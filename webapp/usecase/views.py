import os
import subprocess
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from .models import ActorFeature, AlternativePath, BasicPath, ExceptionPath, UseCaseSpecification  # Import your ActorFeature model



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

def use_case_result(request):
    if request.method == 'POST':
        actor_data = []
        features = []  # Menyimpan fitur yang baru diinputkan

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

        # Generate the PlantUML diagram
        diagram_path = generate_use_case_diagram(actor_data)

        # Pastikan diagram_path menjadi objek Path
        if diagram_path:
            diagram_path = Path(diagram_path)

        # Mengembalikan JSON response jika ini adalah AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Data berhasil disimpan!',
                'features': features,
                'diagram_path': str(diagram_path.relative_to(settings.BASE_DIR)) if diagram_path else None
            })

        context = {
            'actor_data': actor_data,
            'diagram_path': str(diagram_path.relative_to(settings.BASE_DIR)) if diagram_path else None,
            'features': features,  # Mengirimkan hanya fitur yang baru diinputkan
        }
        return render(request, 'use_case_diagram_page/use_case_result.html', context)

    return render(request, 'use_case_diagram_page/use_case_result.html', {'nama': 'hello world'})


# def use_case_result(request):
#     if request.method == 'POST':
#         actor_data = []
#         for key, value in request.POST.items():
#             if 'actor' in key and value:
#                 actor_id = key.replace('actor', '')
#                 features = [
#                     request.POST.get(f'feature{actor_id}_{i}') 
#                     for i in range(1, 10)
#                     if request.POST.get(f'feature{actor_id}_{i}')
#                 ]
#                 for feature in features:
#                     ActorFeature.objects.create(actor_name=value, feature_name=feature)
#                     actor_data.append((value, feature))

#         # Generate the PlantUML diagram
#         diagram_path = generate_use_case_diagram(actor_data)

#         # Pastikan diagram_path menjadi objek Path
#         if diagram_path:
#             diagram_path = Path(diagram_path)

#         # Ambil fitur terbaru dari database
#         features = list(ActorFeature.objects.values_list('feature_name', flat=True).distinct())

#         # Mengembalikan JSON response jika ini adalah AJAX request
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#             return JsonResponse({
#                 'status': 'success',
#                 'message': 'Data berhasil disimpan!',
#                 'features': features,
#                 'diagram_path': str(diagram_path.relative_to(settings.BASE_DIR)) if diagram_path else None
#             })

#         context = {
#             'actor_data': actor_data,
#             'diagram_path': str(diagram_path.relative_to(settings.BASE_DIR)) if diagram_path else None,
#             'features': features,  # Menambahkan fitur ke context
#         }
#         return render(request, 'use case diagram page/use_case_result.html', context)

#     return render(request, 'use case diagram page/use_case_result.html', {'nama': 'hello world'})

def generate_use_case_diagram(actor_data):
    # Generate PlantUML code based on actor_data
    uml_code = '@startuml\n'
    for actor, feature in actor_data:
        uml_code += f'actor "{actor}" as {actor}\n'
        uml_code += f'{actor} --> "{feature}"\n'
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

def save_specification(request):
    if request.method == 'POST':
        # Ambil data dari form
        use_case_name = request.POST.get('use_case_name')
        actor_id = request.POST.get('actor')  # Dapatkan ID aktor yang dipilih
        summary_description = request.POST.get('summary_description')
        pre_conditions = request.POST.get('pre_conditions')
        post_conditions = request.POST.get('post_conditions')

        # Jika actor sudah dipilih dari dropdown, ambil actor yang dipilih
        if actor_id:
            actor = ActorFeature.objects.get(id=actor_id)
        else:
            return HttpResponse("Actor is required", status=400)

        # Simpan Use Case Specification
        use_case_spec = UseCaseSpecification(
            use_case_name=use_case_name,
            actor=actor,  # Simpan objek aktor, bukan hanya nama
            summary_description=summary_description,
            pre_conditions=pre_conditions,
            post_conditions=post_conditions,
        )
        use_case_spec.save()

        # Menyimpan langkah-langkah dalam Basic Path
        basic_actor_steps = request.POST.getlist('basic_actor_step[]')
        basic_system_steps = request.POST.getlist('basic_system_step[]')
        for actor_step, system_step in zip(basic_actor_steps, basic_system_steps):
            if actor_step.strip() or system_step.strip():
                BasicPath.objects.create(
                    use_case_specification=use_case_spec,
                    basic_actor_step=actor_step,
                    basic_system_step=system_step
                )

        # Menyimpan langkah-langkah dalam Alternative Path
        alternative_actor_steps = request.POST.getlist('alternative_actor_step[]')
        alternative_system_steps = request.POST.getlist('alternative_system_step[]')
        for actor_step, system_step in zip(alternative_actor_steps, alternative_system_steps):
            if actor_step.strip() or system_step.strip():
                AlternativePath.objects.create(
                    use_case_specification=use_case_spec,
                    alternative_actor_step=actor_step,
                    alternative_system_step=system_step
                )

        # Menyimpan langkah-langkah dalam Exception Path
        exception_actor_steps = request.POST.getlist('exception_actor_step[]')
        exception_system_steps = request.POST.getlist('exception_system_step[]')
        for actor_step, system_step in zip(exception_actor_steps, exception_system_steps):
            if actor_step.strip() or system_step.strip():
                ExceptionPath.objects.create(
                    use_case_specification=use_case_spec,
                    exception_actor_step=actor_step,
                    exception_system_step=system_step
                )

        return redirect('output_activity')  # Ganti dengan URL yang sesuai
    
    # Ambil daftar aktor yang telah ada
    actors = ActorFeature.objects.all()
    
    
    # Kirimkan data actor yang ada
    return render(request, 'use_case_specification/Specification.html', {'actors': actors})

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
