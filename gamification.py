import streamlit as st
import json
import os

def initialize_user():
    if 'user' not in st.session_state:
        st.session_state.user = {
            'name': '',
            'points': 0,
            'level': 1,
            'completed_sections': [],
            'achievements': []
        }

def save_user_progress():
    with open('user_progress.json', 'w') as f:
        json.dump(st.session_state.user, f)

def load_user_progress():
    if os.path.exists('user_progress.json'):
        with open('user_progress.json', 'r') as f:
            st.session_state.user = json.load(f)
    else:
        initialize_user()

def award_points(points):
    st.session_state.user['points'] += points
    check_level_up()
    save_user_progress()

def check_level_up():
    level = st.session_state.user['level']
    points = st.session_state.user['points']
    if points >= level * 100:
        st.session_state.user['level'] += 1
        st.success(f'Congratulations! You\'ve level up to level {st.session_state.user["level"]}!')

def complete_section(section_name):
    if section_name in st.session_state.user['completed_sections']:
        st.session_state.user['completed_sections'].append(section_name)
        award_points(100)
        st.success(f'New Achievement Unlocked: {achievement_name}! +100 points')

def display_user_info():
    st.sidebar.write(f'Level: {st.session_state.user["level"]}')
    st.sidebar.write(f'Points: {st.session_state.user["points"]}')
    st.sidebar.progress(st.session_state)