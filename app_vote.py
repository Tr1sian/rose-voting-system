import streamlit as st
import pandas as pd
import os
import json
import random
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px

# ================= 1. 极致视觉引擎 (CSS 深度定制) =================
st.set_page_config(page_title="肆叁叁月季起名社", page_icon="💐", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&family=Inter:wght@400;600&display=swap');
    .stApp { background-color: #F5F5F7 !important; background-image: radial-gradient(circle at 50% 20%, #FFFFFF 0%, #E2E2E7 100%) !important; }
    
    /* 窄版面板控制 */
    div[data-testid="stVerticalBlockBorderWrapper"]:first-of-type {
        max-width: 620px !important; margin: 0 auto !important;
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #FFFFFF !important; border-radius: 32px !important;
        box-shadow: 0 20px 60px rgba(0,0,0,0.05), inset 0 1px 2px rgba(255,255,255,0.5) !important;
        padding: 40px !important;
    }

    .header-box { padding-top: 60px; padding-bottom: 20px; text-align: center; }
    .artistic-title { font-family: 'Noto Serif SC', serif; font-size: 58px; font-weight: 900; color: #000000 !important; letter-spacing: 16px; }

    /* 强制横向布局 */
    div[data-testid="stHorizontalBlock"] { flex-direction: row !important; flex-wrap: nowrap !important; align-items: center !important; }
    div[data-testid="column"] { width: 50% !important; min-width: 0 !important; flex: 1 1 auto !important; }

    /* 按钮：蓝底白字 */
    div.stButton > button {
        background-color: #0071E3 !important; color: #FFFFFF !important;
        border-radius: 99px !important; padding: 10px 40px !important;
        border: none !important; width: 100% !important; font-weight: 600 !important;
    }
    div.stButton > button * { color: #FFFFFF !important; } 

    /* 档案排版 */
    .id-title { font-size: 44px; font-weight: 900; color: #000000 !important; margin-top: -10px !important; line-height: 1.1 !important; margin-bottom: 20px !important; }
    .desc-box { color: #1D1D1F !important; font-size: 15px; line-height: 1.8 !important; text-align: justify; }

    .vote-item {
        background: #FFFFFF !important; border-radius: 20px !important;
        padding: 20px 25px !important; border: 1px solid #E5E5E7 !important;
        margin-bottom: 12px !important;
    }

    .fixed-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: rgba(245, 245, 247, 0.95); text-align: center; padding: 15px 0;
        border-top: 1px solid #D2D2D7; color: #86868B !important; font-size: 12px; z-index: 1000;
    }
    .secret-wrap { position: fixed; bottom: 12px; right: 20px; z-index: 1001; opacity: 0.2; }
    header, footer, [data-testid="stHeader"] { visibility: hidden !important; }
            /* 1. 隐藏掉遮挡图标的提示文字 'Press Enter to apply' */

    div[data-testid="InputInstructions"] {
        display: none !important;
    }

</style>
""", unsafe_allow_html=True)

# ================= 2. 实时数据持久化逻辑 (核心修正) =================
DATA_FILE = "vote_data.json"
ADMIN_PWD = "433admin"

def load_data_from_file():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_data_to_file(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 核心变化：每次启动或刷新时，强制从文件读取到 SessionState，不再使用 cache
if 'db_data' not in st.session_state:
    st.session_state.db_data = load_data_from_file()

if 'persistent_id' not in st.session_state:
    st.session_state.persistent_id = "cy24027"

# ================= 3. 品种库配置 =================
varieties = [
    {"id": "cy24027", "desc": "花色为极具质感的深红至黑红色。花瓣厚度极高，带有丝绒般的光泽。花型为深杯状，瓶插寿命长。"},
    {"id": "cy24057", "desc": "花型标准的代表。花瓣排列整齐划一，呈现出完美的数学几何螺旋结构。颜色为纯正的中国红。"},
    {"id": "cy24065", "desc": "植株高大强壮，枝条粗壮。螺旋花心更为宽大舒展，给人一种盛大、热烈的视觉冲击力。"},
    {"id": "cy24001", "desc": "色调明快，偏朱红带橙调。花瓣质地较薄但硬挺，开放姿态轻盈跳跃，如同跳动的火光。"},
    {"id": "cy24051", "desc": "颜色比一号更红、更纯，依然保持了极高的亮度。特异性在于色彩穿透力极强。"},
    {"id": "cy24005", "desc": "短枝型品种。花苞呈现完美的圆球形，就像一颗圆滚滚的宝珠。受宠可爱。"},
    {"id": "cy24045", "desc": "巨大的花冠，花瓣边缘具有非常显著的波浪状褶皱。层层叠叠的粉色花瓣如同海面掀起巨澜。"},
    {"id": "cy24060", "desc": "亮粉色品种，冲击力极强。整体呈现出一种高心翘角的姿态，赋予品种一种气宇轩昂的特质。"},
    {"id": "cy24063", "desc": "标准的高心卷边状，花瓣质地厚实如丝绒。层层花瓣螺旋紧致包裹，勾勒出锐利侧影。"},
    {"id": "cy24080", "desc": "显著的特异性：花朵中心雄蕊瓣化，形成了明显的异色“草心”。如红妆美人的眼眸。"},
    {"id": "cy24086", "desc": "古典的四分莲座状，花瓣数量极多。橙粉复色交织在一起如同华丽的织锦，尽显富丽堂皇。"},
    {"id": "cy24044", "desc": "品种长势弱，花色柔和奶白。姿态轻盈、如梦似幻。非常适合主打文艺清新风格的高端市场。"},
    {"id": "cy24046", "desc": "侧芽萌发力强，生长势头迅猛。花瓣呈角状翻卷，形态像飞鸟的白色羽毛，具有向上的动势。"},
    {"id": "cy24066", "desc": "功能性品种。花瓣易失水但极易复水。寓意万物复苏，商业上耐运输、插水即活。"},
    {"id": "cy24069", "desc": "花色为极淡的白绿色，仿佛山间清晨缭绕的薄雾。这种色调传达了清雅脱俗的色彩氛围。"},
    {"id": "cy24071", "desc": "花色复古灰粉色，带有一种旧时光滤镜感。色彩如陈年佳酿般厚重，展现岁月静谧之美。"},
    {"id": "cy24079", "desc": "亮紫粉色大花，花量巨大且开花整齐。盛开时如同铺开的华丽紫色丝绸，质感细腻，繁花似锦。"},
]

cand_map = {
    "cy24027": ["中农丹赫", "中农绛阙", "中农丹墨", "中农绯重", "中农绛肃", "中农朱极"],
    "cy24057": ["中农丹赫", "中农丹正", "中农绛枢", "中农朱律", "中农绯典", "中农丹楷"],
    "cy24065": ["中农丹赫", "中农丹弘", "中农绯钜", "中农朱硕", "中农绛巍", "中农丹骜"],
    "cy24001": ["中农烨煌", "中农烨炽", "中农烁阳", "中农曦照", "中农烨焱", "中农朝蔚"],
    "cy24051": ["中农烨煌", "中农烨透", "中农烁曜", "中农曦朗", "中农烨纯", "中农烁熠"],
    "cy24005": ["中农烁珠", "中农曦丸", "中农烁圆", "中农烨铃", "中农烁玲"],
    "cy24045": ["中农沁澜", "中农沁涛", "中农嫣漪", "中农脂涌", "中农沁褶", "中农嫣裳"],
    "cy24060": ["中农嫣昂", "中农嫣傲", "中农沁翘", "中农嫣凌", "中农沁扬", "中农嫣耸"],
    "cy24063": ["中农绛芒", "中农绛剑", "中农丹锐", "中农朱矢", "中农绯厉", "中农绛戟"],
    "cy24080": ["中农朱瞳", "中农绛眸", "中农丹睛", "中农朱芯", "中农绯目", "中农绛凝"],
    "cy24086": ["中农烁锦", "中农曦织", "中农烁绣", "中农烨繁", "中农曦缬", "中农烁层"],
    "cy24044": ["中农瑶影", "中农素柔", "中农净怯", "中农瑶梦", "中农素纱", "中农净婉"],
    "cy24046": ["中农净翎", "中农素羽", "中农净翔", "中农瑶鹤", "中农素箭", "中农净翼"],
    "cy24066": ["中农沁苏", "中农沁还", "中农嫣醒", "中农脂回", "中农沁生", "中农嫣复"],
    "cy24069": ["中农翠微", "中农碧烟", "中农翠雾", "中农净岚", "中农碧透", "中农翠幽"],
    "cy24071": ["中农胭檀", "中农沁陈", "中农脂醉", "中农胭古", "中农沁郁", "中农脂暮"],
    "cy24079": ["中农绀绮", "中农绀繁", "中农绀华", "中农绀绸", "中农绀盛", "中农绀簇"],
}

# ================= 4. UI 渲染与同步逻辑 =================
st.markdown('<div class="header-box"><div class="artistic-title">命名工作站</div></div>', unsafe_allow_html=True)

# 动态下拉列表
options_labels = []
saved_index = 0
for i, v in enumerate(varieties):
    vid = v['id']
    label = f"{vid} ✅" if st.session_state.get(f"voted_{vid}") else vid
    options_labels.append(label)
    if vid == st.session_state.persistent_id: saved_index = i

st.markdown('<div style="margin-bottom:10px; font-weight:500;">选择品种查看档案并投票：</div>', unsafe_allow_html=True)
selected_label = st.selectbox("nav", options_labels, index=saved_index, label_visibility="collapsed")

# 切换品种逻辑
new_id = varieties[options_labels.index(selected_label)]['id']
if new_id != st.session_state.persistent_id:
    st.session_state.persistent_id = new_id
    st.rerun()

v_data = next(item for item in varieties if item["id"] == st.session_state.persistent_id)
# 核心修正：确保当前品种在 session 数据库中实时挂载
if v_data["id"] not in st.session_state.db_data:
    st.session_state.db_data[v_data["id"]] = {"votes": {}, "collected": []}

# 信息展示
st.write("")
col_img, col_info = st.columns([1.1, 1])
with col_img:
    img_name = f"{v_data['id']}.jpg"
    if os.path.exists(img_name): st.image(Image.open(img_name), width="stretch")
    else: st.info(f"📷 待上传 {img_name}")
with col_info:
    st.markdown(f'<div class="id-title">{v_data["id"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="desc-box"><b>特征描述：</b><br>{v_data["desc"]}</div>', unsafe_allow_html=True)

# 投票区
st.divider()
st.markdown(f"### 🎰 候选方案投票")
all_candidates = cand_map[v_data["id"]] + st.session_state.db_data[v_data["id"]].get("collected", [])
current_votes = st.session_state.db_data[v_data["id"]]["votes"]

for name in all_candidates:
    c_card, c_vote = st.columns([4, 1.2])
    count = current_votes.get(name, 0)
    with c_card:
        st.markdown(f'<div class="vote-item"><div style="font-size:18px; font-weight:700;">{name}</div>'
                    f'<div style="font-size:12px; color:#0071E3; font-weight:600;">当前累积：{count} 票</div></div>', unsafe_allow_html=True)
    with c_vote:
        st.write(""); st.write("")
        # 实时投票逻辑
        if st.button(f"投票", key=f"v_btn_{v_data['id']}_{name}"):
            if f"voted_{v_data['id']}" not in st.session_state:
                # 1. 立即更新内存
                st.session_state.db_data[v_data['id']]["votes"][name] = count + 1
                # 2. 立即存盘
                save_data_to_file(st.session_state.db_data)
                # 3. 标记本地状态
                st.session_state[f"voted_{v_data['id']}"] = True
                st.balloons()
                # 4. 强制重绘，此时 UI 会读取内存中的最新 db_data
                st.rerun() 
            else:
                st.error("限投一票")

# 名字征集
with st.expander("✨ 灵感征集：在此提交您的新建议"):
    c_in, c_sub = st.columns([3, 1])
    with c_in: new_name = st.text_input("建议名", key=f"in_input_{v_data['id']}", placeholder="例如：中农丹旋（中农+色核+性状）", label_visibility="collapsed")
    with c_sub:
        if st.button("提交建议", key=f"sub_btn_{v_data['id']}"):
            if new_name and new_name not in all_candidates:
                st.session_state.db_data[v_data['id']]["collected"].append(new_name)
                save_data_to_file(st.session_state.db_data)
                st.success("成功！"); st.rerun()

# 计票看板 (实时刷新版)
st.write(""); st.divider()
with st.expander("📊 查看实时计票看板", expanded=True):
    # 直接读取内存中的最新票数
    df_res = pd.DataFrame({'Name': all_candidates, 'Votes': [current_votes.get(n, 0) for n in all_candidates]})
    if df_res['Votes'].sum() > 0:
        h = 380
        g1, g2 = st.columns(2)
        with g1:
            fig_bar = go.Figure(data=[go.Bar(x=df_res['Name'], y=df_res['Votes'], marker_color='#0071E3', marker_line_color='black', marker_line_width=2, width=0.5)])
            fig_bar.update_layout(template="plotly_white", height=h, margin=dict(l=40, r=10, t=20, b=80), yaxis=dict(showline=True, linewidth=2, linecolor='black', ticks='outside'), xaxis=dict(showline=True, linewidth=2, linecolor='black', tickangle=-45, ticks='outside'))
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        with g2:
            fig_pie = px.pie(df_res, values='Votes', names='Name', hole=0.6, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_pie.update_layout(height=h, margin=dict(l=10, r=10, t=20, b=20), legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
    else: st.caption("尚无数据")

# ================= 5. 页脚与秘密重置 =================
st.write("")
st.markdown("""<div class="fixed-footer">© 2026 肆叁叁月季起名社 &nbsp; </div>""", unsafe_allow_html=True)

st.markdown('<div class="secret-wrap">', unsafe_allow_html=True)
if st.button("↵", key="final_reset_trigger"): st.session_state.show_reset = True
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.get("show_reset"):
    pwd = st.text_input("Password", type="password", key="admin_pwd_final")
    if pwd == ADMIN_PWD:
        if st.button("RESET ALL DATA"):
            save_data_to_file({})
            # 清理所有内存状态
            for k in list(st.session_state.keys()):
                if k.startswith("voted_") or k == "db_data": del st.session_state[k]
            st.rerun()