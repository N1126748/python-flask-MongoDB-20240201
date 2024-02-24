
document.addEventListener('DOMContentLoaded', function () {

  const account = document.getElementById('account');
  const password = document.getElementById('password');
  const name = document.getElementById('name');
  const phone = document.getElementById('phone');
  const email = document.getElementById('email');
  const address = document.getElementById('address');
  const submitButton = document.getElementById('send');

  name.addEventListener('input', () => {
    validateField(name, name.value.trim() !== '', '請填寫名稱');
    checkInputs(); // 驗證輸入並更新按鈕狀態
  });

  email.addEventListener('input', () => {
    validateField(email, isEmail(email.value.trim()), '無效的電子信箱');
    checkInputs();
  });

  phone.addEventListener('input', () => {
    validateField(phone, isPhone(phone.value.trim()), '無效的手機號碼');
    checkInputs(); 
  });

  account.addEventListener('input', () => {
    validateField(account, account.value.trim().length >= 8, '帳號過短,請填寫八位數帳號');
    checkInputs();
  });

  password.addEventListener('input', () => {
    validateField(password, password.value.trim().length >= 8, '密碼過短,請填寫八位數密碼');
    checkInputs(); 
  });

  address.addEventListener('input', () => {
    validateField(address, address.value.trim() !== '', '請填寫地址');
    checkInputs(); 
  });

  function checkInputs() {
    let isValid = true;
    // 驗證所有輸入欄位
    if (!(name.value.trim() !== '' && isEmail(email.value.trim()) && isPhone(phone.value.trim()) && account.value.trim().length >= 8 && password.value.trim().length >= 8 && address.value.trim() !== '')) {
      isValid = false;
    }
    // 更新按鈕狀態
    submitButton.disabled = !isValid;
  }

  function validateField(input, condition, errorMessage){
    if(condition){
      setSuccess(input);
    }else{
      setError(input, errorMessage);
    }
  } 
  
  function setError(input, message){
    const formControl = input.parentElement;
    const icon = formControl.querySelector('.icon');
    formControl.className = 'col-md-6 error';
    icon.className = 'icon fas fa-times-circle';
    input.placeholder = message;
  }

  function setSuccess(input){
    const formControl = input.parentElement;
    const icon = formControl.querySelector('.icon');
    formControl.className = 'col-md-6 success';
    icon.className = 'icon fas fa-check-circle';
  };

  function isEmail(email){
    return /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/.test(email);
  }

  function isPhone(phone){
    return /^09\d{8}$/.test(phone);
  }
  
});