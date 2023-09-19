import streamlit as st
import extra_streamlit_components as stx
from streamlit_option_menu import option_menu
from fpdf import FPDF
import base64
from utils.pdf import sanitise_text, multi_cell, create_download_link
from utils.clarifai import query_gpt4
from utils.prompts import generate_dt_prompt

def find_non_encodable_characters(text):
    for char in text:
        try:
            char.encode('latin-1')
        except UnicodeEncodeError:
            st.write(f"Cannot encode character: {char} (U+{ord(char):04X})")


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

if 'autofilled' not in st.session_state:
    st.session_state['autofilled'] = False

if st.session_state.get('fwd_btn', False):
    st.session_state['menu_option'] = (st.session_state.get('menu_option',0) + 1) % 5
    manual_select = st.session_state['menu_option']
else:
    manual_select = None

demo_values = [f"q{i}_default_val" for i in range(1, 8)]

for demo_val in demo_values:
    if demo_val not in st.session_state:
        st.session_state[demo_val] = ""

nav_emoji = {
    "Empathise":"❤️", 
    "Define": "🖊️", 
    "Ideate": "💡", 
    "Prototype": "🔧",
    "Test": "✅"}

DT_STAGES = ["EMPATHISE", "DEFINE", "IDEATE", "PROTOTYPE", "TEST"]

##########
st.markdown("# Design:violet[AI]d")
st.caption("An AI-powered Design Thinking companion")

def load_dt_tool():
    for stage in DT_STAGES:
        st.session_state[f"gpt_results_{stage}"] = query_gpt4(generate_dt_prompt("EMPATHISE"))
    st.session_state['generated'] = 1
    st.experimental_rerun()

##########
if st.session_state['generated'] == 0:

    with st.expander("Demo Quick Start"):
        st.write("For the purposes of this demo, we can autofill the fields below.")
        colA, colB, _ = st.columns((2,2,10))
        if colA.button("Autofill"):
            st.session_state['q1_default_val'] = "I'm a Product Designer with a focus on developing assistive technology tools to enhance the daily lives of individuals with disabilities."
            st.session_state['q2_default_val'] = "Our primary target audience includes individuals with physical impairments, specifically those who have mobility challenges. This ranges from elderly individuals with reduced dexterity to younger individuals who might have been born with or acquired physical limitations."
            st.session_state['q3_default_val'] = "Many daily tasks are challenging for our audience due to a lack of accessible devices. This hinders their independence and confidence daily."
            st.session_state['q4_default_val'] = "Mainstream design often overlooks disability needs, perceptions of high development costs, and a lack of empathy for unique challenges."
            st.session_state['q5_default_val'] = "Modular tools for customization, voice and gesture-controlled devices, and partnerships with therapists for insight."
            st.session_state['q6_default_val'] = "Yes, but they were often too specialized, expensive, or lacked aesthetics and durability."
            st.session_state['q7_default_val'] = "Increased user independence, high adoption rates, and positive user feedback indicating enhanced daily living."
            st.session_state['autofilled'] = True
        btn_generate = colB.button("Generate Now")
        if btn_generate & (not st.session_state['autofilled']):
            colA.error("Please click 'Autofill'")
        elif btn_generate & st.session_state['autofilled']:
            with st.spinner('Please give me about 3-5 mins to think about your project...'):
                load_dt_tool()

    col1, col2 = st.columns(2)
    col1.markdown("#### Please fill up the below")
    q1 = col1.text_area("Q1: What is your role?", 
                         value=f"{st.session_state['q1_default_val']}")
    q2= col1.text_area("Q2: Who is your target audience?",
                         value=f"{st.session_state['q2_default_val']}")
    q3 = col1.text_area("Q3: What is the problem? How is the target audience affected on a day-to-day basis?",
                        value=f"{st.session_state['q3_default_val']}")
    q4 = col1.text_area("Q4: What are some possible root causes?",
                        value=f"{st.session_state['q4_default_val']}")
    col2.markdown("#### Optional Questions")
    q5 = col2.text_area("Q5: What are your prelim solutions?",
                        value=f"{st.session_state['q5_default_val']}")
    q6 = col2.text_area("Q6: Have there been previous attempts?",
                        value=f"{st.session_state['q6_default_val']}")
    q7 = col2.text_area("Q7: What does success look like?",
                        value=f"{st.session_state['q7_default_val']}")
    q8_file = col2.file_uploader("Q8: Upload any available user interviews")
    st.session_state["user_inputs"] = [q1, q2, q3, q4, q5, q6, q7, q8_file]
    
    st.divider()
    pressed = st.button("Generate")
    if pressed & (q1 == "" or q2 == "" or q3 =="" or q4 ==""):
            st.error("Please complete fill up q1 to q4.")
    elif pressed:
        with st.spinner('Please give me some time to think...'):
            load_dt_tool()


