const btnsConfirms = document.querySelectorAll('#btnBorrar')


if(btnsConfirms.length){
    for(const btn of btnsConfirms){
        btn.addEventListener("click", event => {
            const resp = confirm("Esta opción no tiene marcha atrás. ¿Confirma?")
            if (!resp) event.preventDefault()
        })
    }
}

