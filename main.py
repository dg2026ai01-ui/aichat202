import streamlit as st
import anthropic
import time

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="Claude AI Chat",
    page_icon="✦",
    layout="centered",
)

# ── 커스텀 CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600&family=Noto+Sans+KR:wght@400;500;700&display=swap');

/* 전체 배경 — 따뜻한 크림 화이트 */
.stApp {
    background: linear-gradient(145deg, #fffdf8 0%, #fef9f0 50%, #fff8f2 100%);
    font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
    min-height: 100vh;
}

/* 메인 컨테이너 */
.block-container {
    max-width: 760px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

/* 헤더 */
.app-header {
    text-align: center;
    margin-bottom: 2rem;
    padding: 2.2rem 1.5rem 2rem;
    background: linear-gradient(135deg, #ffffff 0%, #fffaf4 100%);
    border-radius: 20px;
    box-shadow: 0 2px 16px rgba(234, 179, 8, 0.08), 0 1px 4px rgba(0,0,0,0.06);
    border: 1.5px solid #fde68a;
}
.app-header h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #1c1917;
    letter-spacing: -0.04em;
    margin: 0;
}
.app-header .tagline {
    font-size: 0.8rem;
    color: #a8a29e;
    margin-top: 0.45rem;
    font-weight: 400;
    letter-spacing: 0.05em;
}

/* 모델 선택 라디오 */
div[data-testid="stRadio"] > label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #78716c;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
div[data-testid="stRadio"] > div {
    gap: 0.75rem;
    margin-top: 0.5rem;
}
div[data-testid="stRadio"] > div > label {
    background: #ffffff;
    border: 1.5px solid #e7e5e4;
    border-radius: 10px;
    padding: 0.55rem 1.2rem;
    color: #44403c;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.18s;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
div[data-testid="stRadio"] > div > label:hover {
    border-color: #f59e0b;
    color: #92400e;
    box-shadow: 0 2px 8px rgba(245,158,11,0.15);
}

/* 텍스트 에리어 */
.stTextArea > div > div > textarea {
    background: #ffffff !important;
    border: 1.5px solid #e7e5e4 !important;
    border-radius: 12px !important;
    color: #1c1917 !important;
    font-family: 'Pretendard', 'Noto Sans KR', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.75 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: #f59e0b !important;
    box-shadow: 0 0 0 3px rgba(245,158,11,0.12) !important;
}
.stTextArea label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #78716c;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* 메인 버튼 */
.stButton > button {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Pretendard', 'Noto Sans KR', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    padding: 0.65rem 1.5rem !important;
    transition: all 0.2s !important;
    box-shadow:
