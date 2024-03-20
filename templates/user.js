const formControl = document.querySelector('.form-control');
formControl.addEventListener('input', function (event) {
    const input = event.target;
    const isInvalid = input.checkValidity() === false;
    input.classList.toggle('is-invalid', isInvalid);
    input.classList.toggle('is-valid', !isInvalid);
    const error = input.nextElementSibling;
    if (error && error.classList.contains('invalid-feedback')) {
        error.textContent = input.validationMessage;
    }
});
const loginBtn = document.querySelector('.btn btn-primary btn-login');
loginBtn.addEventListener('mouseover', function (event) {
    loginBtn.style.width = '50%';
    
});
loginBtn.addEventListener('mouseout', function (event) {
    loginBtn.style.width = ''; // 恢复到原始长度，可以根据需要设置具体的宽度
});

loginBtn.addEventListener('click', function (event) {
    const loader = document.createElement('div');
    loader.classList.add('loader');
    loginBtn.appendChild(loader);

    // 模拟加载完成后移除加载动画
    setTimeout(() => {
        loader.remove();
        // 这里可以添加加载完成后的操作
    }, 2000); // 假设加载时间为 2 秒
});