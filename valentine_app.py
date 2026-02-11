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

    # Generate heart coordinates (normalized)
    heart_positions = []
    for t in range(0, 360, 12):
        theta = math.radians(t)
        r = 10 * (1 - math.sin(theta))
        x = r * math.cos(theta)
        y = -r * math.sin(theta)
        heart_positions.append((x, y))

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

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Responsive Heart</title>

<style>
:root {{
    --scale: min(4vw, 4vh);   /* Automatically fits screen */
}}

body {{
    margin:0;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background: linear-gradient(135deg,#fff0f5,#ffd6e8);
    font-family:Arial, sans-serif;
    overflow:hidden;
}}

.wrapper {{
    position:relative;
    width:90vmin;
    height:90vmin;
}}

.photo {{
    position:absolute;
    transform: translate(-50%, -50%);
    will-change: transform, opacity;
}}

.photo img {{
    width:8vmin;
    height:8vmin;
    object-fit:cover;
    border-radius:1.2vmin;
    box-shadow:0 0 1.5vmin rgba(255,105,180,0.5);
    animation: pulse 4s infinite ease-in-out;
    transition: transform 0.4s ease;
}}

.photo img:hover {{
    transform: scale(1.1);
}}

@keyframes pulse {{
    0% {{ box-shadow:0 0 1vmin rgba(255,105,180,0.4); }}
    50% {{ box-shadow:0 0 3vmin rgba(255,20,147,1); }}
    100% {{ box-shadow:0 0 1vmin rgba(255,105,180,0.4); }}
}}

button {{
    position:absolute;
    bottom:-8vmin;
    left:50%;
    transform:translateX(-50%);
    padding:1vmin 3vmin;
    border:none;
    border-radius:4vmin;
    background:linear-gradient(45deg,#ff4da6,#ff1a75);
    color:white;
    font-size:2vmin;
    cursor:pointer;
    transition:0.3s;
}}

button:hover {{
    transform:translateX(-50%) scale(1.1);
}}

.move-up {{
    animation: floatUp 9s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}}

@keyframes floatUp {{
    0% {{ 
        transform: translate(-50%, -50%) translate3d(0,0,0);
        opacity:1; 
    }}
    100% {{
        transform: translate(-50%, -50%) translate3d(0,-130vh,0);
        opacity:0; 
    }}
}}

.final-message {{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    font-size:4vmin;
    color:#e91e63;
    font-weight:bold;
    opacity:0;
    transition:opacity 3s ease-in-out;
}}

.show-message {{
    opacity:1;
}}

.bg-heart {{
    position:absolute;
    bottom:-30px;
    font-size:3vmin;
    color:#ff4da6;
    animation: rise 14s linear infinite;
    opacity:0.5;
}}

@keyframes rise {{
    0% {{ transform: translateY(0); opacity:0.6; }}
    100% {{ transform: translateY(-140vh); opacity:0; }}
}}
</style>
</head>

<body>

<div class="wrapper">
    {photo_divs}
    <button onclick="startAnimation()">Start 💖</button>
    <div class="final-message" id="finalMsg">
        You Are My Forever ❤️
    </div>
</div>

<script>
function startAnimation(){{
    let photos = document.querySelectorAll('.photo');

    photos.forEach((photo, index)=>{{
        setTimeout(()=>{{
            photo.classList.add('move-up');
        }}, index * 180);   // smoother wave delay
    }});

    setTimeout(()=>{{
        document.getElementById("finalMsg")
        .classList.add("show-message");
    }}, 5000);
}}

for(let i=0;i<25;i++){{
    let heart=document.createElement("div");
    heart.className="bg-heart";
    heart.innerHTML="💖";
    heart.style.left=Math.random()*100+"%";
    heart.style.animationDuration=(10+Math.random()*6)+"s";
    document.body.appendChild(heart);
}}
</script>

</body>
</html>
"""

    with open("index.html", "w") as f:
        f.write(html_content)

    print("💖 Responsive centered heart created.")


def start_server(port=8000):
    print(f"🚀 Open: http://localhost:{port}")
    server = HTTPServer(("localhost", port), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    create_html()
    start_server()
