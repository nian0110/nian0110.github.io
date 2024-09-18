let button = document.getElementById("button");
let refreshButton = document.getElementById("refresh-button");
let prevButton = document.getElementById("previous-button");
let nextButton = document.getElementById("next-button");
let image = document.getElementById("image");
let info = document.getElementById("info");
let imageUrls = [];
let totalImagesCount = 0; // 總圖片數量
let selectedImages = []; // 隨機選中的圖片
let count = document.getElementById("count");
let randomPhoto = 10;
let currentIndex = -1; // 當前顯示的圖片索引

fetch('http://127.0.0.1:5000/images', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ limit: randomPhoto })
})
    .then(response => response.json())
    .then(data => {
        // 使用從 API 獲取的 JSON 資料
        imageUrls = data.Images.map(item => ({
            filename: item.filename.trim(),
            full_path: item.full_path.trim()
        }));
        totalImagesCount = data.totalImagesCount; // 記錄總圖片數量

        // 初始隨機選取 randomPhoto 張圖片
        selectedImages = shuffleArray(imageUrls).slice(0, randomPhoto);
        count.innerHTML = "共 " + totalImagesCount + " 張圖片，已隨機選取 " + randomPhoto + " 張圖片。<br>請點選「隨機顯示圖片」查看！"; // 更新圖片數量
    })
    .catch(error => {
        console.error('Error fetching the JSON data:', error);
    });

button.addEventListener("click", function () {
    if (currentIndex < selectedImages.length - 1) {
        currentIndex++;
        showImage(currentIndex);
    } else {
        alert("所有圖片都已顯示完畢！請按下「重新整理」按鈕來重新開始。");
        count.innerHTML = "共 " + randomPhoto + " 張圖片，所有圖片都已顯示完畢！<br>請按下「重新整理」按鈕來重新開始。";
    }
});

refreshButton.addEventListener("click", function () {
    // 當按下 refresh 按鈕時，重新隨機選取 randomPhoto 張圖片
    if (imageUrls.length >= randomPhoto) {
        selectedImages = shuffleArray(imageUrls).slice(0, randomPhoto); // 隨機選取 randomPhoto 張圖片
        currentIndex = -1; // 重置當前索引
        image.src = ""; // 清除顯示的圖片
        image.style.display = "none"; // 隱藏圖片
        info.innerHTML = ""; // 清除顯示的附加信息
        count.innerHTML = '已重新隨機選取 ' + randomPhoto + ' 張圖片，請點選「隨機顯示圖片」查看！'; // 更新訊息

        // 隱藏其他按鈕
        refreshButton.style.display = "none";
        prevButton.style.display = "none";
        button.textContent = "隨機顯示圖片";
    } else {
        alert("圖片數量不足以隨機選取" + randomPhoto + "張。");
    }
});

prevButton.addEventListener("click", function () {
    if (currentIndex > 0) {
        currentIndex--;
        showImage(currentIndex);
    } else {
        alert("已經是第一張圖片！");
    }
});

nextButton.addEventListener("click", function () {
    if (currentIndex < selectedImages.length - 1) {
        currentIndex++;
        showImage(currentIndex);
    } else {
        alert("所有圖片都已顯示完畢！請按下「重新整理」按鈕來重新開始。");
        count.innerHTML = "共 " + randomPhoto + " 張圖片，所有圖片都已顯示完畢！<br>請按下「重新整理」按鈕來重新開始。";
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

// 顯示圖片並更新訊息
function showImage(index) {
    let imageData = selectedImages[index];
    image.src = imageData.full_path;
    image.style.display = "block";
    // info.innerHTML = `username：${imageData.username}<br>類別：${imageData.root_path}<br>活動名稱：${imageData.children_path}`;
    count.innerHTML = "第 " + (index + 1) + " 張圖片，共 " + selectedImages.length + " 張";

    // 顯示其他按鈕
    refreshButton.style.display = "inline";
    prevButton.style.display = "inline";
    button.textContent = "下一張";
}
