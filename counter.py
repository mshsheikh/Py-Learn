from flask import Flask, render_template_string

app = Flask(__name__)

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Countdown Timer</title>
  <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    body,
    html {
        height: 100%;
        font-family: 'Arial', sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    body.day-mode {
        background-color: skyblue;
        color: black;
    }
    body.night-mode {
        background-color: #2c3e50;
        color: white;
    }
    .container {
        text-align: center;
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }
    body.night-mode .container {
        background-color: #233241;
        color: white;
    }
    .title {
        font-size: 2rem;
        margin-bottom: 1rem;
        color: inherit;
    }
    .input-container {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    input {
        padding: 0.5rem;
        font-size: 1rem;
        border: 1px solid #ccc;
        border-radius: 5px;
        width: 150px;
    }
    button {
        padding: 0.5rem 1rem;
        font-size: 1rem;
        border: none;
        border-radius: 24px;
        cursor: pointer;
        transition: transform 0.1s ease, box-shadow 0.1s ease;
        background-color: #171817;
        color: white;
    }
    button:active {
        transform: scale(0.95);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    button:focus {
        outline: none;
    }
    button:hover {
        transform: scale(1.05);
    }
    .start {
        background-color: #4CAF50;
        color: white;
    }
    .pause {
        background-color: #FF5722;
        color: white;
    }
    .reset {
        background-color: #2196F3;
        color: white;
    }
    .theme-switch-wrapper {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
    }
    .theme-switch {
        position: relative;
        display: inline-block;
        width: 60px;
        height: 34px;
    }
    .theme-switch input {
        opacity: 0;
        width: 0;
        height: 0;
    }
    .slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #ccc;
        transition: .4s;
        border-radius: 34px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 2px;
    }
    .slider:before {
        position: absolute;
        content: "";
        height: 26px;
        width: 26px;
        border-radius: 50%;
        left: 4px;
        bottom: 4px;
        background-color: white;
        transition: .4s;
    }
    input:checked+.slider {
        background-color: #335b77;
    }
    input:checked+.slider:before {
        transform: translateX(26px);
    }
    .sun-icon,
    .moon-icon {
        font-size: 16px;
        color: #fff;
    }
    .sun-icon {
        margin-left: 8px;
    }
    .moon-icon {
        margin-right: 8px;
    }
    .timer {
        font-size: 4rem;
        margin: 1rem 0;
        color: inherit;
        animation: pulse 1s infinite alternate;
    }
    @keyframes pulse {
        0% {
            color: #ff5722;
        }
        100% {
            color: #4CAF50;
        }
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
    }
  </style>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>
<body class="day-mode">
  <div id="app" class="container">
    <h1 class="title">Countdown Timer</h1>
    <div class="input-container">
      <input type="number" id="durationInput" placeholder="Enter seconds">
      <button id="setBtn">Set</button>
    </div>
    <div id="timerDisplay" class="timer">00:00</div>
    <div class="button-container">
      <button id="startBtn" class="start">Start</button>
      <button id="pauseBtn" class="pause">Pause</button>
      <button id="resetBtn" class="reset">Reset</button>
    </div>
    <div class="theme-switch-wrapper">
      <label class="theme-switch" for="themeSwitch">
        <input type="checkbox" id="themeSwitch">
        <span class="slider round">
          <i class="fas fa-sun sun-icon"></i>
          <i class="fas fa-moon moon-icon"></i>
        </span>
      </label>
    </div>
  </div>
  <script>
    document.addEventListener("DOMContentLoaded", function () {
        var countdown = null;
        var remainingTime = 0;
        var timerDisplay = document.getElementById('timerDisplay');
        var durationInput = document.getElementById('durationInput');
        var setBtn = document.getElementById('setBtn');
        var startBtn = document.getElementById('startBtn');
        var pauseBtn = document.getElementById('pauseBtn');
        var resetBtn = document.getElementById('resetBtn');
        var themeSwitch = document.getElementById('themeSwitch');

        function updateDisplay(time) {
            var minutes = Math.floor(time / 60);
            var seconds = time % 60;
            timerDisplay.textContent = "".concat(String(minutes).padStart(2, '0'), ":").concat(String(seconds).padStart(2, '0'));
        }

        function startCountdown() {
            if (countdown !== null) {
                clearInterval(countdown);
            }
            countdown = window.setInterval(function () {
                if (remainingTime <= 0) {
                    clearInterval(countdown);
                    countdown = null;
                    alert("Time's up!");
                    return;
                }
                remainingTime--;
                updateDisplay(remainingTime);
            }, 1000);
        }

        function setTimer() {
            var duration = parseInt(durationInput.value, 10);
            if (isNaN(duration) || duration <= 0) {
                alert("Please enter a valid time in seconds.");
                return;
            }
            remainingTime = duration;
            updateDisplay(remainingTime);
        }

        function pauseCountdown() {
            if (countdown !== null) {
                clearInterval(countdown);
                countdown = null;
            }
        }

        function resetCountdown() {
            if (countdown !== null) {
                clearInterval(countdown);
                countdown = null;
            }
            remainingTime = 0;
            updateDisplay(remainingTime);
        }

        setBtn.addEventListener('click', setTimer);
        startBtn.addEventListener('click', startCountdown);
        pauseBtn.addEventListener('click', pauseCountdown);
        resetBtn.addEventListener('click', resetCountdown);

        // Theme Switch
        themeSwitch.addEventListener('change', function () {
            document.body.classList.toggle('night-mode', themeSwitch.checked);
            document.body.classList.toggle('day-mode', !themeSwitch.checked);
        });

        updateDisplay(remainingTime);
    });
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True)