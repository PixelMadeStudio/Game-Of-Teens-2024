const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
let stopGame = false;
let startpGame = true;

let score;
let scoreText;
let highscore;
let highscoreText;
let player;
let gravity;
let obstacles = [];
let gameSpeed;
let keys = {};

document.addEventListener('keydown', function (evt) {
  keys[evt.code] = true;
});
document.addEventListener('keyup', function (evt) {
  keys[evt.code] = false;
});

class Player {
  constructor(x, y, w, h, src) {
    this.run = 1;
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
    this.img = new Image();
    this.img.src = src;

    this.dy = 0;
    this.jumpForce = 10.35;
    this.originalHeight = h;
    this.grounded = false;
    this.jumpTimer = 0;
  }

  Animate() {
    // Jump
    if (keys['Space'] || keys['KeyW'] || keys['ArrowUp']) {
      this.img.src = `capybara/run${Math.floor(this.run)}.png`;
      this.Jump();
    } else {
      this.jumpTimer = 0;
    }

    if (keys['KeyDown'] || keys['KeyS'] || keys['ArrowDown']) {
      this.h = this.originalHeight / 2;
    } else {
      this.h = this.originalHeight;
    }

    this.y += this.dy;

    // Gravity
    if (this.y + this.h < canvas.height) {
      this.dy += gravity;
      this.grounded = false;
    } else {
      this.dy = 0;
      this.grounded = true;
      this.y = canvas.height - this.h;
    }
    // Draw the image
    console.log(this.run)
    console.log(this.img.src)
    console.log(Math.floor(this.run))
    ctx.drawImage(this.img, this.x, this.y, this.w, this.h);
    // Change image
    if(this.grounded){
      if(this.run > 4)
      this.run = 1;
      this.run = this.run +0.02;
      this.img.src = `capybara/run${Math.floor(this.run)}.png`;}
    else{
    
      
    // .....................................................
    this.img.src = "capybara/jump.png";
  }}

  Jump() {
    if (this.grounded && this.jumpTimer === 0) {
      this.jumpTimer = 1;
      this.dy = -this.jumpForce;
    } else if (this.jumpTimer > 0 && this.jumpTimer < 15) {
      this.img.src = "capybara/jump.png"
      this.jumpTimer++;
      this.dy = -this.jumpForce - (this.jumpTimer / 50);
    }
  }

  Draw() {
    ctx.beginPath();
    ctx.fillStyle = this.c;
    ctx.fillRect(this.x, this.y, this.w, this.h);
    ctx.closePath();
  }
}

class Obstacle {
  constructor(x, y, w, h, src) {
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
    this.img = new Image();
    this.img.src = src;



    this.dx = -gameSpeed;
  }

  Update() {
    if (stopGame) {
      console.log("stopGame");
      let bg = document.getElementById('bg');
      let Start_btn = document.getElementById("start_btn");
      Start_btn.style.display = "block";
      return;
    }

    if (startpGame) {
      this.x += this.dx;
      ctx.drawImage(this.img, this.x, this.y, this.w, this.h);

      this.dx = -gameSpeed;
    }
  }

  Draw() {
    ctx.beginPath();
    ctx.fillStyle = this.c;
    ctx.fillRect(this.x, this.y, this.w, this.h);
    ctx.closePath();
  }
}


class Text {
  constructor (t, x, y, a, c, s) {
    this.t = t;
    this.x = x;
    this.y = y;
    this.a = a;
    this.c = c;
    this.s = s;
  }

  Draw () {
    ctx.beginPath();
    ctx.fillStyle = this.c;
    ctx.font = this.s + "px sans-serif";
    ctx.textAlign = this.a;
    ctx.fillText(this.t, this.x, this.y);
    ctx.closePath();
  }
}

// Game Functions
function SpawnObstacle() {
  let size = RandomIntInRange(64, 128);
  let type = RandomIntInRange(0, 0);
  let obstacle = new Obstacle(canvas.width - size, canvas.height - size, size-(size/3), size, 'mushrooms/mushroom1.png');

  if (type == 1) {
    obstacle.y -= player.originalHeight - 10;
  }
  obstacles.push(obstacle);
}

