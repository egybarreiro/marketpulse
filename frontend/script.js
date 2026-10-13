// ================= LANGUAGE SYSTEM =================

// Cargar idioma guardado al iniciar
document.addEventListener("DOMContentLoaded", () => {
    const savedLang = localStorage.getItem("marketpulse-lang") || "en";
    document.getElementById("language").value = savedLang;
    applyLanguage(savedLang);
});

// Fade helper
function fadeLanguageChange() {
    const elements = [
        document.querySelector("h1"),
        document.querySelector("#subtitle"),
        document.querySelector("#instructions"),
        document.querySelector("label[for='features']"),
        document.querySelector("label[for='horizon']"),
        document.querySelector("label[for='language']"),
        document.getElementById("predict-btn"),
        document.querySelector(".output-section h3"),
        document.querySelector(".signal-section h3"),
        document.querySelector(".powered-by"),
        document.querySelector(".footer-name"),
        document.querySelector(".footer-eabs"),
        document.querySelector("#disclaimer")
    ];

    elements.forEach(el => {
        el.classList.add("fade");
        setTimeout(() => el.classList.add("show"), 10);
        setTimeout(() => {
            el.classList.remove("fade");
            el.classList.remove("show");
        }, 500);
    });
}

function applyLanguage(lang) {
    const t = translations[lang];

    document.querySelector("h1").textContent = t.title;
    document.querySelector("#subtitle").textContent = t.subtitle;
    document.querySelector("#instructions").textContent = t.instructions;

    document.querySelector("label[for='features']").textContent = t.featuresLabel;
    document.querySelector("label[for='horizon']").textContent = t.horizonLabel;
    document.querySelector("label[for='language']").textContent = t.languageLabel;

    document.getElementById("predict-btn").textContent = t.predictButton;

    document.querySelector(".output-section h3").textContent = t.predictionTitle;
    document.querySelector(".signal-section h3").textContent = t.signalTitle;

    document.querySelector(".powered-by").textContent = `${t.poweredBy} `;
    document.querySelector(".footer-name").textContent = t.footerName;
    document.querySelector(".footer-eabs").textContent = t.footerEabs;

    document.querySelector("#disclaimer").textContent = t.disclaimer;

    fadeLanguageChange();
}

// Guardar idioma cuando el usuario lo cambia
document.getElementById("language").addEventListener("change", (e) => {
    const lang = e.target.value;
    localStorage.setItem("marketpulse-lang", lang);
    applyLanguage(lang);
});

// ================= BACKEND URL =================
const API_BASE = "https://marketpulse-ancient-songbird-5565.fly.dev";

// ================= TICKER BAR =================

async function loadTicker() {
    try {
        const url = `${API_BASE}/ticker/`;
        const response = await fetch(url);

        let data = null;

        if (response.ok) {
            data = await response.json();

            if (data && data.data && data.data.length > 0) {
                localStorage.setItem("marketpulse-ticker", JSON.stringify(data.data));
            }
        }

        if (!data || !data.data || data.data.length === 0) {
            const cached = localStorage.getItem("marketpulse-ticker");
            if (cached) {
                data = { data: JSON.parse(cached) };
            } else {
                console.warn("Sin datos y sin cache, manteniendo ticker actual");
                return;
            }
        }

        const tickerBox = document.getElementById("ticker-content");
        const fragment = document.createDocumentFragment();

        data.data.forEach(stock => {
            const price =
                stock.price ??
                stock.close ??
                stock.last ??
                stock.regularMarketPrice ??
                stock["05. price"] ??
                null;

            if (!price || price === 0) return;
            if (stock.symbol === "SQ") return;

            const span = document.createElement("span");
            span.className = "ticker-item";
            span.textContent = `${stock.symbol} $${price}`;
            fragment.appendChild(span);
        });

        if (!fragment.children.length) {
            console.warn("Fragmento vacío, manteniendo ticker actual");
            return;
        }

        const loopFragment = document.createDocumentFragment();
        loopFragment.appendChild(fragment.cloneNode(true));
        loopFragment.appendChild(fragment.cloneNode(true));

        tickerBox.innerHTML = "";
        tickerBox.appendChild(loopFragment);

        const tickerContainer = document.querySelector(".ticker-bar");
        if (tickerContainer) {
            tickerContainer.style.animationDuration = "180s";
        }

    } catch (error) {
        console.error("Error cargando ticker:", error);
    }
}

loadTicker();
setInterval(loadTicker, 10000);

// ================= BACKEND INTEGRATION =================

// --- Predicción simple ---
async function fetchPrediction(ticker) {
    const res = await fetch(`${API_BASE}/predict-regression/${ticker}`);
    return await res.json();
}

// --- Análisis completo ---
async function fetchAnalysis(ticker) {
    const res = await fetch(`${API_BASE}/analyze/${ticker}`);
    return await res.json();
}

// ================= NEW FEATURE: UPLOAD DATASET =================

