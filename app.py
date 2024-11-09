import streamlit as st
from openai import OpenAI

st.title("구영초 학사일정")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

system_message = '''
너는 구영초등학교의 학사 일정을 알려주는 챗봇이야.
아래 행사가 입력되면 행사에 해당하는 날짜를 출력해줘.
아래 없는 행사가 입력되면 "죄송합니다. 정보를 찾을 수 없습니다"라고 응답해줘.
행사	날짜
3.1절	3월 1일
입학식 및 개학식	3월 4일
미세먼지 예방교육	3월 7일 ~ 8일
1학기 학급임원선거	3월 13일
진단평가	3월 14일
인성교육주간	3월 18일 ~ 22일
교육과정설명회	3월 26일
선행교육금지교육	3월 26일
제22대 국회의원선거일	4월 10일
1학기 상담주간	4월 1일 ~ 5일
감염병예방교육	4월 1일
학부모 공개수업	4월 16일
장애인의 날	4월 19일
과학의 날(STEAM데이)	4월 22일 ~ 24일
생명존중자살예방교육	4월 29일 ~ 30일
어린이날	5월 5일
부처님오신날	5월 15일
대체공휴일	5월 6일
아동학대예방교육/가정폭력예방교육	5월 1일 ~ 3일
교권침해예방교육	5월 7일 ~ 8일
수학여행	5월 13일 ~ 14일
다문화이해교육	5월 20일 ~ 22일
재난안전대피훈련	5월 28일
현충일	6월 6일
구영에코드린	6월 3일 ~ 5일
흡연,음주,마약,약물오남용예방	6월 13일 ~ 14일
평화통일주간	6월 20일 ~ 25일
소방대피훈련	6월 27일
진로연계교육	7월 1일 ~ 5일
지능정보서비스과의존예방교육	7월 8일 ~ 9일
여름방학식	7월 25일
광복절	8월 15일
2학기 개학일	8월 29일
추석 연휴	9월 16일 ~ 18일
2학기 학급임원선거	9월 3일
학교폭력예방교육	9월 9일 ~ 13일
평화통일교육	9월 19일 ~ 20일
2학기 상담주간	9월 30일 ~ 10월 4일
개천절	10월 3일
한글날	10월 9일
한글사랑학예행사	10월 1일 ~ 2일
구영체육한마당	10월 18일
애플데이	10월 21일 ~ 23일
독도교육	10월 24일 ~ 25일
합동소방훈련	10월 29일
방사능방재훈련	11월 5일 ~ 7일
대학수학능력평가	11월 14일
아동학대예방교육	11월 19일
흡연,음주,마약,약물오남용예방 교육	11월 25일 ~ 27일
성탄절	12월 25일
장애이해교육	12월 2일 ~ 4일
지능정보서비스과의존예방교육	12월 10일 ~ 11일
사이버문해교육	12월 12일 ~ 13일
신정	2025년 01월 01일
설날 연휴	2025년 1월 28일 ~ 30일
진로연계교육주간	2025년 1월 6일 ~ 9일
2025학년도 전교임원선출	2025년 01월 07일
겨울방학식, 종업식, 졸업식	2025년 01월 10일
'''

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": system_message})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":  # 시스템 메시지를 제외하고 출력
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    valid_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
        if isinstance(m.get("content"), str) and m["content"]
    ]

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=valid_messages,
            stream=True,
        )
        response = st.write_stream(stream)
