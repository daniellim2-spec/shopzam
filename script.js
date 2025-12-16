function startScan() {
    const fileInput = document.getElementById("photoInput");
    const loading = document.getElementById("loading");
    const resultCard = document.getElementById("resultCard");
    const errorBox = document.getElementById("errorBox");
    const previewImage = document.getElementById("previewImage");

    loading.style.display = "none";
    resultCard.style.display = "none";
    errorBox.style.display = "none";

    //if user doesnt upload a photo
    if (!fileInput.files || fileInput.files.length === 0) {
        errorBox.style.display = "block";
        errorBox.innerText = "Please upload a photo before scanning.";
        return;
    }

    loading.style.display = "block";

    const selectedImage = URL.createObjectURL(fileInput.files[0]);
    previewImage.src = selectedImage;
    
    setTimeout(() => {
        loading.style.display = "none";

        resultCard.style.display = "block";
        document.getElementById("productName").textContent = "Blue Lizard 50 Sensitive";
        document.getElementById("productPrice").textContent = "$10.50";

    }, 2000);
}

function resetScan() {
    const preview = document.getElementById("previewImage");
    const resultCard = document.getElementById("resultCard");
    const errorBox = document.getElementById("errorBox");
    const photoInput = document.getElementById("photoInput");
    const loading = document.getElementById("loading");

    preview.src = "";
    preview.style.display = "none";
    resultCard.style.display = "none";
    errorBox.style.display = "none";
    photoInput.value = "";
    loading.style.display = "none";
}