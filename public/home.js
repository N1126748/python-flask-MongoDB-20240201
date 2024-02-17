// 設定數量不能為0或負
function validateQuantity(inputId) {
    var quantityInput = document.getElementById(inputId);
    var quantityValue = parseInt(quantityInput.value);

    if (quantityValue < 1 || isNaN(quantityValue)) {
        quantityInput.value = 1;
    }
}

// 阻止按下submit按鈕刷新網頁
function submitForm(event, inputId) {
    event.preventDefault();  // 阻止默認提交行為
    validateQuantity(inputId);  // 呼叫驗證數量的函數
    // 獲取表單數據
    var form = event.target;  // 取得觸發事件的表單元素
    var formData = new FormData(form);  // 創建 FormData 物件來獲取表單數據
    // 使用 Fetch API 發送, Fetch API 回傳 Promise 物件,處理非同步的網路請求
    fetch(form.action, {
        method: form.method,
        body: formData
    }).then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else if (data.success) {
            alert('已加入購物車');
        }
    });
}