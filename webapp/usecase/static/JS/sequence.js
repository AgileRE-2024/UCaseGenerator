
// Function to dynamically add new input fields for boundary, controller, and entity
function addInputField(containerId, fieldType) {
    const container = document.getElementById(containerId);
    let inputCount = container.getElementsByTagName('input').length + 1; // Menghitung jumlah input yang ada

    // Membuat elemen input baru dan tombol sesuai dengan fieldType
    const newInputGroup = document.createElement('div');
    newInputGroup.classList.add('form-group', 'row', 'align-items-center');

    // Menambahkan input baru ke dalam grup
    const newInputField = document.createElement('div');
    newInputField.classList.add('col-10');
    const input = document.createElement('input');
    input.type = 'text';
    input.name = fieldType.toLowerCase();
    input.classList.add('form-control');
    input.placeholder = fieldType + ' ' + inputCount;
    input.id = `${fieldType.toLowerCase()}-input-${inputCount}`; // Memberikan ID dinamis
    newInputField.appendChild(input);

    // Menambahkan tombol + untuk menambah input baru
    const newButton = document.createElement('div');
    newButton.classList.add('col-2');
    const button = document.createElement('button');
    button.type = 'button';
    button.classList.add('btn', 'btn-success', 'w-100');
    button.textContent = '+';
    button.onclick = function () {
        addInputField(containerId, fieldType); // Memanggil fungsi untuk menambah input baru
    };
    newButton.appendChild(button);

    const deleteButtonWrapper = document.createElement('div');
    deleteButtonWrapper.classList.add('col-2');
    const deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.classList.add('btn', 'btn-danger', 'w-100', 'mt-2');
    deleteButton.textContent = 'Hapus';
    deleteButton.onclick = function () {
        container.removeChild(newInputGroup); // Menghapus grup input
    };
    deleteButtonWrapper.appendChild(deleteButton);

    // Menambahkan grup input dan tombol ke dalam container
    newInputGroup.appendChild(newInputField);
    newInputGroup.appendChild(newButton);
    newInputGroup.appendChild(deleteButtonWrapper);
    container.appendChild(newInputGroup);
}

// Function to update labels and placeholders after adding or deleting an input
function updateLabels(container, labelText) {
    const formGroups = container.querySelectorAll('.form-group');

    formGroups.forEach((group, index) => {
        const label = group.querySelector('label');
        const input = group.querySelector('input');

        // Debug: cek apakah label ditemukan
        console.log(label, input);

        if (label && input) {
            // Update label text and input placeholder based on the current index
            label.textContent = `${labelText}: ${index + 1}`;  // Fixed with backticks
            input.placeholder = `Input ${labelText.toLowerCase()} ${index + 1}`;  // Fixed with backticks
        } else {
            console.error("Label atau Input tidak ditemukan untuk grup ke-" + (index + 1));
        }
    });
}

function getObjectOptions() {
    const objects = [];

    // Dapatkan semua elemen input yang ada di container yang relevan
    document.querySelectorAll('#actor-container input, #boundary-container input, #controller-container input, #entity-container input').forEach(input => {
        if (input.value) objects.push(input.value);
    });

    return [...new Set(objects)];  // Hapus duplikasi   

}

console.log(getObjectOptions());

function updateDropdownOptions() {
    // Define all dropdown groups to update
    const dropdownGroups = [
        // Basic Path Dropdowns
        document.querySelectorAll('[id^="object-start-basic-path-"]'),
        document.querySelectorAll('[id^="object-end-basic-path-"]'),

        // Alternative Path Dropdowns
        document.querySelectorAll('[id^="object-start-alternative-path-"]'),
        document.querySelectorAll('[id^="object-end-alternative-path-"]'),

        // Else Path Dropdowns
        document.querySelectorAll('[id^="else-object-start-alternative-path-"]'),
        document.querySelectorAll('[id^="else-object-end-alternative-path-"]')
    ];

    // Ganti ini dengan `getObjectOptions()` jika data dinamis
    const objects = getObjectOptions();

    dropdownGroups.forEach(dropdowns => {
        dropdowns.forEach(dropdown => {
            // Kosongkan dropdown saat ini
            dropdown.innerHTML = '<option value="">Choose object</option>';

            // Tambahkan opsi baru
            objects.forEach(obj => {
                const option = document.createElement('option');
                option.value = obj; // Menggunakan nama objek sebagai nilai
                option.textContent = obj;
                dropdown.appendChild(option);
            });
        });
    });
}

