# %% 
import datetime
import os
import random
import re
import time
# %% store number of questions per chapter
question_counts = {
    "arithmetic": 35,
    "inequalities_absolute_values": 41,
    "functions_formulas_sequences": 57,
    "fractions_decimals": 38,
    "percents": 54,
    "divisibility_primes": 33,
    "exponents_roots": 31,
    "number_properties": 39,
    "word_problems": 28,
    "two_variable_word_problems": 25,
    "rates_work": 29,
    "variables_in_the_choices_problems": 20,
    "ratios": 36,
    "avg_weighted_avg_median_mode": 37,
    "sd_normal_dist": 31,
    "probability_combinatorics_overlapping_sets": 46,
    "data_interpretation": 49,
    "polygons_rectangular_solids": 22,
    "circles_cylinders": 25,
    "triangles": 42,
    "coordinate_geometry": 24,
    "mixed_geometry": 18,
    "advanced_quant": 42
}
# %% timer function
# Create class that acts as a countdown
def countdown(m):
 
    # Calculate the total number of seconds
    total_seconds = m * 60
 
    # While loop that checks if total_seconds reaches zero
    # If not zero, decrement total time by one second
    while total_seconds > 0:
 
        # Timer represents time left on countdown
        timer = datetime.timedelta(seconds = total_seconds)
        
        # Prints the time left on the timer
        print(timer, end="\r")
 
        # Delays the program one second
        time.sleep(1)
 
        # Reduces total time by one second
        total_seconds -= 1
 
    print("Time over!")
# %%
def choose_by_difficulty(n, topic, difficulty = "all"):
    difficulty = difficulty[0].lower()
    if (topic == "advanced_quant") or (difficulty == "a"):
        return(range(n))
    if difficulty == "e":
        return(range(n)[0:round(n*0.25)])
    if difficulty == "m":
        return(range(n)[round(n*0.25):round(n*0.75)])
    if difficulty == "h":
        return(range(n)[round(n*0.75):n-1])
# %%
def create_question(topic, difficulty):
    n = str(random.choice(choose_by_difficulty(question_counts[topic], topic, difficulty))+1)
    if len(n) == 1:
        n = "0" + n
    q = topic + "_" + n
    return(q)
# %%
def create_practice_set(n=20, t=35, difficulty = "all", history = "no", past_questions = []):
    # determine difficulty level of questions
    difficulty = difficulty.lower()[0]
    while difficulty not in ["a", "e", "m", "h"]:
        difficulty = input("Please choose difficulty level (all, easy, medium, hard): ")[0].lower()
    # adjust weights of topics based on difficulty level
    if difficulty in ["e", "a"]:
        weights = [0.05] * 22 + [0.01]
    elif difficulty == "m":
        weights = [0.95/22] * 22 + [0.05]
    elif difficulty == "h":
        weights = [0.7/22] * 22 + [0.3]
    # choose n topics with replacement
    topics = random.choices(
        list(question_counts.keys()), 
        k = n, 
        weights = weights)
    # sort by order of topics in the book
    # topics = sorted(topics, key = lambda x: list(question_counts.keys()).index(x))
    # topics.sort(key=lambda x: list(question_counts.keys()).index(x)) # to reduce time spent on the search
    questions = list()
    for topic in topics:
        q = create_question(topic, difficulty)
        # avoid duplicate questions, also considering past questions
        while q in past_questions or q in questions:
                q = create_question(topic, difficulty)
        # append new questions
        questions.append(q)
    # define regex pattern to remove numbers from a question name
    pattern = r'[0-9]'
    questions = sorted(questions, key = lambda x: (list(question_counts.keys()).index(re.sub(pattern, '', x)[:-1]), x.split("_")[-1]))
    for i, q in enumerate(questions):
        print(str(i+1) + ") " + q)
    if history[0].lower() == "y":
        with open("5lb_question_history.txt", "a+") as file:
            file.write("\n")
            file.write(str(datetime.datetime.now()))
            for q in questions:
                file.write(q+"\n")
        print("Questions added to 5lb_question_history.txt.")
    # start timer
    input("Hit enter to start.")
    countdown(t)
# %%
n = input("How many questions do you want? ")
t = input("How many minutes do you want to work? ")
d = input("Please choose difficulty level (all, easy, medium, hard): ")
h = input("Do you want to store the questions in your history (yes/no)? ")
n = 20 if n == "" else int(n)
t = 35 if t == "" else int(t)
d = "all" if d == "" else d
h = "no" if h == "" else h
# %%
path = "5lb_question_history.txt"
if os.path.exists(path):
    with open(path) as file:
        history = file.readlines()
    history = [h[0:-2] for h in history if h[0].isalpha()]
else:
    history = []
# %%
create_practice_set(n, t, d, h, history)
# %%
