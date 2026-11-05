console.log("JavaScript conectado!");

const barcodeForm = document.getElementById("barcode-form");
const barcodeInput = document.getElementById("barcode-input");
const startCameraButton = document.getElementById("start-camera");
const stopCameraButton = document.getElementById("stop-camera");
const cameraContainer = document.getElementById("camera-container");
const cameraStatus = document.getElementById("camera-status");
const productSearch = document.getElementById("busca-produtos");
const productRows = document.querySelectorAll("[data-produto]");
const noProductsFound = document.getElementById("nenhum-produto-encontrado");
const themeToggle = document.getElementById("theme-toggle");
const themeLabel = themeToggle.querySelector(".theme-label");
const themeStorageKey = "iel-proj-theme";

let savedTheme = null;
try {
    savedTheme = localStorage.getItem(themeStorageKey);
} catch (error) {
    console.error("Não foi possível carregar a preferência de tema:", error);
}
document.documentElement.dataset.theme = savedTheme === "light" ? "light" : "dark";

function updateThemeToggle(theme) {
    const isLight = theme === "light";
    const nextThemeLabel = isLight ? "Tema escuro" : "Tema claro";
    themeLabel.textContent = nextThemeLabel;
    themeToggle.title = `Alternar para ${nextThemeLabel.toLowerCase()}`;
    themeToggle.setAttribute("aria-label", themeToggle.title);
}

updateThemeToggle(document.documentElement.dataset.theme);

function setTheme(theme) {
    const isLight = theme === "light";
    document.documentElement.dataset.theme = isLight ? "light" : "dark";
    updateThemeToggle(theme);
    try {
        localStorage.setItem(themeStorageKey, isLight ? "light" : "dark");
    } catch (error) {
        console.error("Não foi possível salvar a preferência de tema:", error);
    }
}

let scanner = null;
let cameraRunning = false;
let scanHandled = false;

function showCameraStatus(message) {
    cameraStatus.textContent = message;
}

async function stopCamera() {
    if (!scanner) {
        return;
    }

    if (cameraRunning) {
        await scanner.stop();
        cameraRunning = false;
    }

    scanner.clear();
    scanner = null;
    cameraContainer.hidden = true;
    startCameraButton.hidden = false;
    stopCameraButton.hidden = true;
}

async function startCamera() {
    if (!window.isSecureContext || !navigator.mediaDevices?.getUserMedia) {
        showCameraStatus(
            "A câmera exige que o sistema seja aberto por uma conexão HTTPS segura."
        );
        return;
    }

    if (!window.Html5Qrcode) {
        showCameraStatus(
            "Não foi possível carregar o leitor da câmera. Verifique sua conexão com a internet."
        );
        return;
    }

    startCameraButton.disabled = true;
    showCameraStatus("Solicitando acesso à câmera...");
    cameraContainer.hidden = false;
    if (document.activeElement instanceof HTMLElement) {
        document.activeElement.blur();
    }

    scanner = new Html5Qrcode("barcode-reader");
    try {
        await scanner.start(
            { facingMode: "environment" },
            { fps: 10, qrbox: { width: 280, height: 120 } },
            async (codigo) => {
                if (scanHandled) {
                    return;
                }

                scanHandled = true;
                barcodeInput.value = codigo;
                showCameraStatus("Código lido. Processando...");
                try {
                    await stopCamera();
                } catch (error) {
                    showCameraStatus(
                        `Código lido, mas não foi possível fechar a câmera: ${error.message}`
                    );
                }
                barcodeForm.requestSubmit();
            },
            () => {}
        );
        cameraRunning = true;
        scanHandled = false;
        startCameraButton.hidden = true;
        stopCameraButton.hidden = false;
        showCameraStatus("Aponte a câmera para o código de barras.");
    } catch (error) {
        cameraContainer.hidden = true;
        scanner.clear();
        scanner = null;
        showCameraStatus(`Não foi possível iniciar a câmera: ${error.message}`);
    } finally {
        startCameraButton.disabled = false;
    }
}

startCameraButton.addEventListener("click", startCamera);
stopCameraButton.addEventListener("click", async () => {
    try {
        await stopCamera();
        showCameraStatus("Câmera fechada.");
    } catch (error) {
        showCameraStatus(`Não foi possível fechar a câmera: ${error.message}`);
    }
});

function normalizeSearchText(text) {
    return text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}

productSearch.addEventListener("input", () => {
    const searchTerm = normalizeSearchText(productSearch.value.trim());
    let visibleProducts = 0;

    productRows.forEach((row) => {
        const productName = normalizeSearchText(row.cells[1].textContent || "");
        const matches = productName.includes(searchTerm);
        row.hidden = !matches;
        if (matches) {
            visibleProducts += 1;
        }
    });

    noProductsFound.hidden = !searchTerm || visibleProducts > 0;
});

    themeToggle.addEventListener("click", () => {
        const nextTheme = document.documentElement.dataset.theme === "light"
            ? "dark"
            : "light";
        setTheme(nextTheme);
    });

    window.alert = function (message) {
    const alertBox = document.createElement("jan");
    alertBox.className = "custom-alert";
    alertBox.textContent = message;}