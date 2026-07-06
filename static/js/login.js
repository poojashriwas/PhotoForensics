/* ==========================================
   PHOTO FORENSICS LOGIN
   login.js
========================================== */

/* ==========================
   PARTICLES
========================== */

particlesJS("particles-js", {

    particles: {

        number: {
            value: 90,
            density: {
                enable: true,
                value_area: 900
            }
        },

        color: {
            value: "#3b82f6"
        },

        shape: {
            type: "circle"
        },

        opacity: {
            value: 0.35,
            random: true
        },

        size: {
            value: 3,
            random: true
        },

        line_linked: {
            enable: true,
            distance: 160,
            color: "#3b82f6",
            opacity: 0.25,
            width: 1
        },

        move: {
            enable: true,
            speed: 2,
            direction: "none",
            random: false,
            straight: false,
            out_mode: "out",
            bounce: false
        }

    },

    interactivity: {

        detect_on: "canvas",

        events: {

            onhover: {
                enable: true,
                mode: "grab"
            },

            onclick: {
                enable: true,
                mode: "push"
            },

            resize: true

        },

        modes: {

            grab: {
                distance: 180,
                line_linked: {
                    opacity: 0.8
                }
            },

            push: {
                particles_nb: 4
            }

        }

    },

    retina_detect: true

});


/* ==========================
   INPUT ANIMATION
========================== */

const inputs = document.querySelectorAll(".form-control");

inputs.forEach(input => {

    input.addEventListener("focus", function () {

        this.parentElement.classList.add("active");

    });

    input.addEventListener("blur", function () {

        if (this.value === "") {

            this.parentElement.classList.remove("active");

        }

    });

});


/* ==========================
   BUTTON LOADING
========================== */

const form = document.querySelector("form");

const button = document.querySelector(".login-btn");

form.addEventListener("submit", function () {

    button.disabled = true;

    button.innerHTML = `

    <span class="spinner-border spinner-border-sm me-2"></span>

    Signing In...

    `;

});


/* ==========================
   FLOATING CARDS
========================== */

const cards = document.querySelectorAll(".feature-card");

cards.forEach((card, index) => {

    card.style.animation = `floatCard 5s ease-in-out ${index * 0.2}s infinite`;

});


/* ==========================
   TYPEWRITER EFFECT
========================== */

const subtitle = document.querySelector(".subtitle");

const text = "Login to continue your investigations";

let i = 0;

subtitle.innerHTML = "";

function typing() {

    if (i < text.length) {

        subtitle.innerHTML += text.charAt(i);

        i++;

        setTimeout(typing, 35);

    }

}

typing();


/* ==========================
   LOGIN CARD TILT
========================== */

const loginCard = document.querySelector(".login-card");

document.addEventListener("mousemove", (e) => {

    const x = (window.innerWidth / 2 - e.pageX) / 45;

    const y = (window.innerHeight / 2 - e.pageY) / 45;

    loginCard.style.transform =
        `rotateY(${x}deg) rotateX(${-y}deg)`;

});


document.addEventListener("mouseleave", () => {

    loginCard.style.transform =
        "rotateX(0deg) rotateY(0deg)";

});


/* ==========================
   GLOW EFFECT
========================== */

setInterval(() => {

    loginCard.classList.toggle("glow");

}, 2500);