function addAlternativePathSection() {
    const alternativeContainer = document.getElementById('alternative-path-container');
    const alternativeCount = alternativeContainer.getElementsByClassName('condition-group').length + 1;

    const newAlternativeGroup = document.createElement('div');
    newAlternativeGroup.classList.add('condition-group', 'mb-3');
    newAlternativeGroup.id = `alternative-path-section-${alternativeCount}`;

    newAlternativeGroup.innerHTML = `
        <div class="form-group row align-items-center">
            <label class="col-form-label">Alternative Path Title</label>
            <div class="col-8">
                <input type="text" id="alternative-title-${alternativeCount}" 
                    name="alternative_path_label"
                    id="alternative-title-${alternativeCount}"
                    class="form-control" 
                    placeholder="Input Alternative Title">
            </div>
        </div>
        <div class="form-group row align-items-center">
            <label class="col-2 col-form-label">Alternative Path:</label>
            <div class="col-8">
                <input type="text" 
                    id="alternative-path-${alternativeCount}" 
                    name="alternative_path_input" 
                    class="form-control" 
                    placeholder="Input Alternative Path">
            </div>
        </div>
        <div class="form-group row mt-3">
            <div class="col-6">
                <label for="object-start-alternative-path-${alternativeCount}">Object Start</label>
                <select id="object-start-alternative-path-${alternativeCount}" class="form-select">
                    <option value="">Choose object</option>
                </select>
            </div>
            <div class="col-6">
                <label for="object-end-alternative-path-${alternativeCount}">Object End</label>
                <select id="object-end-alternative-path-${alternativeCount}" class="form-select">
                    <option value="">Choose object</option>
                </select>
            </div>
        </div>
        <div id="else-container-${alternativeCount}" class="mt-3">
            <!-- Else conditions will be added here -->
        </div>
        <div class="mt-3 text-end">
            <button type="button" class="btn btn-success" onclick="addElseSection(${alternativeCount})">Add Else +</button>
            <button type="button" class="btn btn-danger ml-2" onclick="removeAlternativePathSection(this)">Remove Path</button>
        </div>
    `;

    alternativeContainer.appendChild(newAlternativeGroup);

    // Update dropdown options for newly added section
    updateDropdownOptions();
}

function removeAlternativePathSection(button) {
    const alternativeSection = button.closest('.condition-group');
    alternativeSection.remove();
    updateDropdownOptions();
}

function addElseSection(alternativeId) {
    const elseContainer = document.getElementById(`else-container-${alternativeId}`);
    if (!elseContainer) {
        console.error(`Else container for alternative path ${alternativeId} not found`);
        return;
    }

    const elseCount = elseContainer.querySelectorAll('.else-section').length + 1;

    const newElseGroup = document.createElement('div');
    newElseGroup.classList.add('form-group', 'row', 'mt-3', 'else-section');
    newElseGroup.innerHTML = `
        <div class="col-12 mb-2">
            <input type="text" 
                id="else-title-${alternativeId}-${elseCount}" 
                name="else_path_label" 
                class="form-control" 
                placeholder="Input Else Title">
        </div>
        <div class="col-12 mb-2">
            <input type="text" 
                id="else-path-${alternativeId}-${elseCount}" 
                name="else_path_input" 
                class="form-control" 
                placeholder="Input Else Condition">
        </div>
        <div class="col-6">
            <label>Object Start</label>
            <select id="else-object-start-alternative-path-${alternativeId}-${elseCount}" class="form-select">
                <option value="">Choose object</option>
            </select>
        </div>
        <div class="col-6">
            <label>Object End</label>
            <select id="else-object-end-alternative-path-${alternativeId}-${elseCount}" class="form-select">
                <option value="">Choose object</option>
            </select>
        </div>
        <div class="col-12 mt-2 text-right">
            <button type="button" class="btn btn-danger btn-sm" onclick="removeElseSection(this)">Remove Else</button>
        </div>
    `;

    elseContainer.appendChild(newElseGroup);
    updateDropdownOptions();
}


