let button = document.getElementById("button");
let refreshButton = document.getElementById("refresh-button");
let image = document.getElementById("image");
let imageUrls = [];
let removedUrls = [];
let totalImagesCount = 0; // 總圖片數量
let selectedImages = []; // 隨機選中的圖片
let count = document.getElementById("count");
let randomPhoto = 10;

// 使用 fetch 來讀取 CSV 檔案
fetch('images.csv')
    .then(response => response.text())
    .then(data => {
        // 將 CSV 的每一行分割並存入 imageUrls 陣列
        imageUrls = data.split('\n').filter(url => url.trim() !== ""); // 過濾掉空白行
        totalImagesCount = imageUrls.length; // 記錄總圖片數量

        // 初始隨機選取 randomPhoto 張圖片
        selectedImages = shuffleArray(imageUrls).slice(0, randomPhoto);
        count.innerHTML = "共 " + totalImagesCount + " 張圖片，已隨機選取 " + randomPhoto + " 張圖片，剩餘 " + selectedImages.length + " 張圖片"; // 更新圖片數量
    })
    .catch(error => {
        console.error('Error fetching the CSV file:', error);
    });

button.addEventListener("click", function () {
    if (selectedImages.length > 0) {
        // 隨機選擇一張圖片
        let randomIndex = Math.floor(Math.random() * selectedImages.length);
        let selectedImageUrl = selectedImages[randomIndex];

        image.src = selectedImageUrl;
        image.style.display = "block";

        removedUrls.push(selectedImageUrl); // 將顯示過的圖片移至 removedUrls
        selectedImages.splice(randomIndex, 1); // 從 selectedImages 中移除顯示過的圖片
        count.innerHTML = "共 " + randomPhoto + " 張圖片，剩餘 " + selectedImages.length + " 張圖片"; // 更新剩餘圖片數量
    } else {
        alert("所有圖片都已顯示完畢！請按下重新整理按鈕來重新開始。");
        count.innerHTML = "共 " + randomPhoto + " 張圖片，所有圖片都已顯示完畢！"; // 更新剩餘圖片數量
    }
});

refreshButton.addEventListener("click", function () {
    // 當按下 refresh 按鈕時，重新隨機選取 randomPhoto 張圖片
    if (imageUrls.length >= randomPhoto) {
        selectedImages = shuffleArray(imageUrls).slice(0, randomPhoto); // 隨機選取 randomPhoto 張圖片
        removedUrls = []; // 清空已顯示的圖片列表
        image.src = ""; // 清除顯示的圖片
        image.style.display = "none"; // 隱藏圖片
        // 更新為「已隨機選取圖片」的訊息
        count.innerHTML = '已重新隨機選取 ' + randomPhoto + ' 張圖片，請點選「隨機顯示圖片」查看！'; // 更新訊息
    } else {
        alert("圖片數量不足以隨機選取" + randomPhoto + "張。");
    }
});

// 洗牌函數，用於隨機打亂圖片順序
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}
