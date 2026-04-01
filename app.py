import streamlit as st
import pandas as pd
import math
import io
import zipfile
import re

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tách lớp",
    page_icon="🐍",
    layout="centered",
)

# ── Custom CSS (Dark + Light mode aware) ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&display=swap');

/* Light tokens */
:root {
  --bg-page:        #eef2f7;
  --bg-card:        #ffffff;
  --bg-item:        #f1f5fb;
  --bg-tag:         #e8f0fe;
  --accent:         #2563eb;
  --border-card:    #dde4f0;
  --border-item:    #d0d9ec;
  --border-tag:     #a5c0fb;
  --text-heading:   #0f1f44;
  --text-body:      #1e293b;
  --text-sub:       #52637a;
  --text-label:     #2563eb;
  --text-item:      #3d5068;
  --text-tag:       #1a46c4;
  --text-footer:    #a0aec0;
  --shadow-card:    0 4px 20px rgba(37,99,235,0.09), 0 1px 4px rgba(0,0,0,0.05);
  --result-bg:      #ecfdf5;
  --result-border:  #34d399;
  --result-text:    #065f46;
  --hr-color:       #e2e8f2;
  --hero-grad:      linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
}

/* Dark tokens */
[data-theme="dark"] {
  --bg-page:        #0d1117;
  --bg-card:        #161b27;
  --bg-item:        #1e2538;
  --bg-tag:         #1a2645;
  --accent:         #4a8eff;
  --border-card:    #252d45;
  --border-item:    #2d3652;
  --border-tag:     #2e4a80;
  --text-heading:   #e2eafc;
  --text-body:      #c4d0e8;
  --text-sub:       #6e80a0;
  --text-label:     #4a8eff;
  --text-item:      #8a9ab8;
  --text-tag:       #82b4ff;
  --text-footer:    #2e3a52;
  --shadow-card:    0 4px 24px rgba(0,0,0,0.5);
  --result-bg:      #072018;
  --result-border:  #1a7a48;
  --result-text:    #6ee7a0;
  --hr-color:       #252d45;
  --hero-grad:      linear-gradient(135deg, #1a4aaa 0%, #5b21b6 100%);
}

html, body, [class*="css"] { font-family: 'Be Vietnam Pro', sans-serif; }
.main { background: var(--bg-page) !important; }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 780px; }

/* Hero */
.hero {
  background: var(--hero-grad);
  border-radius: 18px;
  padding: 1.8rem 2rem;
  margin-bottom: 1.6rem;
  position: relative;
  overflow: hidden;
}
.hero::after {
  content: '';
  position: absolute;
  right: -30px; top: -30px;
  width: 180px; height: 180px;
  background: rgba(255,255,255,0.06);
  border-radius: 50%;
}
.hero::before {
  content: '';
  position: absolute;
  right: 60px; bottom: -50px;
  width: 120px; height: 120px;
  background: rgba(255,255,255,0.04);
  border-radius: 50%;
}
.hero h1 {
  font-size: 1.75rem !important;
  font-weight: 800 !important;
  color: #ffffff !important;
  letter-spacing: -0.5px;
  margin: 0 0 0.3rem 0 !important;
}
.hero .subtitle {
  color: rgba(255,255,255,0.78) !important;
  font-size: 0.93rem;
  margin: 0;
}

/* Cards with left accent bar */
.card {
  background: var(--bg-card);
  border-radius: 14px;
  padding: 1.3rem 1.6rem 1.3rem 1.8rem;
  margin-bottom: 1rem;
  box-shadow: var(--shadow-card);
  border: 1px solid var(--border-card);
  border-left: 4px solid var(--accent);
}

/* Card title */
.card-title {
  display: flex;
  align-items: center;
  font-size: 0.84rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-label);
  margin-bottom: 0.4rem;
}

/* Step badge */
.step-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--accent);
  color: #fff;
  border-radius: 50%;
  width: 24px; height: 24px;
  font-size: 0.72rem; font-weight: 800;
  margin-right: 10px;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(37,99,235,0.4);
}

/* Info row */
.info-row { display: flex; gap: 0.8rem; margin-top: 0.9rem; flex-wrap: wrap; }
.info-item {
  background: var(--bg-item);
  border-radius: 10px;
  padding: 0.55rem 1rem;
  font-size: 0.83rem;
  color: var(--text-item);
  border: 1px solid var(--border-item);
  display: flex; align-items: center; gap: 6px;
}
.info-item strong { color: var(--text-body); font-size: 1rem; }

