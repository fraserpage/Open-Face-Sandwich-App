let topn = document.getElementById('top-list').innerHTML.split(','); 
let middle = document.getElementById('middle-list').innerHTML.split(','); 
let bottom = document.getElementById('bottom-list').innerHTML.split(','); 

// tops = top_string.split(',')
// for element in tops:
//     top = element.split("_")[0]
//     print("top in sandwich new", top)

let topArray=[];
let middleArray=[];
let bottomArray=[];


for (let element of topn) {
    topArray.push([element.split("_")[0],element.split("_")[1]])
}

for (let element of middle) {
    middleArray.push([element.split("_")[0],element.split("_")[1]])
}

for (let element of bottom) {
    bottomArray.push([element.split("_")[0],element.split("_")[1]])
}

let top_id = topArray[0][1];
let middle_id = middleArray[0][1];
let bottom_id = bottomArray[0][1];


let topPosition = topArray.length
let middlePosition = topArray.length
let bottomPosition = topArray.length

let topForwardArrowEl = document.getElementById("top-forward-arrow");
let topBackwardArrowEl = document.getElementById("top-backward-arrow");
let topCurrentEl = document.getElementById("top-array-output")
topCurrentEl.src = topArray[0][0]

let middleForwardArrowEl = document.getElementById("middle-forward-arrow");
let middleBackwardArrowEl = document.getElementById("middle-backward-arrow");
let middleCurrentEl = document.getElementById("middle-array-output")
middleCurrentEl.src = middleArray[0][0]

let bottomForwardArrowEl = document.getElementById("bottom-forward-arrow");
let bottomBackwardArrowEl = document.getElementById("bottom-backward-arrow");
let bottomCurrentEl = document.getElementById("bottom-array-output")
bottomCurrentEl.src = bottomArray[0][0]

let formEl = document.getElementById('form')
console.log("formEl is", formEl)

topForwardArrowEl.addEventListener("click", () => {topNextRandomSlice(); updatePath()});
topBackwardArrowEl.addEventListener("click", () => {topPreviousSlice(); updatePath()});

middleForwardArrowEl.addEventListener("click", () => {middleNextRandomSlice(); updatePath()});
middleBackwardArrowEl.addEventListener("click", () => {middlePreviousSlice(); updatePath()});

bottomForwardArrowEl.addEventListener("click", () => {bottomNextRandomSlice(); updatePath()});
bottomBackwardArrowEl.addEventListener("click", () => {bottomPreviousSlice(); updatePath()});

function updatePath() {
    formEl.action = `/sandwiches/${top_id}/${middle_id}/${bottom_id}/create/`
    console.log(`/sandwiches/${top_id}/${middle_id}/${bottom_id}/create/`);
}


function topNextRandomSlice() {
  if (topPosition >= topArray.length-1) { 
    topPosition = 0;
  } else {
    topPosition = topPosition + 1;
  }
  topCurrentEl.src = topArray[topPosition][0]
  top_id = topArray[topPosition][1]
}

function topPreviousSlice() {
  let topCurrentEl = document.getElementById("top-array-output")
  if (topPosition <= 0) { 
    topPosition = topArray.length-1;
  } else {
    topPosition = topPosition - 1;
  }
  topCurrentEl.src = topArray[topPosition][0]
  top_id = topArray[topPosition][1]
}

function bottomNextRandomSlice() {
  if (bottomPosition >= bottomArray.length-1) { 
    bottomPosition = 0;
  } else {
    bottomPosition = bottomPosition + 1;
  }
  bottomCurrentEl.src = bottomArray[bottomPosition][0]
  bottom_id = bottomArray[bottomPosition][1]
}

function bottomPreviousSlice() {
  let bottomCurrentEl = document.getElementById("bottom-array-output")
  if (bottomPosition <= 0) { 
    bottomPosition = bottomArray.length-1;
  } else {
    bottomPosition = bottomPosition - 1;
  }
  bottomCurrentEl.src = bottomArray[bottomPosition][0]
  bottom_id = bottomArray[bottomPosition][1]
}

function middleNextRandomSlice() {
  if (middlePosition >= middleArray.length-1) { 
    middlePosition = 0;
  } else {
    middlePosition = middlePosition + 1;
  }
  middleCurrentEl.src = middleArray[middlePosition][0]
  middle_id = middleArray[middlePosition][1]
}

function middlePreviousSlice() {
  let middleCurrentEl = document.getElementById("middle-array-output")
  if (middlePosition <= 0) { 
    middlePosition = middleArray.length-1;
  } else {
    middlePosition = middlePosition - 1;
  }
  middleCurrentEl.src = middleArray[middlePosition][0]
  middle_id = middleArray[middlePosition][1]
}

