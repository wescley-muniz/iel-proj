console.log("JavaScript conectado!");

const barcodeForm = document.getElementById("barcode-form");
const barcodeInput = document.getElementById("barcode-input");
const startCameraButton = document.getElementById("start-camera");
const stopCameraButton = document.getElementById("stop-camera");
const cameraContainer = document.getElementById("camera-container");
const cameraStatus = document.getElementById("camera-status");

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