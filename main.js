let button = document.getElementById("button");
let refreshButton = document.getElementById("refresh-button");
let image = document.getElementById("image");
let filename = document.getElementById("filename"); // 用於顯示檔名的元素
let imageUrls = [];
let removedUrls = [];
let totalImagesCount = 0; // 總圖片數量
let count = document.getElementById("count");

// 使用 fetch 來讀取 CSV 檔案
fetch('images.csv')
    .then(response => response.text())
    .then(data => {
        // 將 CSV 的每一行分割並存入 imageUrls 陣列
        imageUrls = data.split('\n').filter(url => url.trim() !== ""); // 過濾掉空白行
        totalImagesCount = imageUrls.length; // 記錄總圖片數量
        count.innerHTML = "共 " + totalImagesCount + " 張圖片，剩餘 " + imageUrls.length + " 張圖片"; // 更新圖片數量
    })
    .catch(error => {
        console.error('Error fetching the CSV file:', error);
    });

button.addEventListener("click", function() {
    if (imageUrls.length > 0) {
        // 隨機選擇一張圖片
        let randomIndex = Math.floor(Math.random() * imageUrls.length);
        let selectedImageUrl = imageUrls[randomIndex];

        image.src = selectedImageUrl;
        image.style.display = "block";
        
        removedUrls.push(selectedImageUrl); // 將顯示過的圖片移至 removedUrls
        imageUrls.splice(randomIndex, 1); // 從 imageUrls 中移除顯示過的圖片
        count.innerHTML = "共 " + totalImagesCount + " 張圖片，剩餘 " + imageUrls.length + " 張圖片"; // 更新剩餘圖片數量
    } else {
        alert("所有圖片都已顯示完畢！請按下重新整理按鈕來重新開始。");
        count.innerHTML = "共 " + totalImagesCount + " 張圖片，所有圖片都已顯示完畢！"; // 更新剩餘圖片數量
    }
});

refreshButton.addEventListener("click", function() {
    // 將已顯示的圖片重新加入 imageUrls
    imageUrls = imageUrls.concat(removedUrls);
    removedUrls = []; // 清空已顯示的圖片列表
    image.src = ""; // 清除顯示的圖片
    image.style.display = "none"; // 隱藏圖片
    filename.innerHTML = ""; // 清除檔名顯示
    count.innerHTML = "共 " + totalImagesCount + " 張圖片，剩餘 " + imageUrls.length + " 張圖片"; // 更新剩餘圖片數量
});
