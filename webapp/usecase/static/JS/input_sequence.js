document.addEventListener('DOMContentLoaded', function () {
    // Fungsi untuk mendapatkan semua objek dari kategori input yang ada
    function getObjectOptions() {
        const objects = [];
        
        // Dapatkan semua elemen input yang ada di container yang relevan
        document.querySelectorAll('#actor-container input, #boundary-container input, #controller-container input, #entity-container input').forEach(input => {
            if (input.value) objects.push(input.value);
        });

        return [...new Set(objects)];  // Hapus duplikasi
    }

    // Fungsi untuk mengisi dropdown dengan opsi objek
    function populateDropdown(dropdownId) {
        const dropdown = document.getElementById(dropdownId);
        const objects = getObjectOptions();
        
        // Kosongkan dropdown sebelumnya
        dropdown.innerHTML = '<option>Pilih objek</option>';
        
        // Tambahkan opsi baru ke dropdown
        objects.forEach(object => {
            const option = document.createElement('option');
            option.textContent = object;
            option.value = object;
            dropdown.appendChild(option);
        });
    }

    // Fungsi untuk memperbarui semua dropdown saat input berubah
    function updateAllDropdowns() {
        populateDropdown('object-start-basic-path');
        populateDropdown('object-end-basic-path');
        populateDropdown('object-start-alternative-path');
        populateDropdown('object-end-alternative-path');
        populateDropdown('object-start-alternative-path-2');
        populateDropdown('object-end-alternative-path-2');
    }

    // Pasang event listener untuk setiap input yang ada saat ini
    function attachInputListeners() {
        const inputs = document.querySelectorAll('#actor-container input, #boundary-container input, #controller-container input, #entity-container input');
        
        inputs.forEach(input => {
            input.addEventListener('input', updateAllDropdowns);
        });
    }

    // Gunakan MutationObserver untuk mendeteksi penambahan elemen baru
    const observerConfig = { childList: true, subtree: true };
    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            if (mutation.addedNodes.length) {
                // Pasang ulang event listener saat elemen baru ditambahkan
                attachInputListeners();
                updateAllDropdowns();
            }
        });
    });

    // Observasi perubahan pada container input
    const containers = document.querySelectorAll('#actor-container, #boundary-container, #controller-container, #entity-container');
    containers.forEach(container => observer.observe(container, observerConfig));

    // Pasang listener pada input awal dan isi dropdown
    attachInputListeners();
    updateAllDropdowns();
});