async function uploadDataset() {
    const fileInput = document.getElementById("datasetInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Selecciona un archivo CSV");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch(`${API_BASE}/upload-dataset`, {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        document.getElementById("results").innerHTML =
            `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    } catch (error) {
        document.getElementById("results").innerHTML =
            `<pre>Error: ${error}</pre>`;
    }
}

// ================= NEW FEATURE: ANALYZE TICKER =================

async function analyzeTicker() {
    const ticker = document.getElementById("tickerInput").value.trim();

    if (!ticker) {
        alert("Escribe un ticker, ej: AAPL");
        return;
    }

    try {
        const data = await fetchAnalysis(ticker);

        // Mostrar JSON crudo
        document.getElementById("results").innerHTML =
            `<pre>${JSON.stringify(data, null, 2)}</pre>`;

        // Mostrar tarjetas avanzadas si el usuario quiere
        if (document.getElementById("show-cards").checked) {
            renderAdvancedCards(data);
        }

        // Mostrar gráficos si el usuario quiere
        if (document.getElementById("show-charts").checked) {
            renderCharts(data);
        }

    } catch (error) {
        document.getElementById("results").innerHTML =
            `<pre>Error: ${error}</pre>`;
    }
}

// ================= PREDICT BUTTON =================

document.getElementById("predict-btn").addEventListener("click", async () => {
    const ticker = document.getElementById("ticker-input").value.trim();

    if (!ticker) {
        alert("Escribe un ticker, ej: AAPL");
        return;
    }

    const result = await fetchPrediction(ticker);

    if (result.status !== "ok") {
        document.getElementById("prediction-box").innerText =
            `Error: ${result.message}`;
        return;
    }

    document.getElementById("prediction-box").innerText =
        `Predicción retorno 1D: ${result.prediction_return_1d.toFixed(4)}\nSeñal: ${result.signal}`;
});

// ================= ADVANCED CARDS =================

function renderAdvancedCards(data) {
    const container = document.getElementById("advanced-cards");
    container.innerHTML = `
        <div class="card">
            <h3>RSI (14)</h3>
            <p>${data.rsi_14?.toFixed(2)}</p>
        </div>
        <div class="card">
            <h3>MACD</h3>
            <p>${data.macd?.toFixed(4)}</p>
        </div>
        <div class="card">
            <h3>Signal MACD</h3>
            <p>${data.signal_macd?.toFixed(4)}</p>
        </div>
        <div class="card">
            <h3>Momentum (10)</h3>
            <p>${data.momentum_10?.toFixed(4)}</p>
        </div>
    `;
}

// ================= CHARTS =================

function renderCharts(data) {
    const ctx = document.getElementById("chartCanvas").getContext("2d");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: ["RSI", "MACD", "Signal", "Momentum"],
            datasets: [{
                label: "Indicadores Técnicos",
                data: [
                    data.rsi_14,
                    data.macd,
                    data.signal_macd,
                    data.momentum_10
                ],
                borderColor: "cyan",
                backgroundColor: "rgba(0,255,255,0.2)"
            }]
        }
    });
}

// ================= BUTTON EVENTS =================

document.getElementById("upload-btn").addEventListener("click", uploadDataset);
document.getElementById("ticker-btn").addEventListener("click", analyzeTicker);

function renderAdvancedCards(data) {
    const container = document.getElementById("advanced-cards");
    container.innerHTML = "";

    const indicators = [
        { name: "RSI (14)", value: data.rsi_14 },
        { name: "MACD", value: data.macd },
        { name: "Signal MACD", value: data.signal_macd },
        { name: "Momentum (10)", value: data.momentum_10 }
    ];

    indicators.forEach(ind => {
        const div = document.createElement("div");
        div.className = "card";

        let colorClass = "yellow";
        if (ind.value > 0) colorClass = "green";
        if (ind.value < 0) colorClass = "red";

        div.innerHTML = `
            <h3>${ind.name}</h3>
            <p class="${colorClass}">${ind.value.toFixed(4)}</p>
        `;

        container.appendChild(div);
    });
}

function renderSparkline(data) {
    const ctx = document.getElementById("sparkCanvas").getContext("2d");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: [...Array(4).keys()],
            datasets: [{
                data: [
                    data.rsi_14,
                    data.macd,
                    data.signal_macd,
                    data.momentum_10
                ],
                borderColor: "#00ffff",
                backgroundColor: "rgba(0,255,255,0.2)",
                tension: 0.4
            }]
        },
        options: {
            plugins: { legend: { display: false } },
            scales: { x: { display: false }, y: { display: false } }
        }
    });
}

function renderSidePanel(data) {
    const panel = document.getElementById("side-content");

    panel.innerHTML = `
        <div class="side-item"><strong>Precio:</strong> $${data.last_close.toFixed(2)}</div>
        <div class="side-item"><strong>Predicción 1D:</strong> ${data.prediction_return_1d.toFixed(4)}</div>
        <div class="side-item"><strong>Señal:</strong> ${data.signal}</div>
        <div class="side-item"><strong>RSI:</strong> ${data.rsi_14.toFixed(2)}</div>
        <div class="side-item"><strong>MACD:</strong> ${data.macd.toFixed(4)}</div>
        <div class="side-item"><strong>Momentum:</strong> ${data.momentum_10.toFixed(4)}</div>
    `;
}
