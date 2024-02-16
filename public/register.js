document.getElementById("send").addEventListener("click", function () {
    // 檢查所有帶有required屬性的輸入資料是否都有值
    var isValid = Array.from(
      document.querySelectorAll("input[required]")
    ).every(function (input) {
      return input.value.trim() !== "";
    });

    if (!isValid) {
      // 如果有未填寫的資料，顯示警告框
      alert("請填寫完整所有資料！");
    } 
  });