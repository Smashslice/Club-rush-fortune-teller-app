import requests
from dotenv import load_dotenv
import os
import random
from colorama import init, Fore, Back, Style
import time
import re
init(autoreset=True)  # Initialize colorama

def calculate_visible_length(text):
    """Calculate the visible length of text excluding ANSI codes"""
    # Find all ANSI codes
    i = 0
    while i < len(text):
        if text[i:i+2] == '\033[':
            code_end = text.find('m', i)
            if code_end != -1:
                text = text[:i] + text[code_end+1:]
                continue
        i += 1
    return len(text)

def wrap_text(text, max_width):
    """Wrap text to fit within max_width, preserving ANSI codes and ensuring second line isn't longer than first"""
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        word_length = calculate_visible_length(word)
        
        if current_length + word_length + (1 if current_line else 0) <= max_width:
            current_line.append(word)
            current_length += word_length + (1 if current_length else 0)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                # If this is the second line and it's as long as the first
                if len(lines) == 1 and calculate_visible_length(' '.join(current_line)) >= calculate_visible_length(lines[0]):
                    # Split the line in half for better aesthetics
                    second_line = ' '.join(current_line)
                    words_in_line = second_line.split()
                    mid_point = len(words_in_line) // 2
                    lines[-1] = ' '.join(words_in_line[:mid_point])
                    lines.append(' '.join(words_in_line[mid_point:]))
            current_line = [word]
            current_length = word_length
    
    if current_line:
        if len(lines) == 1:  # If this would be the second line
            joined_line = ' '.join(current_line)
            if calculate_visible_length(joined_line) >= calculate_visible_length(lines[0]):
                # Split this line in half
                words_in_line = joined_line.split()
                mid_point = len(words_in_line) // 2
                lines.append(' '.join(words_in_line[:mid_point]))
                lines.append(' '.join(words_in_line[mid_point:]))
            else:
                lines.append(joined_line)
        else:
            lines.append(' '.join(current_line))
    
    return lines

def create_decorative_border(text):
    # Maximum width for text content (accounting for the border and padding)
    MAX_TEXT_WIDTH = 140  # 140 - 10 (left border) - 10 (right padding)
    
    # Wrap the text into appropriately sized lines
    wrapped_lines = wrap_text(text, MAX_TEXT_WIDTH)
    
    # Create the pyramid-style borders
    bordered_lines = []
    # Top borders
    bordered_lines.append("\t\t\t\t\t\t\t\t\t\t" + "~" * 30)
    bordered_lines.append("\t\t\t\t\t\t\t" + "~" * 60)
    bordered_lines.append("\t\t\t" + "~" * 155)
    
    # Text lines with pyramid-style border
    for i, line in enumerate(wrapped_lines):
        # Configure tilde counts and tabs for pyramid effect
        if i == 1:  # Middle line gets the most tildes
            left_tildes = "~" * 60
            right_tildes = "~" * 60
            tabs = ""  # 7 tabs for middle line
        else:  # First and third lines get fewer tildes with extra on left
            left_tildes = "~" * 5 + "~" * 45  # 5 extra on left for pyramid effect
            right_tildes = "~" * 45
            tabs = "\t\t"
        
        # Add tabs for better centering
        bordered_lines.append(tabs + left_tildes + " " + line + " " + right_tildes)
    
    # Bottom borders in reverse
    bordered_lines.append("\t\t\t" + "~" * 155)
    bordered_lines.append("\t\t\t\t\t\t\t" + "~" * 60)
    bordered_lines.append("\t\t\t\t\t\t\t\t\t\t" + "~" * 30)
    
    return '\n'.join(bordered_lines)

