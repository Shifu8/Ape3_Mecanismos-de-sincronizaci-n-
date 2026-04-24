function run(endpoint, btn) {

    const box = document.getElementById("res-" + endpoint);
    box.style.display = "block";
    box.innerHTML = "<span class='loading'>Ejecutando...</span>";

    fetch(`/${endpoint}`)
    .then(res => res.json())
    .then(data => {

        let html = "";

        // =============================
        // MUTEX
        // =============================
        if (endpoint === "mutex") {

            html = `
            <div class="label">Boletos vendidos</div>
            Secuencial: ${data.secuencial.resultado} <br>
            Concurrente: ${data.concurrente.resultado} <br><br>

            <div class="label">Tiempo (segundos)</div>
            Secuencial: ${data.secuencial.tiempo}s <br>
            Concurrente: ${data.concurrente.tiempo}s <br><br>

            <div class="ganador">
                ${ganador(data)}
            </div>
            `;
        }

        // =============================
        // SEMÁFORO
        // =============================
        else if (endpoint === "semaforo") {

    let logsHTML = data.concurrente.logs
        .map(l => "• " + l)
        .join("<br>");

    html = `
    <div class="label">Máximo uso de recursos</div>
    Secuencial: ${data.secuencial.max_uso} <br>
    Concurrente: ${data.concurrente.max_uso} <br><br>

    <div class="label">Tiempo</div>
    Secuencial: ${data.secuencial.tiempo}s <br>
    Concurrente: ${data.concurrente.tiempo}s <br><br>

    <div class="ganador">
        ${ganador(data)}
    </div>

    <br>
    <div class="label">Registro de actividad</div>
    <div style="max-height:150px; overflow:auto; font-size:12px; margin-top:5px;">
        ${logsHTML}
    </div>
    `;
}


        // =============================
        // PRODUCTOR-CONSUMIDOR
        // =============================
        else if (endpoint === "prodcons") {

            html = `
            <div class="label">Producción</div>
            Secuencial: ${data.secuencial.producidos} <br>
            Concurrente: ${data.concurrente.producidos} <br><br>

            <div class="label">Consumo</div>
            Secuencial: ${data.secuencial.consumidos} <br>
            Concurrente: ${data.concurrente.consumidos} <br><br>

            <div class="label">Tiempo</div>
            Secuencial: ${data.secuencial.tiempo}s <br>
            Concurrente: ${data.concurrente.tiempo}s <br><br>

            <div class="ganador">
                ${ganador(data)}
            </div>
            `;
        }

        // =============================
        // LECTORES-ESCRITORES
        // =============================
        else if (endpoint === "lectores") {

    let logsHTML = data.concurrente.operaciones
        .map(l => "• " + l)
        .join("<br>");

    html = `
    <div class="label">Accesos registrados</div>
    Total: ${data.concurrente.operaciones.length} <br><br>

    <div class="label">Tiempo</div>
    Secuencial: ${data.secuencial.tiempo}s <br>
    Concurrente: ${data.concurrente.tiempo}s <br><br>

    <div class="ganador">
        ${ganador(data)}
    </div>

    <br>
    <div class="label">Logs</div>
    <div style="max-height:150px; overflow:auto; font-size:12px;">
        ${logsHTML}
    </div>
    `;
}


        // =============================
        // BARRERA
        // =============================
        else if (endpoint === "barrera") {

    let logsHTML = data.concurrente.orden
        .map(l => "• " + l)
        .join("<br>");

    html = `
    <div class="label">Eventos</div>
    Total: ${data.concurrente.orden.length} <br><br>

    <div class="label">Tiempo</div>
    Secuencial: ${data.secuencial.tiempo}s <br>
    Concurrente: ${data.concurrente.tiempo}s <br><br>

    <div class="ganador">
        ${ganador(data)}
    </div>

    <br>
    <div class="label">Logs de sincronización</div>
    <div style="max-height:150px; overflow:auto; font-size:12px;">
        ${logsHTML}
    </div>
    `;
}


        box.innerHTML = html;

    })
    .catch(err => {
        box.innerText = "Error: " + err;
    });
}


// =============================
// FUNCIÓN PARA DECIDIR GANADOR
// =============================
function ganador(data) {
    return data.concurrente.tiempo < data.secuencial.tiempo
        ? "Concurrente más rápido"
        : "Secuencial más rápido";
}
