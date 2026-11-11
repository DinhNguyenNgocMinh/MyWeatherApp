# My Weather App

## Tình trạng

Repository hiện có hai script Python và hai file CSV. Khi chạy `code/get_data.py`, script gọi API Open-Meteo với tọa độ `21.0245, 105.8412` và timezone `Asia/Singapore`, đọc dữ liệu `hourly.time` và `hourly.temperature_2m`, sau đó xử lý các file trong thư mục `csv/`.

Lần kiểm tra gần nhất, script chạy thành công, nhận 168 dòng từ API, không thêm dòng mới vào `csv/weather.csv` và làm trống `csv/nomatch.csv` sau khi xử lý.

## Cấu trúc thư mục

```text
My Weather App/
├── README.md
├── code/
│   ├── get_api.py       # Tạo request và gọi Open-Meteo
│   └── get_data.py      # Đọc phản hồi API và xử lý các file CSV
└── csv/
    ├── weather.csv      # File dữ liệu chính
    └── nomatch.csv      # File được dùng trong lúc xử lý
```

## Cài đặt và chạy

Yêu cầu: Python 3, thư viện `requests` và kết nối Internet.

```powershell
pip install requests
python code/get_data.py
```

Chạy lệnh từ thư mục gốc của repository. Mã nguồn xác định đường dẫn CSV dựa trên vị trí của `get_data.py`, vì vậy lệnh vẫn tham chiếu đúng các file trong `csv/` khi được chạy từ thư mục gốc.

## Luồng xử lý hiện tại

```text
Open-Meteo API
      |
      v
code/get_api.py
      |
      v
code/get_data.py
      |
      +--> csv/nomatch.csv
      |        |
      |        v
      +--> csv/weather.csv
               |
               v
        csv/nomatch.csv được làm trống
```

1. `get_data.py` gọi hàm `get_api()` trong `get_api.py`.
2. `get_api()` tạo URL tới endpoint `/v1/forecast` của [Open-Meteo](https://open-meteo.com/) với tham số `hourly=temperature_2m`, rồi gửi HTTP GET request bằng `requests.get()`.
3. Khi nhận HTTP 200, script lấy hai mảng `hourly.time` và `hourly.temperature_2m` từ JSON phản hồi.
4. Script ghi từng cặp thời gian/nhiệt độ cùng một thời điểm ghi dữ liệu vào `csv/nomatch.csv`.
5. Script đọc các dòng trong `csv/weather.csv`, tạo khóa gồm hai trường đầu tiên `(datetime, temperature)`, và so sánh với các dòng trong `nomatch.csv`.
6. Các dòng có khóa chưa có trong `weather.csv` được nối thêm vào cuối file. Sau đó `nomatch.csv` được mở ở chế độ ghi để làm trống nội dung.

## Dữ liệu CSV

`csv/weather.csv` có header sau:

```csv
datetime,temperature,write at
```

| Cột | Nguồn/ý nghĩa trong mã nguồn |
| --- | --- |
| `datetime` | Phần tử từ `hourly.time` trong phản hồi API. |
| `temperature` | Phần tử tương ứng từ `hourly.temperature_2m`. |
| `write at` | Giá trị `datetime.datetime.now()` được tạo một lần cho mỗi lượt chạy. |

`csv/nomatch.csv` không được ghi header. File này được ghi đè ở đầu lượt chạy và bị làm trống ở cuối lượt chạy.

## Hành vi xử lý lỗi trong mã nguồn

- `get_api()` trả về JSON khi API trả HTTP 200.
- Với HTTP 400, hàm in URL hiện tại và trả về chuỗi `"Wrong url"`.
- Với mã HTTP khác, hàm trả về mã trạng thái HTTP.
- `get_data.py` truy cập trực tiếp các trường `data["hourly"]["time"]` và `data["hourly"]["temperature_2m"]`; không có nhánh xử lý riêng cho các giá trị không phải JSON mà `get_api()` có thể trả về.

## Ghi chú về cấu hình hiện có

- Tọa độ trong mã nguồn là `lat=21.0245` và `lon=105.8412`.
- Giá trị timezone được truyền vào URL là `Asia%2FSingapore` (tương ứng `Asia/Singapore`).
- Request không truyền tham số `temperature_unit`.
- Điều kiện so sánh dữ liệu dùng cả thời điểm và nhiệt độ; một dòng có cùng `datetime` nhưng `temperature` khác sẽ có khóa khác.