function removeElseSection(button) {
    const elseSection = button.closest('.else-section, .form-group');
    elseSection.remove();
    updateDropdownOptions();
}


// Function to dynamically add a new path section
function addPathSection() {
    const pathContainer = document.getElementById('basic-path-container');
    let pathCount = pathContainer.getElementsByClassName('condition-group').length + 1; // Menghitung jumlah path yang ada

    const newPathGroup = document.createElement('div');
    newPathGroup.classList.add('condition-group', 'mb-3');
    newPathGroup.id = `path-section-${pathCount}`; // Memberikan ID dinamis untuk setiap path section

    // Membuat form group untuk path
    const pathFormGroup = document.createElement('div');
    pathFormGroup.classList.add('form-group', 'row', 'align-items-center');
    const pathLabel = document.createElement('label');
    pathLabel.classList.add('col-2', 'col-form-label');
    pathLabel.setAttribute('for', `basic-path-${pathCount}`);
    pathLabel.textContent = `Path ${pathCount}:`;
    const pathInputWrapper = document.createElement('div');
    pathInputWrapper.classList.add('col-8');
    const pathInput = document.createElement('input');
    pathInput.type = 'text';
    pathInput.name = 'basic_path_input';
    pathInput.classList.add('form-control');
    pathInput.placeholder = `Input Path ${pathCount}`;
    pathInput.id = `basic-path-${pathCount}`; // ID dinamis untuk input path
    pathInputWrapper.appendChild(pathInput);
    pathFormGroup.appendChild(pathLabel);
    pathFormGroup.appendChild(pathInputWrapper);

    // Membuat form group untuk object start dan end
    const objectSelectGroup = document.createElement('div');
    objectSelectGroup.classList.add('form-group', 'row', 'mt-3');
    const objectStartWrapper = document.createElement('div');
    objectStartWrapper.classList.add('col-6');
    const objectStartLabel = document.createElement('label');
    objectStartLabel.setAttribute('for', `object-start-basic-path-${pathCount}`);
    objectStartLabel.textContent = 'Object Start';
    const objectStartSelect = document.createElement('select');
    objectStartSelect.id = `object-start-basic-path-${pathCount}`;
    objectStartSelect.classList.add('form-select');
    const defaultOptionStart = document.createElement('option');
    defaultOptionStart.value = '';
    defaultOptionStart.textContent = 'Choose object';
    objectStartSelect.appendChild(defaultOptionStart);
    objectStartWrapper.appendChild(objectStartLabel);
    objectStartWrapper.appendChild(objectStartSelect);

    const objectEndWrapper = document.createElement('div');
    objectEndWrapper.classList.add('col-6');
    const objectEndLabel = document.createElement('label');
    objectEndLabel.setAttribute('for', `object-end-basic-path-${pathCount}`);
    objectEndLabel.textContent = 'Object End';
    const objectEndSelect = document.createElement('select');
    objectEndSelect.id = `object-end-basic-path-${pathCount}`;
    objectEndSelect.classList.add('form-select');
    const defaultOptionEnd = document.createElement('option');
    defaultOptionEnd.value = '';
    defaultOptionEnd.textContent = 'Choose object';
    objectEndSelect.appendChild(defaultOptionEnd);
    objectEndWrapper.appendChild(objectEndLabel);
    objectEndWrapper.appendChild(objectEndSelect);

    objectSelectGroup.appendChild(objectStartWrapper);
    objectSelectGroup.appendChild(objectEndWrapper);

    const deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.classList.add('btn', 'btn-danger', 'w-100', 'mt-3');
    deleteButton.textContent = 'Hapus Path';
    deleteButton.onclick = function () {
        deletePathSection(deleteButton);  // Memanggil fungsi deletePathSection
    };

    // Menambahkan elemen ke path section baru
    newPathGroup.appendChild(pathFormGroup);
    newPathGroup.appendChild(objectSelectGroup);
    newPathGroup.appendChild(deleteButton);

    // Menambahkan path section ke dalam container
    pathContainer.appendChild(newPathGroup);

    updateDropdownOptions(); // Perbarui opsi dropdown setelah menambahkan path baru
}

