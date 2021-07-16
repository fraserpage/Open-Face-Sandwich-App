// Cached elem references
// ----------------------
let main = document.getElementById('image-cropper')
let imageInput = document.getElementById('croppieInput')
let imageInputLabel = document.getElementById('croppieInputLabel')
let statusElem = document.getElementById('status')
let croppieContainer = document.getElementById('croppie-container')
let croppieActionsElem = document.getElementById('croppie-actions')
let croppieGoBtn =  document.querySelector('.croppie-go')
let croplinesElem = document.getElementById('croplines')
let croppieRotateBtns = document.querySelectorAll('.croppie-rotate')
let croppieInst
let cropSize = {width: 500, height: 630}

// Event listeners
// ---------------
imageInput.addEventListener('change', setupCroppie)
croppieGoBtn.addEventListener('click', croppieGo);
croppieRotateBtns.forEach( el => el.addEventListener('click', rotateCroppie) )

// Functions
// ---------
function setupCroppie(event) {
    imageInputLabel.classList.add('hidden')
    // If Croppie already exists destroy it before re-initializing
    if (croppieInst instanceof Croppie) croppieInst.destroy()
    
    // Sizing variables
    let parentW = main.clientWidth
    let displayWidth = parentW < cropSize.width ? parentW : cropSize.width
    var displayHeight = parentW < cropSize.width ? Math.round(parentW * cropSize.height / cropSize.width) : cropSize.height;

    //Create Croppie Instance
    croppieInst = new Croppie(croppieContainer, {
        viewport: { width: displayWidth, height: displayHeight },
        boundary: { width: displayWidth, height: displayHeight },
        showZoomer: true,
        mouseWheelZoom: false,
        enableExif: true,
        enableOrientation: true
    });

    // Bind Croppie Instance to the selected image
    croppieInst.bind({
        url: URL.createObjectURL(event.target.files[0])
    }).then(()=>{
        // show croppie action buttons and croplines
        croppieActionsElem.classList.remove('hidden')
        croplinesElem.classList.remove('hidden')
    })
}

function rotateCroppie() {
    croppieInst.rotate(parseInt(this.dataset.deg));
}

function croppieGo(){
    disableBtnAndShowUploadingMsg()
    cropImageThen(submitForm)
}

function disableBtnAndShowUploadingMsg(){
    croppieGoBtn.disabled = true
    statusElem.classList.remove('hidden')
    statusElem.innerHTML = "Cropping... Chopping... Uploading..."
}

function cropImageThen(callback) {
    croppieInst.result({
        type: 'blob',
        size: {width: cropSize.width, height: cropSize.height}
    }).then(blob => callback(blob))
}

function submitForm(blob) {    
    let form = document.getElementById('upload-form')
    let formData = new FormData(form)
    formData.append('image',blob)

    fetch(form.action, {
        method: 'post',
        body: formData,
    })
    .then((response) => response.json())
    .then((json) => window.location.pathname = json.url)
    .catch((error) => console.log(error));
}

// ---- To do: handle resize window
// window.addEventListener('resize',scaleCroppie)
// on resize display a button to reload croppie if (main.clientWidth < croppie.clientWidth)
