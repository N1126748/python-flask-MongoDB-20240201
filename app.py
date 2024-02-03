# 初始化資料庫連線
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
uri = "mongodb+srv://root:root123@mycluster.bxxz9hg.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client.member_system

# 初始化 Flask 伺服器
from flask import *
app = Flask(
    __name__,
    static_folder="public", 
    static_url_path="/" 
)
app.secret_key = "any string but secret"

# 登入路由
@app.route("/login")
def login():
    return render_template("login.html")

# 登入錯誤路由
@app.route("/login_error")
def login_():
    return render_template("login.html", error="帳號或密碼錯誤，請重新輸入!")

# 註冊路由
@app.route("/register")
def register():
    return render_template("register.html")

# 註冊錯誤路由
@app.route("/register_error")
def register_error():
    return render_template("register.html", error="帳號或電子郵件已註冊過，請重新輸入!")

# (需會員)
@app.route("/index")
def index():
    if "account" in session:
        return render_template("index.html")
    return redirect("/login")

# 電商首頁
@app.route("/")
def home():
   return render_template("home.html")

# 註冊
@app.route("/signup", methods=["POST"]) 
def signup():
    # 從前端接收資料
    address = request.form["address"]
    nickname = request.form["nickname"]
    email = request.form["email"]
    account = request.form["account"]
    password = request.form["password"]
    phone = request.form["phone"]
    # 根據接收到的資料 處理資料庫
    collection = db.user

    # 檢查是否有相同資料
    result = collection.find_one({
        "$and":[
            {"account":account},
            {"email":email}
        ]
    })
    if result != None:
        return redirect("/register_error")
    
    # 把資料放進資料庫
    collection.insert_one({
        "address":address,
        "nickname":nickname,
        "email":email,
        "account":account,
        "password":password,
        "phone" :phone
    })
    return redirect("/login")

# 登入
@app.route("/signin", methods=["POST"]) 
def signin():
    # 從前端取得使用者輸入
    account = request.form["account"]
    password = request.form["password"]
    # 和資料庫做互動
    collection = db.user
    result = collection.find_one({
        "$and":[
            {"account":account},
            {"password":password}
        ]
    })
    if request.form['button'] == 'login':
        # 找不到資料 導回錯誤登入頁面
        if result == "":
            return redirect("/login_error")
        if result == None:
            return redirect("/login_error")
        # 登入成功 在session 記錄會員資訊導向首頁
        session["email"] = result["email"]
        return redirect("/")
    
    if request.form['button'] == 'register':
        return redirect("/register")
    
# 登出
@app.route("/signout")
def signout():
    # 移除 session 中的會員資訊
    del session["account"]
    return redirect("/login")










app.run(port=3000)





























