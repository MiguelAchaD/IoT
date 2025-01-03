function reversePatientFormVisibility(patientForm, patientFormTrigger) {
    let patientAttributes = patientForm.getAttribute("class").toString()
    if (patientAttributes.includes("hidden")) {
        patientForm.classList.remove("hidden")
        patientFormTrigger.setAttribute("style", "disabled")
        let patientFormCancel = document.getElementById("cancel-patient")
        
        patientFormCancel.addEventListener("click", (form_event) => {
            reversePatientFormVisibility(patientForm, patientFormTrigger)
        })
    } else {
        patientForm.setAttribute("class", "hidden")
        patientFormTrigger.removeAttribute("disabled")
    }
}

addEventListener("DOMContentLoaded", (event) => {
    let patientForm = document.getElementById("add-patient")
    let patientFormTrigger = document.getElementById("add-patient-button")

    patientFormTrigger.addEventListener("click", (form_event) => {
        reversePatientFormVisibility(patientForm, patientFormTrigger)
    })
});