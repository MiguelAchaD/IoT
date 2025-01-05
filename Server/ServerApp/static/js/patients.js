function reversePatientFormVisibility(patientForm, patientFormTrigger) {
    let patientAttributes = patientForm.getAttribute("class").toString()
    if (patientAttributes.includes("hidden")) {
        patientForm.classList.remove("hidden")
        patientFormTrigger.setAttribute("style", "disabled")
        const patientFormCancel = document.getElementById("cancel-patient")
        
        patientFormCancel.addEventListener("click", (form_event) => {
            reversePatientFormVisibility(patientForm, patientFormTrigger)
        })
    } else {
        patientForm.setAttribute("class", "hidden")
        patientFormTrigger.removeAttribute("disabled")
    }
}

addEventListener("DOMContentLoaded", (event) => {
    const patientForm = document.getElementById("add-patient")
    const patientFormTrigger = document.getElementById("add-patient-button")

    patientFormTrigger.addEventListener("click", (form_event) => {
        reversePatientFormVisibility(patientForm, patientFormTrigger)
    })

    const addPatientLink = document.getElementById("add-patient-link");
    const addFormInputs = document.querySelectorAll("#add-patient input");

    addFormInputs.forEach(input => {
        input.addEventListener("input", function () {
            const publicId = document.getElementById("public_id").value || '';
            const name = document.getElementById("name").value || '';
            const sex = document.getElementById("sex").value || '';
            const age = document.getElementById("age").value || '';
            const city = document.getElementById("city").value || '';

            const baseUrl = "/add-patient/";
            const queryParams = `${encodeURIComponent(publicId)};${encodeURIComponent(name)};${encodeURIComponent(age)};${encodeURIComponent(sex)};${encodeURIComponent(city)}`;
            const fullUrl = `${baseUrl}${queryParams}`;

            addPatientLink.setAttribute("href", fullUrl);
        });
    });

    const editPatientLink = document.getElementById("edit-patient-link");
    const editFormInputs = document.querySelectorAll("#edit-patient input");

    editFormInputs.forEach(input => {
        input.addEventListener("input", function () {
            const oldPublicId = document.getElementById("public_id").value || '';
            const publicId = document.getElementById("public_id").value || '';
            const name = document.getElementById("name").value || '';
            const sex = document.getElementById("sex").value || '';
            const age = document.getElementById("age").value || '';
            const city = document.getElementById("city").value || '';

            const baseUrl = "/edit-patient/";
            const queryParams = `${encodeURIComponent(oldPublicId)};${encodeURIComponent(publicId)};${encodeURIComponent(name)};${encodeURIComponent(age)};${encodeURIComponent(sex)};${encodeURIComponent(city)}`;
            const fullUrl = `${baseUrl}${queryParams}`;

            editPatientLink.setAttribute("href", fullUrl);
        });
    });
});