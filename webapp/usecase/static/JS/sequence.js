// Function to dynamically add new input fields for boundary, controller, and entity
function addInputField(containerId, labelText) {
    const container = document.getElementById(containerId);

    // Create a new form-group div
    const newDiv = document.createElement('div');
    newDiv.classList.add('form-group');

    // Create label
    const label = document.createElement('label');
    label.textContent = `${labelText}:`;

    // Create input
    const input = document.createElement('input');
    input.type = 'text';
    input.placeholder = `Input ${labelText.toLowerCase()} ${container.childElementCount + 1}`;

    // Create delete (trash) button
    const deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.classList.add('delete-btn');
    deleteButton.innerHTML = '<i class="fas fa-trash"></i>'; 
    deleteButton.onclick = () => {
        container.removeChild(newDiv);
        updateLabels(container, labelText); 
    };

    // Append label, input, and delete button to newDiv
    newDiv.appendChild(label);
    newDiv.appendChild(input);
    newDiv.appendChild(deleteButton);

    // Append newDiv to the container
    container.appendChild(newDiv);

    // Update labels after adding a new input
    updateLabels(container, labelText);
}

// Function to update labels and placeholders after adding or deleting an input
function updateLabels(container, labelText) {
    const formGroups = container.querySelectorAll('.form-group');

    formGroups.forEach((group, index) => {
        const label = group.querySelector('label');
        const input = group.querySelector('input');

        // Update label text and input placeholder based on the current index
        label.textContent = `${labelText}: ${index + 1}`;
        input.placeholder = `Input ${labelText.toLowerCase()} ${index + 1}`;
    });
}

// Function to dynamically add a new path section
function addPathSection() {
    const container = document.getElementById('basic-path-container');
    const pathSections = container.querySelectorAll('.condition-group');

    // Hitung path baru berdasarkan jumlah section yang ada
    const pathNumber = pathSections.length + 1;

    // Create a new div for the path section
    const newPathSection = document.createElement('div');
    newPathSection.classList.add('condition-group');

    // Add HTML content for the new path section
    newPathSection.innerHTML = `
        <div class="form-group">
            <label>Path ${pathNumber}</label>
            <input type="text" placeholder="Input path ${pathNumber}">
        </div>
        <div class="form-group select-group">
            <label>Object Start</label>
            <select>
                <option>Choose object</option>
            </select>
            <label>Object End</label>
            <select>
                <option>Choose object</option>
            </select>
        </div>
        <div class="button-container">
            <button type="button" class="delete-btn" onclick="deletePathSection(this)"><i class="fas fa-trash"></i></button>
        </div>
    `;

    // Append the new section to the container
    container.appendChild(newPathSection);

    // Update labels after adding new path
    updatePathLabels();
}

// Function to delete a path section
function deletePathSection(button) {
    const pathSection = button.closest('.condition-group');
    pathSection.parentNode.removeChild(pathSection);
    updatePathLabels(); 
}

// Function to update path labels
function updatePathLabels() {
    const paths = document.querySelectorAll('#basic-path-container .condition-group');

    paths.forEach((path, index) => {
        const label = path.querySelector('label');
        const input = path.querySelector('input');

        // Update label text and input placeholder based on the current index
        label.textContent = `Path ${index + 1}`;
        input.placeholder = `Input path ${index + 1}`;
    });
}

// Function to add a new alternative path section
function addAlternativePathSection(button) {
    // Find the closest parent element of the clicked button
    const conditionGroup = button.closest('.condition-group');

    // Count existing paths in the related conditionGroup
    const existingPaths = conditionGroup.querySelectorAll('.alternative-path');
    const pathCount = existingPaths.length + 2; 

    // Create a new div for the added path
    const newPathSection = document.createElement('div');
    newPathSection.classList.add('alternative-path');

    // Add HTML content for the new path
    newPathSection.innerHTML = `
        <div class="form-group">
            <label>Path ${pathCount}</label>
            <input type="text" placeholder="Input path ${pathCount}">
        </div>
        <div class="form-group select-group">
            <label>Object Start</label>
            <select>
                <option>Choose object</option>
            </select>
            <label>Object End</label>
            <select>
                <option>Choose object</option>
            </select>
        </div>
    `;

    // Add delete button with trash icon for the new path
    const deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.classList.add('delete-btn');
    deleteButton.innerHTML = '<i class="fas fa-trash"></i>'; 
    deleteButton.onclick = () => {
        conditionGroup.removeChild(newPathSection);
        updateAltPathLabels(conditionGroup); 
    };

    // Append delete button to the new path section
    newPathSection.appendChild(deleteButton);

    // Add new path to the relevant condition
    conditionGroup.appendChild(newPathSection);

    // Update path labels after adding a new path
    updateAltPathLabels(conditionGroup);
}

// Function to update alternative path labels
function updateAltPathLabels(conditionGroup) {
    const paths = conditionGroup.querySelectorAll('.alternative-path');

    paths.forEach((path, index) => {
        const label = path.querySelector('label');
        const input = path.querySelector('input');

        // Update label text and input placeholder based on the current index
        label.textContent = `Path ${index + 2}`; 
        input.placeholder = `Input path ${index + 2}`;
    });
}
