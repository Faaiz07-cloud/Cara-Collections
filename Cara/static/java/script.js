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

const products = document.querySelectorAll(".prod");
if (products.length > 0) {  // check NodeList is not empty
  products.forEach(product => {
    product.addEventListener('click', () => {
      const url = product.getAttribute("data-url");
      if (url) {  // extra safety check
        window.location.href = url;
      }
    });
  });
}

var main_image = document.getElementById("mainImage");
var small_images = document.getElementsByClassName("thumb");

for (let i = 0; i < small_images.length; i++) {
  small_images[i].onclick = function () {
    
    // Change main image
    main_image.src = this.src;

    // Remove active class from all
    for (let j = 0; j < small_images.length; j++) {
      small_images[j].classList.remove("active");
    }

    // Add active to clicked one
    this.classList.add("active");
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

// Auto play when in viewport
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
// ---------------------------------------