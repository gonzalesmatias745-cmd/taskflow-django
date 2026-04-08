const BASE_URL = "http://127.0.0.1:8000/api";


function mostrarToast(mensaje) {
    const toast = document.getElementById("toast");
    toast.innerText = mensaje;
    toast.style.opacity = "1";
    toast.style.transform = "translateY(0)";

    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(20px)";
    }, 2000);
}

// 🔐 LOGIN
function login() {

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch(`${BASE_URL}/login/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(res => res.json())
    .then(data => {
        if(data.message){
            alert("Login exitoso");

            document.getElementById("login").style.display = "none";
            document.getElementById("app").style.display = "block";

            cargarTareas();
        } else {
            alert("Error login");
        }
    });
}


// ➕ CREAR TAREA
function crearTarea(){

    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;

    fetch(`${BASE_URL}/tasks/create/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: title,
            description: description,
            status: "Pendiente"
        })
    })
    .then(res => res.json())
    .then(data => {
        alert("Tarea creada");
        cargarTareas();
    });
}


// 📋 VER TAREAS
function cargarTareas(){

    fetch(`${BASE_URL}/tasks/`)
    .then(res => res.json())
    .then(data => {

        const lista = document.getElementById("listaTareas");
        lista.innerHTML = "";

        data.forEach(tarea => {

            const li = document.createElement("li");

            li.innerHTML = `
                <b>${tarea.title}</b> - ${tarea.status}
                <br>
                ${tarea.description}
                <br>
                <button onclick="completar('${tarea.id}')">Completar</button>
                <button onclick="eliminar('${tarea.id}')">Eliminar</button>
            `;

            lista.appendChild(li);
        });
    });
}


// ✅ ACTUALIZAR
function completar(id){

    fetch(`${BASE_URL}/tasks/${id}/update/`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            status: "Completada"
        })
    })
    .then(res => res.json())
    .then(data => {
        cargarTareas();
    });
}


// ❌ ELIMINAR
function eliminar(id){

    fetch(`${BASE_URL}/tasks/${id}/delete/`, {
        method: "DELETE"
    })
    .then(res => res.json())
    .then(data => {
        cargarTareas();
    });
}