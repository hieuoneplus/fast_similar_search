
async function displayImageAtPosition(position) {
    const imagesDirectory = 'C:/Users/nshd1/OneDrive/Documents/code/fss/static/image'; // Đường dẫn tới thư mục chứa ảnh
    const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif']; // Các đuôi file ảnh hỗ trợ
    const imageList = []; // Danh sách các ảnh
    const imgElement = document.createElement('img'); // Tạo một thẻ <img>

    // Sử dụng fetch API để đọc nội dung của thư mục chứa ảnh
    const response = await fetch(imagesDirectory);
    if (!response.ok) {
        throw new Error(`Cannot read directory: ${imagesDirectory}`);
    }
    const directoryContent = await response.text();

    // Phân tích nội dung của thư mục chứa ảnh để lấy danh sách các ảnh
    directoryContent.split('\n').forEach((fileName) => {
        if (imageExtensions.includes(fileName.substr(fileName.lastIndexOf('.')))) {
            imageList.push(fileName);
        }
    });

    // Lấy ảnh tại vị trí tương ứng và gán vào thuộc tính src của thẻ <img>
    imgElement.src = `${imagesDirectory}/${imageList[position]}`;

    // Hiển thị ảnh trên trang web
    document.body.appendChild(imgElement);
}
