document.addEventListener("DOMContentLoaded", () => {
    const addPatientForm = document.getElementById("add-patient");
    const addPatientTrigger = document.getElementById("add-patient-button");
    const cancelButtons = document.querySelectorAll("button.cancel");

    function toggleFormVisibility(form, trigger) {
        if (form.classList.contains("hidden")) {
            form.classList.remove("hidden");
            if (trigger) trigger.disabled = true;
        } else {
            form.classList.add("hidden");
            if (trigger) trigger.disabled = false;
            resetForm(form);
        }
    }

    function resetForm(form) {
        const inputs = form.querySelectorAll("input");
        inputs.forEach(input => input.value = "");
        const links = form.querySelectorAll("a");
        links.forEach(link => link.setAttribute("href", "#"));
    }

    addPatientTrigger.addEventListener("click", () => {
        toggleFormVisibility(addPatientForm, addPatientTrigger);
    });


    cancelButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            event.preventDefault();
            const form = button.closest("form");
            if (form.id === "add-patient") {
                toggleFormVisibility(addPatientForm, addPatientTrigger);
            }
        });
    });

    const addFormInputs = document.querySelectorAll("#add-patient input");
    const addPatientLink = document.getElementById("add-patient-link");

    addFormInputs.forEach(input => {
        input.addEventListener("input", () => {
            const publicId = document.getElementById("public_id").value || '';
            const ip = document.getElementById("ip").value || '';
            const name = document.getElementById("name").value || '';
            const sex = document.getElementById("sex").value || '';
            const age = document.getElementById("age").value || '';
            const city = document.getElementById("city").value || '';

            const baseUrl = "/add-patient/";
            const queryParams = `${encodeURIComponent(publicId)};${encodeURIComponent(ip)};${encodeURIComponent(name)};${encodeURIComponent(age)};${encodeURIComponent(sex)};${encodeURIComponent(city)}`;
            const fullUrl = `${baseUrl}${queryParams}`;

            addPatientLink.setAttribute("href", fullUrl);
        });
    });
});
