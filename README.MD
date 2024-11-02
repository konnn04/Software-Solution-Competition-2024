# Web Tìm Trọ

Đây là bản thử nghiệm của ứng dụng web tìm trọ, được phát triển để phục vụ cho cuộc thi Giải Pháp Phần Mềm 2024 của khoa IT trường HCMOU.

## Giới Thiệu

Ứng dụng web tìm trọ giúp người dùng tìm kiếm và quản lý thông tin về các phòng trọ, nhà trọ. Người dùng có thể đăng nhập bằng tài khoản Google hoặc đăng ký tài khoản chủ trọ để quản lý các phòng trọ của mình.

## Các Thành Viên

- **Nguyễn Thanh Triều** - trieukon1011@gmail.com
- **Vương Minh Trí** - minhtri472k4@gmail.com
- **Lê Việt Hải Quân** - rinsenna2004@gmail.com

## Cài Đặt

### Yêu Cầu Hệ Thống

- Python 3.8 trở lên
- pip (Python package installer)

### Các Bước Cài Đặt

1. **Clone repository:**

    ```sh
    git clone https://github.com/your-repo/web-tim-tro.git
    cd web-tim-tro
    ```

2. **Tạo virtual environment và kích hoạt:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # Trên Windows: venv\Scripts\activate
    ```

3. **Cài đặt các thư viện cần thiết:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Cấu hình ứng dụng:**

    - Tạo tệp `config.py` từ tệp mẫu `config[sample].py` và cập nhật thông tin cấu hình cần thiết.

    ```sh
    cp app/config[sample].py app/config.py
    ```

5. **Khởi tạo cơ sở dữ liệu:**

    ```sh
    python app/db_create.py
    ```

## Chạy Ứng Dụng

1. **Chạy ứng dụng:**

    ```sh
    python -m app.index
    ```

2. **Truy cập ứng dụng:**

    Mở trình duyệt và truy cập `https://127.0.0.1:5000`

3. **Truy cập Flask-Admin:**

    Mở trình duyệt và truy cập `https://127.0.0.1:5000/admin` để truy cập vào bảng điều khiển quản trị của Flask-Admin.

## Các API Được Sử Dụng

- **Google OAuth 2.0:** Để xác thực người dùng thông qua tài khoản Google.
- **OpenStreetMap Nominatim API:** Để tìm kiếm và lấy thông tin địa lý.
- **OpenRouteService API:** Để lấy thông tin giao thông và tính toán khoảng cách.
- **flood-api.open-meteo.com**: Để lấy thông tin về nguy cơ lũ lụt.

## Các Chức Năng Chính

- **Đăng nhập và đăng ký:**
  - Đăng nhập bằng tài khoản Google (sinh viên).
  - Đăng ký tài khoản chủ trọ.

- **Quản lý phòng trọ:**
  - Thêm, sửa, xóa thông tin phòng trọ.
  - Quản lý thông tin chi tiết về phòng trọ, bao gồm diện tích, giá cả, loại phòng, và tình trạng.

- **Tìm kiếm phòng trọ:**
  - Tìm kiếm phòng trọ dựa trên vị trí, giá cả, và các tiêu chí khác.
  - Hiển thị kết quả tìm kiếm với thông tin chi tiết và hình ảnh.

- **Đánh giá và nhận xét:**
  - Người dùng có thể đánh giá và nhận xét về các phòng trọ.
  - Hiển thị các đánh giá và nhận xét từ người dùng khác.

## Đóng Góp

Nếu bạn muốn đóng góp cho dự án, vui lòng tạo pull request hoặc mở issue trên GitHub.

## Liên Hệ

Nếu bạn có bất kỳ câu hỏi nào, vui lòng liên hệ với chúng tôi qua email: trieukon1011@gmail.com