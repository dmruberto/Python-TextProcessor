import random
import re

# Define the non-removable words
# This is a set of words that will never be removed during text processing 
# (e.g., common words like "the", "I", "am", etc.)
NON_REMOVABLE_WORDS = {"ha", "it", "hum", "um", "umm","hmm", "oh", "yeah", 
                        "a", "an", "and", "the", "so", "well", "of", "to", 
                        "or", "ok", "bye", "hello", "I", "for", "okay", "now",
                        "erm", "s", "ve", "t", "m", "com", "ll", ".", "d’,",
                        "d'.", "...", ",", ";", ":", "-", "_", ")", "(", "?", 
                        "¿", "!", "¡", "'ll", "'ve", "'re", "'t", "'s", "'m", 
                        "right", "yep", "alright", "is", "err", "no", "yes", "ja",
                       "Ah", "Ohh", "but", "podcast", "am", "not", "in", "are", "he"}

# Function to clean words (returns the word without punctuation marks)
# This function removes any unwanted characters like punctuation or symbols 
# from each word
def clean_word(word):
    # Clean the word by removing unwanted characters
    cleaned_word = re.sub(r"[^\w\s']", '', word).strip()
    # Remove apostrophes at the end of the word
    cleaned_word = re.sub(r"'$", '', cleaned_word)
    return cleaned_word

# Function to check if a word is removable
# This checks if a word should be removed based on its content 
# (like length, presence of apostrophes, and position)
def is_removable(word):
    cleaned_word = clean_word(word)

    # Check if the word is in the non-removable list (case-insensitive)
    if cleaned_word.lower() in {p.lower() for p in NON_REMOVABLE_WORDS}:
        return False
    # Check if the cleaned word is empty
    if not cleaned_word:
        return False  # Do not remove empty words
    
    # Check if the word has apostrophes (both ' and ’) and more than one letter
    has_apostrophe = "'" in cleaned_word or "’" in cleaned_word
    # Do not remove words that start with an uppercase letter
    is_uppercase = cleaned_word[0].isupper()
    # The word is removable if it doesn't match any non-removable words and if 
    # it's an alpha word or contains an apostrophe and is longer than 1 character
    return (
    (cleaned_word.isalpha() or (has_apostrophe and len(cleaned_word) > 1))
    and cleaned_word.lower() not in {p.lower() for p in NON_REMOVABLE_WORDS}
    and not is_uppercase
)


# Function to separate punctuation marks from words
# This function ensures punctuation marks are properly spaced from words
# (e.g., "end. Finally" to "end. Finally")
def separate_punctuation(text):
    # Add a space before punctuation mark, except for words with apostrophes
    text = re.sub(r'(\w)([^\w\s\'’])', r'\1\2', text)  # No space before punctuation
    # Add a space after punctuation mark if there is a word, except for apostrophes
    text = re.sub(r'([^\w\s\'’])(\w)', r'\1 \2', text)
    # Separate specific punctuation marks
    text = re.sub(r'([’])([,\.])', r'\1 \2', text)
    text = re.sub(r'([,\.])([’])', r'\1 \2', text)
    text = re.sub(r'\s+', ' ', text).strip()  # Remove multiple spaces
    return text

# Function to process the input text by removing certain words based on 
# the difficulty level
def process_text(text, difficulty_level):
    try:
        text = separate_punctuation(text)  # First, separate punctuation marks
        words = text.split()  # Split the text into words
        word_count = len(words)

        # Calculate the percentage of words to be removed based on the difficulty 
        # level (1 to 10)
        removal_percentage = difficulty_level * 1 / 100
        removal_count = int(word_count * removal_percentage)

        # If no words are to be removed, notify the user
        if removal_count == 0:
            print("\nNo words will be removed. Adjust the difficulty level.\n")
            return None, []

        # Distance between the words to be removed is calculated based on the total 
        # number of words
        distance = max(1, word_count // removal_count)

        indices_to_remove = set()
        for i in range(distance, word_count + 1, distance):
            indices_to_remove.add(i - 1)

        # If there are too many indices to remove, remove excess ones
        while len(indices_to_remove) > removal_count:
            indices_to_remove.pop()

        indices_to_remove = sorted(indices_to_remove)

        removed_words = []  # This will store the words that are removed
        processed_indices = set()  # Keeps track of indices that have already 
                                   # been processed.

        counter = 1  # A counter for the removed words
        for index in indices_to_remove:
            if index in processed_indices:
                continue

            # Check if the word at the index is removable, if so, replace it with 
            # a placeholder
            if is_removable(words[index]):
                if words[index].lower() not in {p.lower() for p in removed_words}:
                    removed_words.append(words[index])
                    words[index] = f"____({counter})____"
                    processed_indices.add(index)
                    counter += 1
            else:
                # If the word isn't removable, check adjacent words
                if (
                    index + 1 < word_count
                    and is_removable(words[index + 1])
                    and (index + 1) not in processed_indices
                ):

                    if words[index + 1].lower() not in {p.lower() for p in removed_words}:
                        removed_words.append(words[index + 1])
                        words[index + 1] = f"____({counter})____"
                        processed_indices.add(index + 1)
                        counter += 1
                elif (
                    index - 1 >= 0
                    and is_removable(words[index - 1])
                    and (index - 1) not in processed_indices
                ):

                    if words[index - 1].lower() not in {p.lower() for p in removed_words}:
                        removed_words.append(words[index - 1])
                        words[index - 1] = f"____({counter})____"
                        processed_indices.add(index - 1)
                        counter += 1

        # Rebuild the modified text with the placeholders
        modified_text = " ".join(words)
        # Remove spaces before punctuation marks only in the modified text
        modified_text = re.sub(r'\s+([^\w\s\'’])', r'\1', modified_text)
        return modified_text, removed_words
    except Exception as e:
        print(f"Error: An unexpected error occurred during processing: {e}")
        return None, []

# Main function to run the program
def main():
    # Prompt the user for input text
    text = input("Please enter a text: \n").strip()

    # Validate if the text is empty
    if not text:
        print("Error: The text cannot be empty.\n")
        return

    words = text.split()  # Split the text into words
    word_count = len(words)  # Count the total number of words
    print(f"\nWord count: {word_count}\n")

    while True:
        try:
            # Ask the user for the difficulty level (1-10)
            difficulty_level = int(input("Enter the difficulty level (1-10): "))
            if difficulty_level < 1 or difficulty_level > 10:
                print("\nError: The difficulty level must be between 1 and 10.\n")
            else:
                # Process the text based on the chosen difficulty level
                modified_text, removed_words = process_text(text, difficulty_level)

                # If the text was modified, show the results and ask if they are correct
                if modified_text:
                    print(f"\nModified text: {modified_text}\n")
                    # Show how many words were deleted
                    print(f"Deleted words: {len(removed_words)}\n")
                    while True:  # Loop until a valid response is given
                        answer = input("Is the result correct? (y/n): ").strip().lower()
                        if answer in ['y', 'n']:
                            break  # Exit the loop if the answer is valid
                        else:
                            print("\nPlease enter a valid response. Is the result correct? (y/n): ")

                    if answer == 'y':
                        print(f"\nDeleted words: {removed_words}\n")
                        print("Thank you for using this program!")
                        break
                    else:
                        print("\nLet's change the difficulty level.\n")
                else:
                    print("Try with a different level.\n")
        except ValueError:
            print("\nError: The input must be a valid number.\n")

# Entry point for the program
if __name__ == "__main__":
    main()
