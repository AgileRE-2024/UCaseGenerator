function addBasicPathRow() {
    const table = document.getElementById('basicPathTable');
    const row = table.insertRow();

    row.insertCell(0).innerHTML = '';
    row.insertCell(1).innerHTML = '<textarea name="basic_actor_step[]" rows="2"></textarea>';
    row.insertCell(2).innerHTML = '<textarea name="basic_system_step[]" rows="2"></textarea>';

    document.getElementById('deleteBasicRow').style.display = 'inline-block';
}

function addAlternativePathRow() {
    const table = document.getElementById('alternativePathTable');
    const row = table.insertRow();

    row.insertCell(0).innerHTML = '';
    row.insertCell(1).innerHTML = '<textarea name="alternative_actor_step[]" rows="2"></textarea>';
    row.insertCell(2).innerHTML = '<textarea name="alternative_system_step[]" rows="2"></textarea>';

    document.getElementById('deleteAlternativeRow').style.display = 'inline-block';
}

function addExceptionPathRow() {
    const table = document.getElementById('exceptionPathTable');
    const row = table.insertRow();

    row.insertCell(0).innerHTML = '';
    row.insertCell(1).innerHTML = '<textarea name="exception_actor_step[]" rows="2"></textarea>';
    row.insertCell(2).innerHTML = '<textarea name="exception_system_step[]" rows="2"></textarea>';

    document.getElementById('deleteExceptionRow').style.display = 'inline-block';
}

// Event Listeners untuk tombol tambah baris
document.getElementById('addBasicStepButton').addEventListener('click', addBasicPathRow);
document.getElementById('addAlternativeStepButton').addEventListener('click', addAlternativePathRow);
document.getElementById('addExceptionStepButton').addEventListener('click', addExceptionPathRow);


// Event listener untuk ikon delete Basic Path
document.getElementById('deleteBasicRow').addEventListener('click', function () {
    const table = document.getElementById('basicPathTable');
    if (table.rows.length > 2) {
        table.deleteRow(table.rows.length - 1);
        if (table.rows.length === 2) {
            document.getElementById('deleteBasicRow').style.display = 'none';
        }
    }
});

// Event listener untuk ikon delete Alternative Path
document.getElementById('deleteAlternativeRow').addEventListener('click', function () {
    const table = document.getElementById('alternativePathTable');
    if (table.rows.length > 2) {
        table.deleteRow(table.rows.length - 1);
        if (table.rows.length === 2) {
            document.getElementById('deleteAlternativeRow').style.display = 'none';
        }
    }
});

// Event listener untuk ikon delete Exception Path
document.getElementById('deleteExceptionRow').addEventListener('click', function () {
    const table = document.getElementById('exceptionPathTable');
    if (table.rows.length > 2) {
        table.deleteRow(table.rows.length - 1);
        if (table.rows.length === 2) {
            document.getElementById('deleteExceptionRow').style.display = 'none';
        }
    }
});
// // Event Listeners untuk tombol tambah baris
// document.getElementById('addBasicStepButton').addEventListener('click', addBasicPathRow);
// document.getElementById('addAlternativeStepButton').addEventListener('click', addAlternativePathRow);
// document.getElementById('addExceptionStepButton').addEventListener('click', addExceptionPathRow);


document.getElementById('submitbutton').addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById('useCaseForm'));
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let valid = validateSteps();

    if (valid) {
        fetch("{% url 'save_specification' %}", {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert("Data saved successfully!");
                } else {
                    alert("Failed to save data. Please try again.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("An error occurred while saving data.");
            });
    } else {
        alert("Please fill in all fields before generating the diagram.");
    }
});

function validateSteps() {
    let allStepsValid = true;

    // Validasi Basic Path
    const basicActorSteps = document.querySelectorAll('textarea[name="basic_actor_step[]"]');
    const basicSystemSteps = document.querySelectorAll('textarea[name="basic_system_step[]"]');
    allStepsValid = validatePathSteps(basicActorSteps, basicSystemSteps);

    // Validasi Alternative Path
    const altActorSteps = document.querySelectorAll('textarea[name="alternative_actor_step[]"]');
    const altSystemSteps = document.querySelectorAll('textarea[name="alternative_system_step[]"]');
    allStepsValid = validatePathSteps(altActorSteps, altSystemSteps) && allStepsValid;

    // Validasi Exception Path
    const excActorSteps = document.querySelectorAll('textarea[name="exception_actor_step[]"]');
    const excSystemSteps = document.querySelectorAll('textarea[name="exception_system_step[]"]');
    allStepsValid = validatePathSteps(excActorSteps, excSystemSteps) && allStepsValid;

    return allStepsValid;
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const form = document.getElementById('use-case-form');
form.addEventListener('submit', function (event) {
    const actorSelect = document.getElementById('actorSelect');
    if (!actorSelect.value) {
        alert('Please select an actor.');
        event.preventDefault();  // Prevent form submission
    }
});
