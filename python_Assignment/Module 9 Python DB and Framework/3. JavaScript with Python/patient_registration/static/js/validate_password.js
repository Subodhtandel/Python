// validate_password.js
// checks password strength and confirms match
(function(){
  const pwd = document.getElementById('password');
  const confirm = document.getElementById('confirm_password');
  const errPwd = document.getElementById('err-password');
  const errConfirm = document.getElementById('err-confirm_password');
  if(!pwd) return;

  function checkStrength(v){
    if(v.length < 8) return 'Password must be at least 8 characters';
    if(!/[A-Z]/.test(v)) return 'Use at least one uppercase letter';
    if(!/[0-9]/.test(v)) return 'Use at least one number';
    if(!/[\W_]/.test(v)) return 'Use at least one symbol';
    return '';
  }

  pwd.addEventListener('input',()=>{
    const msg = checkStrength(pwd.value);
    errPwd.textContent = msg;
  });

  if(confirm){
    function checkConfirm(){
      if(!confirm.value) { errConfirm.textContent = ''; return; }
      if(pwd.value !== confirm.value) errConfirm.textContent = 'Passwords do not match';
      else errConfirm.textContent = '';
    }
    confirm.addEventListener('input', checkConfirm);
    pwd.addEventListener('input', checkConfirm);
  }
})();
