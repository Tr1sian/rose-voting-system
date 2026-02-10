import streamlit as st
import pandas as pd
import os
import json
import random
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px

# ================= 1. 极致苹果美学引擎 (核心视觉回归) =================
st.set_page_config(page_title="肆叁叁月季起名社", page_icon="💐", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&family=Inter:wght@400;600&display=swap');

    /* 1. 全局背景 */
    .stApp {
        background-color: #F5F5F7 !important;
        background-image: radial-gradient(circle at 50% 20%, #FFFFFF 0%, #E2E2E7 100%) !important;
    }

    /* 2. 标题区美化 */
    .header-box { padding-top: 80px; padding-bottom: 40px; text-align: center; }
    .artistic-title {
        font-family: 'Noto Serif SC', serif; font-size: 58px; font-weight: 900;
        color: #000000 !important; letter-spacing: 16px; margin-bottom: 10px;
    }
    .artistic-subtitle {
        font-family: 'Inter', sans-serif; color: #86868B !important;
        font-size: 13px; letter-spacing: 5px; text-transform: uppercase;
    }

    /* 3. 【核心回归】窄版、纯白、微立体磨砂控制台 */
    div[data-testid="stVerticalBlockBorderWrapper"]:first-of-type {
        max-width: 620px !important;
        margin: 0 auto !important;
        background: rgba(255, 255, 255, 0.88) !important;
        backdrop-filter: blur(50px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(50px) saturate(180%) !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 32px !important;
        box-shadow: 0 20px 60px rgba(0,0,0,0.05), inset 0 1px 2px rgba(255,255,255,0.5) !important;
        padding: 40px !important;
    }

    /* 强制横向布局不坍塌 */
    div[data-testid="stHorizontalBlock"] { flex-direction: row !important; flex-wrap: nowrap !important; align-items: center !important; }
    div[data-testid="column"] { width: 50% !important; min-width: 0 !important; flex: 1 1 auto !important; }

    /* 4. 品种信息排版：直接融入背景 (无框) */
    /* 4. 品种信息排版微调 */
    .id-title { 
        font-size: 48px; 
        font-weight: 900; 
        color: #000000 !important; 
        /* 关键：取消顶部边距，并轻微上提以抵消字体自带行高，确保与照片上缘齐平 */
        margin-top: -12px !important; 
        margin-bottom: 15px !important; 
        line-height: 1 !important;
    }

    .desc-box { 
        color: #1D1D1F !important; 
        font-size: 16px; 
        /* 关键：增加行间距 (2.0) 和 段落顶部间距 (30px) */
        line-height: 2.0 !important; 
        text-align: justify; 
        margin-top: 30px !important; 
    }

    /* 5. 投票卡片 */
    .vote-item {
        background: #FFFFFF !important; border-radius: 20px !important;
        padding: 20px 25px !important; border: 1px solid #E5E5E7 !important;
        margin-bottom: 12px !important; transition: all 0.3s ease;
    }
    .vote-item:hover { border-color: #0071E3; transform: scale(1.02); }
    
    /* 强制纯黑文字 */
    p, span, label, div[data-testid="stMarkdownContainer"] p { color: #000000 !important; font-weight: 500 !important; }

    /* 6. 按钮：苹果蓝胶囊 */
    .stButton>button {
        background: #0071E3 !important; color: #FFFFFF  !important;
        border-radius: 99px !important; padding: 10px 40px !important;
        border: none !important; width: 100%; transition: 0.3s;
    }
    .stButton>button p, .stButton>button span {
    color: #FFFFFF !important;
    }

    /* 7. 秘密按钮 (隐藏于底部右侧) */
    .secret-btn { opacity: 0.01; cursor: default; }
    .secret-btn:hover { opacity: 0.4; }
            
    /* 修复密码输入框图标遮挡文字的问题 */
    .stTextInput div[data-baseweb="input"] {
        height: 48px !important; /* 增加高度 */
        padding-right: 10px !important;
    }
    /* 强制调整密码提示语的位置，防止重叠 */
    .stTextInput div[data-testid="InputInstructions"] {
        display: none !important; /* 隐藏 'Press Enter to apply'，苹果风格通常不需要这个提示 */
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

# ================= 2. 数据存储逻辑 =================
DATA_FILE = "vote_data.json"
ADMIN_PWD = "xcwsalp88"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f: json.dump(data, f, ensure_ascii=False, indent=4)

if 'db_data' not in st.session_state: st.session_state.db_data = load_data()

# ================= 3. 品种库配置 (全量17个) =================
# 这里为了代码简洁，仅展示部分，您可以直接在此列表填满17个品种
varieties = [
    {
        "id": "cy24027",
        "desc": "花色为极具质感的深红至黑红色。其最大的特异性在于花瓣厚度极高，带有丝绒般的光泽。花型为深杯状，花心螺旋紧致深邃，瓶插寿命长，展现出一种沉稳、肃穆的显赫气度。",
        "candidates": ["中农丹赫 ", "中农绛阙", "中农丹墨", "中农绯重", "中农绛肃", "中农朱极"],
        "image": "cy24027.jpg"
    },
    {
        "id": "cy24057",
        "desc": "本品种是该系列中花型最标准的代表。花瓣排列整齐划一，呈现出完美的数学几何螺旋结构。颜色为纯正的中国红，无杂色、无蓝调。它的“赫”体现在其作为商业标准红月季的完美一致性。",
        "candidates": ["中农丹赫 ", "中农丹正", "中农绛枢", "中农朱律", "中农绯典", "中农丹楷"],
        "image": "cy24057.jpg"
    },
    {
        "id": "cy24065",
        "desc": "植株高大强壮，枝条粗壮。花朵体量巨大，完全开放后花径可观。其螺旋花心比前两号更为宽大舒展，给人一种盛大、热烈的视觉冲击力，非常适合用于大型花艺庆典。",
        "candidates": ["中农丹赫 ", "中农丹弘", "中农绯钜", "中农朱硕", "中农绛巍", "中农丹骜"],
        "image": "cy24065.jpg"
    },
    {
        "id": "cy24001",
        "desc": "这是一个色调明快的品种，花色偏朱红，带有明显的橙色底调，在灯光下仿佛自带光源。它更具现代感和活力。花瓣质地较薄但硬挺，开放姿态轻盈跳跃。",
        "candidates": ["中农烨煌 ", "中农烨炽", "中农烁阳", "中农曦照", "中农烨焱", "中农朝蔚"],
        "image": "cy24001.jpg"
    },
    {
        "id": "cy24051",
        "desc": "颜色比一号更红、更纯，但依然保持了极高的亮度。花型紧凑，花瓣边缘有光泽感。其特异性在于色彩的穿透力极强，即便在远距离观看也如灯火般辉煌夺目。",
        "candidates": ["中农烨煌 ", "中农烨透", "中农烁曜", "中农曦朗", "中农烨纯", "中农烁熠"],
        "image": "cy24051.jpg"
    },
    {
        "id": "cy24005",
        "desc": "极具辨识度的短枝型品种。其花苞并非传统的杯状，而是呈现出完美的圆球形，就像一颗圆滚滚的宝珠。配合温暖的橙红花色，形态非常受宠可爱。",
        "candidates": ["中农烁珠 ", "中农曦丸", "中农烁圆", "中农烨铃", "中农曦果", "中农烁玲"],
        "image": "cy24005.jpg"
    },
    {
        "id": "cy24045",
        "desc": "拥有巨大的花冠，花瓣边缘具有非常显著的波浪状褶皱。盛开时，层层叠叠的粉色花瓣如同海面掀起巨澜，是对“边缘波浪”性状最直观的写照。",
        "candidates": ["中农沁澜 ", "中农沁涛", "中农嫣漪", "中农脂涌", "中农沁褶", "中农嫣裳"],
        "image": "cy24045.jpg"
    },
    {
        "id": "cy24060",
        "desc": "亮粉色品种，冲击力极强。其花型结构独特，外层花瓣明显向后翻，而中心花瓣高耸，整体呈现出一种高心翘角的姿态，赋予品种一种气宇轩昂的特质。",
        "candidates": ["中农嫣昂 ", "中农嫣傲", "中农沁翘", "中农嫣凌", "中农沁扬", "中农嫣耸"],
        "image": "cy24060.jpg"
    },
    {
        "id": "cy24063",
        "desc": "标准的高心卷边状，花瓣质地厚实如丝绒。层层花瓣螺旋紧致包裹，勾勒出锐利的侧影。既保留了古典玫瑰的深沉，又具备极佳的开放整齐度。",
        "candidates": ["中农绛芒 ", "中农绛剑", "中农丹锐", "中农朱矢", "中农绯厉", "中农绛戟"],
        "image": "cy24063.jpg"
    },
    {
        "id": "cy24080",
        "desc": "在DUS测试中表现出显著特异性：花朵中心雄蕊瓣化，形成了明显的异色“草心”。这种性状如红妆美人的眼眸，将生理变异转化为了独特的观赏卖点。",
        "candidates": ["中农朱瞳 ", "中农绛眸", "中农丹睛", "中农朱芯", "中农绯目", "中农绛凝"],
        "image": "cy24080.jpg"
    },
    {
        "id": "cy24086",
        "desc": "花型为古典的四分莲座状，花瓣数量极多且排列紧密。橙粉色复色交织在一起如同华丽的织锦，强调其繁复的物理质感，尽显富丽堂皇。",
        "candidates": ["中农烁锦 ", "中农曦织", "中农烁绣", "中农烨繁", "中农曦缬", "中农烁层"],
        "image": "cy24086.jpg"
    },
    {
        "id": "cy24044",
        "desc": "品种长势较弱，花色为柔和的奶白色。姿态轻柔、如梦似幻。具有一种风吹即动的柔弱美感，非常适合主打文艺清新风格的高端市场。",
        "candidates": ["中农瑶影 ", "中农素柔", "中农净怯", "中农瑶梦", "中农素纱", "中农净婉"],
        "image": "cy24044.jpg"
    },
    {
        "id": "cy24046",
        "desc": "侧芽萌发力极强，整株植物生长势头迅猛。花瓣呈明显的角状翻卷，尖端锐利，形态像飞鸟展开的白色羽毛，带有一种向上的动态意象。",
        "candidates": ["中农净翎 ", "中农素羽", "中农净翔", "中农瑶鹤", "中农素箭", "中农净翼"],
        "image": "cy24046.jpg"
    },
    {
        "id": "cy24066",
        "desc": "基于生理特性的功能性品种。花瓣易失水但极易复水，这种特性寓意着万物复苏。同时在商业上暗示其是一款耐运输、插水即活的优秀生产品种。",
        "candidates": ["中农沁苏 ", "中农沁还", "中农嫣醒", "中农脂回", "中农沁生", "中农嫣复"],
        "image": "cy24066.jpg"
    },
    {
        "id": "cy24069",
        "desc": "花色为极淡的白绿色，仿佛山间清晨缭绕的薄雾。这种色调精准传达了若隐若现、清雅脱俗的色彩氛围，极具东方美学的高级感。",
        "candidates": ["中农翠微 ", "中农碧烟", "中农翠雾", "中农净岚", "中农碧透", "中农翠幽"],
        "image": "cy24069.jpg"
    },
    {
        "id": "cy24071",
        "desc": "花色为复古的Dusty Pink，带有一种老电影般的旧时光滤镜感。色彩如陈年佳酿般厚重，耐人寻味。它展现的是一种岁月沉淀后的静谧之美。",
        "candidates": ["中农胭檀 ", "中农沁陈", "中农脂醉", "中农胭古", "中农沁郁", "中农脂暮"],
        "image": "cy24071.jpg"
    },
    {
        "id": "cy24079",
        "desc": "亮紫粉色的大花品种，花量巨大且开花整齐。盛开时如同铺开的华丽紫色丝绸，质感细腻，繁花似锦。其名字读音上扬，富有华贵之气。",
        "candidates": ["中农绀绮 ", "中农绀繁", "中农绀华", "中农绀绸", "中农绀盛", "中农绀簇"],
        "image": "cy24079.jpg"
    }
]

# ================= 4. UI 渲染逻辑 =================

st.markdown("""
<div class="header-box">
    <div class="artistic-title">命名工作站</div>
    <div class="artistic-subtitle">CRAFTING SOULS FOR EVERY ROSE</div>
</div>
""", unsafe_allow_html=True)

# 品种切换选择器 (窄版玻璃样式)
selected_id = st.selectbox("(o゜▽゜)o☆ 切换品种查看档案并投票：", [v["id"] for v in varieties])
v_data = next(item for item in varieties if item["id"] == selected_id)

if selected_id not in st.session_state.db_data:
    st.session_state.db_data[selected_id] = {"votes": {}, "collected": []}
    save_data(st.session_state.db_data)

# 品种信息档案 (无框、直接展示)
st.write("")
st.markdown('<div style="max-width:620px; margin: 0 auto;">', unsafe_allow_html=True)
col_img, col_info = st.columns([1.1, 1])
with col_img:
    if os.path.exists(v_data["image"]):
        st.image(Image.open(v_data["image"]), width="stretch")
    else:
        st.info(f"📷 待上传图片 {v_data['image']}")
with col_info:
    st.markdown(f'<div class="id-title">{v_data["id"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="desc-box"><b>特征描述：</b><br>{v_data["desc"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 投票区
st.divider()
st.markdown(f"<h3 style='text-align:center; color:#000000; margin-bottom:30px;'>🎰 候选方案投票</h3>", unsafe_allow_html=True)

all_candidates = v_data["candidates"] + st.session_state.db_data[selected_id].get("collected", [])
current_votes = st.session_state.db_data[selected_id]["votes"]

for name in all_candidates:
    c_card, c_vote = st.columns([4, 1.2])
    count = current_votes.get(name, 0)
    with c_card:
        st.markdown(f'<div class="vote-item"><div style="font-size:18px; font-weight:700;">{name}</div>'
                    f'<div style="font-size:12px; color:#0071E3;">当前票数：{count}</div></div>', unsafe_allow_html=True)
    with c_vote:
        st.write(""); st.write("")
        if st.button(f"投票", key=f"v_{selected_id}_{name}"):
            if f"voted_{selected_id}" not in st.session_state:
                st.session_state.db_data[selected_id]["votes"][name] = count + 1
                save_data(st.session_state.db_data); st.session_state[f"voted_{selected_id}"] = True
                st.balloons(); st.rerun()
            else:
                st.error("限投一票")

# 名字征集
st.write("")
with st.expander("✨ 灵感征集：在此提交您的新建议"):
    c_in, c_sub = st.columns([3, 1])
    with c_in: new_name = st.text_input("建议名", key=f"in_{selected_id}", placeholder="中农+色核+表型/意象", label_visibility="collapsed")
    with c_sub:
        if st.button("提交建议", key=f"sub_{selected_id}"):
            if new_name and new_name not in all_candidates:
                st.session_state.db_data[selected_id]["collected"].append(new_name); save_data(st.session_state.db_data)
                st.success("成功征集！"); st.rerun()

# 计票看板 (Prism + Donut)
st.write("")
st.divider()
with st.expander("📊 查看实时计票看板 ", expanded=True):
    df_res = pd.DataFrame({'Name': all_candidates, 'Votes': [current_votes.get(n, 0) for n in all_candidates]})
    if df_res['Votes'].sum() > 0:
        g1, g2 = st.columns(2)
        with g1:
            fig_bar = go.Figure(data=[go.Bar(x=df_res['Name'], y=df_res['Votes'], marker_color='#0071E3', marker_line_color='black', marker_line_width=2)])
            fig_bar.update_layout(template="plotly_white", height=350, font=dict(family="Arial"), yaxis=dict(showline=True, linewidth=2, linecolor='black'), xaxis=dict(showline=True, linewidth=2, linecolor='black'))
            st.plotly_chart(fig_bar, use_container_width=True)
        with g2:
            fig_pie = px.pie(df_res, values='Votes', names='Name', hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_pie.update_layout(showlegend=False, height=350, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_pie, use_container_width=True)
    else: st.caption("尚无投票数据")

# ================= 5. 页脚与秘密入口 (回车符) =================
# ================= 5. 页脚与秘密入口 (修改版) =================
st.write("")
st.write("")
col_f1, col_f2 = st.columns([0.9, 0.1])
with col_f2:
    # 秘密按钮
    if st.button("↵", help="Admin", key="reset_key", type="secondary"):
        st.session_state.show_reset = not st.session_state.get("show_reset", False)

# 当开启重置模式时，在页面中央显示一个较宽的输入框
if st.session_state.get("show_reset"):
    st.write("")
    # 创建三个列，让输入框居中且宽度适中（占中间 2/4）
    _, mid_col, _ = st.columns([1, 2, 1])
    with mid_col:
        st.markdown('<div style="text-align:center; font-size:14px; color:#86868B;">ADMIN ACCESS</div>', unsafe_allow_html=True)
        pwd = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="输入管理员密码")
        if pwd == ADMIN_PWD:
            if st.button("RESET ALL DATA", type="primary", use_container_width=True):
                st.session_state.db_data = {}
                save_data({})
                st.rerun()

st.markdown("""<div class="fixed-footer">© 2026 肆叁叁月季起名社 &nbsp; </div>""", unsafe_allow_html=True)