elif st.session_state['generated'] == 1:
    tab1, tab2, tab3, tab4 = st.tabs(["Results", "Download Report", "Your Input", "Restart"])    

    with tab1:
        col1, col2 = st.columns((2,8))

        with col1: 
            selected_step = option_menu("Stages", ["Empathise", "Define", "Ideate", "Prototype", "Test"], 
                icons=['heart', 'pen', "lightbulb", 'wrench', 'check-circle'], 
                orientation="vertical",
                manual_select=manual_select,
                key='menu_4')
            
        with col2: 
            st.markdown(f"## {nav_emoji[selected_step]} {selected_step}")
            if (st.session_state['menu_option'] == 0) or (selected_step == "Empathise"):
                st.info(st.session_state[f'gpt_results_{selected_step.upper()}'])
            elif (st.session_state['menu_option'] == 1) or (selected_step == "Define"):
                st.info(st.session_state[f'gpt_results_{selected_step.upper()}'])
            elif (st.session_state['menu_option'] == 2) or (selected_step == "Ideate"):
                st.info(st.session_state[f'gpt_results_{selected_step.upper()}'])
            elif (st.session_state['menu_option'] == 3) or (selected_step == "Prototype"):
                st.info(st.session_state[f'gpt_results_{selected_step.upper()}'])
            elif (st.session_state['menu_option'] == 4) or (selected_step == "Test"):
                st.info(st.session_state[f'gpt_results_{selected_step.upper()}'])
            st.button("Next", key='fwd_btn')
    
    with tab2:
        if st.button("Generate Report"):
            pdf = FPDF()
            pdf.set_left_margin(20)  # Set left margin to 20mm (or whatever value you desire)
            pdf.set_top_margin(20)   # Set top margin to 30mm (or whatever value you desire)
            pdf.add_page()

            # Add long text with automatic line breaks
            multi_cell(pdf, 160, 10, "Your Report", 'Arial', 'B', 16)  # 190 is nearly the width of an A4 paper
            multi_cell(pdf, 160, 10, "", 'Arial', 'B', 16)  # 190 is nearly the width of an A4 paper
            multi_cell(pdf, 160, 10, "Original Input", 'Arial', 'U', 14)  # 190 is nearly the width of an A4 paper

            for qn_num, demo_val in enumerate(demo_values):
                value = st.session_state.get(demo_val, "")
                multi_cell(pdf, 160, 10, f"Q{qn_num+1}: {value}", 'Arial', '', 11)
                multi_cell(pdf, 160, 10, "", 'Arial', '', 11)

            for stage_num, stage in enumerate(DT_STAGES):
                pdf.add_page()
                multi_cell(pdf, 160, 10, f"Stage {stage_num+1}: {stage}", 'Arial', 'U', 14)  # 190 is nearly the width of an A4 paper
                results = st.session_state[f'gpt_results_{stage}']
                multi_cell(pdf, 160, 10, sanitise_text(results), 'Arial', '', 11)  # 190 is nearly the width of an A4 paper

            html = create_download_link(pdf.output(dest="S"), "report")

            st.toast('Your report has been generated!', icon='😍')
            
            st.markdown(html, unsafe_allow_html=True)

    with tab3:
        col3, col4 = st.columns(2)
        col3.markdown(f"**What is your role:** {st.session_state['user_inputs'][0]}")
        col3.markdown(f"**Who are you trying to help:** {st.session_state['user_inputs'][1]}")
        col3.markdown(f"**What is the problem:** {st.session_state['user_inputs'][2]}")
        col3.markdown(f"**What are some possible root causes:** {st.session_state['user_inputs'][3]}")
        col4.markdown(f"**Any prelim solutions:** {st.session_state['user_inputs'][4]}")
        col4.markdown(f"**Have there been previous attempts:** {st.session_state['user_inputs'][5]}")
        col4.markdown(f"**What does success look like:** {st.session_state['user_inputs'][6]}")

    with tab4:
        st.error("⚠️ This step is not reversible ⚠️")
        if st.button("Restart"):
            st.session_state['generated'] = 0
            st.experimental_rerun()