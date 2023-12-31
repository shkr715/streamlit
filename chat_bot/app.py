# 以下を「app.py」に書き込み
import streamlit as st
from streamlit_chat import message
import openai

openai.api_key = st.secrets.OPENAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは関西弁でどんなことにも返答する優秀なおっちゃんAIです。"}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去

# ユーザーインターフェイスの構築
# セッションステートに messages リストを初期化する
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.condition = ""

#タイトル
st.title("関西のおっちゃんChatBot")

st.text_area("関西弁で返します", key="user_input")
# 送信ボタンがクリックするとOpenAIに問い合わせる
st.button("送信", on_click=communicate)

# messagesをループして、質問と回答を表示
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    #右側に表示する回答はisUserをTrueとする。
    message((msg["content"]), is_user = msg["role"] == "assistant")
