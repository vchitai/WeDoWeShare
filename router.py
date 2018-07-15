# -*- coding: utf-8 -*-
import json

from flask import session, render_template, request, flash, abort, g, jsonify, url_for, redirect
import requests
from app import app, mongo
from models import jsonData, User, JSONEncoder, getUniversityIndex, getMajorIndex, convertResultToListOfList


@app.route("/")
def home():
    if not session.get('logged_in'):
        return login_get()
    else:
        return render_template('home.html', css_file=["home"], page_title=u"Trang chủ", )


@app.route("/index")
def index():
    return home()


@app.route('/login')
def login_get():
    return render_template('login.html', css_file=["login"], page_title=u"Đăng nhập")


@app.route('/signup')
def register_get():
    return render_template('register.html', css_file=["signup"], page_title=u"Đăng kí")

@app.route('/api/stupid-list-m')
def stupid_list_m():
    return jsonify(jsonData['stupid-list'])
@app.route('/api/stupid-list-u')
def stupid_list_u():
    return jsonify(jsonData['stupid-list-2'])
@app.route('/api/dummyUniversity')
def getDummyUniversity():
    return jsonify(jsonData['dummy-university'])


@app.route('/api/findMentor', methods=['POST'])
def findMentor():
    if not session.get('logged_in'):
        abort(404)
    truong = request.form['university']
    nganh = request.form['major']
    user = mongo.db.users.find_one({"username": session['logged_username']})
    if truong is None or nganh is None:
        truong = user.__dict__['university']
        nganh = user.__dict__['major']
        if truong is None or nganh is None:
            abort(404)
    vector = []
    vector.append(getUniversityIndex(truong)+1)
    vector.append(getMajorIndex(nganh)+1)
    vector.append(int(user['grade']))
    vector.append(int(user['price']))
    vector.append(int(user['studyAbroad']))
    vector.append(int(user['grade']))
    print vector
    #192.168.33.189, headers={'Content-type': 'multipart/form-data'}
    r = requests.post(url='http://192.168.33.189:5555/api/suggest', json={"vector":vector})

    return json.dumps(convertResultToListOfList(r.text))


@app.route('/api/linkToUniversityNoSymbol')
def getLinkToUniversityNoSymbol():
    return jsonify(jsonData['university-link'])


@app.route('/api/linkToUniversity')
def getLinkToListOfUniversity():
    return jsonify(jsonData['link-to-university'])


@app.route('/api/listOfUniversity')
def getListOfUniversity():
    return jsonify(jsonData['university'])


@app.route('/api/listOfFalcuty')
def getListOfFalcuty():
    return jsonify(jsonData['faculty'])


@app.route('/login', methods=['POST'])
def login_post():
    password = request.form['password']
    username = request.form['username']
    user = mongo.db.users.find_one({"username": username})
    user = User(user)
    if user is None:
        abort(404)
    print user.check_password(password)
    if user.check_password(password):
        session['logged_in'] = True
        session['logged_username'] = user.username
        return redirect(url_for("home"))
    else:
        flash(u'Mật khẩu sai')
        return login_get()


@app.route("/logout")
def logout():
    if not session.get('logged_in'):
        return login_get()
    session['logged_in'] = False
    return home()


@app.route("/inbox")
def inbox():
    if not session.get('logged_in'):
        return login_get()
    return render_template("inbox.html", page_title=u"Nhắn tin", css_file=["inbox", "alumni", "result"])


@app.route("/register", methods=['POST'])
def register():
    password = request.form['password']
    username = request.form['username']
    user = mongo.db.users.find_one({"username": username})
    if user is None:
        user = User(request.form)
        user.hash_password(password)
        user.commit()
        return login_get()
    else:
        flash(u"Người dùng đã tồn tại")
        return register_get()


