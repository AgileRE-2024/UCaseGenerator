let classCounter = 1;

function addClassSection() {
    const classContainer = document.getElementById("class-container");

    // Create a new class section
    const classSection = document.createElement("section");
    classSection.classList.add("class-section");
    classSection.innerHTML = `
        <h3>Nama Class ${classCounter}:</h3>
        <input type="text" placeholder="Input class name ${classCounter}" class="input-box">

        <div class="class-stuff">
            <h4>Class Stuff:</h4>
            
            <div class="attributes-container">
                <label>Attribute:</label>
                <div class="attribute-group">
                    <input type="text" placeholder="1." class="input-box">
                    <button class="delete-attr-btn" onclick="deleteAttribute(this)"><i class="fas fa-trash-alt"></i></button>
                </div>
            </div>
            
            <div class="operations-container">
                <label>Operation:</label>
                <div class="operation-group">
                    <input type="text" placeholder="1." class="input-box">
                    <button class="delete-op-btn" onclick="deleteOperation(this)"><i class="fas fa-trash-alt"></i></button>
                </div>
            </div>
        </div>
    `;

    // Add the new class section to the container
    classContainer.appendChild(classSection);

    // Add delete button only if this is not the first class
    if (classCounter > 1) {
        const deleteButton = document.createElement("button");
        deleteButton.classList.add("delete-btn");
        deleteButton.innerHTML = '<i class="fas fa-trash-alt"></i>'; // Trash can icon
        deleteButton.onclick = () => deleteClassSection(deleteButton);
        classSection.appendChild(deleteButton);
    }

    // Update the "+" button to only be at the bottom
    updateAddClassButton();

    // Add the "+" buttons for attribute and operation in the new class
    addAttributeButton(classSection.querySelector(".attributes-container"));
    addOperationButton(classSection.querySelector(".operations-container"));

    classCounter++;
}

function deleteClassSection(button) {
    const classSection = button.closest(".class-section");
    classSection.remove(); // Remove class section

    // Update class numbers after deletion
    updateClassNumbers();

    // Update "+" button if needed
    updateAddClassButton();
}

function updateClassNumbers() {
    const classSections = document.querySelectorAll(".class-section");
    classSections.forEach((section, index) => {
        const className = section.querySelector("h3");
        className.textContent = `Nama Class ${index + 1}:`;
        const inputBox = section.querySelector("input[type='text']");
        inputBox.placeholder = `Input class name ${index + 1}`;
    });
    classCounter = classSections.length + 1; // Update the global classCounter to reflect the current count
}

function updateAddClassButton() {
    // Remove all existing "+" buttons
    document.querySelectorAll(".add-class-btn").forEach(btn => btn.remove());

    // Add "+" button only to the last class
    const classContainer = document.getElementById("class-container");
    const lastClassSection = classContainer.lastElementChild;

    if (lastClassSection) {
        const addClassBtn = document.createElement("button");
        addClassBtn.classList.add("add-btn", "add-class-btn");
        addClassBtn.textContent = "+";
        addClassBtn.onclick = addClassSection;
        lastClassSection.appendChild(addClassBtn);
    }
}

function addAttribute(button) {
    const attributesContainer = button.closest(".attributes-container");

    const newAttributeGroup = document.createElement("div");
    newAttributeGroup.classList.add("attribute-group");

    const newAttributeInput = document.createElement("input");
    newAttributeInput.type = "text";
    newAttributeInput.classList.add("input-box");

    const deleteButton = document.createElement("button");
    deleteButton.classList.add("delete-attr-btn");
    deleteButton.innerHTML = '<i class="fas fa-trash-alt"></i>'; // Trash can icon
    deleteButton.onclick = () => deleteAttribute(deleteButton);

    newAttributeGroup.appendChild(newAttributeInput);
    newAttributeGroup.appendChild(deleteButton);
    attributesContainer.appendChild(newAttributeGroup);

    // Update attribute numbering after addition
    updateAttributeNumbers(attributesContainer);

    // Ensure "+" button is at the bottom
    addAttributeButton(attributesContainer);
}

function deleteAttribute(button) {
    const attributeGroup = button.closest(".attribute-group");
    const attributesContainer = button.closest(".attributes-container");
    attributeGroup.remove(); // Remove the attribute input field

    // Immediately update numbers without waiting for "+" button
    updateAttributeNumbers(attributesContainer);

    // Ensure "+" button is placed at the bottom
    addAttributeButton(attributesContainer);
}

function updateAttributeNumbers(container) {
    const attributeGroups = container.querySelectorAll(".attribute-group");
    attributeGroups.forEach((group, index) => {
        const inputBox = group.querySelector("input[type='text']");
        inputBox.placeholder = `${index + 1}.`;
    });
}

function addOperation(button) {
    const operationsContainer = button.closest(".operations-container");

    const newOperationGroup = document.createElement("div");
    newOperationGroup.classList.add("operation-group");

    const newOperationInput = document.createElement("input");
    newOperationInput.type = "text";
    newOperationInput.classList.add("input-box");

    const deleteButton = document.createElement("button");
    deleteButton.classList.add("delete-op-btn");
    deleteButton.innerHTML = '<i class="fas fa-trash-alt"></i>'; // Trash can icon
    deleteButton.onclick = () => deleteOperation(deleteButton);

    newOperationGroup.appendChild(newOperationInput);
    newOperationGroup.appendChild(deleteButton);
    operationsContainer.appendChild(newOperationGroup);

    // Update operation numbering after addition
    updateOperationNumbers(operationsContainer);

    // Ensure "+" button is at the bottom
    addOperationButton(operationsContainer);
}

