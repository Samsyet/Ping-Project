import typer
import logging
import random

app = typer.Typer()

# Configure logging
logging.basicConfig(filename='game.log', level=logging.INFO)

# Dictionary to store user details
user_details = {
    "name": None,
    "location": "Village",
    "talked_to": set(),
    "can_talk": True,
    "can_fight": False,
    "has_sword": False,
    "has_armor": False,
    "health": 100,  # User's initial health
}

# Dragon's initial health
dragon_health = 1000

# Dictionary to store general details about the map
map_details = {
    "locations": {
        "Village": {
            "can_talk": True,
            "can_fight": False,
            "neighbors": {"east": "Mountain of Doom", "north": "Kakori Forest", "west": "Caves of the People in Robes", "south": "Gwen's Village"},
            "people": ["Old man in the Village"],
        },
        "Kakori Forest": {
            "can_talk": True,
            "can_fight": False,
            "neighbors": {"south": "Village"},
            "people": ["Ascalon's Soul"],
        },
        "Gwen's Village": {
            "can_talk": True,
            "can_fight": False,
            "neighbors": {"north": "Village"},
            "people": ["Gwen"],
        },
        "Caves of the People in Robes": {
            "can_talk": True,
            "can_fight": False,
            "neighbors": {"east": "Village"},
            "people": ["Leader of the People in the Robes"],
        },
        "Mountain of Doom": {
            "can_talk": True,
            "can_fight": True,  # The dragon is here
            "neighbors": {"west": "Village"},
            "people": ["Dragon"],
        },
    },
}

# Dictionary to store characters and their respective locations
characters = {
    "Old man in the Village": "Village",
    "Ascalon's Soul": "Kakori Forest",
    "Gwen": "Gwen's Village",
    "Leader of the People in the Robes": "Caves of the People in Robes",
    "Dragon": "Mountain of Doom",
}

def move(direction: str):
    """
    Move the player in a specified direction (north, south, east, west).
    """
    current_location = user_details["location"]
    location_details = map_details["locations"][current_location]
    neighbors = location_details["neighbors"]

    if direction in neighbors:
        next_location = neighbors[direction]
        next_location_details = map_details["locations"][next_location]
        
        # Check if the user is allowed to move to the next location
        if next_location_details["can_talk"] or next_location_details["can_fight"]:
            # Log user action
            logging.info(f"{user_details['name']} moved {direction} to {next_location}")

            # Move the user to the next location
            user_details["location"] = next_location
            typer.echo(f"Moving {direction} to {next_location}...")
        else:
            typer.echo("You can't go there right now.")
    else:
        # Display available directions and their corresponding places
        available_directions = ", ".join([f"{dir}: {neighbor}" for dir, neighbor in neighbors.items()])
        typer.echo(f"Invalid direction. Available directions: {available_directions}")

def talk_to():
    """
    Talk to a person.
    """
    current_location = user_details["location"]
    location_details = map_details["locations"][current_location]

    available_people = location_details["people"]
    typer.echo("Choose a person to talk to:")
    options = [f"{i+1}. {person}" for i, person in enumerate(available_people)]
    for option in options:
        typer.echo(option)

    choice = typer.prompt("Enter the number of the person you want to talk to:")

    try:
        choice_index = int(choice) - 1
        selected_person = available_people[choice_index]

        if selected_person in location_details["people"]:
            # Log user action
            logging.info(f"{user_details['name']} talked to {selected_person} at {current_location}")

            # Implement logic to talk to the specified person
            user_details["talked_to"].add(selected_person)
            typer.echo(f"You talked to {selected_person} at {current_location}.")

            # Interaction with characters based on the story
            if selected_person == "Old man in the Village" and current_location == "Village":
                typer.echo("The old man tells you about the People in the Robes.")
                typer.echo("He suggests you should visit them for further guidance.")
                user_details["can_talk"] = False  # Prevent talking to the old man again
                user_details["location"] = "Caves of the People in Robes"  # Move user to the next location

            elif selected_person == "Leader of the People in the Robes" and current_location == "Caves of the People in Robes":
                typer.echo("The leader tells you about the Sword of Ascalon and its importance.")
                typer.echo("He suggests you should go to Gwen's Village to get the armor.")
                user_details["location"] = "Gwen's Village"  # Move user to the next location

            elif selected_person == "Gwen" and current_location == "Gwen's Village":
                typer.echo("Gwen forges the armor for you and tells you to go to the Kakori Forest.")
                typer.echo("She says you will find Ascalon's Soul there.")
                user_details["has_armor"] = True
                user_details["location"] = "Kakori Forest"  # Move user to the next location

            elif selected_person == "Ascalon's Soul" and current_location == "Kakori Forest":
                typer.echo("Ascalon's Soul bestows the Sword of Ascalon upon you.")
                user_details["has_sword"] = True
                user_details["can_fight"] = True
                typer.echo("You are now ready to fight the Dragon!")
                user_details["location"] = "Mountain of Doom"  # Move user to the final location

        else:
            typer.echo(f"{selected_person} is not here.")

    except ValueError:
        typer.echo("Invalid choice. Please enter a valid number.")

