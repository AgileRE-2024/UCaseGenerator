let classCounter = 1;

// Fungsi untuk mengambil CSRF token dari cookie
function getCSRFToken() {
    let csrfToken = null;
    const cookies = document.cookie.split(';');
    cookies.forEach(cookie => {
        if (cookie.trim().startsWith('csrftoken=')) {
            csrfToken = cookie.trim().substring('csrftoken='.length);
        }
    });
    return csrfToken;
}

function addClassSection() {
    const classContainer = document.getElementById("class-container");

    // Buat section untuk class baru
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

    // Tambahkan section baru ke dalam container
    classContainer.appendChild(classSection);

    // Tambahkan tombol hapus untuk class kecuali class pertama
    if (classCounter > 1) {
        const deleteButton = document.createElement("button");
        deleteButton.classList.add("delete-btn");
        deleteButton.innerHTML = '<i class="fas fa-trash-alt"></i>';
        deleteButton.onclick = () => deleteClassSection(deleteButton);
        classSection.appendChild(deleteButton);
    }

    // Tambahkan tombol "+" untuk attribute dan operation
    addAttributeButton(classSection.querySelector(".attributes-container"));
    addOperationButton(classSection.querySelector(".operations-container"));

    // Perbarui tombol "+" untuk class
    updateAddClassButton();

    classCounter++;
}

function deleteClassSection(button) {
    const classSection = button.closest(".class-section");
    classSection.remove(); // Hapus section class

    // Perbarui nomor class setelah penghapusan
    updateClassNumbers();

    // Perbarui tombol "+"
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
    classCounter = classSections.length + 1; // Perbarui counter global
}

function updateAddClassButton() {
    // Hapus semua tombol "+"
    document.querySelectorAll(".add-class-btn").forEach(btn => btn.remove());

    // Tambahkan tombol "+" hanya pada class terakhir
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

function addAttributeButton(container) {
    // Pastikan hanya ada satu tombol "+" di dalam container
    let addButton = container.querySelector(".add-attribute-btn");
    if (!addButton) {
        addButton = document.createElement("button");
        addButton.classList.add("add-btn", "add-attribute-btn");
        addButton.innerText = "+";
        addButton.onclick = () => addAttribute(container); // Panggil fungsi tambah attribute
        container.appendChild(addButton);
    }
}

function addOperationButton(container) {
    // Pastikan hanya ada satu tombol "+" di dalam container
    let addButton = container.querySelector(".add-operation-btn");
    if (!addButton) {
        addButton = document.createElement("button");
        addButton.classList.add("add-btn", "add-operation-btn");
        addButton.innerText = "+";
        addButton.onclick = () => addOperation(container); // Panggil fungsi tambah operation
        container.appendChild(addButton);
    }
}

function addAttribute(container) {
    const newAttributeGroup = document.createElement("div");
    newAttributeGroup.classList.add("attribute-group");

    const newAttributeInput = document.createElement("input");
    newAttributeInput.type = "text";
    newAttributeInput.classList.add("input-box");

    const deleteButton = document.createElement("button");
    deleteButton.classList.add("delete-attr-btn");
    deleteButton.innerHTML = '<i class="fas fa-trash-alt"></i>';
    deleteButton.onclick = () => {
        deleteAttribute(deleteButton);
        updateAttributeNumbers(container);
    };

    newAttributeGroup.appendChild(newAttributeInput);
    newAttributeGroup.appendChild(deleteButton);
    container.insertBefore(newAttributeGroup, container.querySelector(".add-attribute-btn"));

    updateAttributeNumbers(container);
}

function addOperation(container) {
    const newOperationGroup = document.createElement("div");
    newOperationGroup.classList.add("operation-group");

    const newOperationInput = document.createElement("input");
    newOperationInput.type = "text";
    newOperationInput.classList.add("input-box");

    const deleteButton = document.createElement("button");
    deleteButton.classList.add("delete-op-btn");
    deleteButton.innerHTML = '<i class="fas fa-trash-alt"></i>';
    deleteButton.onclick = () => {
        deleteOperation(deleteButton);
        updateOperationNumbers(container);
    };

    newOperationGroup.appendChild(newOperationInput);
    newOperationGroup.appendChild(deleteButton);
    container.insertBefore(newOperationGroup, container.querySelector(".add-operation-btn"));

    updateOperationNumbers(container);
}

function deleteAttribute(button) {
    const attributeGroup = button.closest(".attribute-group");
    const attributesContainer = button.closest(".attributes-container");
    attributeGroup.remove();
    updateAttributeNumbers(attributesContainer);
}

function deleteOperation(button) {
    const operationGroup = button.closest(".operation-group");
    const operationsContainer = button.closest(".operations-container");
    operationGroup.remove();
    updateOperationNumbers(operationsContainer);
}

function updateAttributeNumbers(container) {
    const attributeGroups = container.querySelectorAll(".attribute-group");
    attributeGroups.forEach((group, index) => {
        const inputBox = group.querySelector("input[type='text']");
        inputBox.placeholder = `${index + 1}.`;
    });
}

function updateOperationNumbers(container) {
    const operationGroups = container.querySelectorAll(".operation-group");
    operationGroups.forEach((group, index) => {
        const inputBox = group.querySelector("input[type='text']");
        inputBox.placeholder = `${index + 1}.`;
    });
}

// Fungsi untuk memperbarui dropdown kelas
function updateDropdowns(classes) {
    const classStartDropdown = document.getElementById("class-start");
    const classEndDropdown = document.getElementById("class-end");

    // Kosongkan dropdown terlebih dahulu
    classStartDropdown.innerHTML = '<option value="">Choose class</option>';
    classEndDropdown.innerHTML = '<option value="">Choose class</option>';

    // Tambahkan opsi baru
    classes.forEach(cls => {
        const optionStart = document.createElement("option");
        optionStart.value = cls.id; // ID class
        optionStart.textContent = cls.name; // Nama class

        // Tambahkan ke dropdown Class Start
        classStartDropdown.appendChild(optionStart);

        // Clone dan tambahkan ke dropdown Class End
        const optionEnd = optionStart.cloneNode(true);
        classEndDropdown.appendChild(optionEnd);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    addClassSection(); // Tambahkan class pertama

    document.querySelector(".save-btn").addEventListener("click", function () {
        const classesData = [];
        const connectionsData = [];

        document.querySelectorAll(".class-section").forEach(classSection => {
            const className = classSection.querySelector("input[type='text']").value;
            const attributes = [];
            const operations = [];

            classSection.querySelectorAll(".attribute-group input").forEach(input => {
                attributes.push(input.value);
            });

            classSection.querySelectorAll(".operation-group input").forEach(input => {
                operations.push(input.value);
            });

            classesData.push({
                name: className,
                attributes: attributes,
                operations: operations
            });
        });

        fetch('/save_data/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ classes: classesData, connections: connectionsData }),
        })
            .then(response => response.json())
            .then(data => {
                alert("Data berhasil disimpan!");
                updateDropdowns(data.classes); // Update dropdown dengan data kelas yang baru
            })
            .catch(error => {
                console.error("Error saat menyimpan data:", error);
                alert("Gagal menyimpan data.");
            });
    });
});
