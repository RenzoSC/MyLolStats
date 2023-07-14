// Datos de ejemplo (cantidad de partidas ganadas)
var partidasGanadas = 50;
var partidasPerdidas = 30;

// Configuración del gráfico
var data = {
    datasets: [{
        data: [partidasGanadas, partidasPerdidas],
        backgroundColor: ["green", "red"]
    }]
};

// Opciones del gráfico
var options = {
    responsive: true,
    maintainAspectRatio: false
};

// Crear y mostrar el gráfico de anillo
var ctx = document.getElementById("donutChart").getContext("2d");
new Chart(ctx, {
    type: "doughnut",
    data: data,
    options: options
});