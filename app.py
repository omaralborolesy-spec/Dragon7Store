import streamlit as st
import json
import os
import base64
import urllib.parse

st.set_page_config(
    page_title="Dragon Store - متجر الأناقة الأسطورية",
    page_icon="🐉",
    layout="wide"
)

def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

lamp_base64 = get_image_base64("lamp_isolated.png")
logo_base64 = get_image_base64("logo.png")

if "login_state" not in st.session_state:
    st.session_state.login_state = "normal"
if "support_messages" not in st.session_state:
    st.session_state.support_messages = {}

st.markdown(
    f"""
    <!-- استدعاء مكتبة model-viewer لعرض الـ 3D الحقيقي والتفاعلي -->
    <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>

    <style>
    .stApp {{
        background: linear-gradient(135deg, #070a09 0%, #0d1411 50%, #111e19 100%);
        color: #ffffff;
        font-family: 'Cairo', sans-serif;
    }}
    
    .top-left-container {{
        position: fixed;
        top: 20px;
        left: 30px;
        z-index: 999;
        display: flex;
        align-items: center;
        gap: 15px;
    }}

    .store-logo img {{
        width: 65px;
        height: 65px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #00ff88;
        box-shadow: 0 0 20px rgba(0, 255, 128, 0.8);
        background: rgba(0,0,0,0.5);
    }}

    .top-left-lamp {{
        animation: lampEntranceShake 1.4s cubic-bezier(0.36, 0.07, 0.19, 0.97) forwards, lampGlowEffect 2s ease-in-out infinite alternate;
    }}
    .top-left-lamp img {{
        width: 120px;
        height: auto;
        background: transparent !important;
        mix-blend-mode: screen;
        filter: drop-shadow(0 0 40px #00ff88) drop-shadow(0 0 70px rgba(0,255,136,0.6));
    }}

    @keyframes lampEntranceShake {{
        0% {{ opacity: 0; transform: translateY(-40px) scale(0.7); }}
        20% {{ opacity: 1; transform: translateY(10px) rotate(-12deg) scale(1.15); }}
        40% {{ transform: translateY(-8px) rotate(10deg) scale(0.9); }}
        60% {{ transform: translateY(5px) rotate(-6deg) scale(1.05); }}
        100% {{ opacity: 1; transform: translateY(0) rotate(0deg) scale(1); }}
    }}

    @keyframes lampGlowEffect {{
        0% {{ filter: drop-shadow(0 0 25px #00ff88); transform: scale(1); }}
        100% {{ filter: drop-shadow(0 0 50px #00ff88); transform: scale(1.03); }}
    }}

    .login-right-container {{
        display: flex;
        justify-content: flex-end;
        align-items: center;
        min-height: 80vh;
        padding-right: 50px;
    }}

    .login-box {{
        background: rgba(12, 20, 17, 0.92);
        border: 1px solid rgba(0, 255, 128, 0.4);
        border-radius: 20px;
        padding: 30px 40px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.95), 0 0 30px rgba(0, 255, 128, 0.2);
        width: 440px;
        text-align: right;
        backdrop-filter: blur(12px);
    }}

    /* حاوية عنصر الـ 3D الحقيقي في أسفل الشاشة */
    .robot-3d-container {{
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        width: 160px;
        height: 160px;
        z-index: 999;
        background: transparent;
        pointer-events: auto;
        filter: drop-shadow(0 0 25px rgba(0, 255, 128, 0.8));
    }}

    .stTextInput label {{
        color: #00ff88 !important;
        text-align: right !important;
        direction: rtl !important;
        font-weight: bold;
    }}

    .stButton button {{
        background: linear-gradient(90deg, #00ff88, #00cc66) !important;
        color: #0b0f0e !important;
        border: 2px solid #00ff88 !important;
        border-radius: 12px;
        font-weight: bold;
        font-size: 17px;
        width: 100%;
        padding: 12px;
        box-shadow: 0 0 25px rgba(0, 255, 136, 0.7);
        transition: all 0.3s ease;
    }}
    
    .stButton button:hover {{
        background: linear-gradient(90deg, #00ffaa, #00ff88) !important;
        box-shadow: 0 0 35px rgba(0, 255, 136, 1);
        transform: translateY(-2px);
    }}

    .sidebar-logo img {{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #00ff88;
        vertical-align: middle;
        margin-left: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "cart" not in st.session_state:
    st.session_state.cart = []

ORDERS_FILE = "orders_db.json"
PRODUCTS_FILE = "products_db.json"

def load_json(file_path, default_val):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default_val
    return default_val

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

orders_db = load_json(ORDERS_FILE, {})
products_db = load_json(PRODUCTS_FILE, {})

if not st.session_state.logged_in:
    top_left_html = '<div class="top-left-container">'
    if logo_base64:
        top_left_html += f'<div class="store-logo"><img src="data:image/png;base64,{logo_base64}" alt="Logo"></div>'
    if lamp_base64:
        top_left_html += f'<div class="top-left-lamp"><img src="data:image/png;base64,{lamp_base64}" alt="Lamp"></div>'
    top_left_html += '</div>'
    
    st.markdown(top_left_html, unsafe_allow_html=True)
    
    # نموذج الـ 3D الحقيقي شغال أوتوماتيك وجاهز بالتفاعل التام
    st.markdown(
        """
        <div class="robot-3d-container">
            <model-viewer 
                src="https://modelviewer.dev/shared-assets/models/RobotExpressive.glb" 
                alt="3D Robot" 
                auto-rotate 
                camera-controls 
                disable-zoom
                style="width: 100%; height: 100%; background-color: transparent;">
            </model-viewer>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="login-right-container"><div class="login-box">', unsafe_allow_html=True)
    st.markdown("<h2 style='color: #ffffff; margin-bottom: 2px; text-align: right;'>مرحباً بعودتك.</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00ff88; font-size: 13px; margin-bottom: 20px; text-align: right;'>أنر طريقك مع متجر التنين</p>", unsafe_allow_html=True)
    
    with st.form("video_login_form"):
        user_input = st.text_input("اسم المستخدم", placeholder="ادخل اسم المستخدم (أو admin)...")
        pass_input = st.text_input("كلمة المرور", type="password", placeholder="ادخل كلمة المرور...")
        
        submit_btn = st.form_submit_button("تسجيل الدخول ➔")
        
        if submit_btn:
            if user_input.strip() == "":
                st.warning("الرجاء إدخال اسم المستخدم.")
                st.rerun()
            elif user_input.strip().lower() == "admin" and pass_input == "admin123":
                st.session_state.logged_in = True
                st.session_state.username = "المسؤول (Admin)"
                st.session_state.is_admin = True
                st.success("تم تسجيل دخول الأدمن بنجاح! 🛠️")
                st.rerun()
            elif user_input.strip().lower() != "admin" and pass_input == "12345":
                st.session_state.logged_in = True
                st.session_state.username = user_input
                st.session_state.is_admin = False
                st.success("تم تسجيل الدخول بنجاح! 🚀")
                st.rerun()
            else:
                st.error("خطأ في اسم المستخدم أو كلمة المرور!")
                st.rerun()
                
    st.markdown('</div></div>', unsafe_allow_html=True)

else:
    if logo_base64:
        st.sidebar.markdown(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 20px; border-bottom: 1px solid rgba(0,255,128,0.2); padding-bottom: 15px;">
                <div class="sidebar-logo"><img src="data:image/png;base64,{logo_base64}" alt="Logo"></div>
                <div>
                    <h3 style="color: #00ff88; margin: 0; font-size: 18px;">Dragon Store</h3>
                    <p style="color: #bbb; margin: 0; font-size: 12px;">أهلاً، {st.session_state.username}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    if st.sidebar.button("تسجيل الخروج 🚪"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.is_admin = False
        st.session_state.cart = []
        st.rerun()
        
    menu_options = ["الرئيسية والمتجر 🛒", "سلة الشراء والفاتورة 🛍️", "تتبع الطلب 📦", "الدعم الفني 🎧"]
    if st.session_state.is_admin:
        menu_options.append("لوحة الأدمن 🛠️")
        
    page = st.sidebar.radio("الانتقال إلى:", menu_options)

    if page == "الرئيسية والمتجر 🛒":
        st.title("🐉 متجر الأناقة الأسطورية - Dragon Store")
        st.write(f"مرحباً بك يا **{st.session_state.username}**! تصفح المنتجات وأضفها لسلة الشراء:")
        
        if not products_db:
            st.info("📦 الكتالوج فارغ حالياً.")
        else:
            cols = st.columns(2)
            for i, (p_id, p_info) in enumerate(products_db.items()):
                with cols[i % 2]:
                    stock_qty = p_info.get('qty', 10)
                    st.markdown(
                        f"""
                        <div style="background: rgba(19, 28, 24, 0.85); border: 1px solid rgba(0, 255, 128, 0.3); border-radius: 15px; padding: 20px; margin-bottom: 20px;">
                            <h3 style="color: #00ff88; margin-top: 0;">{p_info.get('name')}</h3>
                            <p><b>السعر:</b> {p_info.get('price')} ج.م</p>
                            <p><b>الكمية المتاحة:</b> {stock_qty} قطعة</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    if stock_qty > 0:
                        if st.button(f"إضافة للسلة 🛒", key=f"add_{p_id}"):
                            st.session_state.cart.append(p_info)
                            st.success(f"تم إضافة {p_info.get('name')} للسلة!")
                    else:
                        st.error("نفذت الكمية ❌")

    elif page == "سلة الشراء والفاتورة 🛍️":
        st.title("🧾 الفاتورة والدفع")
        if not st.session_state.cart:
            st.warning("سلة الشراء فارغة حالياً!")
        else:
            total_price = 0
            items_summary = ""
            for idx, item in enumerate(st.session_state.cart):
                st.write(f"{idx+1}. **{item['name']}** - {item['price']} ج.م")
                total_price += item['price']
                items_summary += f"- {item['name']} ({item['price']} ج.م)\n"
            st.markdown(f"### 💰 الإجمالي: **{total_price} ج.م**")
            
            cust_name = st.text_input("اسم العميل بالكامل", value=st.session_state.username)
            cust_phone = st.text_input("رقم الهاتف للتواصل")
            cust_address = st.text_area("عنوان التوصيل بالتفصيل")
            
            if st.button("إتمام الطلب وإرسال الفاتورة عبر الواتساب 📲"):
                if not cust_phone or not cust_address:
                    st.error("الرجاء إدخال رقم الهاتف والعنوان.")
                else:
                    order_id = f"ORD-{len(orders_db) + 1001}"
                    orders_db[order_id] = {
                        "name": cust_name, "phone": cust_phone, "address": cust_address,
                        "total": total_price, "items": items_summary, "status": "قيد المعالجة ⏳"
                    }
                    save_json(ORDERS_FILE, orders_db)
                    invoice_text = f"🐉 *فاتورة جديدة*\n*رقم الطلب:* {order_id}\n*العميل:* {cust_name}\n*الهاتف:* {cust_phone}\n*الإجمالي:* {total_price} ج.م"
                    whatsapp_url = f"https://wa.me/201558478544?text={urllib.parse.quote(invoice_text)}"
                    st.success(f"✅ تم تسجيل الطلب! رقمك: {order_id}")
                    st.markdown(f"[اضغط هنا لإرسال الفاتورة للواتساب 📲]({whatsapp_url})")
                    st.session_state.cart = []

    elif page == "تتبع الطلب 📦":
        st.markdown("## 📦 تتبع حالة طلبك")
        search_query = st.text_input("🔍 أدخل رقم الطلب أو الهاتف:")
        if st.button("بحث 🚀"):
            found = False
            for order_id, details in orders_db.items():
                if search_query.strip() == order_id or search_query.strip() == details.get("phone"):
                    found = True
                    st.success(f"📌 **رقم الطلب:** {order_id} | **الحالة:** {details.get('status')}")
            if not found and search_query.strip():
                st.error("❌ لم يتم العثور على طلب.")

    elif page == "الدعم الفني 🎧":
        st.markdown("## 🎧 مركز الدعم الفني")
        user_key = st.session_state.username
        if user_key not in st.session_state.support_messages:
            st.session_state.support_messages[user_key] = []
            
        with st.form(f"support_form_{user_key}"):
            sup_name = st.text_input("اسمك ", value=st.session_state.username)
            sup_issue_no = st.text_input("رقم المشكلة أو الطلب")
            sup_desc = st.text_area("تفاصيل المشكلة")
            if st.button("إرسال للدعم عبر الواتساب 📲"):
                if sup_desc.strip():
                    msg = f"🎧 *دعم فني*\n*العميل:* {sup_name}\n*التفاصيل:* {sup_desc}"
                    w_url = f"https://wa.me/201558478544?text={urllib.parse.quote(msg)}"
                    st.success("✅ تم التسجيل!")
                    st.markdown(f"[اضغط للإرسال عبر الواتساب 📲]({w_url})")

    elif page == "لوحة الأدمن 🛠️" and st.session_state.is_admin:
        st.title("🛠️ لوحة تحكم الأدمن")
        p_name = st.text_input("اسم المنتج")
        p_price = st.number_input("السعر", value=100.0)
        p_qty = st.number_input("الكمية", value=10, step=1)
        if st.button("حفظ المنتج"):
            if p_name:
                p_id = str(len(products_db) + 1001)
                products_db[p_id] = {"name": p_name, "price": p_price, "qty": p_qty}
                save_json(PRODUCTS_FILE, products_db)
                st.success("تمت الإضافة!")
                st.rerun()