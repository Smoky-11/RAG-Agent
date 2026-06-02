import streamlit as st
from agent.react_agent import ReactAgent
import time

st.title('扫地机器人客服')
st.divider()

if 'agent' not in st.session_state:
    st.session_state['agent']=ReactAgent()

if 'message' not in st.session_state:
    st.session_state['message']=[]

for message in st.session_state['message']:
    st.chat_message(message['role']).write(message['content'])

prompt=st.chat_input()  #用户输入提问

if prompt:
    st.chat_message('user').write(prompt)
    st.session_state['message'].append({'role':'user','content':prompt})


    res_message=[]
    with st.spinner('正在思考中……'):
        res=st.session_state['agent'].execute_stream(prompt)

        def capture(generator,cache):
            for chunk in generator:
                cache.append(chunk)

                for i in chunk:
                    time.sleep(0.01)
                    yield i
    
        st.chat_message('assistant').write_stream(capture(res,res_message))
    st.session_state['message'].append({'role':"assistant","content":res_message[-1]})
    st.rerun()