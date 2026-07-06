"""
Wordle: Terminal Edition
A command-line implementation of the popular word-guessing game Wordle.
Designed for Stanford Code in Place 2026.

This program chooses a random 5-letter secret word from a predefined pool.
The player has 6 attempts to guess the secret word.
Feedback is given after each guess:
- Correct letter in the correct position: [L] (capitalized in brackets)
- Correct letter in the wrong position: l* (lowercase with an asterisk)
- Letter not in the secret word: _ (underscore)
"""

import random
import sys

# Predefined clean list of common 5-letter English words.
# Defensively filtered to ensure all entries are exactly 5 alphabetic letters.
RAW_WORDS_POOL = [
    "about", "above", "actor", "acute", "admit", "adopt", "adult", "after", "again", "agent",
    "agree", "ahead", "alarm", "album", "alert", "alike", "alive", "allow", "alone", "along",
    "alter", "among", "anger", "angle", "angry", "apart", "apple", "apply", "arena", "argue",
    "arise", "array", "arrow", "aside", "asset", "audio", "audit", "avoid", "award", "aware",
    "baker", "basic", "basis", "beach", "began", "begin", "begun", "being", "below", "bench",
    "birth", "black", "blade", "blame", "blind", "block", "blood", "board", "boost", "booth",
    "bound", "brain", "brand", "bread", "break", "breed", "brief", "bring", "broad", "broke",
    "brown", "build", "built", "buyer", "cable", "candy", "carry", "carve", "catch", "cause",
    "chain", "chair", "chart", "chase", "cheap", "check", "chest", "chief", "child", "china",
    "choir", "chose", "cigar", "claim", "class", "clean", "clear", "climb", "clock", "close",
    "cloud", "coach", "coast", "court", "cover", "craft", "crash", "cream", "crime", "cross",
    "crowd", "crown", "crude", "crush", "curve", "cycle", "daily", "dance", "death", "depth",
    "dirty", "doubt", "draft", "drama", "dream", "dress", "drink", "drive", "drove", "dying",
    "eager", "early", "earth", "eight", "elite", "empty", "enemy", "enjoy", "enter", "entry",
    "equal", "error", "event", "every", "exact", "exist", "extra", "faith", "false", "fatal",
    "fault", "fiber", "field", "fifth", "fifty", "fight", "final", "first", "fixed", "flame",
    "flesh", "float", "flood", "floor", "fluid", "flyer", "focus", "force", "frame", "frank",
    "fresh", "front", "fruit", "fully", "funny", "giant", "given", "glass", "globe", "going",
    "grace", "grade", "grand", "grant", "grass", "grave", "great", "green", "gross", "group",
    "grown", "guard", "guess", "guest", "guide", "habit", "happy", "harsh", "heavy", "hence",
    "honey", "honor", "horse", "hotel", "house", "human", "ideal", "image", "index", "inner",
    "input", "irony", "issue", "joint", "judge", "juice", "knife", "knock", "known", "label",
    "labor", "large", "laser", "later", "laugh", "layer", "learn", "lease", "least", "leave",
    "legal", "lemon", "level", "light", "limit", "logic", "loose", "lower", "lucky", "lunch",
    "lying", "magic", "major", "maker", "march", "match", "maybe", "mayor", "meant", "media",
    "metal", "might", "minor", "minus", "mixed", "model", "money", "month", "moral", "motor",
    "mount", "mouse", "mouth", "movie", "music", "needs", "never", "newly", "night", "noise",
    "north", "noted", "novel", "nurse", "occur", "ocean", "offer", "often", "order", "other",
    "ought", "outer", "owned", "owner", "paint", "panel", "paper", "party", "peace", "phase",
    "phone", "photo", "piano", "piece", "pilot", "pitch", "place", "plain", "plane", "plant",
    "plate", "point", "pound", "power", "press", "price", "pride", "prime", "print", "prior",
    "prize", "prove", "proud", "quick", "quiet", "quite", "radio", "raise", "range", "ratio",
    "reach", "react", "ready", "refer", "right", "rival", "river", "robot", "rough", "round",
    "route", "royal", "rugby", "ruler", "rural", "sadly", "safer", "salad", "sales", "scale",
    "scene", "scope", "score", "sense", "serve", "seven", "shall", "shame", "shape", "share",
    "sharp", "sheet", "shelf", "shell", "shift", "shine", "shirt", "shock", "shoot", "shore",
    "short", "shown", "sight", "since", "sites", "sixth", "sixty", "sized", "skill", "sleep",
    "slide", "small", "smart", "smile", "smoke", "solid", "solve", "sorry", "sound", "south",
    "space", "spare", "speak", "speed", "spend", "spent", "split", "spoke", "sport", "staff",
    "stage", "stake", "stand", "start", "state", "steam", "steel", "stick", "still", "stock",
    "stone", "stood", "store", "storm", "story", "strip", "stuck", "study", "style", "sugar",
    "suite", "super", "sweet", "swept", "swift", "swing", "table", "taken", "taste", "taxed",
    "teach", "teeth", "terry", "texas", "thank", "theft", "their", "theme", "there", "these",
    "thick", "thief", "thigh", "thing", "think", "third", "those", "three", "threw", "throw",
    "tight", "times", "tired", "title", "today", "token", "tonal", "topic", "total", "touch",
    "tough", "tower", "track", "trade", "trail", "train", "trait", "treat", "trend", "trial",
    "tribe", "trick", "tried", "tries", "truck", "truly", "trust", "truth", "twice", "under",
    "undue", "union", "unity", "until", "upper", "upset", "urban", "usage", "usual", "vague",
    "valid", "value", "video", "virus", "visit", "vital", "voice", "waste", "watch", "water",
    "wheel", "where", "which", "while", "white", "whole", "whose", "wider", "widow", "woman",
    "women", "world", "worry", "worse", "worst", "worth", "would", "wound", "write", "wrong",
    "wrote", "yield", "young", "youth", "zebra"
]

MAX_ATTEMPTS = 6
WORD_LENGTH = 5


def load_words() -> list[str]:
    """
    Cleans and loads the list of words.
    Returns a list of 5-letter uppercase alphabetic strings.
    """
    cleaned_words = []
    for word in RAW_WORDS_POOL:
        stripped = word.strip().upper()
        if len(stripped) == WORD_LENGTH and stripped.isalpha():
            cleaned_words.append(stripped)
    return cleaned_words


def get_valid_guess() -> str:
    """
    Prompts the user to enter a 5-letter word guess.
    Validates that the input consists of exactly 5 alphabetical characters.
    Repeats until a valid guess is entered.
    
    Returns:
        str: A valid uppercase 5-letter string.
    """
    while True:
        guess = input(f"Enter your guess (must be {WORD_LENGTH} letters): ").strip()
        
        # Check length
        if len(guess) != WORD_LENGTH:
            print(f"Error: Guess must be exactly {WORD_LENGTH} letters long.")
            continue
            
        # Check if alphabetic
        if not guess.isalpha():
            print("Error: Guess must contain only alphabetic characters (A-Z).")
            continue
            
        return guess.upper()


def get_feedback(secret_word: str, guess: str) -> str:
    """
    Compares the guess with the secret word and generates the Wordle feedback.
    Correctly handles duplicate letters by matching exact spots first,
    then partial spots based on remaining count, and marking others as absent.

    Feedback Rules:
    - Right letter, right spot: [L]
    - Right letter, wrong spot: l*
    - Wrong letter: _

    Args:
        secret_word (str): The uppercase secret word to be guessed.
        guess (str): The uppercase 5-letter guess.

    Returns:
        str: A space-separated feedback string.
    """
    # Initialize list of feedbacks for each letter position
    feedback = [None] * WORD_LENGTH
    
    # Count occurrences of each letter in the secret word to track matches
    secret_letter_counts = {}
    for letter in secret_word:
        secret_letter_counts[letter] = secret_letter_counts.get(letter, 0) + 1
        
    # Pass 1: Look for exact matches (right spot / green / [L])
    for i in range(WORD_LENGTH):
        if guess[i] == secret_word[i]:
            feedback[i] = f"[{guess[i]}]"
            secret_letter_counts[guess[i]] -= 1

    # Pass 2: Look for partial matches (wrong spot / yellow / l*)
    for i in range(WORD_LENGTH):
        if feedback[i] is None:
            letter = guess[i]
            # If the letter exists in secret and has remaining unmatched counts
            if letter in secret_letter_counts and secret_letter_counts[letter] > 0:
                feedback[i] = f"{letter.lower()}*"
                secret_letter_counts[letter] -= 1
            else:
                feedback[i] = "_"

    return " ".join(feedback)


def play_game(word_list: list[str]) -> bool:
    """
    Executes a single game of Wordle.
    
    Args:
        word_list (list[str]): The pool of secret words.
        
    Returns:
        bool: True if the user won, False otherwise.
    """
    # Choose a random secret word
    secret_word = random.choice(word_list)
    
    print("\n" + "=" * 50)
    print("A new word has been chosen! Can you guess it?")
    print("Feedback Legend:")
    print("  [A] -> Correct letter in the correct spot.")
    print("  a*  -> Correct letter, but in the wrong spot.")
    print("  _   -> Letter is not in the word at all.")
    print("=" * 50)

    # Store game history to show the board progress at each step
    guess_history = []
    
    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n--- Attempt {attempt} of {MAX_ATTEMPTS} ---")
        guess = get_valid_guess()
        
        # Get feedback for the current guess
        feedback = get_feedback(secret_word, guess)
        guess_history.append((guess, feedback))
        
        # Display the board showing all previous attempts
        print("\n--- Current Board ---")
        for i, (g, fb) in enumerate(guess_history):
            print(f"Guess {i+1}: {fb}  (guessed: {g})")
            
        # Check if the player won
        if guess == secret_word:
            print(f"\n🎉 Congratulations! You guessed the word '{secret_word}' in {attempt} attempts!")
            return True

    print(f"\nGame Over! You've run out of attempts. The secret word was '{secret_word}'.")
    return False


def main():
    """
    Main entry point for Wordle: Terminal Edition.
    Presents the welcome message, initializes the words, and handles replays.
    """
    # Print welcome banner
    print("==========================================")
    print("       WORDLE: TERMINAL EDITION")
    print("==========================================")
    print("Welcome to Wordle! Try to guess the secret 5-letter word.")
    print("You have 6 attempts. Let's see how smart you are!")
    
    # Load and sanitize the word pool
    word_list = load_words()
    if not word_list:
        print("Error: The word pool is empty. Please check your word definition list.", file=sys.stderr)
        sys.exit(1)
        
    # Stats tracking
    games_played = 0
    games_won = 0

    while True:
        games_played += 1
        won = play_game(word_list)
        if won:
            games_won += 1
            
        print("\n" + "-" * 30)
        print(f"Stats: {games_won}/{games_played} games won ({games_won/games_played:.1%})")
        print("-" * 30)
        
        # Ask to replay
        replay = input("\nWould you like to play again? (y/n): ").strip().lower()
        if replay not in ['y', 'yes']:
            print("\nThank you for playing Wordle: Terminal Edition! Goodbye!")
            break


if __name__ == "__main__":
    main()