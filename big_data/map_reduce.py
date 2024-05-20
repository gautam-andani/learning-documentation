x = """Q. Create a MapReduce program to count the number of unique words in a given input text file.

Dataset –
The quick brown fox jumps over the lazy dog.
How much wood would a woodchuck chuck if a woodchuck could chuck wood?
Peter Piper picked a peck of pickled peppers.
She sells seashells by the seashore.
I scream, you scream, we all scream for ice cream.
To be or not to be, that is the question.
All's well that ends well.
"""

import re
from collections import defaultdict

# Define a function to tokenize the text into a list of words 
def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

# Mapper function
def mapper(text):
    words = tokenize(text)
    print(words)
    mapped = []
    for word in words:
        mapped.append((word, 1))
    return mapped

# Shuffle and Sort function
def shuffle_and_sort(mapped_data):
    shuffled = defaultdict(list)
    for word, count in mapped_data:
        shuffled[word].append(count)
    return shuffled

# Reducer function
def reducer(shuffled_data):
    reduced = {}
    for word, counts in shuffled_data.items():
        reduced[word] = sum(counts)
    return reduced

# count unique words
def count_unique_words(reduced_data):
    unique_words = list(reduced_data.keys())
    return unique_words, len(unique_words)

# dataset
dataset = [
    "The quick brown fox jumps over the lazy dog.",
    "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
    "Peter Piper picked a peck of pickled peppers.",
    "She sells seashells by the seashore.",
    "I scream, you scream, we all scream for ice cream.",
    "To be or not to be, that is the question.",
    "All's well that ends well."
]

# Combine all lines into a single text
combined_text = " ".join(dataset)

mapped_data = mapper(combined_text)
shuffled_data = shuffle_and_sort(mapped_data)
reduced_data = reducer(shuffled_data)
unique_words, unique_count = count_unique_words(reduced_data)

print("Unique words:", unique_words)
print("Number of unique words:", unique_count)
