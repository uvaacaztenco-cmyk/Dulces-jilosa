// Configuración Global
const API = "http://127.0.0.1:8000";
async function login(){

let username = document.getElementById("username").value
let password = document.getElementById("password").value

let formData = new URLSearchParams()

formData.append("username", username)
formData.append("password", password)

try{

let response = await fetch(API + "/login",{

method:"POST",

headers:{
"Content-Type":"application/x-www-form-urlencoded"
},

body:formData

})

let data = await response.json()

if(response.ok){

localStorage.setItem("token", data.access_token)

window.location.href = "pos.html"

}else{

document.getElementById("mensaje").innerText = data.detail

}

}catch(error){

console.error("Error login:", error)

}

}
let carrito = [];
let productosGlobal = [];

/** * Gestión de Sesión 
 */
function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

/** * Lógica de Productos 
 */
async function cargarProductos() {
    let token = localStorage.getItem("token");
    try {
        let response = await fetch(`${API}/productos`, {
            headers: {
                Authorization: "Bearer " + token
            }
        });

        if (!response.ok) throw new Error("No se pudieron cargar los productos");

        let productos = await response.json();
        productosGlobal = productos;
        mostrarProductos(productos);
    } catch (error) {
        console.error("Error:", error);
    }
}

function mostrarProductos(productos) {
    let contenedor = document.getElementById("productos");
    contenedor.innerHTML = "";

    productos.forEach(p => {
        let btn = document.createElement("button");
        btn.className = "producto-btn"; // Clase opcional para CSS
        btn.innerText = `${p.name} $${p.price}`;
        btn.onclick = () => agregarCarrito(p);
        contenedor.appendChild(btn);
    });
}

function buscarProducto() {
    let texto = document.getElementById("busqueda").value.toLowerCase();
    let filtrados = productosGlobal.filter(p =>
        p.name.toLowerCase().includes(texto)
    );
    mostrarProductos(filtrados);
}

/** * Gestión del Carrito 
 */
function agregarCarrito(producto) {
    let existente = carrito.find(p => p.product_id == producto.id);

    if (existente) {
        existente.quantity++;
    } else {
        carrito.push({
            product_id: producto.id,
            name: producto.name,
            price: producto.price,
            quantity: 1
        });
    }
    renderCarrito();
}

function eliminarProducto(index) {
    carrito.splice(index, 1);
    renderCarrito();
}

function renderCarrito() {
    let lista = document.getElementById("carrito");
    let totalElement = document.getElementById("total");
    lista.innerHTML = "";
    let total = 0;

    carrito.forEach((p, index) => {
        let li = document.createElement("li");
        let subtotal = p.price * p.quantity;
        total += subtotal;

        // Corregido: Uso de template literals con backticks
        li.innerHTML = `
            ${p.name} x${p.quantity} - $${subtotal.toFixed(2)}
            <button onclick="eliminarProducto(${index})">❌</button>
        `;
        lista.appendChild(li);
    });

    totalElement.innerText = total.toFixed(2);
}

/** * Cálculos y Finalización de Venta 
 */
function calcularCambio() {
    let total = parseFloat(document.getElementById("total").innerText);
    let pago = parseFloat(document.getElementById("pago").value);

    if (isNaN(pago)) {
        alert("Por favor, ingresa un monto válido");
        return;
    }

    let cambio = pago - total;

    if (cambio < 0) {
        alert("Dinero insuficiente");
        return;
    }

    document.getElementById("cambio").innerText = cambio.toFixed(2);
}

async function registrarVenta() {
    if (carrito.length === 0) {
        alert("El carrito está vacío");
        return;
    }

    let token = localStorage.getItem("token");

    try {
        let response = await fetch(`${API}/ventas`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + token
            },
            body: JSON.stringify({
                items: carrito
            })
        });

        let data = await response.json();

        if (response.ok) {
            alert("Venta registrada con éxito. Total: $" + data.total);
            carrito = [];
            renderCarrito();
            document.getElementById("pago").value = "";
            document.getElementById("cambio").innerText = "0";
        } else {
            alert("Error al registrar venta: " + data.detail);
        }
    } catch (error) {
        console.error("Error en la venta:", error);
    }
}

/** * Inicialización 
 */
if (window.location.pathname.includes("pos.html")) {
    cargarProductos();
}