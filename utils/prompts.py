import streamlit as st

def generate_dt_prompt(stage):
    
    prompt = f"""
        Imagine you are a digitial design thinking companion to help users with design thinking. There are 5 stages: EMPATHIZE, DEFINE, IDEATE, PROTOTYPE, TEST

        We are now at the {stage} stage of the Design Thinking process.

        You have received the following inputs from a user:
        {st.session_state['q1_default_val']}
        {st.session_state['q2_default_val']}
        {st.session_state['q3_default_val']}
        {st.session_state['q4_default_val']}
        {st.session_state['q5_default_val']}
        {st.session_state['q6_default_val']}
        {st.session_state['q7_default_val']}

        Specific to the {stage} stage, provide some commentary about the importance of this step and guiding questions the participant should think about.

        Suggest common design thinking frameworks that may be relevant to the {stage} stage. Your commenary can leverage this framework.

        Format your reply only in utf-8
        """
    return prompt