function deleteOperation(button) {
    const operationGroup = button.closest(".operation-group");
    const operationsContainer = button.closest(".operations-container");
    operationGroup.remove(); // Remove the operation input field

    // Immediately update numbers without waiting for "+" button
    updateOperationNumbers(operationsContainer);

    // Ensure "+" button is placed at the bottom
    addOperationButton(operationsContainer);
}

function updateOperationNumbers(container) {
    const operationGroups = container.querySelectorAll(".operation-group");
    operationGroups.forEach((group, index) => {
        const inputBox = group.querySelector("input[type='text']");
        inputBox.placeholder = `${index + 1}.`;
    });
}

function addAttributeButton(container) {
    // Remove any existing "+" buttons
    const existingButton = container.querySelector(".add-btn");
    if (existingButton) {
        existingButton.remove();
    }

    const addButton = document.createElement("button");
    addButton.classList.add("add-btn");
    addButton.innerText = "+";
    addButton.onclick = () => addAttribute(addButton);

    container.appendChild(addButton);
}

function addOperationButton(container) {
    // Remove any existing "+" buttons
    const existingButton = container.querySelector(".add-btn");
    if (existingButton) {
        existingButton.remove();
    }

    const addButton = document.createElement("button");
    addButton.classList.add("add-btn");
    addButton.innerText = "+";
    addButton.onclick = () => addOperation(addButton);

    container.appendChild(addButton);
}

document.addEventListener("DOMContentLoaded", () => {
    addClassSection(); // Automatically add the first class box
    document.querySelector(".save-btn").addEventListener("click", () => {
        alert("Class data saved!");
    });
});

let connectionCounter = 1;

function addConnection() {
    const connectionsWrapper = document.getElementById("connections-wrapper");

    // Buat container connection baru
    const newConnectionContainer = document.createElement("div");
    newConnectionContainer.classList.add("connection-container");
    newConnectionContainer.innerHTML = `
        <h3>Connection ${connectionCounter}:</h3>
        <label>Path Name</label>
        <input type="text" placeholder="input path name" class="input-box">
        
        <label>Relation</label>
        <select class="input-box">
            <option>Choose relation</option>
        </select>
        
        <div class="class-selection">
            <label>Class Start</label>
            <select class="input-box">
                <option>Choose class</option>
            </select>
            
            <label>Class End</label>
            <select class="input-box">
                <option>Choose class</option>
            </select>
        </div>
        
        <div class="relation-reverse">
            <label>Relation reverse</label>
            <select class="input-box">
                <option>Choose reverse relation</option>
            </select>
        </div>
    `;

    // Tambahkan tombol delete
    // Tambahkan tombol delete dengan ikon yang sama seperti di class container
    const deleteBtn = document.createElement("button");
    deleteBtn.classList.add("delete-connection-btn");
    deleteBtn.innerHTML = '<i class="fas fa-trash-alt"></i>'; // Ikon Font Awesome untuk tempat sampah
    deleteBtn.onclick = () => deleteConnection(newConnectionContainer);
    newConnectionContainer.appendChild(deleteBtn);


    // Tambahkan tombol + hanya di container connection paling bawah
    const addConnectionBtn = document.createElement("button");
    addConnectionBtn.classList.add("add-connection-btn");
    addConnectionBtn.textContent = "+";
    addConnectionBtn.onclick = addConnection;
    newConnectionContainer.appendChild(addConnectionBtn);

    // Hapus tombol + dari connection sebelumnya
    const previousConnection = document.querySelector(".connection-container:last-child .add-connection-btn");
    if (previousConnection) previousConnection.remove();

    connectionsWrapper.appendChild(newConnectionContainer);

    // Perbarui penomoran
    updateConnectionNumbers();
}

function deleteConnection(connectionElement) {
    connectionElement.remove();

    // Perbarui penomoran
    updateConnectionNumbers();
}

function updateConnectionNumbers() {
    const connections = document.querySelectorAll(".connection-container");
    connectionCounter = 1;

    connections.forEach((connection, index) => {
        connection.id = `connection-${index + 1}`;
        connection.querySelector("h3").textContent = `Connection ${index + 1}:`;
    });

    // Pastikan hanya connection paling bawah yang memiliki tombol +
    const lastConnection = document.querySelector(".connection-container:last-child");
    if (lastConnection && !lastConnection.querySelector(".add-connection-btn")) {
        const addConnectionBtn = document.createElement("button");
        addConnectionBtn.classList.add("add-connection-btn");
        addConnectionBtn.textContent = "+";
        addConnectionBtn.onclick = addConnection;
        lastConnection.appendChild(addConnectionBtn);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const initialAddConnectionBtn = document.querySelector(".add-connection-btn");
    initialAddConnectionBtn.addEventListener("click", addConnection);
});