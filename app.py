# import streamlit as st
# from pathlib import Path
# from langchain_groq import ChatGroq
# from langchain.agents import create_sql_agent
# from langchain.agents.agent_types import AgentType
# from langchain.callbacks import StreamlitCallbackHandler
# from langchain.agents.agent_toolkits import SQLDatabaseToolkit
# import sqlite3
# from langchain.sql_database import SQLDatabase
# from sqlalchemy import create_engine
# st.set_page_config(page_title='Langchain:Chat with SQL DB',page_icon='🐦')
# st.title('🐦 Langchain: Chat with SQL db')

# LOCALDB='USE_LOCALDB'
# MYSQL='USE_MYSQL'

# radio_opt=['Use SQLLite3 database-Student.db','Connect to your SQL DB']
# selected_opt=st.sidebar.radio(label='Choose the DB with which you want to chat',options=radio_opt)
# if radio_opt.index(selected_opt)==1:
#     db_uri=MYSQL
#     mysql_host=st.sidebar.text_input('Provide mysql host')
#     mysql_user=st.sidebar.text_input('MySQL user')
#     mysql_password=st.sidebar.text_input('MySQL password',type='password')
#     mysql_db=st.sidebar.text_input('MySQL database')
# else:
#     db_uri=LOCALDB

# # import os
# # from dotenv import load_dotenv
# # load_dotenv()
# # api_key = os.getenv("GROK_API_KEY")
# api_key=st.sidebar.text_input(label='Groq_api_key',type='password')
# if not db_uri:
#     st.info("Please enter the information and the URI")

# if not api_key:
#     st.info('Please add the groq api key')
#     st.stop()

# llm=ChatGroq(groq_api_key=api_key,model='llama3-8b-8192',streaming=True)
# @st.cache_resource(ttl='2h')
# def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
#     if db_uri==LOCALDB:
#         dbfilepath=(Path(__file__).parent/'student.db').absolute()
#         print(dbfilepath)
#         creator=lambda:sqlite3.connect(f'file:{dbfilepath}?mode=ro',uri=True)
#         return SQLDatabase(create_engine('sqlite:///student.db',creator=creator))
#     elif db_uri==MYSQL:
#         if not (mysql_db and mysql_host and mysql_password and mysql_user):
#             st.error('Please provide all connection details correctly.')
#             st.stop()
#         return SQLDatabase(create_engine(f'mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}'))


# if db_uri==MYSQL:
#     db=configure_db(db_uri,mysql_host,mysql_user,mysql_password,mysql_db)
# else:
#     db=configure_db(db_uri)

# toolkit=SQLDatabaseToolkit(db=db,llm=llm)
# agent=create_sql_agent(
#     llm=llm,
#     toolkit=toolkit,
#     verbose=True,
#     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    
# )

# if 'messages' not in st.session_state or st.sidebar.button('Clear message history'):
#     st.session_state['messages']=[{'role':'assistant','content':'How can I help you'}]

# for msg in st.session_state.messages:
#     st.chat_message(msg['role']).write(msg['content'])

# user_query=st.chat_input(placeholder='Ask anything from the database')

# if user_query:
#     st.session_state.messages.append({'role':'user','content':user_query})
#     st.chat_message('user').write(user_query)

#     with st.chat_message('assistant'):
#         streamlit_callback=StreamlitCallbackHandler(st.container())
#         response=agent.run(user_query,callbacks=[streamlit_callback])
#         st.session_state.messages.append({'role':'assistant','content':response})
#         st.write(response)

import streamlit as st
from pathlib import Path
from langchain_groq import ChatGroq
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
import sqlite3

# ---------------- Streamlit UI Setup -------------------
st.set_page_config(page_title='Langchain: Chat with SQL DB', page_icon='🐦')
st.title('🐦 Langchain: Chat with SQL DB')

# ---------------- User Options -------------------
LOCALDB = 'USE_LOCALDB'
MYSQL = 'USE_MYSQL'

radio_opt = ['Use SQLite3 database - student.db', 'Connect to your MySQL DB']
selected_opt = st.sidebar.radio('Choose the DB to chat with', options=radio_opt)

# DB Configuration
if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input('MySQL Host')
    mysql_user = st.sidebar.text_input('MySQL User')
    mysql_password = st.sidebar.text_input('MySQL Password', type='password')
    mysql_db = st.sidebar.text_input('MySQL Database')
else:
    db_uri = LOCALDB

# Groq API Key
api_key = st.sidebar.text_input(label='Groq API Key', type='password')

if not api_key:
    st.info('Please provide the Groq API key.')
    st.stop()

# ---------------- Database Config -------------------
@st.cache_resource(ttl='2h')
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent / 'student.db').absolute()
        if not dbfilepath.exists():
            st.error(f"Database file not found: {dbfilepath}")
            st.stop()
        engine = create_engine(
            f"sqlite:///{dbfilepath}",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        return SQLDatabase(engine)
    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please fill in all MySQL credentials.")
            st.stop()
        uri = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
        return SQLDatabase(create_engine(uri))

# ---------------- LLM + Agent Setup -------------------
llm = ChatGroq(groq_api_key=api_key, model='llama3-8b-8192', streaming=True)

if db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = configure_db(db_uri)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

# ---------------- Chat Interface -------------------
if 'messages' not in st.session_state or st.sidebar.button('Clear chat'):
    st.session_state['messages'] = [{'role': 'assistant', 'content': 'How can I help you?'}]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

user_query = st.chat_input("Ask your database anything...")

if user_query:
    st.session_state.messages.append({'role': 'user', 'content': user_query})
    st.chat_message('user').write(user_query)

    with st.chat_message('assistant'):
        try:
            streamlit_callback = StreamlitCallbackHandler(st.container())
            response = agent.run(user_query, callbacks=[streamlit_callback])
        except Exception as e:
            response = f"⚠️ Error: {e}"
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.write(response)
    