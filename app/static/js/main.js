/* =====================================================================
   FASTag Portal — main.js
   ===================================================================== */

document.addEventListener('DOMContentLoaded', function () {

  /* ══════════════════════════════════════════════════════════════════
     PASSWORD VISIBILITY TOGGLE
  ══════════════════════════════════════════════════════════════════ */
  function makeEyeToggle(btnId, iconId, inputId) {
    var btn  = document.getElementById(btnId);
    var icon = document.getElementById(iconId);
    var inp  = document.getElementById(inputId);
    if (!btn || !inp) return;
    btn.addEventListener('click', function () {
      var show = inp.type === 'password';
      inp.type = show ? 'text' : 'password';
      icon.className = show ? 'bi bi-eye-slash' : 'bi bi-eye';
    });
  }
  makeEyeToggle('eyeBtn',       'eyeIcon',        'password');
  makeEyeToggle('eyeBtnSignup', 'eyeIconSignup',  'signupPwd');
  makeEyeToggle('eyeBtnConfirm','eyeIconConfirm', 'confirmPwd');

  /* ══════════════════════════════════════════════════════════════════
     FLASH MESSAGES — Auto-dismiss after 5s
  ══════════════════════════════════════════════════════════════════ */
  document.querySelectorAll('.flash-alert').forEach(function (el) {
    setTimeout(function () {
      el.style.transition = 'opacity .4s ease, transform .4s ease';
      el.style.opacity    = '0';
      el.style.transform  = 'translateX(20px)';
      setTimeout(function () { el.remove(); }, 420);
    }, 5000);
  });

  /* ══════════════════════════════════════════════════════════════════
     VISUAL TEXT CAPTCHA ENGINE
  ══════════════════════════════════════════════════════════════════ */
  var captchaCanvas   = document.getElementById('captchaCanvas');
  var captchaInput    = document.getElementById('captchaInput');
  var captchaRefresh  = document.getElementById('captchaRefresh');
  var captchaWidget   = document.getElementById('captchaWidget');
  var captchaStatus   = document.getElementById('captchaStatus');
  var captchaError    = document.getElementById('captchaError');
  var captchaVerified = false;
  var captchaAnswer   = '';

  if (captchaCanvas && captchaCanvas.getContext) {

    /* Character pool — excludes ambiguous 0,O,I,1,l */
    var CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';

    function generateCode(n) {
      var s = '';
      for (var i = 0; i < (n || 6); i++)
        s += CHARS[Math.floor(Math.random() * CHARS.length)];
      return s;
    }

    function drawCaptcha(code) {
      var ctx = captchaCanvas.getContext('2d');
      var W = captchaCanvas.width, H = captchaCanvas.height;
      ctx.clearRect(0, 0, W, H);

      /* Background */
      var bg = ctx.createLinearGradient(0, 0, W, H);
      bg.addColorStop(0,   '#f8f9ff');
      bg.addColorStop(.5,  '#eef2ff');
      bg.addColorStop(1,   '#f8f9ff');
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, W, H);

      /* Noise dots */
      for (var d = 0; d < 70; d++) {
        ctx.beginPath();
        ctx.arc(Math.random()*W, Math.random()*H, Math.random()*1.6+.3, 0, Math.PI*2);
        ctx.fillStyle = 'rgba('+
          Math.floor(Math.random()*80+110)+','+
          Math.floor(Math.random()*80+110)+','+
          Math.floor(Math.random()*120+80)+',' +
          (Math.random()*.35+.15)+')';
        ctx.fill();
      }

      /* Noise bezier lines */
      for (var l = 0; l < 4; l++) {
        ctx.beginPath();
        ctx.moveTo(Math.random()*W, Math.random()*H);
        ctx.bezierCurveTo(
          Math.random()*W, Math.random()*H,
          Math.random()*W, Math.random()*H,
          Math.random()*W, Math.random()*H
        );
        ctx.strokeStyle = 'rgba('+
          Math.floor(Math.random()*60+80)+','+
          Math.floor(Math.random()*60+80)+','+
          Math.floor(Math.random()*140+80)+','+
          (Math.random()*.18+.07)+')';
        ctx.lineWidth = Math.random()*1.5 + .4;
        ctx.stroke();
      }

      /* Characters */
      var colors  = ['#102040','#163058','#1d4280','#0a1628','#2555a8','#102040'];
      var sizes   = [22, 25, 24, 22, 24, 23];
      var charW   = (W - 36) / code.length;

      for (var c = 0; c < code.length; c++) {
        ctx.save();
        var cx  = 18 + charW * c + charW / 2;
        var cy  = H / 2;
        var ang = (Math.random() - .5) * .45;
        var fs  = sizes[c % sizes.length] + Math.floor(Math.random() * 3);
        ctx.translate(cx, cy + (Math.random()-.5)*7);
        ctx.rotate(ang);
        ctx.shadowColor   = 'rgba(22,48,88,.18)';
        ctx.shadowBlur    = 3;
        ctx.shadowOffsetY = 1;
        ctx.font          = '800 ' + fs + 'px Inter, Arial, sans-serif';
        ctx.fillStyle     = colors[c % colors.length];
        ctx.textAlign     = 'center';
        ctx.textBaseline  = 'middle';
        ctx.fillText(code[c], 0, 0);
        ctx.restore();
      }

      /* Edge accents */
      ctx.fillStyle = 'rgba(37,85,168,.05)';
      ctx.fillRect(0, 0, W, 2);
      ctx.fillRect(0, H-2, W, 2);
    }

    function refreshCaptcha() {
      captchaAnswer   = generateCode(6);
      captchaVerified = false;
      drawCaptcha(captchaAnswer);
      if (captchaInput)  captchaInput.value = '';
      if (captchaStatus) captchaStatus.innerHTML = '';
      if (captchaError)  captchaError.style.display = 'none';
      if (captchaWidget) captchaWidget.classList.remove('captcha-verified','captcha-shake');
    }

    refreshCaptcha();

    if (captchaRefresh) {
      captchaRefresh.addEventListener('click', function () {
        this.classList.add('spinning');
        var self = this;
        setTimeout(function () { self.classList.remove('spinning'); }, 420);
        refreshCaptcha();
        if (captchaInput) captchaInput.focus();
      });
    }

    if (captchaInput) {
      captchaInput.addEventListener('input', function () {
        var val = this.value.toUpperCase().replace(/[^A-Z0-9]/g,'');
        this.value = val;
        if (captchaError) captchaError.style.display = 'none';

        if (val.length === 6) {
          if (val === captchaAnswer) {
            captchaVerified = true;
            captchaWidget.classList.add('captcha-verified');
            captchaWidget.classList.remove('captcha-shake');
            captchaStatus.innerHTML = '<i class="bi bi-check-circle-fill" style="color:#059669"></i>';
          } else {
            captchaVerified = false;
            captchaWidget.classList.remove('captcha-verified');
            captchaStatus.innerHTML = '<i class="bi bi-x-circle-fill" style="color:#dc2626"></i>';
            captchaWidget.classList.remove('captcha-shake');
            void captchaWidget.offsetWidth;
            captchaWidget.classList.add('captcha-shake');
            if (captchaError) captchaError.style.display = 'flex';
            setTimeout(refreshCaptcha, 850);
          }
        } else {
          captchaVerified = false;
          captchaWidget.classList.remove('captcha-verified');
          captchaStatus.innerHTML = '';
        }
      });
    }

    /* Block form submit if CAPTCHA not solved */
    var loginForm = document.getElementById('loginForm');
    if (loginForm) {
      loginForm.addEventListener('submit', function (e) {
        if (!captchaVerified) {
          e.preventDefault();
          captchaWidget.classList.remove('captcha-shake');
          void captchaWidget.offsetWidth;
          captchaWidget.classList.add('captcha-shake');
          if (captchaError) {
            captchaError.style.display = 'flex';
            document.getElementById('captchaErrorText').textContent =
              captchaInput && captchaInput.value
                ? 'Incorrect characters — please try again.'
                : 'Please complete the security check.';
          }
          if (captchaInput) captchaInput.focus();
        }
      });
    }

  } // end captcha

  /* ══════════════════════════════════════════════════════════════════
     OTP — Get OTP button + timer + auto-advance boxes
  ══════════════════════════════════════════════════════════════════ */
  var getOtpBtn    = document.getElementById('getOtpBtn');
  var otpInputGroup = document.getElementById('otpInputGroup');
  var otpSigninBtn  = document.getElementById('otpSigninBtn');
  var timerInterval;

  if (getOtpBtn) {
    getOtpBtn.addEventListener('click', function () {
      var mobile = document.getElementById('otpMobile').value.trim();
      if (!/^\d{10}$/.test(mobile)) {
        alert('Please enter a valid 10-digit mobile number.');
        return;
      }
      otpInputGroup.style.display = 'block';
      otpSigninBtn.style.display  = 'flex';
      getOtpBtn.disabled = true;
      getOtpBtn.textContent = 'Sent ✓';
      startOtpTimer();
      var firstCell = document.querySelectorAll('.otp-cell')[0];
      if (firstCell) firstCell.focus();
    });
  }

  /* OTP auto-advance */
  document.querySelectorAll('.otp-cell').forEach(function (box, idx, all) {
    box.addEventListener('input', function () {
      if (this.value.length === 1 && idx < all.length - 1) all[idx+1].focus();
    });
    box.addEventListener('keydown', function (e) {
      if (e.key === 'Backspace' && this.value === '' && idx > 0) all[idx-1].focus();
    });
  });

  function startOtpTimer() {
    var secs = 30;
    var timerText  = document.getElementById('timerText');
    var resendLink = document.getElementById('resendLink');
    if (!timerText) return;
    resendLink.style.pointerEvents = 'none';
    resendLink.style.opacity = '.4';
    timerText.textContent = '(' + secs + 's)';
    timerInterval = setInterval(function () {
      secs--;
      timerText.textContent = secs > 0 ? '(' + secs + 's)' : '';
      if (secs <= 0) {
        clearInterval(timerInterval);
        resendLink.style.pointerEvents = '';
        resendLink.style.opacity = '1';
        if (getOtpBtn) { getOtpBtn.disabled = false; getOtpBtn.textContent = 'Resend'; }
      }
    }, 1000);
  }

  var resendLink = document.getElementById('resendLink');
  if (resendLink) {
    resendLink.addEventListener('click', function (e) {
      e.preventDefault();
      document.querySelectorAll('.otp-cell').forEach(function (b) { b.value = ''; });
      var firstCell = document.querySelectorAll('.otp-cell')[0];
      if (firstCell) firstCell.focus();
      startOtpTimer();
    });
  }

  /* Tab reset */
  document.querySelectorAll('.auth-tab').forEach(function (tab) {
    tab.addEventListener('shown.bs.tab', function () {
      document.querySelectorAll('.field-error').forEach(function (el) { el.textContent = ''; });
    });
  });

  /* ══════════════════════════════════════════════════════════════════
     SIGNUP — Password strength + match + progress
  ══════════════════════════════════════════════════════════════════ */
  var signupPwd    = document.getElementById('signupPwd');
  var confirmPwd   = document.getElementById('confirmPwd');
  var strengthSegs = ['seg1','seg2','seg3','seg4'].map(function(id){ return document.getElementById(id); });
  var strengthLabel = document.getElementById('strengthLabel');
  var matchCopy     = document.getElementById('matchIndicator');
  var progressFill  = document.getElementById('signupProgress');
  var progressLabel = document.getElementById('progressLabel');

  var strengthColors = ['', '#ef4444', '#f59e0b', '#3b82f6', '#10b981'];
  var strengthTexts  = ['', 'Weak — add more variety', 'Fair — getting better', 'Good — almost there', 'Strong ✓'];

  function getStrength(pwd) {
    var s = 0;
    if (pwd.length >= 8)           s++;
    if (/[A-Z]/.test(pwd))         s++;
    if (/\d/.test(pwd))            s++;
    if (/[^A-Za-z0-9]/.test(pwd)) s++;
    return s;
  }

  function updateStrength() {
    if (!signupPwd) return;
    var score = getStrength(signupPwd.value);
    strengthSegs.forEach(function (seg, i) {
      if (seg) seg.style.background = i < score ? strengthColors[score] : '';
    });
    if (strengthLabel) {
      strengthLabel.textContent = signupPwd.value ? strengthTexts[score] : '';
      strengthLabel.style.color = strengthColors[score];
    }
  }

  function checkMatch() {
    if (!confirmPwd || !signupPwd || !matchCopy) return;
    if (!confirmPwd.value) { matchCopy.innerHTML = ''; return; }
    if (confirmPwd.value === signupPwd.value) {
      matchCopy.innerHTML = '<i class="bi bi-check-circle-fill" style="color:#059669"></i><span style="color:#059669">Passwords match</span>';
    } else {
      matchCopy.innerHTML = '<i class="bi bi-x-circle-fill" style="color:#dc2626"></i><span style="color:#dc2626">Passwords do not match</span>';
    }
  }

  var signupFieldIds = ['fullName','emailAddr','mobileNum','signupPwd','confirmPwd'];
  var progressMsgs = [
    'Fill in your details to get started',
    'Great start! Keep going…',
    'Looking good! Almost there…',
    'Set a strong password',
    'Confirm your password',
    'All set — ready to create your account!',
    'Ready to create your account!'
  ];

  function updateProgress() {
    if (!progressFill) return;
    var filled = 0;
    signupFieldIds.forEach(function (id) {
      var el = document.getElementById(id);
      if (el && el.value.trim()) filled++;
    });
    var pct = Math.round((filled / signupFieldIds.length) * 100);
    progressFill.style.width = pct + '%';
    if (progressLabel) progressLabel.textContent = progressMsgs[Math.min(filled, progressMsgs.length-1)];
  }

  if (signupPwd)  signupPwd.addEventListener('input',  function () { updateStrength(); checkMatch(); updateProgress(); });
  if (confirmPwd) confirmPwd.addEventListener('input',  function () { checkMatch(); updateProgress(); });

  signupFieldIds.forEach(function (id) {
    var el = document.getElementById(id);
    if (el) el.addEventListener('input', updateProgress);
  });

  /* Digits-only mobile input */
  var mobileInput = document.getElementById('mobileNum');
  if (mobileInput) {
    mobileInput.addEventListener('input', function () {
      this.value = this.value.replace(/\D/g,'').slice(0,10);
    });
  }

});