/* Tags */
.tag-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 0.6rem; }
.tag {
  background: var(--bg-tag);
  color: var(--text-tag);
  border: 1px solid var(--border-tag);
  border-radius: 20px;
  padding: 4px 13px;
  font-size: 0.8rem;
  font-weight: 600;
}

/* Divider */
hr { border: none; border-top: 1px solid var(--hr-color); margin: 1rem 0; }

/* Result box */
.result-box {
  background: var(--result-bg);
  border: 1px solid var(--result-border);
  border-left: 4px solid var(--result-border);
  border-radius: 10px;
  padding: 0.9rem 1.2rem;
  color: var(--result-text);
  font-size: 0.9rem;
  margin-top: 1rem;
  font-weight: 500;
}

/* Primary button */
.stButton > button {
  background: linear-gradient(135deg, #2563eb, #4f46e5) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 0.7rem 2.2rem !important;
  font-family: 'Be Vietnam Pro', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
  transition: all 0.2s !important;
  box-shadow: 0 4px 16px rgba(37,99,235,0.4) !important;
  width: 100% !important;
  letter-spacing: 0.2px !important;
}
.stButton > button:hover {
  background: linear-gradient(135deg, #1d4ed8, #4338ca) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 22px rgba(37,99,235,0.5) !important;
}
.stButton > button:disabled {
  background: linear-gradient(135deg, #94a3b8, #7f8ea8) !important;
  opacity: 0.6 !important;
  box-shadow: none !important;
}

/* Download button */
.stDownloadButton > button {
  background: linear-gradient(135deg, #059669, #0d9488) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 0.7rem 2.2rem !important;
  font-family: 'Be Vietnam Pro', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
  width: 100% !important;
  box-shadow: 0 4px 16px rgba(5,150,105,0.4) !important;
  transition: all 0.2s !important;
  letter-spacing: 0.2px !important;
}
.stDownloadButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 22px rgba(5,150,105,0.5) !important;
}

/* File uploader */
[data-testid="stFileUploaderDropzone"] {
  background: var(--bg-item) !important;
  border: 2px dashed var(--border-card) !important;
  border-radius: 12px !important;
  transition: border-color 0.2s !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
  border-color: var(--accent) !important;
}

/* Footer */
.footer {
  text-align: center;
  color: var(--text-footer);
  font-size: .78rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--hr-color);
}
</style>
""", unsafe_allow_html=True)

# ── Hero Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>&#128194; T&#225;ch l&#7899;p t&#7915; file Excel</h1>
  <p class="subtitle">T&#7921; &#273;&#7897;ng t&#225;ch d&#7919; li&#7879;u theo l&#7899;p th&#224;nh t&#7915;ng file ri&#234;ng bi&#7879;t</p>
</div>
""", unsafe_allow_html=True)



# ── Helpers ───────────────────────────────────────────────────────────────────
CLASS_COL_PATTERNS = [
    r'^lớp$', r'^lop$', r'^lớp học$', r'^class$',
    r'^lop hoc$', r'^classname$', r'^class name$',
]

def detect_class_column(df: pd.DataFrame):
    for col in df.columns:
        normalized = col.strip().lower()
        for pat in CLASS_COL_PATTERNS:
            if re.fullmatch(pat, normalized):
                return col
    return None

def safe_sheet_name(name: str) -> str:
    name = re.sub(r'[\\/*?:\[\]]', '_', str(name))
    return name[:31]

# ── Step 1 – Upload ───────────────────────────────────────────────────────────
st.markdown("""
<div class="card">
  <div class="card-title"><span class="step-badge">1</span>Tải lên file Excel</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    label="Chọn file .xlsx hoặc .xls",
    type=["xlsx", "xls"],
    label_visibility="collapsed",
)

# ── Analyse uploaded file ─────────────────────────────────────────────────────
sheets_info = {}   # sheet_name -> (df, class_col)
all_classes = set()

if uploaded_file:
    try:
        xls = pd.ExcelFile(uploaded_file)
        for sheet in xls.sheet_names:
            df  = pd.read_excel(xls, sheet)
            col = detect_class_column(df)
            sheets_info[sheet] = (df, col)
            if col:
                all_classes.update(df[col].dropna().unique())

        detected_sheets = [s for s, (_, c) in sheets_info.items() if c]
        tags_html = "".join(f'<span class="tag">{c}</span>' for c in sorted(all_classes))

        st.markdown(f"""
        <div class="card">
          <div class="card-title">Thông tin file</div>
          <div class="info-row">
            <div class="info-item">📄 <strong>{len(xls.sheet_names)}</strong> sheet</div>
            <div class="info-item">✅ <strong>{len(detected_sheets)}</strong> sheet có cột lớp</div>
            <div class="info-item">🎓 <strong>{len(all_classes)}</strong> lớp tìm thấy</div>
          </div>
          <hr/>
          <div class="card-title" style="margin-top:.5rem">Danh sách lớp</div>
          <div class="tag-row">{tags_html if tags_html else
            '<span style="color:#94a3b8;font-size:.85rem">Không tìm thấy cột lớp nào</span>'}</div>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Không đọc được file: {e}")

# ── Step 2 – Process & Download ───────────────────────────────────────────────
st.markdown("""
<div class="card">
  <div class="card-title"><span class="step-badge">2</span>Xử lý &amp; tải xuống</div>
</div>
""", unsafe_allow_html=True)

run_btn = st.button("⚙️ Tách lớp ngay", disabled=not uploaded_file or not all_classes)

if run_btn and uploaded_file and all_classes:
    # Derive zip name from input filename (strip extension)
    input_stem = re.sub(r'\.xlsx?$', '', uploaded_file.name, flags=re.IGNORECASE)
    zip_name   = f"{input_stem}.zip"

    zip_buf = io.BytesIO()
    progress = st.progress(0, text="Đang xử lý…")
    classes_sorted = sorted(all_classes)

    with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for idx, class_name in enumerate(classes_sorted):
            wb_buf = io.BytesIO()
            has_data = False

            with pd.ExcelWriter(wb_buf, engine='xlsxwriter') as writer:
                for sheet_name, (df, class_col) in sheets_info.items():
                    if class_col is None:
                        continue
                    df_class = df[df[class_col] == class_name].reset_index(drop=True)
                    if df_class.empty:
                        continue
                    has_data = True

                    sn = safe_sheet_name(sheet_name)
                    df_class.to_excel(writer, sheet_name=sn, index=False)

                    workbook  = writer.book
                    worksheet = writer.sheets[sn]
                    border_fmt = workbook.add_format({'border': 1})

                    last_row, last_col = df_class.shape
                    for row in range(last_row + 1):
                        for col in range(last_col):
                            cell_value = (df_class.columns[col] if row == 0
                                          else df_class.iloc[row - 1, col])
                            if isinstance(cell_value, float) and (
                                    math.isnan(cell_value) or math.isinf(cell_value)):
                                cell_value = ""
                            worksheet.write(row, col, cell_value, border_fmt)

                    for col_num, col_name in enumerate(df_class.columns):
                        col_data   = df_class[col_name].fillna("").astype(str)
                        cell_lens  = col_data.apply(lambda x: len(x))
                        max_length = int(max(cell_lens.max() if len(cell_lens) > 0 else 0,
                                            len(str(col_name)))) + 2
                        worksheet.set_column(col_num, col_num, min(max_length, 60))

            if has_data:
                safe_class = re.sub(r'[\\/*?:\[\]/]', '_', str(class_name))
                # Store files inside a folder named after the input file
                zf.writestr(f"{input_stem}/{safe_class}.xlsx", wb_buf.getvalue())

            progress.progress(
                (idx + 1) / len(classes_sorted),
                text=f"Đang xử lý lớp {class_name}… ({idx+1}/{len(classes_sorted)})"
            )

    progress.empty()
    zip_buf.seek(0)

    st.markdown(f"""
    <div class="result-box">
      ✅ Đã tách xong <strong>{len(classes_sorted)}</strong> lớp thành công!
      Nhấn nút bên dưới để tải file ZIP về máy.
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label="⬇️ Tải xuống tất cả (ZIP)",
        data=zip_buf,
        file_name=zip_name,
        mime="application/zip",
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Hỗ trợ nhận dạng cột: <em>Lớp · Lớp học · Lop · Class · Class Name</em>
</div>
""", unsafe_allow_html=True)
