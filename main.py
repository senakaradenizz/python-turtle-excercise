# Name: Sena Karadeniz
# Student ID: 11862894
# University: Charles Sturt University (Melbourne Campus)
# Subject: S-ITC558_202630 Programming Principles
# Assessment: Assessment 3 – Drawing with Functions

import turtle
import random

# ---------------- Constants ----------------

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 650

SPOT_SIZE = 45
ROWS_PER_BLOCK = 2
COLS_PER_BLOCK = 6

CODE_A = 65

VALID_BG_COLOURS = ["lightgrey", "skyblue", "yellow"]
VALID_AVAILABLE_COLOURS = ["red", "green", "blue"]

DEFAULT_BG_COLOUR = "lightgrey"
DEFAULT_AVAILABLE_COLOUR = "white"
DEFAULT_UNAVAILABLE_COLOUR = "red"


# ---------------- Input Functions ----------------

def get_check_in_hour():
    """
    Gets check-in hour from the user and validates the input.
    Ensures the value is numeric and between 0 and 23.

    Returns:
        int: valid check-in hour
    """
    user_input = input("Enter check-in time (0-23): ")

    while not user_input.isdigit() or int(user_input) < 0 or int(user_input) > 23:
        print("Invalid hour. Please enter a numeric value between 0 and 23.")
        user_input = input("Enter check-in time (0-23): ")

    return int(user_input)


def get_background_colour():
    """
    Gets background colour from user and validates input.

    Returns:
        str: valid background colour
    """
    print("Choose a background colour (lightgrey, skyblue, yellow).")
    colour = input("Background colour [default: lightgrey]: ")

    if colour == "":
        colour = DEFAULT_BG_COLOUR

    while colour not in VALID_BG_COLOURS:
        print("Invalid colour. Please choose lightgrey, skyblue, or yellow.")
        colour = input("Background colour [default: lightgrey]: ")

        if colour == "":
            colour = DEFAULT_BG_COLOUR

    return colour


def get_unavailable_colour():
    """
    Gets unavailable spot colour from user and validates input.

    Returns:
        str: valid unavailable colour
    """
    print("Choose an unavailable spot colour (red, green, blue).")
    colour = input("Enter unavailable spot colour [default: red]: ")

    if colour == "":
        colour = DEFAULT_UNAVAILABLE_COLOUR

    while colour not in VALID_AVAILABLE_COLOURS:
        print("Invalid colour. Please choose red, green, or blue.")
        colour = input("Enter unavailable spot colour [default: red]: ")

        if colour == "":
            colour = DEFAULT_UNAVAILABLE_COLOUR

    return colour


# ---------------- Availability Logic ----------------

def get_availability_percentage(hour):
    """
    Determines parking availability percentage based on hour.

    Args:
        hour (int): check-in time

    Returns:
        float: availability percentage
    """
    if 7 <= hour <= 11:
        return 0.20
    elif 12 <= hour <= 17:
        return 0.50
    else:
        return 0.80


def is_spot_available(availability):
    """
    Determines if a parking spot is available using probability.

    Args:
        availability (float): probability value

    Returns:
        bool: True if available, False otherwise
    """
    if random.random() > availability:
        return False
    else:
        return True


# ---------------- Drawing Functions ----------------

def move_to(t, x, y):
    """
    Moves turtle to a position without drawing.

    Args:
        t (Turtle): turtle object
        x (int): x-coordinate
        y (int): y-coordinate
    """
    t.penup()
    t.goto(x, y)
    t.pendown()


def draw_square(t, x, y, size, fill_colour):
    """
    Draws a filled square at a given position.

    Args:
        t (Turtle): turtle object
        x (int): x-coordinate
        y (int): y-coordinate
        size (int): size of square
        fill_colour (str): colour of square
    """
    move_to(t, x, y)
    t.fillcolor(fill_colour)
    t.begin_fill()

    for _ in range(4):
        t.forward(size)
        t.right(90)

    t.end_fill()


def draw_spot(t, x, y, available, unavailable_colour):
    """
    Draws a parking spot based on availability.

    Args:
        t (Turtle): turtle object
        x (int): x-coordinate
        y (int): y-coordinate
        available (bool): availability status
        unavailable_colour (str): colour for unavailable spots
    """
    if available:
        fill_colour = DEFAULT_AVAILABLE_COLOUR
    else:
        fill_colour = unavailable_colour

    draw_square(t, x, y, SPOT_SIZE, fill_colour)


def draw_block(t, start_x, start_y, availability, unavailable_colour):
    """
    Draws a block of parking spots.

    Returns:
        tuple: (available_count, total_count)
    """
    available_count = 0
    total_count = ROWS_PER_BLOCK * COLS_PER_BLOCK

    for row in range(ROWS_PER_BLOCK):
        for col in range(COLS_PER_BLOCK):
            available = is_spot_available(availability)

            if available:
                available_count += 1

            x = start_x + col * SPOT_SIZE
            y = start_y - row * SPOT_SIZE

            draw_spot(t, x, y, available, unavailable_colour)

    return available_count, total_count


def write_text(t, text, x, y, size, style="normal"):
    """
    Writes text on screen.
    """
    move_to(t, x, y)
    t.write(text, align="center", font=("Arial", size, style))


def draw_labels(t):
    """
    Draws row and column labels.
    """
    for i in range(6):
        letter = chr(CODE_A + i)
        write_text(t, letter, -285 + i * SPOT_SIZE, -230, 14, "bold")

    for i in range(6):
        letter = chr(CODE_A + 6 + i)
        write_text(t, letter, 95 + i * SPOT_SIZE, -230, 14, "bold")


def draw_legend(t, unavailable_colour):
    """
    Draws legend for available and unavailable spots.
    """
    draw_square(t, -330, -280, 25, DEFAULT_AVAILABLE_COLOUR)
    write_text(t, "Available", -250, -287, 13)

    draw_square(t, -170, -280, 25, unavailable_colour)
    write_text(t, "Unavailable", -65, -287, 13)


def draw_parking_layout(t, availability, unavailable_colour):
    """
    Draws entire parking layout.

    Returns:
        tuple: total available and total spots
    """
    total_available = 0
    total_spots = 0

    block_positions = [
        (-310, 190), (80, 190),
        (-310, 55), (80, 55),
        (-310, -80), (80, -80)
    ]

    for x, y in block_positions:
        available, total = draw_block(t, x, y, availability, unavailable_colour)
        total_available += available
        total_spots += total

    return total_available, total_spots


# ---------------- Main ----------------

def main():
    """
    Main function to run the parking visualiser system.
    """
    hour = get_check_in_hour()
    bg_colour = get_background_colour()
    unavailable_colour = get_unavailable_colour()

    availability = get_availability_percentage(hour)

    turtle.setup(WINDOW_WIDTH, WINDOW_HEIGHT)
    turtle.bgcolor(bg_colour)
    turtle.tracer(5)

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)

    total_available, total_spots = draw_parking_layout(
        t, availability, unavailable_colour
    )

    draw_labels(t)
    draw_legend(t, unavailable_colour)

    avg = int((total_available / total_spots) * 100)
    print("Average parking availability:", str(avg) + "%")

    turtle.update()
    turtle.done()

main()