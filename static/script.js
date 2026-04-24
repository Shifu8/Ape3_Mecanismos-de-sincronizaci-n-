function run(endpoint, btn) {

    const box = document.getElementById("res-" + endpoint);
    box.style.display = "block";

    // estado de carga
    box.innerHTML = "<span class='loading'>Simulando ejecución...</span>";

    fetch(`/${endpoint}`)
    .then(res => res.json())
    .then(data => {

        let html = "";

        // helper logs
        const renderLogs = (logs) => {
            if (!logs) return "";
            return `
            <br>
            <div class="label">Registro de actividad</div>
            <div class="logs-box">
                ${logs.map(l => "• " + l).join("<br>")}
            </div>
            `;
        };

        // =============================
        // MUTEX
        // =============================
        if (endpoint === "mutex") {

            html = `
            <div class="label">Boletos vendidos</div>
            Secuencial: ${data.secuencial.resultado} <br>
            Concurrente: ${data.concurrente.resultado} <br><br>

            ${renderTiempo(data)}

            ${renderGanador(data)}

            ${renderLogs(data.concurrente.logs)}
            `;
        }

        // =============================
        // SEMÁFORO
        // =============================
        else if (endpoint === "semaforo") {

            html = `
            <div class="label">Uso de recursos</div>
            Secuencial: ${data.secuencial.max_uso} <br>
            Concurrente: ${data.concurrente.max_uso} <br><br>

            ${renderTiempo(data)}

            ${renderGanador(data)}

            ${renderLogs(data.concurrente.logs)}
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

            ${renderTiempo(data)}

            ${renderGanador(data)}

            ${renderLogs(data.concurrente.logs)}
            `;
        }

        // =============================
        // LECTORES-ESCRITORES
        // =============================
        else if (endpoint === "lectores") {

            html = `
            <div class="label">Accesos registrados</div>
            Total: ${data.concurrente.operaciones.length} <br><br>

            ${renderTiempo(data)}

            ${renderGanador(data)}

            ${renderLogs(data.concurrente.operaciones)}
            `;
        }

        // =============================
        // BARRERA
        // =============================
        else if (endpoint === "barrera") {

            html = `
            <div class="label">Eventos sincronizados</div>
            Total: ${data.concurrente.orden.length} <br><br>

            ${renderTiempo(data)}

            ${renderGanador(data)}

            ${renderLogs(data.concurrente.orden)}
            `;
        }

        box.innerHTML = html;

    })
    .catch(err => {
        box.innerHTML = "<span style='color:red;'>Error: " + err + "</span>";
    });
}


// =============================
// 🔹 BLOQUES REUTILIZABLES
// =============================

function renderTiempo(data) {
    return `
    <div class="label">Tiempo (segundos)</div>
    Secuencial: ${data.secuencial.tiempo}s <br>
    Concurrente: ${data.concurrente.tiempo}s <br><br>
    `;
}

function renderGanador(data) {
    const esConc = data.concurrente.tiempo < data.secuencial.tiempo;

    return `
    <div class="ganador ${esConc ? 'ok' : 'warn'}">
        ${esConc ? "Concurrente más rápido" : "Secuencial más rápido"}
    </div>
    `;
}
