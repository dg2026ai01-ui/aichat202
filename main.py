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
    box-shadow: 0 3px 10px rgba(217,119,6,0.3) !important;
    width: 100%;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #d97706 0%, #b45309 100%) !important;
    transform: translateY(-1px);
    box-shadow: 0 5px 16px rgba(217,119,6,0.4) !important;
}
.stButton > button:active {
    transform: translateY(0);
}

/* 초기화 버튼 (두 번째 컬럼) */
div[data-testid="column"]:nth-child(2) .stButton > button {
    background: #ffffff !important;
    color: #78716c !important;
    border: 1.5px solid #e7e5e4 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button:hover {
    background: #fafaf9 !important;
    color: #44403c !important;
    border-color: #d6d3d1 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}

/* 답변 박스 */
.answer-box {
    background: #ffffff;
    border: 1.5px solid #fde68a;
    border-left: 5px solid #f59e0b;
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    margin-top: 1.5rem;
    color: #1c1917;
    font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
    font-size: 0.95rem;
    line-height: 1.9;
    white-space: pre-wrap;
    word-break: break-word;
    box-shadow: 0 2px 12px rgba(234,179,8,0.08), 0 1px 4px rgba(0,0,0,0.04);
}

/* 사용량 카드 */
.usage-row {
    display: flex;
    gap: 0.75rem;
    margin-top: 1rem;
}
.usage-card {
    flex: 1;
    background: #ffffff;
    border: 1.5px solid #fde68a;
    border-radius: 12px;
    padding: 0.9rem 0.75rem;
    text-align: center;
    box-shadow: 0 1px 4px rgba(234,179,8,0.1);
}
.usage-card .val {
    font-size: 1.45rem;
    font-weight: 700;
    color: #d97706;
    line-height: 1;
    letter-spacing: -0.02em;
}
.usage-card .lbl {
    font-size: 0.68rem;
    font-weight: 600;
    color: #a8a29e;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-top: 0.35rem;
}

/* 오류 박스 */
.error-box {
    background: #fff7ed;
    border: 1.5px solid #fed7aa;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #c2410c;
    font-size: 0.85rem;
    margin-top: 1rem;
}

/* 구분선 */
hr {
    border: none;
    border-top: 1.5px solid #f5f5f4;
    margin: 1.8rem 0;
}

/* 스피너 */
.stSpinner > div {
    border-top-color: #f59e0b !important;
}

/* 경고 메시지 */
.stWarning {
    background: #fffbeb;
    border-color: #fde68a;
    color: #92400e;
    border-radius: 10px;
}

/* ── 멀티턴 채팅 말풍선 ── */
.chat-history {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.chat-bubble {
    max-width: 88%;
    padding: 0.85rem 1.1rem;
    border-radius: 16px;
    font-size: 0.92rem;
    line-height: 1.75;
    word-break: break-word;
    white-space: pre-wrap;
}
/* 사용자 말풍선 — 오른쪽 */
.chat-bubble.user {
    align-self: flex-end;
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: #ffffff;
    border-bottom-right-radius: 4px;
    box-shadow: 0 2px 8px rgba(217,119,6,0.25);
}
/* AI 말풍선 — 왼쪽 */
.chat-bubble.assistant {
    align-self: flex-start;
    background: #ffffff;
    color: #1c1917;
    border: 1.5px solid #fde68a;
    border-left: 4px solid #f59e0b;
    border-bottom-left-radius: 4px;
    box-shadow: 0 2px 8px rgba(234,179,8,0.08);
}
.chat-bubble .bubble-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    opacity: 0.7;
    margin-bottom: 0.3rem;
}
.chat-bubble.user .bubble-label { color: #fff8e1; }
.chat-bubble.assistant .bubble-label { color: #a8a29e; }

/* 채팅 히스토리 구분선 */
.chat-divider {
    border: none;
    border-top: 1.5px dashed #fde68a;
    margin: 0.5rem 0 1.2rem;
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

# ── 대화 히스토리 초기화 ──────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []   # [{role, content, usage?, elapsed?}]

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
    st.session_state["chat_history"] = []   # 대화 히스토리도 초기화
    st.rerun()

# ── 시스템 프롬프트 (이모지 포함 지시) ──────────────────────────
SYSTEM_PROMPT = """당신은 친절하고 유익한 AI 어시스턴트입니다.

답변 작성 규칙:
1. 답변 맨 첫 줄에 질문의 주제나 분위기에 딱 맞는 이모지를 2~4개 나란히 배치하세요.
   예) 요리 질문: 🍳🥘👨‍🍳✨  /  여행 질문: ✈️🗺️🌍🎒  /  과학 질문: 🔬⚗️🧬💡
2. 답변 본문에도 각 항목이나 중요 포인트 앞에 적절한 이모지를 자연스럽게 삽입하세요.
3. 이모지는 내용과 반드시 연관되어야 하며, 답변을 더 읽기 쉽고 생동감 있게 만들어야 합니다.
4. 이모지를 과도하게 남용하지 말고, 핵심 위치에만 전략적으로 사용하세요.
5. 한국어로 명확하고 친절하게 답변하세요.
6. 마크다운 형식(**, ##, - 등)을 활용해 구조적으로 답변하세요."""

# ── 대화 히스토리 출력 ────────────────────────────────────────
history = st.session_state["chat_history"]

if history:
    st.markdown('<div class="chat-history">', unsafe_allow_html=True)
    for turn in history:
        role = turn["role"]
        content = turn["content"]
        label = "나" if role == "user" else "Claude"
        bubble_class = "user" if role == "user" else "assistant"
        st.markdown(
            f'<div class="chat-bubble {bubble_class}">'
            f'<div class="bubble-label">{label}</div>'
            f'{content}'
            f'</div>',
            unsafe_allow_html=True,
        )
        # AI 답변 아래 사용량 표시
        if role == "assistant" and "usage" in turn:
            u = turn["usage"]
            st.markdown(f"""
            <div class="usage-row">
                <div class="usage-card">
                    <div class="val">{u['input']:,}</div>
                    <div class="lbl">입력 토큰</div>
                </div>
                <div class="usage-card">
                    <div class="val">{u['output']:,}</div>
                    <div class="lbl">출력 토큰</div>
                </div>
                <div class="usage-card">
                    <div class="val">{u['total']:,}</div>
                    <div class="lbl">총 토큰</div>
                </div>
                <div class="usage-card">
                    <div class="val">{u['elapsed']:.1f}s</div>
                    <div class="lbl">응답 시간</div>
                </div>
            </div>
            <div style="text-align:right;margin-top:0.4rem;font-size:0.7rem;color:#a8a29e;">
                모델: {u['model']}
            </div>
            <hr class="chat-divider">
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── API 호출 (스트리밍 + 멀티턴) ──────────────────────────────
if submit:
    if not question.strip():
        st.warning("질문을 입력해 주세요.")
    else:
        # 사용자 메시지를 히스토리에 추가
        st.session_state["chat_history"].append({
            "role": "user",
            "content": question.strip(),
        })

        # API에 보낼 messages 목록 (role/content만 추출)
        api_messages = [
            {"role": t["role"], "content": t["content"]}
            for t in st.session_state["chat_history"]
        ]

        # 사용자 말풍선 즉시 표시
        st.markdown(
            f'<div class="chat-bubble user">'
            f'<div class="bubble-label">나</div>'
            f'{question.strip()}'
            f'</div>',
            unsafe_allow_html=True,
        )

        # AI 답변을 스트리밍으로 출력
        st.markdown(
            '<div class="chat-bubble assistant">'
            '<div class="bubble-label">Claude</div>',
            unsafe_allow_html=True,
        )
        stream_placeholder = st.empty()

        try:
            t0 = time.time()
            full_text = ""
            input_tokens = 0
            output_tokens = 0

            with client.messages.stream(
                model=selected_model,
                max_tokens=2048,
                system=SYSTEM_PROMPT,
                messages=api_messages,
            ) as stream:
                for text_chunk in stream.text_stream:
                    full_text += text_chunk
                    stream_placeholder.markdown(full_text + "▌")

                # 스트림 완료 후 커서 제거
                stream_placeholder.markdown(full_text)
                final_msg = stream.get_final_message()
                input_tokens  = final_msg.usage.input_tokens
                output_tokens = final_msg.usage.output_tokens

            elapsed = time.time() - t0
            st.markdown('</div>', unsafe_allow_html=True)

            usage_data = {
                "input":   input_tokens,
                "output":  output_tokens,
                "total":   input_tokens + output_tokens,
                "elapsed": elapsed,
                "model":   selected_model,
            }

            # 히스토리에 AI 답변 저장
            st.session_state["chat_history"].append({
                "role":    "assistant",
                "content": full_text,
                "usage":   usage_data,
            })

            # 사용량 카드 출력
            st.markdown(f"""
            <div class="usage-row">
                <div class="usage-card">
                    <div class="val">{input_tokens:,}</div>
                    <div class="lbl">입력 토큰</div>
                </div>
                <div class="usage-card">
                    <div class="val">{output_tokens:,}</div>
                    <div class="lbl">출력 토큰</div>
                </div>
                <div class="usage-card">
                    <div class="val">{input_tokens+output_tokens:,}</div>
                    <div class="lbl">총 토큰</div>
                </div>
                <div class="usage-card">
                    <div class="val">{elapsed:.1f}s</div>
                    <div class="lbl">응답 시간</div>
                </div>
            </div>
            <div style="text-align:right;margin-top:0.5rem;font-size:0.72rem;
                        color:#a8a29e;font-family:'Pretendard','Noto Sans KR',sans-serif;">
                모델: {selected_model}
            </div>
            """, unsafe_allow_html=True)

            # 기존 last_answer/last_usage 호환 유지
            st.session_state["last_answer"] = full_text
            st.session_state["last_usage"]  = usage_data

        except anthropic.AuthenticationError:
            st.markdown("""
            <div class="error-box">
            🔑 <strong>인증 오류:</strong> API 키가 올바르지 않습니다. Secrets를 확인해 주세요.
            </div>
            """, unsafe_allow_html=True)
            st.session_state["chat_history"].pop()   # 실패한 user 메시지 제거
        except anthropic.RateLimitError:
            st.markdown("""
            <div class="error-box">
            ⏳ <strong>요청 한도 초과:</strong> 잠시 후 다시 시도해 주세요.
            </div>
            """, unsafe_allow_html=True)
            st.session_state["chat_history"].pop()
        except Exception as e:
            st.markdown(f"""
            <div class="error-box">
            ❌ <strong>오류 발생:</strong> {str(e)}
            </div>
            """, unsafe_allow_html=True)
            st.session_state["chat_history"].pop()

# ── 결과 출력 (히스토리가 없을 때 단독 답변 표시 — 하위 호환) ──
# 멀티턴 모드에서는 위의 채팅 히스토리 루프가 담당하므로
# 아래 블록은 히스토리가 비어있을 때만 표시합니다.
if "last_answer" in st.session_state and not st.session_state["chat_history"]:
    answer = st.session_state["last_answer"]
    usage  = st.session_state["last_usage"]

    st.markdown(
        f'<div class="answer-box">{answer}</div>',
        unsafe_allow_html=True,
    )

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
    <div style="text-align:right; margin-top:0.6rem; font-size:0.72rem;
                color:#a8a29e; font-family:'Pretendard','Noto Sans KR',sans-serif;
                letter-spacing:0.02em;">
        모델: {usage['model']}
    </div>
    """, unsafe_allow_html=True)