def fight():
    """
    Fight with the Dragon.
    """
    global dragon_health

    current_location = user_details["location"]
    location_details = map_details["locations"][current_location]

    if location_details["can_fight"]:
        if user_details["has_sword"] and user_details["has_armor"]:
            typer.echo("You encounter the Dragon! What will you do?")

            user_health = user_details["health"]
            typer.echo(f"Your Health: {user_health} | Dragon's Health: {dragon_health}")

            while True:
                typer.echo("1. Slash")
                typer.echo("2. Stab")
                typer.echo("3. Special")
                typer.echo("4. Run")
                typer.echo()

                choice = typer.prompt("Enter your choice (1-4):", default="1")

                if choice == "1":
                    # Slash attack
                    damage = random.randint(10, 20)
                    dragon_health -= damage
                    typer.echo(f"You slash the Dragon! It takes {damage} damage.")

                elif choice == "2":
                    # Stab attack
                    damage = random.randint(15, 25)
                    dragon_health -= damage
                    typer.echo(f"You stab the Dragon! It takes {damage} damage.")

                elif choice == "3":
                    # Special attack
                    damage = random.randint(25, 35)
                    dragon_health -= damage
                    typer.echo(f"You use your special attack! The Dragon takes {damage} damage.")

                elif choice == "4":
                    # Run away
                    typer.echo("You managed to escape from the Dragon!")
                    break

                else:
                    typer.echo("Invalid choice. Please choose again.")
                
                # Check if the Dragon is defeated
                if dragon_health <= 0:
                    typer.echo("Congratulations! You have defeated the Dragon!")
                    typer.echo("You have saved the village and its people!")
                    break
                
                # Dragon's turn
                user_health -= random.randint(10, 20)
                typer.echo(f"The Dragon attacks you! You take damage. Your Health: {user_health}")

                # Check if the user is defeated
                if user_health <= 0:
                    retry = typer.confirm("You have been defeated by the Dragon! Do you want to retry?")
                    if retry:
                        user_details["health"] = 100  # Reset user's health
                        dragon_health = 1000  # Reset dragon's health
                        fight()  # Retry the fight
                    else:
                        break
        else:
            typer.echo("You don't have the necessary equipment to fight the Dragon.")
    else:
        typer.echo("There's nothing to fight here.")

@app.command()
def start():
    """
    Start the game.
    """
    user_details["name"] = typer.prompt("Enter your name:")
    typer.echo(f"Welcome, {user_details['name']}! Let's get started.")

    # Log user action
    logging.info(f"{user_details['name']} started the game")

    # Display introductory text
    typer.echo(
        "Once there was a village, surrounded by mountains that held creatures of a thousand kinds.\n"
        "The mountain which stood the highest was the home to a mighty dragon.\n"
        "The dragon could be called the ruler of the whole region, and it was a time of peace.\n"
        "However one day, a huge roar was heard coming from the Dragons den.\n"
        "People rushed to see the giant dragon screaming, and as the dragon saw them, it let out a huge breath of fire!\n"
        "Everyone was terrified of the huge dragon suddenly attacking the people it once protected and cared for.\n"
        "A group called the People in the Robes arrived there, and after hours of back and forth, managed to seal the dragon away.\n"
        "However, they realized that they can't keep the seal held for long, so someone will have to somehow tame the dragon, or slay it.\n"
    )

    # Initialize game state and start the game loop
    play()

@app.command()
def play():
    """
    Enter the game loop to play the game.
    """
    typer.echo("You are now in the game. Choose an action:")

    while True:
        option = typer.prompt(
            "1. Talk       2. Fight\n3. Move       4. Quit\n"
        )

        if option == "1":
            if user_details["can_talk"]:
                talk_to()
            else:
                typer.echo("You can't talk right now.")
        elif option == "2":
            if user_details["can_fight"]:
                fight()
            else:
                typer.echo("You can't fight right now.")
        elif option == "3":
            direction = typer.prompt("Enter the direction you want to move:")
            move(direction)
        elif option == "4":
            confirm = typer.confirm("Are you sure you want to quit?")
            if confirm:
                typer.echo("Exiting game.")
                break
        else:
            typer.echo("Invalid option. Choose again.")

if __name__ == "__main__":
    app()