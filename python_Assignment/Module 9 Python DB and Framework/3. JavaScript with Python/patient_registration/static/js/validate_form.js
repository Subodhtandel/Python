// validate_form.js
// orchestrates all checks before allowing submit
(function(){
  const form = document.getElementById('regForm');
  if(!form) return;

  function setError(id,msg){
    const el = document.getElementById('err-'+id);
    if(el) el.textContent = msg || '';
  }

  form.addEventListener('submit', function(e){
    let hasError = false;
    const data = new FormData(form);
    const first = (data.get('first_name')||'').trim();
    const last = (data.get('last_name')||'').trim();
    const email = (data.get('email')||'').trim();
    const phone = (data.get('phone')||'').trim();
    const age = data.get('age');
    const pwd = data.get('password')||'';
    const confirm = data.get('confirm_password')||'';

    // simple checks
    if(!first){ setError('first_name','First name is required'); hasError=true } else setError('first_name','');
    if(!last){ setError('last_name','Last name is required'); hasError=true } else setError('last_name','');
    if(!email){ setError('email','Email is required'); hasError=true } else setError('email','');
    if(!phone || phone.length < 7){ setError('phone','Enter a valid phone'); hasError=true } else setError('phone','');
    const ageNum = Number(age);
    if(!age || isNaN(ageNum) || ageNum < 0 || ageNum > 120){ setError('age','Enter a valid age'); hasError=true } else setError('age','');

    // password checks (same logic as validate_password.js)
    if(pwd.length < 8){ setError('password','Password must be at least 8 characters'); hasError=true }
    else if(!/[A-Z]/.test(pwd)){ setError('password','Use at least one uppercase letter'); hasError=true }
    else if(!/[0-9]/.test(pwd)){ setError('password','Use at least one number'); hasError=true }
    else if(!/[\W_]/.test(pwd)){ setError('password','Use at least one symbol'); hasError=true }
    else setError('password','');

    if(pwd !== confirm){ setError('confirm_password','Passwords do not match'); hasError=true } else setError('confirm_password','');

    if(hasError){ e.preventDefault(); window.scrollTo({top:0,behavior:'smooth'}); }
  });
})();
