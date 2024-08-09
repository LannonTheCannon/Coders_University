import streamlit as st

# Setting the page configuration
st.set_page_config(
    page_title='Streamlit Masterclass',
    page_icon='🚀',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help': 'https://www.streamlit.io/community',
        'Report a Bug': 'https://www.streamlit.io/community',
        'About': '# This is a Streamlit Bonanaza'
    },
)

def main():
    st.sidebar.title('Coders University')
    main_sections = [
        'Basics of Streamlit',
        'Intermediate Concepts',
        'Advanced Topics',
        'Styling and Customization',
    ]

    selected_section = st.sidebar.radio('Navigation', main_sections)

    if selected_section == ':coffee: Home':
        home()

def home():
    st.title('Coders University')


if __name__ == '__main__':
    main()