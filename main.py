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
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&display=swap');

/* 전체 배경 */
.stApp {
    background: #0d0d0f;
    font-family: 'DM Mono', monospace;
}

/* 메인 컨테이너 */
.block-container {
    max-width: 780px;
    padding-top: 3rem;
    padding-bottom: 4rem;
}

/* 헤더 */
.app-header {
    text-align: center;
    margin-bottom: 2.5rem;
}
.app-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    color: #f0ede6;
    letter-spacing: -0.02em;
    margin: 0;
    line-height: 1;
}
.app-header .tagline {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #5a5a6e;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 0.6rem;
}

/* 모델 선택 라디오 */
div[data-testid="stRadio"] > label {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #8888a0;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
div[data-testid="stRadio"] > div {
    gap: 1rem;
    margin-top: 0.4rem;
}
div[data-testid="stRadio"] > div > label {
    background: #16161e;
    border: 1px solid #2a2a38;
    border-radius: 6px;
    padding: 0.5rem 1.1rem;
    color: #c8c8d8;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all 0.2s;
}
div[data-testid="stRadio"] > div > label:hover {
    border-color: #c8a96e;
    color: #f0ede6;
}
div[data-testid="stRadio"] > div > label[data-baseweb="radio"] {
    background: #1e1e2e;
}

/* 텍스트 에리어 */
.stTextArea > div > div > textarea {
    background: #13131b !important;
    border: 1px solid #2a2a38 !important;
    border-radius: 8px !important;
    color: #e0ddd6 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.88rem !important;
    resize: vertical;
}
.stTextArea > div > div > textarea:focus {
    border-color: #c8a96e !important;
    box-shadow: 0 0 0 2px rgba(200,169,110,0.12) !important;
}
.stTextArea label {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #8888a0;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* 버튼 */
.stButton > button {
    background: #c8a96e !important;
    color: #0d0d0f !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.55rem 2rem !important;
    transition: all 0.2s !important;
    width: 100%;
}
.stButton > button:hover {
    background: #e0c080 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(200,169,110,0.25) !important;
}
.stButton > button:active {
    transform: translateY(0);
}

/* 답변 박스 */
.answer-box {
    background: #13131b;
    border: 1px solid #2a2a38;
    border-left: 3px solid #c8a96e;
    border-radius: 8px;
    padding: 1.4rem 1.6rem;
    margin-top: 1.5rem;
    color: #d8d5ce;
    font-family: 'DM Mono', monospace;
    font-size: 0.88rem;
    line-height: 1.85;
    white-space: pre-wrap;
    word-break: break-word;
}

/* 사용량 카드 */
.usage-row {
    display: flex;
    gap: 0.75rem;
    margin-top: 1rem;
}
.usage-card {
    flex: 1;
    background: #16161e;
    border: 1px solid #2a2a38;
    border-radius: 6px;
    padding: 0.75rem 1rem;
    text-align: center;
}
.usage-card .val {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: #c8a96e;
    line-height: 1;
}
.usage-card .lbl {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #5a5a6e;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

/* 오류 박스 */
.error-box {
    background: #1e0f0f;
    border: 1px solid #6e2a2a;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: #e07070;
    font-size: 0.82rem;
    margin-top: 1rem;
}

/* 구분선 */
hr {
    border: none;
    border-top: 1px solid #1e1e2a;
    margin: 2rem 0;
}

/* 스피너 색상 */
.stSpinner > div {
    border-top-color: #c8a96e !important;
}
</style>
""", unsafe_allow_html=True)

# ── 헤더 ─────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>✦ Claude Chat</h1>
    <div class="tagline">Powered by Anthropic API</div>
</div>
""", unsafe_allow_html=True)

# ── API 키 로드 ───────────────────────────────────────────────
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except (KeyError, FileNotFoundError):
    st.markdown("""
    <div class="error-box">
    ⚠ <strong>API 키가 설정되지 않았습니다.</strong><br>
    Streamlit Cloud → Settings → Secrets 에서<br>
    <code>ANTHROPIC_API_KEY = "sk-ant-..."</code> 를 추가해 주세요.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

client = anthropic.Anthropic(api_key=api_key)

# ── 모델 선택 ─────────────────────────────────────────────────
MODEL_OPTIONS = {
    "Claude Sonnet 4.6  —  빠르고 효율적": "claude-sonnet-4-6",
    "Claude Opus 4.6  —  강력하고 정교함": "claude-opus-4-6",
}

st.markdown("<br>", unsafe_allow_html=True)
model_label = st.radio(
    "모델 선택",
    list(MODEL_OPTIONS.keys()),
    horizontal=True,
    index=0,
)
selected_model = MODEL_OPTIONS[model_label]

st.markdown("<hr>", unsafe_allow_html=True)

# ── 입력 ──────────────────────────────────────────────────────
question = st.text_area(
    "질문 입력",
    placeholder="무엇이든 물어보세요...",
    height=130,
    key="question_input",
)

col_btn, col_clear = st.columns([3, 1])
with col_btn:
    submit = st.button("✦ 답변 생성", use_container_width=True)
with col_clear:
    clear = st.button("초기화", use_container_width=True)

if clear:
    st.session_state.pop("last_answer", None)
    st.session_state.pop("last_usage", None)
    st.session_state.pop("last_model", None)
    st.rerun()

# ── API 호출 ──────────────────────────────────────────────────
if submit:
    if not question.strip():
        st.warning("질문을 입력해 주세요.")
    else:
        with st.spinner("AI가 생각하는 중..."):
            try:
                t0 = time.time()
                response = client.messages.create(
                    model=selected_model,
                    max_tokens=2048,
                    messages=[{"role": "user", "content": question.strip()}],
                )
                elapsed = time.time() - t0

                answer = response.content[0].text
                usage = response.usage

                st.session_state["last_answer"] = answer
                st.session_state["last_usage"] = {
                    "input": usage.input_tokens,
                    "output": usage.output_tokens,
                    "total": usage.input_tokens + usage.output_tokens,
                    "elapsed": elapsed,
                    "model": selected_model,
                }

            except anthropic.AuthenticationError:
                st.markdown("""
                <div class="error-box">
                🔑 <strong>인증 오류:</strong> API 키가 올바르지 않습니다. Secrets를 확인해 주세요.
                </div>
                """, unsafe_allow_html=True)
            except anthropic.RateLimitError:
                st.markdown("""
                <div class="error-box">
                ⏳ <strong>요청 한도 초과:</strong> 잠시 후 다시 시도해 주세요.
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                ❌ <strong>오류 발생:</strong> {str(e)}
                </div>
                """, unsafe_allow_html=True)

# ── 결과 출력 ─────────────────────────────────────────────────
if "last_answer" in st.session_state:
    answer = st.session_state["last_answer"]
    usage = st.session_state["last_usage"]

    st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="usage-row">
        <div class="usage-card">
            <div class="val">{usage['input']:,}</div>
            <div class="lbl">입력 토큰</div>
        </div>
        <div class="usage-card">
            <div class="val">{usage['output']:,}</div>
            <div class="lbl">출력 토큰</div>
        </div>
        <div class="usage-card">
            <div class="val">{usage['total']:,}</div>
            <div class="lbl">총 토큰</div>
        </div>
        <div class="usage-card">
            <div class="val">{usage['elapsed']:.1f}s</div>
            <div class="lbl">응답 시간</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:right; margin-top:0.6rem; font-size:0.68rem;
                color:#3a3a50; font-family:'DM Mono',monospace; letter-spacing:0.08em;">
        모델: {usage['model']}
    </div>
    """, unsafe_allow_html=True)
