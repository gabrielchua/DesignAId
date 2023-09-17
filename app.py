import streamlit as st
import extra_streamlit_components as stx
# from annotated_text import annotated_text, parameters
from streamlit_option_menu import option_menu

##########
st.set_page_config(
    page_title="designAId",
    page_icon="🧑‍🎨",
    layout="wide",
    initial_sidebar_state="auto"
)

if 'menu_option' not in st.session_state:
    st.session_state['menu_option'] = 0

if 'generated' not in st.session_state:
    st.session_state['generated'] = 0

if st.session_state.get('fwd_btn', False):
    st.session_state['menu_option'] = (st.session_state.get('menu_option',0) + 1) % 5
    manual_select = st.session_state['menu_option']
else:
    manual_select = None

nav_emoji = {
    "Empathise":"❤️", 
    "Define": "🖊️", 
    "Ideate": "💡", 
    "Prototype": "🔧",
    "Test": "✅"}

##########
st.markdown("# Design:violet[AI]d")
st.caption("An AI-powered Design Thinking companion")

with st.expander("For Demo only"):
    st.write("For the purposes of this demo, we pre-filled the fields below.")
    st.button("Quick Start")

##########

if st.session_state['generated'] == 0:
    col1, col2 = st.columns(2)
    col1.markdown("#### Please fill up the below")
    q1 = col1.text_input("Q1: What is your role?")
    q2= col1.text_input("Q2: What is your target audience?")
    q3 = col1.text_input("Q3: What is the problem? How is the target audience affected on a day-to-day basis?")
    q4 = col1.text_input("Q4: What are some possible root causes?")
    col2.markdown("#### Optional Questions")
    q5 = col2.text_input("Q5: What are your prelim solutions?")
    q6 = col2.text_input("Q6: Have there been previous attempts?")
    q7 = col2.text_input("Q7: What does success look like?")
    q8_file = col2.file_uploader("Q8: Upload any available user interviews")
    st.session_state["user_inputs"] = [q1, q2, q3, q4, q5, q6, q7, q8_file]
    

    st.divider()
    pressed = st.button("Generate")
    if pressed & (q1 == "" or q2 == "" or q3 =="" or q4 ==""):
            st.error("Please complete fill up q1 to q4.")
    elif pressed:
            st.session_state['generated'] = 1
            st.experimental_rerun()


else:
    tab1, tab2, tab3, tab4 = st.tabs(["Results", "Download Report", "Your Input", "Restart"])    

    with tab1:
        col1, col2 = st.columns((2,8))

        with col1: 
            selected_step = option_menu("Stages", ["Empathise", "Define", "Ideate", "Prototype", "Test"], 
                icons=['heart', 'pen', "lightbulb", 'diagram-2', 'check-circle'], 
                orientation="vertical",
                manual_select=manual_select,
                key='menu_4')
            
        with col2: 
            st.markdown(f"## {nav_emoji[selected_step]} {selected_step}")
            if st.session_state['menu_option'] == 0:
                st.info("A")
            elif st.session_state['menu_option'] == 1:
                st.info("B")
            elif st.session_state['menu_option'] == 2:
                st.info("C")
            elif st.session_state['menu_option'] == 3:
                st.info("D")
            elif st.session_state['menu_option'] == 4:
                st.info("E")
            st.button("Done", key='fwd_btn')
    
    with tab2:
        st.download_button("Download Report", "test.csv")

    with tab3:
        col3, col4 = st.columns(2)
        col3.markdown(f"**What is your role:** {st.session_state['user_inputs'][0]}")
        col3.markdown(f"**Who are you trying to help:** {st.session_state['user_inputs'][1]}")
        col3.markdown(f"**What is the problem:** {st.session_state['user_inputs'][2]}")
        col3.markdown(f"**What are some possible root causes:** {st.session_state['user_inputs'][3]}")
        col4.markdown(f"**Any prelim solutions:** {st.session_state['user_inputs'][4]}")

    with tab4:
        st.error("⚠️ This step is not reversible ⚠️")
        if st.button("Restart"):
            st.session_state['generated'] = 0
            st.experimental_rerun()

# st.divider()

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Accept user input
# if prompt := st.chat_input("What is up?"):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     # Display assistant response in chat message container
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""

#############
# annotated_text(
#     "An ",
#     ("AI", "", "#8ef"),
#     "-powered",
#     ("Design Thinking", "", "#afa") ,
#     " companion 🧑‍🎨")


# parameters.SHOW_LABEL_SEPARATOR = False
# parameters.BORDER_RADIUS = 0
# parameters.PADDING = "0 0.3rem"