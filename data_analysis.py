# data example

import streamlit as st

import streamlit as st
import pandas as pd
import plotly.express as px

# Load the Minecraft data
@st.cache_data
def load_data():
    # This is a simplified dataset. In a real scenario, you'd have more data points.
    data = {
        'item': ['Diamond', 'Iron', 'Gold', 'Emerald', 'Coal', 'Lapis Lazuli', 'Redstone'],
        'rarity': [0.0846, 0.77, 0.143, 0.0846, 1.0, 0.118, 0.827],
        'max_vein_size': [8, 9, 9, 1, 17, 7, 8],
        'min_depth': [-64, -64, -64, -64, -64, -64, -64],
        'max_depth': [16, 72, 32, 16, 192, 64, 16]
    }
    return pd.DataFrame(data)

def main():
    st.title("🎮 Minecraft Ore Explorer 💎")
    st.write("Discover hidden insights about Minecraft ores!")

    df = load_data()

    # Sidebar for user input
    st.sidebar.header("Explore Ores")
    selected_ore = st.sidebar.selectbox("Choose an ore to examine:", df['item'])

    # Main content
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ore Rarity")
        fig = px.bar(df, x='item', y='rarity', color='item', 
                     title="Rarity of Minecraft Ores")
        st.plotly_chart(fig)

    with col2:
        st.subheader("Max Vein Size")
        fig = px.scatter(df, x='item', y='max_vein_size', size='max_vein_size', 
                         color='item', title="Maximum Vein Size of Ores")
        st.plotly_chart(fig)

    st.subheader("Ore Depth Range")
    fig = px.bar(df, x='item', y=['min_depth', 'max_depth'], 
                 title="Depth Range for Finding Ores",
                 labels={'value': 'Depth', 'variable': 'Depth Type'})
    st.plotly_chart(fig)

    # Detailed info about selected ore
    st.subheader(f"Details about {selected_ore}")
    ore_data = df[df['item'] == selected_ore].iloc[0]
    st.write(f"Rarity: {ore_data['rarity']:.4f}")
    st.write(f"Max Vein Size: {ore_data['max_vein_size']}")
    st.write(f"Depth Range: {ore_data['min_depth']} to {ore_data['max_depth']}")

    # Fun fact generator
    st.subheader("🎲 Random Minecraft Fact")
    if st.button("Generate Fun Fact"):
        facts = [
            "The creeper was originally a failed pig model!",
            "Minecraft's original name was 'Cave Game'.",
            "The Enderman language is actually reversed and distorted English.",
            "Minecraft has been used in schools to teach subjects like history and science!",
            f"You're most likely to find {selected_ore} between depths {ore_data['min_depth']} and {ore_data['max_depth']}!"
        ]
        st.write(pd.Series(facts).sample().values[0])

if __name__ == "__main__":
    main()
