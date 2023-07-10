description = """
Bài tập lớn môn **Lập trình python**
## Thành viên nhóm
* **A39482 Nguyễn Ngọc Anh**
* **A38303 Phùng Thị Diệu Linh**
* **A38207 Nguyễn Thị Lan**
* **A37672 Trần Hoàng Anh** (_Trưởng nhóm_).
"""
tags_metadata = [
    {
        "name" : "Trang chủ",
        "description" : "Hiển thị thông tin của nhóm và thông tin thành viên"
    }, 
    {
        "name" : " Ngọc Anh Numpy", 
        "description" : "Cập nhập thông tin Lương tháng và lấy lương tổng kết tháng của một nhân viên"
    }, 
    {
        "name" : " Ngọc Anh Pandas",
        "description" : "Thống kê Lương tháng của từng nhân viên theo mã dự án tham gia và Tìm kiếm thông tin nhân viên"
    },
    {
        'name' : 'Hoàng Anh Pandas',
        "description": 'Hiển thị bảng lương của nhân viên theo mã nhân viên và Cập nhập mã dự án tham gia (thêm/xóa nhân viên khỏi một dự án)'
    },
    {
        'name' : 'Hoàng Anh Numpy', 
        "description": 'Hiển thị lương tháng trung bình của nhân viên theo mã dự án và Hiển thị tổng lương 2 dự án của nhân viên theo mã dự án tham gia và mã nhân viên (điều kiện: nhân viên tham gia >= 2 dự án)'
    },
    {
        'name' : 'Linh Numpy',
        'description': 'Các API ứng dụng Numpy'
    },
    {
        'name' : 'Linh Pandas',
        'description': 'Các API ứng dụng Pandas'
    },
    {
        'name' : 'Lan Numpy',
        'description' : 'Hiển thị trạng thái của dự án (hoàn thành hay chưa hoàn thành và Lấy số lượng người tham gia dự án theo mã dự án'
    },
    {
        'name' : 'Lan Pandas',
        'description' : 'Lấy thông tin nhân viên có đánh giá năng lực cao nhất (=5) và thấp nhất (=1) trong dự án và Tổng số dự án đã hoàn thành theo mã dự án'
    }
]

descriptionApi = {
    "NgocAnhPd": { 
        "ThongKeLuongThuongThang" : "Nhập mã dự án để nhận lại thông tin trả về là 1 bảng lương thưởng của từng dự án. projectid mang giá trị số nguyên dương",
        "TimKiemNhanVien": "Nhập một trong các thông tin cá nhân của nhân viên để nhận lại thông tin của bảng chứa các thông tin cần tìm"
    },
    "NgocAnhNp" : {
        "LuongTongKetThangCuaNhanVien": "Nhập mã nhân viên để nhận lại tổng lương tháng của nhân viên(Tổng lương của tất cả các dự án đã tham gia)",
        "CapNhatLuongTheoThang": "Nhập các thông tin: employeeid, projectid, lương cứng, lương tham gia dự án sau đó sẽ tự động cập nhật thông tin của nhân viên ở mã dự án đó trong cơ sở dữ liệu"
    },
    'LinhNP' : {
        'BangXepHang' : 'Hiện bảng xếp hạng lương tháng của nhân viên và đánh giá năng lực tương ứng',
        'CapNhatDanhGiaNhanVien' : 'Nhập các thông tin: employeeid, rate (muốn cập nhật) sau đó sẽ tự động cập nhật thông tin đánh giá của nhân viên trong cơ sở dữ liệu'
    },
    'LinhPD' : {
        'DanhSachNhanVienTop' : 'Hiển thị top 10 những nhân viên có lương tháng cao nhất trong tháng',
        'LuongTrungBinhPhongBan' : 'Nhập mã phòng ban để có thể xem trung bình lương theo mã phòng ban'
    },
    'HoangAnhPandas': {
        'LuongCuaNhanVien': 'Nhập mã nhân viên để có thể xem bảng lương của nhân viên đó',
        'CapNhatMaDuAn': 'Cho phép người dùng đổi mã dự án, đổi nhân viên tham gia dự án theo projectid'
    },
    'HoangAnhNumpy':{
        'LuongTrungBinhDuAn': 'Nhập mã dự án để có thể xem được lương tháng trung bình của dự án',
        'TongHaiDuAn': 'Nhập mã nhân viên, mã của 2 dự án thì sẽ trả về tổng luong của nhân viên đấy'
    },
    'LanNumpy':{
        'TrangThaiDuAn' : 'Nhập trạng thái dự án (hoàn thành hoặc chưa hoàn thành) để hiển ra thông tin của dự án theo trạng thái đấy',
        'SoLuongNguoiThamGia' : 'Nhập mã dự án để xem số lượng người tham gia dụ án là bao nhiêu'
    },
    'LanPandas':{
        'ThongTinNVLuongCaoVaThapNhat' : 'Nhập mã dự án để xem thông tin nhân viên có đánh giá năng lực cao nhất và thấp nhất của dự án đó',
        'TongSoDuAnHoanThanh' : 'Thống kê tổng dự án đã hoàn thành'
    }
}