import streamlit as st
import google.generativeai as genai

# data
url1 = "https://raw.githubusercontent.com/aritsarann/chat_with_gemini/refs/heads/main/transactions.csv"
url2 = "https://raw.githubusercontent.com/aritsarann/chat_with_gemini/refs/heads/main/data_dict.csv"

transaction_df = pd.read_csv(url1)
data_dict_df = pd.read_csv(url2)

df_name = 'transaction_df'
example_record = transaction_df.head(2).to_string()
data_dict_text = '\n'.join('- ' + data_dict_df['column_name'] +
                           ': ' +data_dict_df['data_type'] +
                           '. ' +data_dict_df['description'])



try:
    key = st.secrets['gemini_api_key']
    
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
    st.title('Gemini Pro Test')

    def role_to_streamlit(role:str) -> str:
        if role == 'model':
            return 'assistant'
        else:
            return role
        
    for message in st.session_state.chat.history:
        with st.chat_message(role_to_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    if prompt := st.chat_input("Text Here"):
        st.chat_message('user').markdown(prompt)
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message('assistant'):
            st.markdown(response.text)
    
except Exception as e :
    st.error(f'An error occurred {e}')
