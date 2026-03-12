const API = "http://127.0.0.1:8000"

function logout(){

localStorage.removeItem("token")

window.location.href="login.html"

}

async function cargarProductos(){

let token = localStorage.getItem("token")

let response = await fetch(API + "/productos",{

headers:{
Authorization:"Bearer " + token
}

})

let productos = await response.json()

let tabla = document.getElementById("tablaProductos")

tabla.innerHTML=""

productos.forEach(p=>{

let fila = document.createElement("tr")

fila.innerHTML = `

<td>${p.id}</td>

<td>${p.name}</td>

<td>${p.price}</td>

<td>${p.stock}</td>

<td>

<button onclick="editarProducto(${p.id})">Editar</button>

<button onclick="eliminarProducto(${p.id})">Eliminar</button>

</td>

`

tabla.appendChild(fila)

})

}

async function crearProducto(){

let token = localStorage.getItem("token")

let nombre = document.getElementById("nombre").value
let precio = document.getElementById("precio").value
let stock = document.getElementById("stock").value

await fetch(API + "/productos?name=" + nombre + "&price=" + precio + "&stock=" + stock,{

method:"POST",

headers:{
Authorization:"Bearer " + token
}

})

cargarProductos()

}

async function editarProducto(id){

let nombre = prompt("Nuevo nombre")
let precio = prompt("Nuevo precio")
let stock = prompt("Nuevo stock")

let token = localStorage.getItem("token")

await fetch(API + "/productos/" + id + "?name=" + nombre + "&price=" + precio + "&stock=" + stock,{

method:"PUT",

headers:{
Authorization:"Bearer " + token
}

})

cargarProductos()

}

async function eliminarProducto(id){

let token = localStorage.getItem("token")

await fetch(API + "/productos/" + id,{

method:"DELETE",

headers:{
Authorization:"Bearer " + token
}

})

cargarProductos()

}

cargarProductos()