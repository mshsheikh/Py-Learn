import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_stars(width=80, height=20, star_density=0.1):

    star_field = []
    for _ in range(height):
        row = ''.join('*' if random.random() < star_density else ' ' for _ in range(width))
        star_field.append(row)
    return star_field

def display_star_gazing():
    print("Welcome!")
    print("Press Ctrl+C to EXIT.")
    time.sleep(2)
    
    try:
        while True:
            clear_screen()
            star_field = generate_stars(width=100, height=50, star_density=0.1)
            for row in star_field:
                print(row)
            time.sleep(0.6)       # -- Speed -- #
    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    display_star_gazing()