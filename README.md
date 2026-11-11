# My Weather App

`My Weather App` là script Python nhỏ dùng để lấy dự báo **nhiệt độ theo giờ tại Hà Nội** từ API [Open-Meteo](https://open-meteo.com/), rồi lưu vào CSV. Mỗi lần chạy, ứng dụng chỉ thêm các bản ghi có cặp **thời điểm dự báo + nhiệt độ** chưa xuất hiện trong dữ liệu lịch sử.

## Yêu cầu

- Python 3
- Thư viện `requests`
- Kết nối Internet để gọi Open-Meteo

## Cài đặt và chạy

Từ thư mục gốc của dự án, cài dependency và chạy script:

```powershell
pip install requests
python code/get_data.py
```

Script dùng tọa độ Hà Nội (`21.0245`, `105.8412`) và gửi timezone `Asia/Singapore` cho API.

## Data flow

```text
Tọa độ Hà Nội + timezone
          |
          v
code/get_data.py
          |
          | gọi get_api(lat, lon, timezone)
          v
code/get_api.py
          |
          | HTTP GET /v1/forecast?hourly=temperature_2m
          v
Open-Meteo API
          |
          | JSON: hourly.time, hourly.temperature_2m
          v
csv/nomatch.csv
          |
          | so sánh (datetime, temperature)
          v
csv/weather.csv
          |
          v
Làm trống csv/nomatch.csv
```

Chi tiết xử lý:

1. `get_api.py` tạo URL Open-Meteo và gọi API bằng `requests.get()`.
2. Khi nhận HTTP `200`, API trả JSON chứa mảng thời điểm (`hourly.time`) và nhiệt độ (`hourly.temperature_2m`).
3. `get_data.py` ghép hai mảng theo chỉ số, thêm thời điểm ghi hiện tại và ghi các dòng vào `csv/nomatch.csv`.
4. Các khóa `(datetime, temperature)` trong file tạm được đối chiếu với `csv/weather.csv`.
5. Chỉ các dòng chưa tồn tại được nối vào file lịch sử; sau đó file tạm bị làm trống.

## Dữ liệu đầu ra

`csv/weather.csv` tự được tạo header khi đang rỗng:

```csv
datetime,temperature,write at
2026-11-11T00:00,16.8,2026-11-11 17:03:34.889131
```

| Cột | Ý nghĩa |
| --- | --- |
| `datetime` | Thời điểm dự báo theo giờ do Open-Meteo trả về. |
| `temperature` | Nhiệt độ ở độ cao 2 m (`temperature_2m`). |
| `write at` | Thời điểm script ghi bản ghi vào file tạm/lịch sử. |

`csv/nomatch.csv` là vùng đệm cho một lượt chạy. Nội dung của file này được ghi đè trước khi đối chiếu và bị làm trống khi hoàn tất.

## Cấu trúc thư mục

```text
My Weather App/
├── README.md                 # Tài liệu dự án
├── code/
│   ├── get_api.py            # Xây dựng request và lấy JSON từ Open-Meteo
│   └── get_data.py           # Ghi/đối chiếu dữ liệu CSV, tránh trùng lặp
└── csv/
    ├── weather.csv           # Lịch sử dự báo đã lưu
    └── nomatch.csv           # Dữ liệu tạm trong quá trình đồng bộ
```

## Lưu ý

- Việc lọc trùng dựa trên cả `datetime` và `temperature`; nếu nhiệt độ dự báo tại cùng thời điểm thay đổi, dòng mới sẽ vẫn được lưu.
- `get_data.py` đang giả định phản hồi API hợp lệ có trường `hourly`. Nếu API lỗi hoặc thay đổi cấu trúc phản hồi, script có thể phát sinh lỗi khi đọc dữ liệu.
- Với HTTP `400`, `get_api()` in URL đang dùng và trả về chuỗi `"Wrong url"`; với các mã lỗi khác, hàm trả về mã trạng thái HTTP.
