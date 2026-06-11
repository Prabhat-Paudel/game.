import random

WIDTH = 10
HEIGHT = 10

player = {
    "x": 0,
    "y": 0,
    "hp": 100,
    "attack": 20
}

enemy = {
    "x": random.randint(1, WIDTH - 1),
    "y": random.randint(1, HEIGHT - 1),
    "hp": 50,
    "attack": 10
}

treasure = {
    "x": random.randint(1, WIDTH - 1),
    "y": random.randint(1, HEIGHT - 1)
}

def draw_map():
    print("\nMap:")
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if x == player["x"] and y == player["y"]:
                print("P", end=" ")
            elif x == enemy["x"] and y == enemy["y"] and enemy["hp"] > 0:
                print("E", end=" ")
            elif x == treasure["x"] and y == treasure["y"]:
                print("T", end=" ")
            else:
                print(".", end=" ")
        print()

def fight():
    print("\nEnemy encountered!")

    while player["hp"] > 0 and enemy["hp"] > 0:
        print(f"Your HP: {player['hp']}")
        print(f"Enemy HP: {enemy['hp']}")

        action = input("Attack (a) or Run (r): ").lower()

        if action == "a":
            damage = random.randint(10, player["attack"])
            enemy["hp"] -= damage
            print(f"You dealt {damage} damage!")

            if enemy["hp"] <= 0:
                print("Enemy defeated!")
                return

            damage = random.randint(5, enemy["attack"])
            player["hp"] -= damage
            print(f"Enemy dealt {damage} damage!")

        elif action == "r":
            print("You escaped!")
            return

def move(direction):
    if direction == "w" and player["y"] > 0:
        player["y"] -= 1
    elif direction == "s" and player["y"] < HEIGHT - 1:
        player["y"] += 1
    elif direction == "a" and player["x"] > 0:
        player["x"] -= 1
    elif direction == "d" and player["x"] < WIDTH - 1:
        player["x"] += 1

def game():
    print("=== DUNGEON EXPLORER ===")
    print("Controls: W A S D")

    while True:
        draw_map()

        print(f"\nHP: {player['hp']}")

        if player["hp"] <= 0:
            print("Game Over!")
            break

        if (player["x"] == enemy["x"] and
            player["y"] == enemy["y"] and
            enemy["hp"] > 0):
            fight()

        if (player["x"] == treasure["x"] and
            player["y"] == treasure["y"]):
            print("\n🏆 You found the treasure!")
            print("YOU WIN!")
            break

        direction = input("\nMove (W/A/S/D): ").lower()
        move(direction)

game()