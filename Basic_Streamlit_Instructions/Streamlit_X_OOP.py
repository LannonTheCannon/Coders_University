import streamlit as st


def intro_page():
    st.title("🧟‍♂️ Welcome to Your Zombie Game Code Journey!")
    st.write("""
    Hey there, future game developer! You've created an awesome zombie escape game, and I'm here to help you understand 
    exactly how it works. We'll break everything down piece by piece, and by the end, you'll be amazed at how much 
    you understand!
    """)

    st.info("""
    👋 Before we start:
    - Take your time with each section
    - Try to predict what code does before reading the explanation
    - Don't worry if you don't get everything right away
    - Feel free to come back to any section
    """)

    st.subheader("🎯 What We'll Learn")
    st.write("""
    1. How your game is organized (Game Architecture)
    2. How different parts talk to each other (Game Flow)
    3. How to track what's happening (Game State)
    4. How to handle player choices (Events)
    5. How to create new features (Extending the Game)
    """)


def classes_explained():
    st.title("🏗️ Understanding Classes: The Building Blocks")

    st.write("""
    Imagine you're building with LEGO®. Classes are like your LEGO instruction booklets - they tell you how to build
    something specific. Let's break this down!
    """)

    tabs = st.tabs(["Classes Basics", "Inheritance", "Methods", "Example Time!"])

    with tabs[0]:
        st.header("What is a Class?")
        st.write("""
        A class is like a blueprint that tells us how to create something. In your game, we have several blueprints:
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### Game Classes
            1. `ZombieGame` - The main game manager
            2. `MiniGame` - Template for mini-games
            3. `ZombieHordeGame` - The number guessing game
            4. `SurvivorEvent` - Managing survivor encounters
            """)

        with col2:
            st.markdown("""
            ### What They Do
            1. Controls everything in the game
            2. Provides basic mini-game features
            3. Handles the zombie sneaking challenge
            4. Manages meeting and saving survivors
            """)

    with tabs[1]:
        st.header("Class Inheritance: Sharing Features")
        st.write("""
        Remember how some LEGO pieces can stack on top of others? That's like class inheritance!
        """)

        st.code("""
        class MiniGame:  # Parent class
            def __init__(self):
                self.is_complete = False    # Is the game finished?
                self.was_successful = False # Did the player win?

        class ZombieHordeGame(MiniGame):  # Child class
            def __init__(self):
                super().__init__()         # Get parent features
                self.state_key = "horde_game_state"  # Add own features
        """)

        st.info("""
        🔍 Let's break down what's happening:
        1. `MiniGame` is our parent class (base LEGO piece)
        2. `ZombieHordeGame` is our child class (piece we stack on top)
        3. `super().__init__()` is like clicking the pieces together
        4. After connecting, we can add our own special features
        """)

    with tabs[2]:
        st.header("Methods: Making Things Happen")
        st.write("Methods are like instruction steps in your LEGO manual. They tell the class what to do.")

        method_expander = st.expander("See Common Methods")
        with method_expander:
            st.markdown("""
            ### Important Methods in Your Game

            #### ZombieGame Class
            - `initialize_game_state()`: Sets up the game
            - `handle_movement()`: Moves the player
            - `show_status()`: Shows game information

            #### ZombieHordeGame Class
            - `initialize_state()`: Prepares the mini-game
            - `render()`: Shows the game screen
            - `update()`: Changes game state based on player actions
            """)

    with tabs[3]:
        st.header("Let's Try It!")
        st.write("Here's a simple example we can build together:")

        st.code("""
        # Let's create a simple game character system
        class GameCharacter:
            def __init__(self):
                self.health = 100
                self.is_alive = True

            def take_damage(self, amount):
                self.health -= amount
                if self.health <= 0:
                    self.is_alive = False

        # Now let's make a specific type of character
        class Survivor(GameCharacter):
            def __init__(self):
                super().__init__()  # Get basic character features
                self.has_weapon = False  # Add survivor-specific feature

            def find_weapon(self):
                self.has_weapon = True
        """)

        if st.button("Run This Code"):
            st.write("Let's see what happens when we create a survivor:")

            class GameCharacter:
                def __init__(self):
                    self.health = 100
                    self.is_alive = True

                def take_damage(self, amount):
                    self.health -= amount
                    if self.health <= 0:
                        self.is_alive = False

            class Survivor(GameCharacter):
                def __init__(self):
                    super().__init__()
                    self.has_weapon = False

                def find_weapon(self):
                    self.has_weapon = True

            survivor = Survivor()
            st.write(f"Health: {survivor.health}")
            st.write(f"Is Alive: {survivor.is_alive}")
            st.write(f"Has Weapon: {survivor.has_weapon}")

            st.success(
                "See how our Survivor got basic features (health, is_alive) from GameCharacter AND its own feature (has_weapon)?")


