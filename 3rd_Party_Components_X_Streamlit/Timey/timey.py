
import streamlit as st
import streamlit_timeline

def timey_func(): 
    # load data
    with open('../../example.json', "r") as f:
        data = f.read()

    # render timeline
    streamlit_timeline.timeline(data, height=800)

    