// Function to delete path section
function deletePathSection(button) {
    const pathSection = button.closest('.condition-group');
    pathSection.parentElement.removeChild(pathSection);
    updateDropdownOptions();  // Perbarui opsi dropdown setelah path section dihapus
}


// Function to update path labels
function updatePathLabels() {
    // Mengambil semua elemen dengan class .condition-group di dalam #basic-path-container
    const paths = document.querySelectorAll('#basic-path-container .condition-group');

    // Iterasi untuk setiap elemen path yang ditemukan
    paths.forEach((path, index) => {
        const label = path.querySelector('label');
        const input = path.querySelector('input');

        // Pastikan label dan input ditemukan sebelum melakukan perubahan
        if (label) {
            label.textContent = `Path ${index + 1}`;  // Mengubah label sesuai dengan indeks
        }

        if (input) {
            input.placeholder = `Input path ${index + 1}`;  // Mengubah placeholder input sesuai dengan indeks
        }
    });
}

function generatePaths() {
    const paths = [];
    const alternativePaths = [];

    // Basic Paths (Tidak diubah)
    const basicPathSections = document.querySelectorAll('#basic-path-container .condition-group');
    basicPathSections.forEach((section) => {
        const pathInput = section.querySelector(`[id^="basic-path-"]`);
        const startElement = section.querySelector(`[id^="object-start-basic-path-"]`);
        const endElement = section.querySelector(`[id^="object-end-basic-path-"]`);

        const path = pathInput ? pathInput.value.trim() : '';
        const start = startElement ? startElement.value.trim() : '';
        const end = endElement ? endElement.value.trim() : '';

        if (path && start && end) {
            paths.push({
                path: `${start} -> ${end} : ${path}`,
            });
        }
    });

    // Alternative Paths
    const alternativePathSections = document.querySelectorAll('#alternative-path-container .condition-group');
    console.log("Alternative Path Sections Found:", alternativePathSections.length);

    alternativePathSections.forEach((section, index) => {
        // Gunakan selector yang lebih spesifik dan gunakan console.log untuk debugging
        const titleInput = section.querySelector(`[id^="alternative-title-${index + 1}"]`);
        const conditionInput = section.querySelector(`[id^="alternative-path-${index + 1}"]`);
        const pathInput = section.querySelector(`[id^="alternative-path-${index + 1}"]`);
        const startElement = section.querySelector(`[id^="object-start-alternative-path-${index + 1}"]`);
        const endElement = section.querySelector(`[id^="object-end-alternative-path-${index + 1}"]`);

        console.log("Alternative Path Debug:", {
            titleInput: titleInput ? titleInput.value : 'NOT FOUND',
            conditionInput: conditionInput ? conditionInput.value : 'NOT FOUND',
            pathInput: pathInput ? pathInput.value : 'NOT FOUND',
            startElement: startElement ? startElement.value : 'NOT FOUND',
            endElement: endElement ? endElement.value : 'NOT FOUND'
        });

        const title = titleInput ? titleInput.value.trim() : '';
        const condition = conditionInput ? conditionInput.value.trim() : '';
        const path = pathInput ? pathInput.value.trim() : '';
        const start = startElement ? startElement.value.trim() : '';
        const end = endElement ? endElement.value.trim() : '';

        // Validate main alternative path
        if (title && condition && start && end) {
            const alternativePath = {
                title: title,
                condition: condition,
                path: `${start} -> ${end} : ${condition}`,
                elseConditions: []
            };

            // Process Else Conditions
            const elseSections = section.querySelectorAll('.else-section');
            console.log(`Else Sections for Alternative Path ${index + 1}:`, elseSections.length);

            elseSections.forEach((elseSection, elseIndex) => {
                const elseTitleInput = elseSection.querySelector(`[id^="else-title-${index + 1}"]`);
                const elseConditionInput = elseSection.querySelector(`[id^="else-path-${index + 1}"]`);
                const elseStartElement = elseSection.querySelector(`[id^="else-object-start-alternative-path-${index + 1}"]`);
                const elseEndElement = elseSection.querySelector(`[id^="else-object-end-alternative-path-${index + 1}"]`);

                console.log(`Else Condition ${elseIndex + 1} Debug:`, {
                    elseTitleInput: elseTitleInput ? elseTitleInput.value : 'NOT FOUND',
                    elseConditionInput: elseConditionInput ? elseConditionInput.value : 'NOT FOUND',
                    elseStartElement: elseStartElement ? elseStartElement.value : 'NOT FOUND',
                    elseEndElement: elseEndElement ? elseEndElement.value : 'NOT FOUND'
                });

                const elseTitle = elseTitleInput ? elseTitleInput.value.trim() : '';
                const elseCondition = elseConditionInput ? elseConditionInput.value.trim() : '';
                const elseStart = elseStartElement ? elseStartElement.value.trim() : '';
                const elseEnd = elseEndElement ? elseEndElement.value.trim() : '';

                if (elseTitle && elseCondition && elseStart && elseEnd) {
                    alternativePath.elseConditions.push({
                        title: elseTitle,
                        condition: elseCondition,
                        path: `${elseStart} -> ${elseEnd} : ${elseCondition}`,
                    });
                }
            });

            alternativePaths.push(alternativePath);
        }
    });

    console.log("Generated Paths:", paths);
    console.log("Generated Alternative Paths:", alternativePaths);

    return { paths, alternativePaths };
}