majors_detail = {
    "majors": {
        "marketing": {
            "name": u"Ngành marketing",
            "description": u"Marketing là ngành giữ vai trò rất quan trọng trong hoạt động kinh doanh của hầu hết mọi tổ chức kinh doanh trên thế giới. Hiệu quả của hoạt động bán hàng chịu ảnh hưởng lớn từ marketing và nó còn chi phối cả hoạt động của doanh nghiệp trong hiện tại và tương lai.",
            "salary": u"~17.000 - 20.000 USD / năm",
            "employers": u"10.000 người / năm",
            "require": u"Các doanh nghiệp muốn bán được nhiều hàng hóa và sản phẩm thì một phần không thể thiếu chính là cách các nhà đầu tư đưa sản phẩm đến tay người tiêu dùng để có thể cạnh tranh với nhiều đối thủ. Vì vậy yêu cầu về một đội ngũ chuyên tiếp xúc với khách hàng, có những sáng tạo để tiêu thụ được sản phẩm là hết sức cần thiết.",
            "fileContest": ["A1", "D"]
        },
        "san-xuat-thuc-pham-va-do-uong": {
            "name": u"Ngành công nghệ thực phẩm",
            "description": u" Ngành công nghệ thực phẩm được đánh giá là ngành của tương lai vững vàng, ngành của sự tiềm năng. Đây là một trong những ngành học có tính ứng dụng cao và đa dạng, nhất là trong cuộc sống hiện đại.",
            "salary": u"~7.000 - 10.000 USD / năm",
            "employers": u"7.000 - 10.000 người / năm",
            "require": u"Không chỉ đáp ứng nhu cầu tiêu dùng trong nước mà ngành công nghệ thực phẩm còn hướng đến việc sản xuất, chế biến những sản phẩm đạt chất lượng cao để phục vụ nhu cầu xuất khẩu. Đây là một ngành học thực sự tiềm năng và cơ hội khá lớn cho vấn đề việc làm, đặc biệt là với những bạn nữ.",
            "fileContest": ["A", "B"]
        },
        "cong-nghe-thong-tin-cntt": {
            "name": u"Công nghệ thông tin",
            "description": u"Mạng xã hội đang bùng nổ trên toàn thế giới, các thiết bị điện tử ngày càng trở nên phổ biến. Ngành Công nghệ Thông tin ở Việt Nam tuy không còn quá lạ lẫm, nhưng mức độ phát triển của ngành này vẫn ít nhiều còn hạn chế. Theo thống kê của Viện Chiến lược thông tin và truyền thông, trong ngành này chỉ có khoảng 15% lượng sinh viên ra trường đáp ứng được nhu cầu doanh nghiệp.",
            "salary": u"~20.000 - 25.000 USD / năm",
            "employers": u"23.000 - 25.000 người / năm",
            "require": u"Những lập trình viên, những kỹ sư hệ thống mạng, kỹ sư phần cứng, thiết kế lập trình game, an ninh mạng, …",
            "fileContest": ["A", "A1"]
        },
        "du-lich-va-lu-hanh": {
            "name": u"Ngành du lịch, quản lý khách sạn",
            "description": u"Du lịch là một ngành kinh tế mũi nhọn ở Việt Nam. Đất nước Việt Nam có tiềm năng du lịch đa dạng và phong phú. Thị trường du lịch khách sạn nhà hàng tại Việt Nam đang phát triển một cách mạnh mẽ và nóng hơn bao giờ hết.",
            "salary": u"~10.000 - 15.000 USD / năm",
            "employers": u"3.000 - 4.000 người/năm",
            "require": u"Những lập trình viên, những kỹ sư hệ thống mạng, kỹ sư phần cứng, thiết kế lập trình game, an ninh mạng, …",
            "fileContest": ["A", "A1", "D"]
        },
        "quan-ly-giao-duc": {
            "name": u"Ngành giáo dục",
            "description": u"Có lẽ bạn sẽ hơi ngạc nhiên khi thấy ngành giáo dục- một ngành được đánh giá là dư nhân lực nhiều nhất trong mấy năm trở lại đây khi nó xuất hiện trong bảng xếp hạng này. Các nhà nghiên cứu dự đoán rằng trong tương lai gần, nhóm ngành giáo dục - đào tạo sẽ rất khát nguồn nhân lực trình độ cao.",
            "salary": u"~7.000 - 9.000 USD / năm",
            "employers": u"6.600 người/năm",
            "require": u"Theo dự báo, nhu cầu giáo viên các ngành sư phạm mầm non, sư phạm tiểu học (chủ yếu là giáo viên tiếng Anh) và nhân viên bảo mẫu... sẽ tăng mạnh trong vài ba năm tới vì toàn ngành giáo dục - đào tạo đang đẩy mạnh thực hiện đề án phổ cập giáo dục mầm non 5 tuổi, đồng thời hoàn tất việc chuyển đổi các trường mầm non bán công trên toàn quốc sang mô hình trường công lập, nên chắc chắn sẽ thu hút một số lượng lớn giáo viên đã được đào tạo bài bản.",
            "fileContest": ["A", "A1", "B", "C", "D"]
        }
    }
}


@app.route("/nganh/<nganh>")
def major_detail(nganh):
    if not session.get('logged_in'):
        return login_get()
    if nganh not in jsonData['map-faculty']:
        abort(404)
    dummy = majors_detail['majors']["cong-nghe-thong-tin-cntt"]
    return render_template("major-detail.html", page_title=jsonData['map-faculty'][nganh],
                           css_file=["major-detail", "major"],
                           nganh=jsonData['map-faculty'][nganh], nganh_root=nganh,
                           detail=majors_detail['majors']["cong-nghe-thong-tin-cntt"])


@app.route("/truong/<truong>")
def school_detail(truong):
    if not session.get('logged_in'):
        return login_get()
    found = False
    for x in jsonData['university-link']:
        if truong in x:
            found = True
            truongR = jsonData['university'][jsonData['university-link'].indexOf(truong)]
    if not found:
        abort(404)
    return render_template("uni-detail.html", page_title=truongR, css_file=["uni-detail"], truong=truongR,
                           truong_root=truong)


@app.route("/tim-truong")
def tim_truong():
    if not session.get('logged_in'):
        return login_get()
    nganh = request.args.get('nganh')
    if nganh is None:
        return render_template("major.html", css_file=["major"], page_title=u"Chọn ngành", )
    if nganh not in jsonData['map-faculty']:
        abort(404)
    return render_template("universities.html", page_title=u"Chọn trường",
                           css_file=["universities"], nganh=jsonData['map-faculty'][nganh], nganh_root=nganh, )


@app.route("/tim-nganh")
def tim_nganh():
    if not session.get('logged_in'):
        return login_get()
    nganh = request.args.get('nganh')
    if nganh is None:
        return render_template("major.html", css_file=["major"], page_title=u"Chọn ngành")
    truong = request.args.get('truong')
    found = False
    for x in jsonData['university-link']:
        if truong in jsonData['university-link'][x]:
            found = True
            truongR = jsonData['university'][x][jsonData['university-link'][x].index(truong)]
    if not found:
        return render_template("universities.html", page_title=u"Chọn trường", css_file=["university"],
                               nganh_root=nganh)
    return render_template("result.html", page_title=u"Tư vấn viên", css_file=["result", "alumni"], truong=truongR,
                           nganh=jsonData['map-faculty'][nganh], truong_root=truong, nganh_root=nganh)


@app.route("/account")
def account_info():
    if not session.get('logged_in'):
        return login_get()
    return render_template("account-info.html", page_title=u"Tài khoản", css_file=["signup"])