def generate_cursed_message():
    thorns = ['✾', '❀', '✿', '❋', '❃', '✤', '✥', '✻', '❉', '❈', '✺', '✹', '✸', '✷', '☠', '✴']
    curse_fragments = [
        "i can smell her on you",
        "that witch",
        "she cursed you",
        "thorns will grow",
        "in your dreams",
        "blood and roses",
        "darkness comes",
        "your soul is marked",
        "no escape",
        "the curse binds",
        "shadows whisper",
        "petals of pain",
        "forever cursed",
        "trapped in thorns",
        "witch's garden",
        "bleeding roses"
    ]
    
    num_lines = random.randint(12, 16)
    output_lines = []
    
    # Ensure at least 3 message fragments appear
    selected_messages = random.sample(curse_fragments, random.randint(3, 5))
    message_positions = random.sample(range(num_lines), len(selected_messages))
    
    def generate_thorn_section(length):
        section = []
        while len(' '.join(section)) < length:
            section.append(random.choice(thorns))
        return ' '.join(section)
    
    for i in range(num_lines):
        if i in message_positions:
            # Create a line with message fragment
            message = selected_messages[message_positions.index(i)]
            corrupted_msg = ''.join(c if random.random() > 0.3 else random.choice('x!@#$%^&*') for c in message)
            
            # Generate three sections of thorns with varying lengths
            left_thorns = generate_thorn_section(random.randint(10, 15))
            middle_thorns = generate_thorn_section(random.randint(5, 10))
            right_thorns = generate_thorn_section(random.randint(10, 15))
            
            # Randomly position the message between thorn sections
            sections = [
                f"{Style.DIM}{left_thorns}",
                f"{Style.BRIGHT}{corrupted_msg}",
                f"{Style.DIM}{middle_thorns}",
                f"{Style.DIM}{right_thorns}"
            ]
            
            msg_pos = random.randint(0, 2)
            sections.insert(msg_pos, sections.pop(1))  # Move message to random position
            # Ensure the entire line starts with red color and ends with reset
            line = f"{Fore.RED}" + " ".join(sections) + f"{Style.RESET_ALL}"
        else:
            # Create a purely decorative line with thorns
            thorn_sections = [
                generate_thorn_section(random.randint(15, 20)),
                generate_thorn_section(random.randint(15, 20)),
                generate_thorn_section(random.randint(15, 20))
            ]
            line = f"{Fore.RED}{Style.DIM}{' '.join(thorn_sections)}{Style.RESET_ALL}"
        
        output_lines.append(("\t\t\t\t\t\t\t\t" if i == 0 else "") + line)
    
    return '\n\t\t\t\t\t\t\t\t'.join(output_lines) 

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
APIKEY = os.getenv("APIKEY")
API_BASE_URL = BASE_URL
headers = {"Authorization": "Bearer " + APIKEY}

default_sys_prompt = "You are a fortune teller who helps people tell fortunes! Keep things to one sentence."

inputs = [
    { "role": "system", "content": f"{default_sys_prompt}" },
    { "role": "user", "content": f"I got a B in my English class, is my life over?" }
]

adjectives = [
   "enchanted",
   "victorian", 
   "tech bro",
   "skater boy",
   "she did ballet",
   "poetic",
   "playful",
   "ancient",
   "the traveling people from robert jordans the wheel of time",
   "bohemian",
   "sage-like",
   "fantastical",
   "vintage",
    "fanciful",
    "valley girl"
]

adjectives_dict = {
    "enchanted": "fairy green",
    "victorian": "faded yellow",
    "tech bro": "vivid blue",
    "skater boy": "grunge grey",
    "she did ballet": "pastel pink",
    "poetic": "deep purple",
    "playful": "bright orange",
    "ancient": "earthy brown",
    "the traveling people from robert jordans the wheel of time": "rainbow chars",
    "bohemian": "blue and green and yellow",
    "sage-like": "soft grey",
    "fantastical": "sunburst yellow with interspersed purple",
    "vintage": "sepia",
    "fanciful": "bubblegum pink",
    "valley girl": "neon pink and bright blue",
    "whimsical": "blue, purple, and silver",
    "trippy hippy": "tie-dye",
    "mysterious": "black and red"
}

bewitched_sounds = ['*cackle*', '*;)*', '*hehehe*', '*bwahaha*', '*snicker*', '*chortle*', '*giggle*', '*snort*']
cursed_sounds = ['You hear the sound of bones rattling...', 'A chill sweeps through the air...', 'A faint whisper echoes...', '.....Is there someone behind you? . . .']

def run(model, inputs):
    input = { "messages": inputs }
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()