def game_state_management():
    st.title("🎮 Game State: Keeping Track of Everything")

    st.write("""
    Imagine you're reading a book and using a bookmark to keep track of where you are. 
    Game state is like having multiple bookmarks for different things in your game!
    """)

    tabs = st.tabs(["State Basics", "Session State", "Tracking Events", "Practice"])

    with tabs[0]:
        st.header("What is Game State?")
        st.write("""
        Game state is ALL the information about what's happening in your game right now:
        - Where is the player?
        - How much time is left?
        - Who has been saved?
        - What events are completed?
        """)

        st.code("""
        # Here's how we set up the game state
        if "game_state" not in st.session_state:
            st.session_state.game_state = {
                "current_room": "Camp Goodman",  # Where player starts
                "time_remaining": 12,            # Hours left
                "events_completed": set(),       # Empty list of done events
                "survivors_saved": set(),        # Empty list of saved people
                "is_game_over": False           # Game still running
            }
        """)

        st.info("""
        💡 Think of this like setting up a new save file in your favorite video game:
        - You start in a specific place
        - You have full health/time
        - Nothing has been done yet
        """)

    with tabs[1]:
        st.header("Streamlit Session State")
        st.write("""
        Streamlit's session state is like a magical notebook that remembers things even when 
        the page refreshes. Let's see how it works!
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Without Session State")
            st.code("""
            counter = 0  # Regular variable
            # This resets to 0 every refresh!
            """)

        with col2:
            st.markdown("### With Session State")
            st.code("""
            if "counter" not in st.session_state:
                st.session_state.counter = 0
            # This remembers its value!
            """)

        if "demo_counter" not in st.session_state:
            st.session_state.demo_counter = 0

        if st.button("Add 1 to counter"):
            st.session_state.demo_counter += 1

        st.write(f"Current count: {st.session_state.demo_counter}")
        st.write("(Try clicking the button - the number stays even when other sections change!)")

    with tabs[2]:
        st.header("Tracking Events and Changes")
        st.write("Let's see how we track different events in the game:")

        event_expander = st.expander("Show Event Tracking Example")
        with event_expander:
            st.code("""
            # When player saves a survivor:
            def handle_survivor_event(self, room_name):
                survivor = room['event']['survivor']
                if survivor.was_successful:
                    # Update time
                    st.session_state.game_state["time_remaining"] -= survivor.time_cost

                    # Add to saved list
                    st.session_state.game_state["survivors_saved"].add(survivor.survivor_name)

                    # Mark event complete
                    st.session_state.game_state["events_completed"].add(room_name)
            """)

            st.markdown("""
            This code:
            1. Reduces remaining time
            2. Adds survivor to saved list
            3. Marks the event as done

            Like checking off items in a todo list!
            """)

    with tabs[3]:
        st.header("Try It Yourself!")
        st.write("Let's create a simple inventory system:")

        if "practice_inventory" not in st.session_state:
            st.session_state.practice_inventory = []

        item = st.text_input("Enter an item to add:")
        if st.button("Add to Inventory"):
            if item:
                st.session_state.practice_inventory.append(item)

        st.write("Your inventory:", st.session_state.practice_inventory)

        if st.button("Clear Inventory"):
            st.session_state.practice_inventory = []


def rooms_and_navigation():
    st.title("🏰 Rooms and Navigation: Moving Around")

    st.write("""
    Your game world is like a map made up of connected rooms. Let's see how it all works!
    """)

    tabs = st.tabs(["Room Structure", "Navigation System", "Room Events", "Try It!"])

    with tabs[0]:
        st.header("How Rooms Are Built")
        st.write("""
        Each room in your game is like a real room with specific features:
        - Doors to other rooms (exits)
        - A description of what's there
        - Special events that might happen
        - An image to show the player
        """)

        st.code("""
        'Drytron Mall': {
            'exits': {
                'left': 'Camp Goodman',
                'right': 'parking lot',
                'down': 'The Suburbs'
            },
            'description': "You walk past the empty stalls...",
            'image': "./images/Drytronmall1.jpg",
            'event': {
                'type': 'survivor',
                'survivor': SurvivorEvent("Drew"),
                'description': "You hear someone calling for help..."
            }
        }
        """)

        st.info("""
        🏗️ Think of each room like a LEGO® piece:
        - The connectors are the exits
        - The design is the description
        - The special features are the events
        """)

    with tabs[1]:
        st.header("Moving Between Rooms")
        st.write("Let's see how the player moves around:")

        st.code("""
        def handle_movement(self, direction):
            current = st.session_state.game_state["current_room"]
            if direction in self.rooms[current]['exits']:
                # Move to new room
                st.session_state.game_state["current_room"] = self.rooms[current]['exits'][direction]
                # Reduce time
                st.session_state.game_state["time_remaining"] -= 1
                return True
            return False
        """)

        st.markdown("""
        This code:
        1. Checks if the direction is valid
        2. Moves to the new room if possible
        3. Takes 1 hour of game time
        4. Returns True/False based on success
        """)

    with tabs[2]:
        st.header("Room Events")
        st.write("""
        Some rooms have special events that happen when you enter.
        Let's break down how they work:
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Types of Events")
            st.markdown("""
            - Survivor encounters
            - Zombie hordes
            - (Future expansion!)
            """)

        with col2:
            st.markdown("### Event Results")
            st.markdown("""
            - Success/Failure
            - Time cost
            - Game state changes
            """)

    with tabs[3]:
        st.header("Build Your Own Room!")
        st.write("Let's create a room together:")

        room_name = st.text_input("Room Name:")
        description = st.text_area("Description:")

        col1, col2 = st.columns(2)
        with col1:
            has_north = st.checkbox("Exit to North?")
            has_south = st.checkbox("Exit to South?")
        with col2:
            has_east = st.checkbox("Exit to East?")
            has_west = st.checkbox("Exit to West?")

        if st.button("Create Room"):
            exits = {}
            if has_north: exits['up'] = "North Room"
            if has_south: exits['down'] = "South Room"
            if has_east: exits['right'] = "East Room"
            if has_west: exits['left'] = "West Room"

            room = {
                'exits': exits,
                'description': description,
                'image': "placeholder.jpg"
            }

            st.code(f"{room_name} = {str(room)}")
            st.success("Room created! This is how it would look in your game's code.")


def events_and_minigames():
    st.title("🎲 Events and Mini-games: Making Things Happen!")

    st.write("""
    Events and mini-games make your zombie game exciting! Let's learn how they work.
    """)

    tabs = st.tabs(["Event Types", "Mini-game System", "Survivor Events", "Create Events"])

    with tabs[0]:
        st.header("Understanding Events")
        st.write("""
        Your game has two main types of events:
        1. Mini-games (like the zombie horde)
        2. Survivor encounters
        """)

        st.markdown("""
        ### How Events Work
        1. Check if room has an event
        2. If event not completed:
            - Show event description
            - Let player make choices
            - Update game state
        3. Mark event as complete
        """)

        st.code("""
        def handle_event(self, room_name):
            room = self.rooms[room_name]
            if 'event' not in room:
                return None  # No event in this room

            if room_name not in st.session_state.game_state["events_completed"]:
                # Run the event!
                return self.run_event(room['event'])
        """)

    with tabs[1]:
        st.header("Mini-game System")
        st.write("Let's break down how mini-games work:")

        st.code("""
        class ZombieHordeGame(MiniGame):
            def __init__(self):
                super().__init__()
                self.state_key = "horde_game_state"

            def initialize_state(self):
                if self.state_key not in st.session_state:
                    st.session_state[self.state_key] = {
                        "secret_number": random.randint(1, 40),
                        "guesses_remaining": 8,
                        "last_guess": None,
                        "message": None
                    }
        """)

        st.info("""
        Mini-games have:
        1. Their own state tracking
        2. Success/failure conditions
        3. Player interaction
        4. Results that affect the main game
        """)

        st.markdown("""
        ### Mini-game Flow
        1. Initialize game state
        2. Show game interface
        3. Handle player input
        4. Update game state
        5. Check win/lose conditions
        6. Affect main game based on result
        """)

    with tabs[2]:
        st.header("Survivor Events")
        st.write("""
        Survivor events are simpler than mini-games but still interesting!
        """)

        st.code("""
        class SurvivorEvent:
            def __init__(self, survivor_name, time_cost=None):
                self.survivor_name = survivor_name
                self.time_cost = time_cost or random.randint(1, 3)
                self.is_complete = False
                self.was_successful = False
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Event Features")
            st.markdown("""
            - Survivor's name
            - Time cost to save
            - Success tracking
            - Completion status
            """)

        with col2:
            st.markdown("### Player Choices")
            st.markdown("""
            1. Save survivor
                - Costs time
                - Adds to saved list
            2. Leave survivor
                - No time cost
                - Affects game ending
            """)

    with tabs[3]:
        st.header("Design Your Own Event!")
        st.write("Let's create a custom event:")

        event_type = st.selectbox("Event Type:",
                                  ["Survivor Encounter", "Mini-game Challenge"])

        if event_type == "Survivor Encounter":
            name = st.text_input("Survivor Name:")
            time = st.number_input("Time Cost:", 1, 5)
            story = st.text_area("Survivor's Story:")

            if st.button("Create Survivor Event"):
                event = {
                    'type': 'survivor',
                    'survivor': {
                        'name': name,
                        'time_cost': time,
                        'story': story
                    }
                }
                st.code(str(event))
                st.success("Survivor event created!")

        else:
            challenge = st.text_input("Challenge Name:")
            attempts = st.number_input("Allowed Attempts:", 1, 10)
            success_msg = st.text_input("Success Message:")
            fail_msg = st.text_input("Failure Message:")

            if st.button("Create Mini-game"):
                game = {
                    'type': 'minigame',
                    'game': {
                        'name': challenge,
                        'attempts': attempts,
                        'success_message': success_msg,
                        'failure_message': fail_msg
                    }
                }
                st.code(str(game))
                st.success("Mini-game created!")


def putting_it_all_together():
    st.title("🎯 Putting It All Together")

    tabs = st.tabs(["Game Flow", "Code Walkthrough", "Visual Map", "Practice Challenge"])

    with tabs[0]:
        st.header("How Everything Connects")
        st.write("""
        Let's see how all the pieces of your game work together:
        """)

        # Replace mermaid with a visual flow using columns and emojis
        st.write("### Game Flow Diagram")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            #### Game Start and Setup
            🎮 Player Starts Game
            ⬇️
            🎲 Initialize Game State
            ⬇️
            🏗️ Create Game World/Rooms
            ⬇️
            🔄 Game Loop Starts
            """)

        with col2:
            st.markdown("""
            #### Game Loop Details
            📍 Check Current Room
            ⬇️
            📊 Show Status
            ⬇️
            ❓ Check for Events
            ⬇️
            Either:
            - 🎲 Run Event 
            - 🚶‍♂️ Allow Movement
            """)

        st.info("""
        🔍 The game cycle:
        1. Start game & setup
        2. Show where player is
        3. Check for events
        4. Handle player actions
        5. Update game state
        6. Repeat!
        """)

        # Add detailed explanation
        st.write("""
        #### How It Works Step by Step:

        1. **Game Initialization**:
           - Set up initial game state (time, room, etc.)
           - Create all rooms and their connections
           - Set up events and mini-games

        2. **Main Game Loop**:
           - Display current room and status
           - Check if there's an event (survivor or zombie horde)
           - Handle player input (movement or event choices)
           - Update game state based on actions
           - Check win/lose conditions
        """)
    with tabs[1]:
        st.header("Code Flow Example")
        st.write("Let's follow what happens when a player moves to a room with a survivor:")

        code_steps = {
            "Step 1: Player Moves": """
            def handle_movement(self, direction):
                # Check if movement is valid
                # Update room if it is
                # Reduce time by 1
            """,

            "Step 2: Check Room": """
            def run(self):
                # Show status
                # Check for events
                if self.handle_survivor_event(current_room):
                    return  # Wait for player choice
            """,

            "Step 3: Handle Survivor": """
            def handle_survivor_event(self, room_name):
                survivor = room['event']['survivor']
                # Show survivor options
                # Handle player choice
                # Update game state
            """
        }

        step = st.selectbox("Select step to examine:", list(code_steps.keys()))
        st.code(code_steps[step])

    with tabs[2]:
        st.header("Visual Game Map")
        st.write("Here's how the rooms connect and where events happen:")

        st.image("./images/Zombie_Game_map.png")

        st.markdown("""
        🗺️ **Map Features:**
        - Rooms are connected by directions (left, right, up, down)
        - Some rooms have survivors
        - Some rooms have zombie hordes
        - You need to reach the airport!
        """)

    with tabs[3]:
        st.header("Build A Mini Feature")
        st.write("Let's practice putting concepts together by adding a new feature!")

        feature_type = st.selectbox(
            "What would you like to add?",
            ["New Room", "New Survivor", "New Mini-game"]
        )

        if feature_type == "New Room":
            st.write("Create a new room that connects to existing rooms:")
            room_name = st.text_input("Room Name")
            description = st.text_area("Description")
            has_survivor = st.checkbox("Has Survivor?")
            has_zombies = st.checkbox("Has Zombie Horde?")

            if st.button("Generate Room Code"):
                room_code = {
                    'exits': {'left': 'Previous Room'},
                    'description': description,
                    'image': "placeholder.jpg"
                }
                if has_survivor:
                    room_code['event'] = {
                        'type': 'survivor',
                        'survivor': 'NewSurvivor'
                    }
                if has_zombies:
                    room_code['event'] = {
                        'type': 'minigame',
                        'game': 'ZombieHorde'
                    }
                st.code(f"{room_name} = {str(room_code)}")

        elif feature_type == "New Survivor":
            # Add survivor creation interface
            st.write("Create a new survivor to add to a room:")
            survivor_name = st.text_input("Survivor Name")
            time_cost = st.number_input("Time to Save", 1, 5)
            story = st.text_area("Survivor's Story")

            if st.button("Generate Survivor Code"):
                st.code(f"""
                new_survivor = SurvivorEvent("{survivor_name}", {time_cost})
                # Add to room:
                room['event'] = {{
                    'type': 'survivor',
                    'survivor': new_survivor,
                    'description': "{story}"
                }}
                """)

        elif feature_type == "New Mini-game":
            st.write("Design a new mini-game:")
            game_name = st.text_input("Game Name")
            attempts = st.number_input("Number of Attempts", 1, 10)

            if st.button("Generate Mini-game Template"):
                st.code(f"""
                class {game_name}(MiniGame):
                    def __init__(self):
                        super().__init__()
                        self.state_key = "{game_name.lower()}_state"

                    def initialize_state(self):
                        if self.state_key not in st.session_state:
                            st.session_state[self.state_key] = {{
                                "attempts_remaining": {attempts},
                                "is_complete": False
                            }}

                    def render(self):
                        # Add your game interface here
                        pass

                    def update(self, player_input):
                        # Add your game logic here
                        pass
                """)


def main():
    st.sidebar.title("🧟‍♂️ Game Code Tutorial")

    pages = {
        "Introduction": intro_page,
        "Understanding Classes": classes_explained,
        "Game State Management": game_state_management,
        "Rooms & Navigation": rooms_and_navigation,
        "Events & Mini-games": events_and_minigames,
        "Putting It All Together": putting_it_all_together  # Add new section
    }

    selection = st.sidebar.radio("Choose a section:", list(pages.keys()))

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 📝 Your Progress
    Keep track of what you've learned:
    - [ ] Basic Class Concepts
    - [ ] Inheritance
    - [ ] Game State
    - [ ] Navigation
    - [ ] Events
    - [ ] Integration  # Added new progress item
    """)

    # Show selected page
    pages[selection]()

if __name__ == "__main__":
    main()