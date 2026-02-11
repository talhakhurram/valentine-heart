import os
import math
from http.server import HTTPServer, SimpleHTTPRequestHandler


def create_html():
    photo_dir = "photos"

    if not os.path.exists(photo_dir):
        print("❌ 'photos' folder not found.")
        return

    photos = [
        f for f in os.listdir(photo_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    if not photos:
        print("❌ No photos found.")
        return

    heart_positions = []
    for t in range(0, 360, 14):
        theta = math.radians(t)
        x = 16 * math.sin(theta) ** 3
        y = (
            13 * math.cos(theta)
            - 5 * math.cos(2 * theta)
            - 2 * math.cos(3 * theta)
            - math.cos(4 * theta)
        )
        heart_positions.append((x, -y))

    photo_divs = ""
    for i, (x, y) in enumerate(heart_positions):
        photo = photos[i % len(photos)]
        photo_divs += f"""
        <div class="photo"
             style="left: calc(50% + {x} * var(--scale));
                    top: calc(50% + {y} * var(--scale));">
            <img src="photos/{photo}">
        </div>
        """

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>For Someone Special 💖</title>

<style>
:root { --scale: 3.8vmin; }

body {
    margin:0;
    height:100vh;
    background: linear-gradient(135deg,#fff0f5,#ffd6e8);
    font-family:Arial, sans-serif;
    overflow:hidden;
}

.center {
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    text-align:center;
    width:90%;
}

.hidden { display:none; }

button {
    padding:2vmin 5vmin;
    border:none;
    border-radius:6vmin;
    background:linear-gradient(45deg,#ff4da6,#ff1a75);
    color:white;
    font-size:3.5vmin;
    margin:1.5vmin;
}

.wrapper {
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    width:90vmin;
    height:90vmin;
}

.photo {
    position:absolute;
    transform: translate(-50%, -50%);
}

.photo img {
    width:10vmin;
    height:10vmin;
    object-fit:cover;
    border-radius:1.5vmin;
    box-shadow:0 0 3vmin rgba(255,20,147,0.6);
}

.move-up {
    animation: floatUp 9s forwards;
}

@keyframes floatUp {
    100% {
        transform: translate(-50%, -150vh);
        opacity:0;
    }
}

.final-message {
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    font-size:5vmin;
    color:#e91e63;
    font-weight:bold;
    opacity:0;
    text-shadow:0 0 20px hotpink;
    transition:opacity 3s;
}

.show-message { opacity:1; }

.typewriter {
    font-size:4vmin;
    color:#e91e63;
    white-space:nowrap;
    overflow:hidden;
    border-right:.15em solid pink;
}

input[type=range] {
    -webkit-appearance:none;
    width:70vmin;
    height:2vmin;
    border-radius:2vmin;
    background:linear-gradient(90deg,#ff4da6,#ff85c2);
}

input[type=range]::-webkit-slider-thumb {
    -webkit-appearance:none;
    width:6vmin;
    height:6vmin;
    border-radius:50%;
    background:white;
}
</style>
</head>

<body>

<audio id="bgMusic" loop>
    <source src="Edd_Sheeran_-_Perfect_(mp3.pm).mp3" type="audio/mp3">
</audio>


<div class="center" id="intro">
    <div class="typewriter" id="typeText"></div><br><br>
    <button onclick="goProposal()">Continue 💖</button>
</div>

<div class="center hidden" id="proposal">
    <h2>Will You Be Mine? 💍</h2>
    <p>You can press <b>NO</b>… if you want 😏</p>
    <button onclick="startSlider()">YES 💖</button>
    <button id="noBtn">NO 😈</button>
</div>

<div class="center hidden" id="sliderScreen">
    <h2>Unlock My Heart 💖</h2>
    <p>Slide until the heart is full</p>
    <input type="range" min="0" max="100" value="0" id="loveSlider">
    <div id="heartFill" style="font-size:6vmin;margin-top:2vmin;">🤍</div>
</div>

<div class="wrapper hidden" id="mainContent">
    __PHOTOS__
    <div class="final-message" id="finalMsg">
        From the moment you came into my life, everything felt more certain, more beautiful, more real. Just like “Perfect”. Forever Starts With You. I miss you. Happy Valentines! ❤️
    </div>
</div>

<script>
let text="Happy Valentine’s, Hamna Baby. I love you. More than words, more than reasons, more every single day. ❤️";
let i=0;

function typeWriter(){
    if(i<text.length){
        document.getElementById("typeText").innerHTML+=text.charAt(i);
        i++;
        setTimeout(typeWriter,60);
    }
}
typeWriter();

function goProposal(){
    intro.classList.add("hidden");
    proposal.classList.remove("hidden");
}

const noBtn=document.getElementById("noBtn");
noBtn.addEventListener("click",()=>{
    noBtn.innerHTML="YES 💖";
    noBtn.onclick=startSlider;
});

function startSlider(){
    proposal.classList.add("hidden");
    sliderScreen.classList.remove("hidden");
}

const slider=document.getElementById("loveSlider");
const heart=document.getElementById("heartFill");

slider.addEventListener("input",()=>{
    if(slider.value<30) heart.innerHTML="🤍";
    else if(slider.value<60) heart.innerHTML="💗";
    else if(slider.value<90) heart.innerHTML="💖";
    else{
        heart.innerHTML="❤️";
        sliderScreen.classList.add("hidden");
        startAnimation();
    }
});

function startAnimation(){
    bgMusic.play();
    mainContent.classList.remove("hidden");
    document.querySelectorAll(".photo").forEach((p,i)=>{
        setTimeout(()=>p.classList.add("move-up"),i*150);
    });
    setTimeout(()=>finalMsg.classList.add("show-message"),4000);
}
</script>

</body>
</html>
"""

    html = html.replace("__PHOTOS__", photo_divs)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("💖 Fixed! HTML generated successfully.")


def start_server(port=8000):
    print(f"🚀 Open on laptop: http://localhost:{port}")
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    create_html()
    start_server()