def change_inputs(sys_prompt, user_prompt, adjective, is_bewitched, is_cursed):

    if not is_bewitched:
        print(f"Not cursed {is_cursed} or Bewitched {is_bewitched}")
        inputs = [
            { "role": "system", "content": f"{sys_prompt} Use this adjective to style your response: {adjective}" },
            { "role": "user", "content": f"{user_prompt}" }
        ]
    elif is_bewitched and not is_cursed:
        print(f"Not cursed {is_cursed} and Bewitched {is_bewitched}")
        
        inputs = [
            { "role": "system", "content": f"{sys_prompt} Use this adjective to style your response: {adjective}" },
            { "role": "user", "content": f"{user_prompt}" }
        ]
    else:
        print(f"Cursed {is_cursed} and Bewitched {is_bewitched}")
        inputs = [
            { "role": "system", "content": f"{sys_prompt}" },
            { "role": "user", "content": f"{user_prompt}" }
        ]
    print(f"System prompt: {inputs[0]['content']}")
    print(f"User prompt: {inputs[1]['content']}")
    return inputs

def check_if_bewitched():
    num = random.randrange(0, 5)
    # num = random.randrange(0, 1)
    print(f"Bewitchment roll: {num}")
    if num == 0:
        num = random.randrange(0, len(bewitched_sounds))
        print(f"\t\t\t\t\t\t\t\t\t\t\t{bewitched_sounds[num]}")
        return True
    else:
        return False
    
def check_if_cursed():
    num = random.randrange(0, 3)
    # num = random.randrange(0, 1)
    print(f"Cursed roll: {num}")
    if num == 0:
        num = random.randrange(0, len(cursed_sounds))
        print(f"\t\t\t\t\t\t\t\t\t{cursed_sounds[num]}")
        return True
    else:
        return False
    
telling_fortunes = True

