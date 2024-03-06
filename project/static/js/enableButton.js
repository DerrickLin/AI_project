function enableButton() {
    var fileInput = document.getElementById('input');
    var submitButton = document.getElementById('submitButton');

    // 檢查是否選擇文件
    if (fileInput.files.length === 0) {
        // 如果沒有，禁用按鈕
        submitButton.disabled = true;
    } else {
        // 如果有，啟用
        submitButton.disabled = false;
    }
}