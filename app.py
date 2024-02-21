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

# 電商首頁
@app.route("/")
def home():
   if "email" in session:
        state = None
        return render_template("home.html", state=state)
   return render_template("home.html")

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

# 購物車(需會員)
@app.route("/cart")
def index():
    if "email" in session:
        collection = db.user
        email = session["email"]
        cartInfo = collection.find_one({
            "email":email
        })
        
        Pants = 0
        sweater = 0
        coat = 0
        shoes = 0
        
        if 'Pants' in cartInfo:
            for size in ['S','M','L','XL']:
                if size in cartInfo['Pants']:
                    Pants += cartInfo['Pants'][size][0]

        if 'sweater' in cartInfo:          
            for size in ['S','M','L','XL']:
                if size in cartInfo['sweater']:
                    sweater += cartInfo['sweater'][size][0]

        if 'coat' in cartInfo:          
            for size in ['S','M','L','XL']:
                if size in cartInfo['coat']:
                    coat += cartInfo['coat'][size][0]

        if 'shoes' in cartInfo:
            for size in ['US-9','US-10','US-11','US-12']:
                if size in cartInfo['shoes']:
                    shoes += cartInfo['shoes'][size][0]
                    
        total = Pants + sweater + coat + shoes
        if total == 0:
            return render_template("cart.html", cartInfo=cartInfo)
        elif total > 0:
            return render_template("cart.html", cartInfo=cartInfo, total=total)
            
    return redirect("/login")

# 新增至購物車
@app.route("/update/<Prodact>/<size>/<price>/<quantity>", methods=["POST"])
def update(Prodact, size, price, quantity):
    if "email" in session:

        size_ = request.form[size]
        price_ = int(request.form[price])
        quantity_ = int(request.form[quantity])
        total = price_ * quantity_

        key_to_update = Prodact + '.' + size_
        new_value = [total, quantity_]

        collection = db.user
        collection.update_one({
            "email":session["email"]
        }, {
            "$set":{
                key_to_update: new_value
            }
        })
        #偵測是否登入會員,這兩個 jsonify 語句用於將成功或失敗的訊息以 JSON 格式回傳給前端
        return jsonify({"success": True})

    else:
        return jsonify({"error": "請先登入會員"})

# 刪除商品
@app.route("/clear/<Prodact>/<size>")
def clear(Prodact, size):
    key_to_update = Prodact + '.' + size
    collection = db.user
    collection.update_one({
        "email":session["email"]
        }, {
            "$unset":{
                key_to_update:''
            }
        })
    
    cartInfo = collection.find_one({
            "email":session["email"]
        })
    
    if cartInfo[Prodact] == {}:
        collection.update_one({
                "email":session["email"]
                }, {
                    "$unset":{
                        Prodact:''
                    }
                })
        return redirect("/cart")
    return redirect("/cart")

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
        "$or":[
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
    del session["email"]
    return redirect("/")






app.run(port=3000)





























