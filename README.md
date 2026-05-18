# Các bước demo dự án
## Bước 1: Export môi trường ESP-IDF
- & 'c:\Users\THANH\.vscode\extensions\espressif.esp-idf-extension-2.0.2\export.ps1'
## Bước 2:
- chạy lệnh python run_test.py 
- Sau đó nhập model muốn update: VD Lenet 300-100 từ 3 lên version 6 thì sẽ nhập 30036
- Khi monitor đã return -> bấm CTR + "]" để tiếp tục

# Quy trình Test: Build, flash và monitor lần lượt 3 project Flash_Model, Q_HUFDEL và Check_Model
- Ghi model cũ (là model lenet 300-100_3 với input là 30036) vào flash bằng project `Flash_Model`.
- Dùng Q_HUFDEF để update model trong flash từ file bin trong sdcard
- Check model mới ở trong flash bằng project `Check_Model`

# Specific 
- Model được cấp phát 300 000 bytes ở phân vùng model (flash được chia phân vùng theo file partiotions.csv)
- Model update trước được ghi vào flash được lưu tạm ở trong vùng PSRAM

# Valid model update: 
- 513
- 536
- 547
- 568
- 569
- 579
- 5710
- 5910
- 30013
- 30015
- 30047
- 30068
- 30069
- 300610
- 300710