document.getElementById('generate-btn').addEventListener('click', async function (event) {
    event.preventDefault();

    const diagramContainer = document.getElementById('diagram-result');
    diagramContainer.innerHTML = '<div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div>';

    const form = document.getElementById('sequence-form');
    const formData = new FormData(form);

    for (const [key, value] of formData.entries()) {
        console.log(`${key}: ${value}`);
    }

    const { paths, alternativePaths } = generatePaths();

    console.log("Basic Paths:", paths);
    console.log("Alternative Paths:", alternativePaths);

    // Tambahkan basic paths ke FormData
    paths.forEach((pathObj, index) => {
        formData.append(`basic_path[${index}]`, pathObj.path);
    });

    // Tambahkan alternative paths ke FormData
    alternativePaths.forEach((altPath, index) => {
        formData.append(`alternative_path[${index}][]`, altPath.title);
        formData.append(`alternative_path[${index}][]`, altPath.condition);
        formData.append(`alternative_path[${index}][]`, altPath.path);

        // Tambahkan else conditions
        altPath.elseConditions.forEach((elseCond) => {
            formData.append(`alternative_path[${index}][]`, elseCond.title);
            formData.append(`alternative_path[${index}][]`, elseCond.condition);
            formData.append(`alternative_path[${index}][]`, elseCond.path);
        });
    });

    // Ambil token CSRF dari halaman atau cookie
    const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfTokenElement) {
        console.error('CSRF token tidak ditemukan!');
        alert('CSRF token tidak ditemukan.');
        return;
    }
    const csrfToken = csrfTokenElement.value;

    try {
        // Kirim data ke server
        const response = await fetch('/generate-sequence-diagram/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            if (data.success && data.redirect_url) {
                // Navigasi ke halaman output
                window.location.href = data.redirect_url;
            } else {
                console.error('Error Data:', data.error || 'Unknown Error');
                diagramContainer.innerHTML = `
                    <div class="alert alert-warning" role="alert">
                        ${data.error || 'Diagram could not be generated'}
                    </div>
                `;
            }
        } else {
            const errorData = await response.text();
            console.error('Response Error Data:', errorData);
            diagramContainer.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    Error: ${errorData}
                </div>
            `;
        }
    } catch (error) {
        console.error('Error:', error);
        diagramContainer.innerHTML = `
            <div class="alert alert-danger" role="alert">
                An error occurred while generating the diagram: ${error.message}
            </div>
        `;
    }
});
