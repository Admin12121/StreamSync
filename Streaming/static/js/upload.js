 const dropArea = document.getElementById("drop-area");
 const inputFile = document.getElementById("input-file");
 const imageView = document.getElementById("img-view");

 inputFile.addEventListener( "change", uploadImage) 

 function uploadImage() {
   let imgLink =URL.createObjectURL(inputFile.files[0]);
   imageView.style.backgroundImage=`url(${imgLink})`;  
   imageView.textContent = "";
 }

 dropArea.addEventListener("dragover", function(e){
   e.preventDefault();
 });
 dropArea.addEventListener("drop", function(e){
   e.preventDefault();
   inputFile.files = e.dataTransfer.files;
   uploadImage();
 })

const videodropArea = document.getElementById("video-drop-area");
const videoinputFile = document.getElementById("video-input-file");
const videoView = document.getElementById("video-view");

videoinputFile.addEventListener("change", uploadVideo);

function uploadVideo() {
    let videoLink = URL.createObjectURL(videoinputFile.files[0]);
    const video = document.createElement("video");
    video.src = videoLink;
    video.autoplay = true; // Autoplay the video
    video.loop = true; // Loop the video
    video.muted = true; // Mute the video for autoplay in some browsers
    video.setAttribute("playsinline", ""); // Enable inline playback for mobile
    videoView.textContent = "";
    videoView.appendChild(video);
}

videodropArea.addEventListener("dragover", function (e) {
    e.preventDefault();
});

videodropArea.addEventListener("drop", function (e) {
    e.preventDefault();
    videoinputFile.files = e.dataTransfer.files;
    uploadVideo();
});