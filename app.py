import streamlit as st
import pandas as pd
import math
import io
import zipfile
import re

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tách lớp từ Excel",
    page_icon="📂",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Be Vietnam Pro', sans-serif; }
.main { background: #f0f4f8; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 760px; }
h1 { font-size: 1.8rem !important; font-weight: 700 !important; color: #1a2744 !important; letter-spacing: -0.5px; }
.subtitle { color: #5a6a85; font-size: 0.95rem; margin-top: -0.4rem; margin-bottom: 1.5rem; }
.card { background: white; border-radius: 14px; padding: 1.6rem 1.8rem; margin-bottom: 1.2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06); border: 1px solid #e8edf4; }
.card-title { font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;
              color: #8a9ab5; margin-bottom: 0.8rem; }
.stButton > button { background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border: none;
    border-radius: 10px; padding: 0.65rem 2.2rem; font-family: 'Be Vietnam Pro', sans-serif;
    font-weight: 600; font-size: 0.95rem; cursor: pointer; transition: all 0.2s;
    box-shadow: 0 4px 14px rgba(37,99,235,0.35); width: 100%; }
.stButton > button:hover { background: linear-gradient(135deg, #1d4ed8, #1e40af);
    transform: translateY(-1px); box-shadow: 0 6px 18px rgba(37,99,235,0.45); }
.result-box { background: #f0fdf4; border: 1px solid #86efac; border-radius: 10px;
              padding: 1rem 1.2rem; color: #166534; font-size: 0.9rem; margin-top: 1rem; }
.tag-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 0.5rem; }
.tag { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; border-radius: 20px;
       padding: 3px 12px; font-size: 0.8rem; font-weight: 500; }
.info-row { display: flex; gap: 1.5rem; margin-top: 0.8rem; flex-wrap: wrap; }
.info-item { background: #f8fafc; border-radius: 8px; padding: 0.5rem 1rem;
             font-size: 0.82rem; color: #475569; border: 1px solid #e2e8f0; }
.info-item strong { color: #1e293b; }
.stDownloadButton > button { background: linear-gradient(135deg, #059669, #047857) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    padding: 0.65rem 2.2rem !important; font-family: 'Be Vietnam Pro', sans-serif !important;
    font-weight: 600 !important; font-size: 0.95rem !important; width: 100% !important;
    box-shadow: 0 4px 14px rgba(5,150,105,0.35) !important; }
hr { border: none; border-top: 1px solid #e8edf4; margin: 1rem 0; }
.step-badge { display: inline-block; background: #2563eb; color: white; border-radius: 50%;
    width: 22px; height: 22px; text-align: center; line-height: 22px;
    font-size: 0.75rem; font-weight: 700; margin-right: 8px; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 📂 Tách lớp từ file Excel")
st.markdown('<p class="subtitle">Tự động tách dữ liệu theo lớp thành từng file riêng biệt</p>',
            unsafe_allow_html=True)

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

# ── Step 2 – Prefix ───────────────────────────────────────────────────────────
st.markdown("""
<div class="card">
  <div class="card-title"><span class="step-badge">2</span>Tuỳ chọn tiền tố tên file đầu ra</div>
</div>
""", unsafe_allow_html=True)

prefix = st.text_input(
    "Tiền tố (để trống nếu không cần)",
    placeholder="Ví dụ: HocSinh_   →   HocSinh_10A1.xlsx",
    label_visibility="collapsed",
)

# ── Step 3 – Process & Download ───────────────────────────────────────────────
st.markdown("""
<div class="card">
  <div class="card-title"><span class="step-badge">3</span>Xử lý &amp; tải xuống</div>
</div>
""", unsafe_allow_html=True)

run_btn = st.button("⚙️ Tách lớp ngay", disabled=not uploaded_file or not all_classes)

if run_btn and uploaded_file and all_classes:
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
                filename   = f"{prefix}{safe_class}.xlsx"
                zf.writestr(filename, wb_buf.getvalue())

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
        file_name="tach_lop.zip",
        mime="application/zip",
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#b0bec5;font-size:.78rem;margin-top:2.5rem;">
  Hỗ trợ nhận dạng cột: <em>Lớp · Lớp học · Lop · Class · Class Name</em>
</div>
""", unsafe_allow_html=True)
