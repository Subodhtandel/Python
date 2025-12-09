// validate_email.js
// simple email regex and live validation
(function(){
  const emailField = document.getElementById('email');
  const err = document.getElementById('err-email');
  if(!emailField) return;
  const re = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
  emailField.addEventListener('input',()=>{
    const v = emailField.value.trim();
    if(!v){ err.textContent = ''; return; }
    if(!re.test(v)){
      err.textContent = 'Enter a valid email address';
    } else { err.textContent = ''; }
  });
})();
