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

// ================= TICKER =================

async function loadTicker() {
    try {
        const url = "http://127.0.0.1:8000/ticker/";
        const response = await fetch(url);

        let data = null;

        if (response.ok) {
            data = await response.json();

            // Guardar última data buena
            if (data && data.data && data.data.length > 0) {
                localStorage.setItem("marketpulse-ticker", JSON.stringify(data.data));
            }
        }

        // Usar fallback si no hay data nueva
        if (!data || !data.data || data.data.length === 0) {
            const cached = localStorage.getItem("marketpulse-ticker");
            if (cached) {
                data = { data: JSON.parse(cached) };
            } else {
                console.warn("Sin datos y sin cache, manteniendo ticker actual");
                return; // 🔥 NO limpiar el ticker
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

        // 🔥 SI EL FRAGMENTO ESTÁ VACÍO → NO LIMPIAR EL TICKER
        if (!fragment.children.length) {
            console.warn("Fragmento vacío, manteniendo ticker actual");
            return;
        }

        // Construir loop infinito
        const loopFragment = document.createDocumentFragment();
        loopFragment.appendChild(fragment.cloneNode(true));
        loopFragment.appendChild(fragment.cloneNode(true));

        // 🔥 SOLO AHORA limpiamos y reemplazamos
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