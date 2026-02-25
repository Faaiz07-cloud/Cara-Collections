const bar = document.getElementById("bar");
const close_bar = document.getElementById("close");
const navbar = document.getElementById("navbar");

if (bar) {
  bar.addEventListener("click", () => {
    navbar.classList.add("active");
  });
}

if (close_bar) {
  close_bar.addEventListener("click", () => {
    navbar.classList.remove("active");
  });
}

const btn_1001 = document.getElementById("1001");
if (btn_1001) {
  btn_1001.addEventListener("click", () => {
    const url = btn_1001.getAttribute("data-url");
    window.location.href = url;
  });
}

const product_card = document.querySelectorAll(".prod");

if (product_card) {
  product_card.forEach((card) => {
    card.addEventListener("click", () => {
      const url = card.getAttribute("data-url");
      window.location.href = url;
    });
  });
}

var main_image = document.getElementById("main");
var small_image = document.getElementsByClassName("s_img");

/*
small_image[0].onclick = function(){
    let temp = main_image.src;
    main_image.src = small_image[0].src;
    small_image[0].src = temp;
}

small_image[1].onclick = function(){
    let temp = main_image.src;
    main_image.src = small_image[1].src;
    small_image[1].src = temp;
}

small_image[2].onclick = function(){
    let temp = main_image.src;
    main_image.src = small_image[2].src;
    small_image[2].src = temp;
}

small_image[3].onclick = function(){
    let temp = main_image.src;
    main_image.src = small_image[3].src;
    small_image[3].src = temp;
}
*/

//using loop

for (let i = 0; i < small_image.length; i++) {
  small_image[i].onclick = function () {
    let temp = main_image.src;
    main_image.src = small_image[i].src;
    small_image[i].src = temp;
  };
}

// video in about page
const video = document.querySelector("#about-video video");

// Click to play/pause
video.addEventListener("click", () => {
  if(video.paused){
    video.play();
  }else{
    video.pause();
  }
});

// Auto play when in viewport (UX feature)
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if(entry.isIntersecting){
      video.play();
    }else{
      video.pause();
    }
  });
}, { threshold: 0.6 });

observer.observe(video);