function RandomIntInRange(min, max) {
  return Math.round(Math.random() * (max - min) + min);
}

function Start() {
  if (stopGame) {
    console.log("stopGame");
    let bg = document.getElementById('bg');
    bg.style.background = "url(/capybara/gameover.jpg)";
    gameover = new Text("Game Over", 500, 250, "left", "#212121", "200");
    gameover.Draw();
    let Start_btn = document.getElementById("start_btn");
    Start_btn.style.display = "block";
    return;
    
  }

  if (startpGame) {
    let bg = document.getElementById('bg');
    bg.style.background = "url(/capybara/background.jpg)";
    bg.style.display = "block";
    console.log("startGame");
    let Start_btn = document.getElementById("start_btn");
    Start_btn.style.display = "none";

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    ctx.font = "20px sans-serif";

    gameSpeed = 3.5;
    gravity = 0.43;

    score = 0;
    highscore = 0;
    if (localStorage.getItem('highscore')) {
      highscore = localStorage.getItem('highscore');
    }
    if(highscore == NaN || highscore == null || highscore == "" || highscore == undefined || highscore == "undefined"){
      highscore = 1;
    }

    // ццццц
    player = new Player(25, 0, 120, 160, "capybara/run1.png");

    scoreText = new Text("Score: " + score, 55, 55, "left", "#ce00af", "30");
    highscoreText = new Text("Highscore: " + highscore, canvas.width - 15, 15, "right", "#ce00af", "30");

    
    requestAnimationFrame(Update);
    // player.classList.add("capy")
    // playerElement.classList.add("capy")
    // playerElement.style.background = "url(capybara/run1.png)";
    // playerElement.style.backgroundSize = "cover";
    // 
  }
}

let initialSpawnTimer = 200;
let spawnTimer = initialSpawnTimer;
function Update() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  spawnTimer--;
  if (spawnTimer <= 0) {
    SpawnObstacle();
    spawnTimer = initialSpawnTimer - gameSpeed * 8;

    if (spawnTimer < 60) {
      spawnTimer = 60;
    }
  }

  // Spawn Enemies
  for (let i = 0; i < obstacles.length; i++) {
    let o = obstacles[i];

    if (o.x + o.w < 0) {
      obstacles.splice(i, 1);
    }

    if (
      player.x < o.x + o.w &&
      player.x + player.w > o.x &&
      player.y < o.y + o.h &&
      player.y + player.h > o.y
    ) {
      obstacles = [];
      Over();
    }

    o.Update();
  }

  player.Animate();

  score++;
  highscore++;
  scoreText.t = "Score: " + score;
  scoreText.Draw();

  if (score > highscore) {
    window.localStorage.setItem('highscore', score);
    highscore = score;
    highscoreText.t = "Highscore: " + highscore;
  }
  if(highscore >= 10000){
    Won();
  }
  highscoreText.Draw();

  gameSpeed += 0.0016;

  

  if (!stopGame) {
    requestAnimationFrame(Update);
  }
}

function Over() {
  stopGame = true;
  window.localStorage.setItem('highscore', highscore);
  Start();

}

function Show_goal(){
  alert("P.S - get 10000 score for gift")
}

function Restart() {
  stopGame = false;
  startpGame = true;  
  window.localStorage.setItem('highscore', highscore);
  Start();
}


function Won() {
  stopGame = true;
  window.localStorage.setItem('highscore', 0);
  bg = document.getElementById('bg');
  bg.style.background = "url(/capybara/won.jpg)";
  gameover = new Text("You won!", 500, 250, "left", "#212121", "200");
  gameover.Draw();
  ps = new Text("Check your profile ;)", 500, 500, "left", "#212121", "70");
  ps.Draw();
  rest = new Text("Refresh the page to restart", 500, 600, "left", "#212121", "100");
  rest.Draw();
  // let Start_btn = document.getElementById("start_btn");
  // Start_btn.style.display = "block";
  let Formm = document.getElementById("form123");
  let urlWin = "/won_";
  RequestToServer(Formm, urlWin);
}

