import streamlit as st
import pandas as pd
import os
import json
import random
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px

# ================= 1. Apple Pro 视觉引擎 (极致响应式) =================
st.set_page_config(page_title="肆叁叁月季起名社", page_icon="💐", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&family=Inter:wght@400;600&display=swap');
    
    /* 全局背景 */
    .stApp { 
        background-color: #F5F5F7 !important; 
        background-image: radial-gradient(circle at 50% 20%, #FFFFFF 0%, #E2E2E7 100%) !important;
        color: #000000 !important; 
    }
    
    /* 标题区 */
    .header-box { padding-top: 40px; padding-bottom: 10px; text-align: center; }
    .artistic-title { font-family: 'Noto Serif SC', serif; font-size: 52px; font-weight: 900; color: #000000 !important; letter-spacing: 12px; }

    /* 气泡导航容器 */
    .bubble-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin-bottom: 25px; }

    /* 基础气泡按钮 */
    div.stButton > button {
        border-radius: 99px !important;
        padding: 4px 16px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        border: 1px solid #D2D2D7 !important;
        transition: all 0.2s ease;
        background-color: #FFFFFF !important;
        color: #1D1D1F !important;
        width: 100%;
    }

    /* 选中状态：蓝色 */
    .selected-bubble button {
        background-color: #0071E3 !important;
        color: #FFFFFF !important;
        border-color: #0071E3 !important;
    }
    .selected-bubble button p, .selected-bubble button span { color: #FFFFFF !important; }

    /* 已投票状态：绿色 */
    .voted-bubble button {
        background-color: #34C759 !important;
        color: #FFFFFF !important;
        border-color: #34C759 !important;
    }
    .voted-bubble button p, .voted-bubble button span { color: #FFFFFF !important; }

    /* 投票主按钮容器 (强制白字) */
    .vote-btn-wrap button {
        background-color: #0071E3 !important;
        color: #FFFFFF !important;
        border: none !important;
        height: 50px;
        font-weight: 600 !important;
    }
    .vote-btn-wrap button p, .vote-btn-wrap button span, .vote-btn-wrap button * {
        color: #FFFFFF !important;
    }

    /* 品种档案排版 */
    .id-title { font-size: 42px; font-weight: 900; color: #000000 !important; margin-top: -10px !important; line-height: 1 !important; }
    .desc-box { color: #1D1D1F !important; font-size: 15px; line-height: 1.8 !important; text-align: justify; margin-top: 20px !important; }

    /* 投票列表项 */
    .vote-item {
        background: #FFFFFF !important; border-radius: 20px !important;
        padding: 15px 20px !important; border: 1px solid #E5E5E7 !important;
        margin-bottom: 10px !important;
    }

    /* 固定页脚 */
    .fixed-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: rgba(245, 245, 247, 0.95); text-align: center; padding: 15px 0;
        border-top: 1px solid #D2D2D7; color: #86868B !important; font-size: 12px; z-index: 1000;
    }
    header, footer, [data-testid="stHeader"] { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ================= 2. 数据与逻辑 =================
DATA_FILE = "vote_data.json"
ADMIN_PWD = "433admin"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f: json.dump(data, f, ensure_ascii=False, indent=4)

if 'db_data' not in st.session_state: st.session_state.db_data = load_data()
if 'selected_id' not in st.session_state: st.session_state.selected_id = "cy24027"

# --- 全量 17 个品种数据 ---
varieties = [
    {"id": "cy24027", "desc": "极具质感的深红至黑红色，花瓣厚度极高，带有丝绒般的光泽。花型为深杯状。", "candidates": ["中农丹赫 ", "中农绛阙", "中农丹墨", "中农绯重", "中农绛肃", "中农朱极"], "image": "cy24027.jpg"},
    {"id": "cy24057", "desc": "花型标准的代表，花瓣排列整齐划一，纯正中国红，商业标准红月季的定海神针。", "candidates": ["中农丹赫 ", "中农丹正", "中农绛枢", "中农朱律", "中农绯典", "中农丹楷"], "image": "cy24057.jpg"},
    {"id": "cy24065", "desc": "植株高大强壮。螺旋花心宽大舒展，给人一种盛大、热烈的视觉冲击力。", "candidates": ["中农丹赫 ", "中农丹弘", "中农绯钜", "中农朱硕", "中农绛巍", "中农丹骜"], "image": "cy24065.jpg"},
    {"id": "cy24001", "desc": "色调明快，偏朱红带橙调。花瓣质地硬挺，开放姿态轻盈跳跃，如同跳动的火光。", "candidates": ["中农烨煌 ", "中农烨炽", "中农烁阳", "中农曦照", "中农烨焱", "中农朝蔚"], "image": "cy24001.jpg"},
    {"id": "cy24051", "desc": "颜色更红、更纯。特异性在于色彩穿透力极强，即便在远距离也如灯火般辉煌夺目。", "candidates": ["中农烨煌 ", "中农烨透", "中农烁曜", "中农曦朗", "中农烨纯", "中农烁熠"], "image": "cy24051.jpg"},
    {"id": "cy24005", "desc": "短枝型。花苞呈现完美的圆球形，就像一颗宝珠。配合温暖橙红，形态受宠可爱。", "candidates": ["中农烁珠 ", "中农曦丸", "中农烁圆", "中农烨铃", "中农曦果", "中农烁玲"], "image": "cy24005.jpg"},
    {"id": "cy24045", "desc": "巨大花冠，花瓣边缘有显著波浪状褶皱。如同海面掀起巨澜，是对边缘波浪最直观的写照。", "candidates": ["中农沁澜 ", "中农沁涛", "中农嫣漪", "中农脂涌", "中农沁褶", "中农嫣裳"], "image": "cy24045.jpg"},
    {"id": "cy24060", "desc": "亮粉色，冲击力极强。外层花瓣向后翻，中心高耸，呈现高心翘角，气宇轩昂。", "candidates": ["中农嫣昂 ", "中农嫣傲", "中农沁翘", "中农嫣凌", "中农沁扬", "中农嫣耸"], "image": "cy24060.jpg"},
    {"id": "cy24063", "desc": "标准高心卷边状，花瓣质地厚实如丝绒。螺旋紧致包裹，勾勒出锐利的侧影。", "candidates": ["中农绛芒 ", "中农绛剑", "中农丹锐", "中农朱矢", "中农绯厉", "中农绛戟"], "image": "cy24063.jpg"},
    {"id": "cy24080", "desc": "显著特异性：花朵中心雄蕊瓣化，形成异色“草心”。如红妆美人的眼眸。", "candidates": ["中农朱瞳 ", "中农绛眸", "中农丹睛", "中农朱芯", "中农绯目", "中农绛凝"], "image": "cy24080.jpg"},
    {"id": "cy24086", "desc": "古典四分莲座状，花瓣数量极多。橙粉复色交织如华丽织锦，尽显富丽堂皇。", "candidates": ["中农烁锦 ", "中农曦织", "中农烁绣", "中农烨繁", "中农曦缬", "中农烁层"], "image": "cy24086.jpg"},
    {"id": "cy24044", "desc": "长势弱，花色柔和奶白。姿态轻柔、如梦似幻。风吹即动，适合文艺清新风格。", "candidates": ["中农瑶影 ", "中农素柔", "中农净怯", "中农瑶梦", "中农素纱", "中农净婉"], "image": "cy24044.jpg"},
    {"id": "cy24046", "desc": "侧芽萌发力强。花瓣呈角状翻卷，形态像飞鸟羽毛，带有一种向上的动态意象。", "candidates": ["中农净翎 ", "中农素羽", "中农净翔", "中农瑶鹤", "中农素箭", "中农净翼"], "image": "cy24046.jpg"},
    {"id": "cy24066", "desc": "功能性品种。花瓣易失水但极易复水。寓意万物复苏，耐运输，插水即活。", "candidates": ["中农沁苏 ", "中农沁还", "中农嫣醒", "中农脂回", "中农沁生", "中农嫣复"], "image": "cy24066.jpg"},
    {"id": "cy24069", "desc": "极淡白绿色，仿佛山间清晨缭绕的薄雾。色调清雅脱俗，极具东方美学高级感。", "candidates": ["中农翠微 ", "中农碧烟", "中农翠雾", "中农净岚", "中农碧透", "中农翠幽"], "image": "cy24069.jpg"},
    {"id": "cy24071", "desc": "复古灰粉色，带有一种旧时光滤镜感。如陈年佳酿般厚重，展现岁月静谧之美。", "candidates": ["中农胭檀 ", "中农沁陈", "中农脂醉", "中农胭古", "中农沁郁", "中农脂暮"], "image": "cy24071.jpg"},
    {"id": "cy24079", "desc": "亮紫粉大花，花量巨大。盛开时如同铺开的华丽紫色丝绸，质感细腻，繁花似锦。", "candidates": ["中农绀绮 ", "中农绀繁", "中农绀华", "中农绀绸", "中农绀盛", "中农绀簇"], "image": "cy24079.jpg"},
]

# ================= 3. UI 渲染 =================
st.markdown('<div class="header-box"><div class="artistic-title">命名工作站</div></div>', unsafe_allow_html=True)

# 气泡导航阵列 (适配 17 个品种)
st.write("🍎 快速切换品种：")
rows = [varieties[i:i + 6] for i in range(0, len(varieties), 6)] # 每行显示6个

for row in rows:
    cols = st.columns(len(row))
    for i, v in enumerate(row):
        vid = v['id']
        is_selected = (st.session_state.selected_id == vid)
        is_voted = (f"voted_{vid}" in st.session_state)
        
        style_class = "voted-bubble" if is_voted else ("selected-bubble" if is_selected else "")
        
        with cols[i]:
            st.markdown(f'<div class="{style_class}">', unsafe_allow_html=True)
            if st.button(vid.replace("cy24", ""), key=f"nav_{vid}", help=f"查看 {vid}"):
                st.session_state.selected_id = vid
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# 加载选中品种数据
v_data = next(item for item in varieties if item["id"] == st.session_state.selected_id)
if v_data["id"] not in st.session_state.db_data:
    st.session_state.db_data[v_data["id"]] = {"votes": {}, "collected": []}
    save_data(st.session_state.db_data)

# 档案展示
st.write("")
col_img, col_info = st.columns([1, 1])
with col_img:
    if os.path.exists(v_data["image"]): st.image(Image.open(v_data["image"]), width="stretch")
    else: st.info(f"📷 待上传 {v_data['image']}")
with col_info:
    st.markdown(f'<div class="id-title">{v_data["id"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="desc-box"><b>特征描述：</b><br>{v_data["desc"]}</div>', unsafe_allow_html=True)

# 投票区
st.divider()
st.markdown(f"### 🎰 候选方案投票")
all_candidates = v_data["candidates"] + st.session_state.db_data[v_data["id"]].get("collected", [])
current_votes = st.session_state.db_data[v_data["id"]]["votes"]

for name in all_candidates:
    c_card, c_vote = st.columns([2.5, 1])
    count = current_votes.get(name, 0)
    with c_card:
        st.markdown(f'<div class="vote-item"><div style="font-size:18px; font-weight:700;">{name}</div>'
                    f'<div style="font-size:12px; color:#0071E3;">当前累积：{count} 票</div></div>', unsafe_allow_html=True)
    with c_vote:
        st.write(""); st.write("")
        st.markdown('<div class="vote-btn-wrap">', unsafe_allow_html=True)
        if st.button(f"投票", key=f"v_{v_data['id']}_{name}"):
            if f"voted_{v_data['id']}" not in st.session_state:
                st.session_state.db_data[v_data['id']]["votes"][name] = count + 1
                save_data(st.session_state.db_data); st.session_state[f"voted_{v_data['id']}"] = True
                st.balloons(); st.rerun()
            else:
                st.error("此品种已投票")
        st.markdown('</div>', unsafe_allow_html=True)

# 看板与征集 (省略部分逻辑以节省篇幅)
with st.expander("📊 查看计票看板"):
    df_res = pd.DataFrame({'Name': all_candidates, 'Votes': [current_votes.get(n, 0) for n in all_candidates]})
    if df_res['Votes'].sum() > 0:
        g1, g2 = st.columns(2)
        with g1:
            fig_bar = go.Figure(data=[go.Bar(x=df_res['Name'], y=df_res['Votes'], marker_color='#0071E3', marker_line_color='black', marker_line_width=2)])
            st.plotly_chart(fig_bar, use_container_width=True)
        with g2:
            fig_pie = px.pie(df_res, values='Votes', names='Name', hole=0.5)
            st.plotly_chart(fig_pie, use_container_width=True)

# 秘密重置 (回车符)
col_f1, col_f2 = st.columns([0.96, 0.04])
with col_f2:
    if st.button("↵", key="reset_key", type="secondary"): st.session_state.show_reset = True
if st.session_state.get("show_reset"):
    pwd = st.text_input("Admin", type="password")
    if pwd == ADMIN_PWD:
        if st.button("RESET"): st.session_state.db_data = {}; save_data({}); st.rerun()

st.markdown("""<div class="fixed-footer">© 2026 肆叁叁月季起名社</div>""", unsafe_allow_html=True)