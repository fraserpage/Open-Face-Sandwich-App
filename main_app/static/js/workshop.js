//Elem references
//--------------

// Cubes
let cubeElems = {
  top: document.getElementById("c1"),
  middle: document.getElementById("c2"),
  bottom: document.getElementById("c3"),
}

// Form
let formEl = document.getElementById('form')

// Arrows
let topForwardArrowEl = document.getElementById("top-forward-arrow");
let topBackwardArrowEl = document.getElementById("top-backward-arrow");

let middleForwardArrowEl = document.getElementById("middle-forward-arrow");
let middleBackwardArrowEl = document.getElementById("middle-backward-arrow");

let bottomForwardArrowEl = document.getElementById("bottom-forward-arrow");
let bottomBackwardArrowEl = document.getElementById("bottom-backward-arrow");

// Event listeners
// ---------------
topForwardArrowEl.addEventListener("click", () => rotateBlockForward('top'));
topBackwardArrowEl.addEventListener("click", () => rotateBlockBack('top'));

middleForwardArrowEl.addEventListener("click", () => rotateBlockForward('middle'));
middleBackwardArrowEl.addEventListener("click", () => rotateBlockBack('middle'));

bottomForwardArrowEl.addEventListener("click", () => rotateBlockForward('bottom'));
bottomBackwardArrowEl.addEventListener("click", () => rotateBlockBack('bottom'));

// Variables
// --------
let nextPhoto = {}
let prevPhotos = {
  top:[],
  middle:[],
  bottom:[]
}

// Track the current front of each cube
let cubeFront = {
  top:0,
  middle:0,
  bottom:0
}

// Track the rotation of each cube
let cubeRotation = {
  top:-9,
  middle:-9,
  bottom:-9
}

// Functions
// ---------
init()

function init(){
  // currentSandwich.top == 'undefined' means that we are on the New page (not update or from_photo) and so will have to populate the current photos
  if (typeof currentSandwich.top == 'undefined'){
    setCurrentRandomPhoto('top')
    setCurrentRandomPhoto('middle')
    setCurrentRandomPhoto('bottom')
  }
  else{
    // call update path to setup the submit button
    updatePath()
  }

  // set the next photos
  setNextRandomPhoto('top')
  setNextRandomPhoto('middle')
  setNextRandomPhoto('bottom')
}

function randomPhoto(pos){
  let keys = Object.keys(photos);
  let key = keys[ keys.length * Math.random() << 0]
  photo = {
    id: key,
    img: photos[key][pos]
  }
  return photo
}

function setCurrentRandomPhoto(pos){
  let photo = randomPhoto(pos)
  cubeElems[pos].children[cubeFront[pos]].innerHTML = `<img src="${photo.img}" alt="">`
  currentSandwich[pos] = photo.id
  updatePath()
}

function setNextRandomPhoto(pos){
  let photo = randomPhoto(pos)
  let next = nextFace(pos)
  cubeElems[pos].children[next].innerHTML = `<img src="${photo.img}" alt="">`
  nextPhoto[pos] = photo.id
}

function rotateBlockForward(pos){
  cubeFront[pos] = nextFace(pos)
  cubeRotation[pos] -= 90 //- (360*2)
  cubeElems[pos].style.transform = `rotateY(${cubeRotation[pos]}deg)`
  prevPhotos[pos].unshift(currentSandwich[pos])
  currentSandwich[pos] = nextPhoto[pos]
  updatePath()
  setNextRandomPhoto(pos)
}

function rotateBlockBack(pos){
  cubeFront[pos] = prevFace(pos)
  cubeRotation[pos] += 90 
  cubeElems[pos].style.transform = `rotateY(${cubeRotation[pos]}deg)`
  nextPhoto[pos] = currentSandwich[pos] 
  currentSandwich[pos] = prevPhotos[pos].shift()
  if (typeof currentSandwich[pos] == 'undefined') setCurrentRandomPhoto(pos)
  updatePath()
}

function nextFace(pos){
  let next = cubeFront[pos] === 3 ? 0 : cubeFront[pos] + 1
  return next
}

function prevFace(pos){
  let prev = cubeFront[pos] === 0 ? 3 : cubeFront[pos] - 1
  return prev
}

function updatePath() {
  if (typeof editSandwich !== 'undefined') {
    formEl.action = `/sandwiches/${editSandwich.id}/${currentSandwich.top}/${currentSandwich.middle}/${currentSandwich.bottom}/update/`;
  } 
  else {
    formEl.action = `/sandwiches/${currentSandwich.top}/${currentSandwich.middle}/${currentSandwich.bottom}/create/`;
  }
}
