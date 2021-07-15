let topn = document.getElementById('top-list').innerHTML.split(','); 
let middle = document.getElementById('middle-list').innerHTML.split(','); 
let bottom = document.getElementById('bottom-list').innerHTML.split(','); 

let topId = document.getElementById("top-id").innerHTML;
let middleId = document.getElementById("middle-id").innerHTML;
let bottomId = document.getElementById("bottom-id").innerHTML;

let sandwich_id = document.getElementById("sandwich-id").innerHTML;
let top_id, middle_id, bottom_id;

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

let topForwardArrowEl = document.getElementById("top-forward-arrow");
let topBackwardArrowEl = document.getElementById("top-backward-arrow");
let topCurrentEl = document.getElementById("top-array-output")

let middleForwardArrowEl = document.getElementById("middle-forward-arrow");
let middleBackwardArrowEl = document.getElementById("middle-backward-arrow");
let middleCurrentEl = document.getElementById("middle-array-output")

let bottomForwardArrowEl = document.getElementById("bottom-forward-arrow");
let bottomBackwardArrowEl = document.getElementById("bottom-backward-arrow");
let bottomCurrentEl = document.getElementById("bottom-array-output")

// Customize this block if you're passing in ids already or not
if (topId && middleId && bottomId) {
  top_id = topId;
  middle_id = middleId;
  bottom_id = bottomId;
  for (let element of topArray) {
    if (element[1] == topId){
      topCurrentEl.src = element[0];
    }
  }
  for (let element of middleArray) {
    if (element[1] == middleId){
      middleCurrentEl.src = element[0];
    }
  }
  for (let element of bottomArray) {
    if (element[1] == bottomId){
      bottomCurrentEl.src = element[0];
    }
  }
} else {
  topCurrentEl.src = topArray[0][0]
  middleCurrentEl.src = middleArray[0][0]
  bottomCurrentEl.src = bottomArray[0][0]
  top_id = topArray[0][1];
  middle_id = middleArray[0][1];
  bottom_id = bottomArray[0][1];
}

let topPosition = topArray.length
let middlePosition = topArray.length
let bottomPosition = topArray.length

let formEl = document.getElementById('form')
if (sandwich_id) {
  formEl.action = `/sandwiches/${sandwich_id}/${top_id}/${middle_id}/${bottom_id}/update/`
} else {
  formEl.action = `/sandwiches/${top_id}/${middle_id}/${bottom_id}/create/`
}

topForwardArrowEl.addEventListener("click", () => {topNextRandomSlice(); updatePath()});
topBackwardArrowEl.addEventListener("click", () => {topPreviousSlice(); updatePath()});

middleForwardArrowEl.addEventListener("click", () => {middleNextRandomSlice(); updatePath()});
middleBackwardArrowEl.addEventListener("click", () => {middlePreviousSlice(); updatePath()});

bottomForwardArrowEl.addEventListener("click", () => {bottomNextRandomSlice(); updatePath()});
bottomBackwardArrowEl.addEventListener("click", () => {bottomPreviousSlice(); updatePath()});

function updatePath() {
  if (sandwich_id) {
    formEl.action = `/sandwiches/${sandwich_id}/${top_id}/${middle_id}/${bottom_id}/update/`;
  } else {
    formEl.action = `/sandwiches/${top_id}/${middle_id}/${bottom_id}/create/`;
  }
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

