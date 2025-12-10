// Geo Data
const geoData = {
    "Chile": ["Santiago", "Valparaíso", "Concepción", "La Serena", "Antofagasta", "Temuco"],
    "Colombia": ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena"],
    "México": ["Ciudad de México", "Guadalajara", "Monterrey", "Puebla", "Cancún"],
    "Argentina": ["Buenos Aires", "Córdoba", "Rosario", "Mendoza"],
    "Bolivia": ["La Paz", "Santa Cruz", "Cochabamba"],
    "Ecuador": ["Quito", "Guayaquil", "Cuenca"],
    "Perú": ["Lima", "Arequipa", "Trujillo"],
    "Uruguay": ["Montevideo", "Salto", "Punta del Este"]
};

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Flatpickr for Time Inputs
    flatpickr(".time-picker", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr: true,
    });

    // 2. Initialize Geo Dropdowns with 'Otro' logic
    const countrySelect = document.getElementById('pais');
    const citySelect = document.getElementById('ciudad');
    const countryOtherInput = document.getElementById('pais_otro');
    const cityOtherInput = document.getElementById('ciudad_otro');

    function populateCountries() {
        const priority = ["Chile", "Colombia", "México"];
        const others = Object.keys(geoData).filter(c => !priority.includes(c)).sort();
        const allCountries = [...priority, ...others];

        allCountries.forEach(country => {
            const option = document.createElement('option');
            option.value = country;
            option.textContent = country;
            countrySelect.appendChild(option);
        });

        // Add option "Otro"
        const optionOther = document.createElement('option');
        optionOther.value = "Otro";
        optionOther.textContent = "Otro";
        countrySelect.appendChild(optionOther);

        // Trigger city population for default selection
        handleCountryChange(countrySelect.value);
    }

    function populateCities(country) {
        citySelect.innerHTML = ''; // Clear

        let cities = [];
        if (country !== "Otro") {
            cities = geoData[country] || [];
        }

        cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            citySelect.appendChild(option);
        });

        // Add option "Otro" always
        const optionOther = document.createElement('option');
        optionOther.value = "Otro";
        optionOther.textContent = "Otro";
        citySelect.appendChild(optionOther);

        handleCityChange(citySelect.value);
    }

    function handleCountryChange(val) {
        if (val === "Otro") {
            countryOtherInput.style.display = "block";
            countryOtherInput.required = true;
            countryOtherInput.focus();
            populateCities("Otro");
        } else {
            countryOtherInput.style.display = "none";
            countryOtherInput.required = false;
            populateCities(val);
        }
    }

    function handleCityChange(val) {
        if (val === "Otro") {
            cityOtherInput.style.display = "block";
            cityOtherInput.required = true;
            cityOtherInput.focus();
        } else {
            cityOtherInput.style.display = "none";
            cityOtherInput.required = false;
        }
    }

    if (countrySelect && citySelect) {
        countrySelect.addEventListener('change', (e) => handleCountryChange(e.target.value));
        citySelect.addEventListener('change', (e) => handleCityChange(e.target.value));
        populateCountries();
    }

    // Set default date to today
    const dateInput = document.getElementById('fecha_entrega');
    if (dateInput) dateInput.valueAsDate = new Date();

    // ---------------------------------------------------------
    // DYNAMIC TAGS BUILDER LOGIC
    // ---------------------------------------------------------
    const addTagBtn = document.getElementById('addTagBtn');
    const tagsContainer = document.getElementById('tagsContainer');
    const tagTemplate = document.getElementById('tagTemplate');

    if (addTagBtn && tagsContainer && tagTemplate) {
        console.log("Tag Builder Initialized"); // Debug

        addTagBtn.addEventListener('click', () => {
            console.log("Adding Tag Group...");
            const clone = tagTemplate.content.cloneNode(true);
            const card = clone.querySelector('.tag-card');

            // Remove Tag Group Button
            const removeTagBtn = card.querySelector('.remove-tag-btn');
            removeTagBtn.addEventListener('click', () => {
                card.remove();
            });

            // Add Value Button
            const valuesContainer = card.querySelector('.tag-values-container');
            const addValueBtn = card.querySelector('.add-value-btn');

            addValueBtn.addEventListener('click', () => {
                console.log("Adding Value Input...");
                const div = document.createElement('div');
                div.style.display = 'flex';
                div.style.gap = '0.5rem';
                div.style.alignItems = 'center';
                div.innerHTML = `
                    <input type="text" class="form-input tag-value" placeholder="Valor (Ej: Rojo)" required>
                    <button type="button" class="remove-value-btn" style="border:none; background:none; cursor:pointer; color: var(--red-500); font-size: 1.2rem;">&times;</button>
                `;
                // Remove Value Button Logic
                div.querySelector('.remove-value-btn').addEventListener('click', () => div.remove());
                valuesContainer.appendChild(div);
            });

            tagsContainer.appendChild(card);
        });
    } else {
        console.error("Tags elements missing in DOM");
    }

    // ---------------------------------------------------------
    // FORM SUBMISSION
    // ---------------------------------------------------------
    const form = document.getElementById('generateForm');
    const submitBtn = document.getElementById('submitBtn');

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            console.log("Form Submitting...");

            // Validation
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            // Resolve Final Country/City
            let finalCountry = data.pais;
            if (finalCountry === "Otro") {
                finalCountry = data.pais_otro.trim();
            }

            let finalCity = data.ciudad;
            if (finalCity === "Otro") {
                finalCity = data.ciudad_otro.trim();
            }

            if (!finalCountry) {
                showToast('Error: Especifique el País.', 'error');
                return;
            }
            if (!finalCity) {
                showToast('Error: Especifique la Ciudad.', 'error');
                return;
            }

            // 1. Validate Arrays
            if (parseInt(data.cantidad_ordenes) <= 0) {
                showToast('Error: La cantidad de órdenes debe ser mayor a 0.', 'error');
                return;
            }

            // 2. Validate CT Origen (Required)
            if (!data.ct_origen || data.ct_origen.trim() === '') {
                showToast('Error: El CT Origen es obligatorio.', 'error');
                return;
            }

            // 3. Validate Time Windows
            if (data.ventana_inicio >= data.ventana_fin) {
                showToast('Error: La Ventana 1 Inicio debe ser anterior a Ventana 1 Fin.', 'error');
                return;
            }

            if (data.ventana2_inicio && data.ventana2_fin) {
                if (data.ventana2_inicio >= data.ventana2_fin) {
                    showToast('Error: La Ventana 2 Inicio debe ser anterior a Ventana 2 Fin.', 'error');
                    return;
                }
            }

            // 4. Validate Capacity Range
            if (parseFloat(data.capacidad_min) > parseFloat(data.capacidad_max)) {
                showToast('Error: La capacidad mínima no puede ser mayor que la capacidad máxima.', 'error');
                return;
            }

            // 5. Build Tags Payload
            const tags = [];
            const tagCards = tagsContainer.querySelectorAll('.tag-card');
            for (const card of tagCards) {
                const headerInput = card.querySelector('.tag-header');
                const header = headerInput ? headerInput.value.trim() : null;
                const valueInputs = card.querySelectorAll('.tag-value');
                const values = Array.from(valueInputs).map(input => input.value.trim()).filter(v => v !== "");

                if (header && values.length > 0) {
                    tags.push({ header, values });
                }
            }

            // Loading State
            setLoading(true);

            try {
                // Transform data logic
                const payload = {
                    ...data,
                    cantidad_ordenes: parseInt(data.cantidad_ordenes),
                    // Override with resolved strings
                    pais: finalCountry,
                    ciudad: finalCity,
                    // Default Items to 1 if empty/null
                    items_por_orden: data.items_por_orden ? parseInt(data.items_por_orden) : 1,
                    capacidad_min: parseFloat(data.capacidad_min),
                    capacidad_max: parseFloat(data.capacidad_max),
                    // Cap 2 Optional (Handle 0 correctly)
                    capacidad2_min: data.capacidad2_min !== "" ? parseFloat(data.capacidad2_min) : null,
                    capacidad2_max: data.capacidad2_max !== "" ? parseFloat(data.capacidad2_max) : null,
                    service_time: data.service_time ? parseInt(data.service_time) : null,
                    tags: tags
                };

                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                if (!response.ok) {
                    const errJson = await response.json();
                    throw new Error(errJson.error || 'Error en el servidor al generar archivo.');
                }

                // Handle file download
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                const filename = `ordenes_${finalCity}_${new Date().toISOString().slice(0, 10)}.xlsx`;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                a.remove();

                showToast(`¡Éxito! Archivo "${filename}" descargado.`, 'success');
            } catch (error) {
                console.error(error);
                showToast(error.message, 'error');
            } finally {
                setLoading(false);
            }
        });
    }

    function setLoading(isLoading) {
        if (submitBtn) {
            submitBtn.disabled = isLoading;
            if (isLoading) {
                submitBtn.innerHTML = '<div class="spinner"></div> Generando...';
            } else {
                submitBtn.innerHTML = '<span id="btnText">Generar y Descargar .xlsx</span> <i class="ph-bold ph-download-simple"></i>';
            }
        }
    }

    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icon = type === 'success' ? '<i class="ph-bold ph-check-circle"></i>' : '<i class="ph-bold ph-warning-circle"></i>';

        // Ensure toastContainer exists
        let container = document.getElementById('toastContainer');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toastContainer';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }

        toast.innerHTML = `
            ${icon}
            <span>${message}</span>
        `;

        container.appendChild(toast);

        // Remove after 4 seconds
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(10px)';
            toast.style.transition = 'all 0.3s';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }
});