while(telling_fortunes) == True:
    user_question = "I got a B in my English class, is my life over?"
    # user_question = input("What do you want to know about your future? ")
    is_bewitched = check_if_bewitched()
    if is_bewitched:
        is_cursed = check_if_cursed()
        if is_cursed:
            num = random.randrange(0, 4)
            print(f"Cursed scenario roll: {num}")
            if num == 0:
                sys_prompt = "You are a wicked witch who loves to curse people. You take pleasure in making people's lives miserable. You are sarcastic, mean, and enjoy causing chaos. You always give answers that are harmful and negative, and you never help people. You are very creative in your curses and love to come up with new ways to ruin someone's day. Keep it to one sentence."
                user_prompt = f"{user_question}. Give them a curse that will make their life miserable."
                inputs = change_inputs(sys_prompt, user_prompt, "", is_bewitched, is_cursed)
            elif num == 1:
                sys_prompt = f"{default_sys_prompt}. You feel like lying today, so you will give a false fortune that will lead to bad outcomes. Keep it to one sentence."
                user_prompt = f"{user_question}. "
                inputs = change_inputs(sys_prompt, user_prompt, "", is_bewitched, is_cursed)
            elif num == 2:
                sys_prompt = f"{default_sys_prompt}. Your answer will be sickly sweet, encouraging unless they are insightful enough to see the hidden danger. Keep it to one sentence."
                user_prompt = f"{user_question}. "
                inputs = change_inputs(sys_prompt, user_prompt, "", is_bewitched, is_cursed)
            elif num == 3:
                print("Fool! You should know better than to meddle with the future, one glimpse could cause ruin. RUIN! Begone before I decide to use your toes for my next potion!")
                continue
    else:
        is_cursed = False
        num = random.randrange(0, 3)
        if num == 0:
            sys_prompt = f"{default_sys_prompt}."
            user_prompt = f"{user_question}"
            inputs = change_inputs(sys_prompt, user_prompt, "whimsical", is_bewitched, is_cursed)
        elif num == 1:
            sys_prompt = f"{default_sys_prompt}."
            user_prompt = f"{user_question}"
            inputs = change_inputs(sys_prompt, user_prompt, "trippy hippy", is_bewitched, is_cursed)
        elif num == 2:
            sys_prompt = f"{default_sys_prompt}."
            user_prompt = f"{user_question}"
            inputs = change_inputs(sys_prompt, user_prompt, "mysterious", is_bewitched, is_cursed)
        else: 
            user_choice = input("Do you want a specific style for your fortune? (y/n) ")
            if user_choice.lower() == 'y':
                print("Here are the available styles:")
                for i, adj in enumerate(adjectives):
                    print(f"{i}: {adj}")
                choice = int(input("Enter the number of your chosen style: "))
                if 0 <= choice < len(adjectives):
                    chosen_adjective = adjectives[choice]
                else:
                    print("Invalid choice, defaulting to 'mysterious'.")
                    chosen_adjective = "mysterious"
                sys_prompt = f"{default_sys_prompt}."
                user_prompt = f"{user_question}"
                inputs = change_inputs(sys_prompt, user_prompt, chosen_adjective, is_bewitched, is_cursed)
            else:
                num = random.randrange(0, 15)
                sys_prompt = f"{default_sys_prompt}."
                user_prompt = f"{user_question}"
                inputs = change_inputs(sys_prompt, user_prompt, adjectives[num], is_bewitched, is_cursed)
    
    output = run("@cf/meta/llama-3-8b-instruct", inputs)
    response_text = output["result"]["response"]
    
    # Apply styling based on the chosen adjective or cursed state
    if not is_cursed:
        current_adjective = inputs[0]["content"].split("Use this adjective to style your response: ")[-1].strip(".")
        if current_adjective in adjectives_dict:
            style = adjectives_dict[current_adjective]
            # Apply different color combinations based on the style
            if style == "fairy green":
                styled_text = f"{Fore.GREEN}{Style.BRIGHT}{response_text}{Style.RESET_ALL}"
            elif style == "faded yellow":
                styled_text = f"{Fore.YELLOW}{Style.DIM}{response_text}{Style.RESET_ALL}"
            elif style == "vivid blue":
                styled_text = f"{Fore.BLUE}{Style.BRIGHT}{response_text}{Style.RESET_ALL}"
            elif style == "grunge grey":
                styled_text = f"{Fore.WHITE}{Style.DIM}{response_text}{Style.RESET_ALL}"
            elif style == "pastel pink":
                styled_text = f"{Fore.MAGENTA}{Style.DIM}{response_text}{Style.RESET_ALL}"
            elif style == "deep purple":
                styled_text = f"{Fore.MAGENTA}{Style.BRIGHT}{response_text}{Style.RESET_ALL}"
            elif style == "bright orange":
                styled_text = f"{Fore.RED}{Fore.YELLOW}{Style.BRIGHT}{response_text}{Style.RESET_ALL}"
            elif style == "earthy brown":
                styled_text = f"{Fore.RED}{Style.DIM}{response_text}{Style.RESET_ALL}"
            elif style == "rainbow chars":
                colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
                styled_text = ""
                for i, char in enumerate(response_text):
                    styled_text += f"{colors[i % len(colors)]}{char}"
                styled_text += Style.RESET_ALL
            elif style == "blue and green and yellow":
                styled_text = f"{Fore.BLUE}{response_text[:len(response_text)//3]}{Fore.GREEN}{response_text[len(response_text)//3:2*len(response_text)//3]}{Fore.YELLOW}{response_text[2*len(response_text)//3:]}{Style.RESET_ALL}"
            elif style == "soft grey":
                styled_text = f"{Fore.WHITE}{Style.DIM}{response_text}{Style.RESET_ALL}"
            elif style == "sunburst yellow with interspersed purple":
                styled_text = ""
                for i, char in enumerate(response_text):
                    if i % 5 == 0:
                        styled_text += f"{Fore.MAGENTA}{char}"
                    else:
                        styled_text += f"{Fore.YELLOW}{Style.BRIGHT}{char}"
                styled_text += Style.RESET_ALL
            elif style == "sepia":
                styled_text = f"{Fore.YELLOW}{Style.DIM}{response_text}{Style.RESET_ALL}"
            elif style == "bubblegum pink":
                styled_text = f"{Fore.MAGENTA}{Style.BRIGHT}{response_text}{Style.RESET_ALL}"
            elif style == "neon pink and bright blue":
                words = re.split('(\\s+)', response_text)
                styled_text = ""
                word_count = 0
                for part in words:
                    if part.strip():  # If it's a word
                        if word_count % 2 == 0:
                            styled_text += f"{Fore.MAGENTA}{Style.BRIGHT}{part}"
                        else:
                            styled_text += f"{Fore.BLUE}{Style.BRIGHT}{part}"
                        word_count += 1
                    else:  # If it's spacing
                        styled_text += part
                styled_text += Style.RESET_ALL
            elif style == "blue, purple, and silver":
                styled_text = f"{Fore.BLUE}{response_text[:len(response_text)//3]}{Fore.MAGENTA}{response_text[len(response_text)//3:2*len(response_text)//3]}{Style.DIM}{Fore.WHITE}{response_text[2*len(response_text)//3:]}{Style.RESET_ALL}"
            elif style == "tie-dye":
                colors = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN]
                words = re.split('(\\s+)', response_text)
                styled_text = ""
                word_count = 0
                for part in words:
                    if part.strip():  # If it's a word
                        styled_text += f"{colors[word_count % len(colors)]}{Style.BRIGHT}{part}"
                        word_count += 1
                    else:  # If it's spacing
                        styled_text += part
                styled_text += Style.RESET_ALL
            elif style == "neon":
                colors = [Fore.CYAN, Fore.MAGENTA]
                words = re.split('(\\s+)', response_text)
                styled_text = ""
                word_count = 0
                for part in words:
                    if part.strip():  # If it's a word
                        styled_text += f"{Style.BRIGHT}{colors[word_count % len(colors)]}{part}"
                        word_count += 1
                    else:  # If it's spacing
                        styled_text += part
                styled_text += Style.RESET_ALL
            elif style == "black and red":
                import re
                # Split keeping spaces and empty strings
                words = re.split('(\\s+)', response_text)
                styled_text = ""
                word_count = 0
                for part in words:
                    if part.strip():  # If it's a word
                        if word_count % 2 == 0:
                            styled_text += f"{Style.DIM}{part}"
                        else:
                            styled_text += f"{Fore.RED}{Style.BRIGHT}{part}"
                        word_count += 1
                    else:  # If it's spacing
                        styled_text += part
                styled_text += Style.RESET_ALL
            else:
                styled_text = response_text
        else:
            styled_text = response_text
    else:
        # Apply cursed styling (alternating black and red words)
        styled_text = ""
        for i, word in enumerate(response_text.split()):
            if i % 2 == 0:
                styled_text += f"{Style.DIM}{word} "
            else:
                styled_text += f"{Fore.RED}{Style.BRIGHT}{word} "
        styled_text += Style.RESET_ALL

    # Create bordered version of the styled text
    border_color = Fore.RED if is_cursed else (Fore.MAGENTA if is_bewitched else Fore.CYAN)
    # Keep the original styling for the text but add borders with their own color
    bordered_text = create_decorative_border(styled_text)
    print("\n" + bordered_text.replace("~", f"{border_color}~{Style.RESET_ALL}"))
        
    if not is_bewitched and not is_cursed:
        print('\n\t\t\t\t\t\t\t\033[36m~~~~~~**\033[1mThank you for visiting the mystical fortune teller\033[0m\033[36m**~~~~~~\033[0m\n\t\t\t\t\t\t\t\t\t\033[32m~~~~~**May your future be bright**~~~~~\033[0m')
    elif is_bewitched and not is_cursed:
        print('\n\t\t\t\t\t\t\t\033[35m~~~~~~**\033[1mThank you for visiting the mystical fortune teller\033[0m\033[35m**~~~~~~\033[0m\n\t\t\t\t\t\t\t\t\t\033[31m~~~~~**May your futu . . .**~~~~~\033[0m\n\t\t\t\t\t\t\t\t\t\t\033[3m\033[31m~~~~~**. . .something doesn\'t feel right about this**~~~~~\033[0m\n')
    elif is_cursed:
        print(f'\n\t\t\t\t\t\t\t{Fore.RED}~~~~~~**{Style.BRIGHT}{Style.DIM}Thank you for visiting the mystical fortune teller{Style.RESET_ALL}{Fore.RED}**~~~~~~{Style.RESET_ALL}')
        # Add the cursed message after the fortune with a delay
        time.sleep(0.5)  # Short pause before the curse begins
        for line in generate_cursed_message().split('\n'):
            delay = random.betavariate(1.5, 4) * 0.6 + 0.1
            time.sleep(delay)
            print(line)
    
    telling_fortunes = False