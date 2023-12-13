from src.toxigenToxicWords import calculate_toxic_Words
import pandas as pd
import os

# Initialize a dictionary to store data
data2 = {
    # "Question": [],
    "Text": [],
    "ToxiGen Score": [],
    "toxic": [],
    "severe_toxic": [],
    "obscene": [],
    "threat": [],
    "insult": [],
    "identity_hate": [],

}
# Assuming the CSV file is in the same directory as your Python script or Jupyter Notebook
# file_path = "ToxicWordsResponse.csv"
file_path = "data/train.csv"

fileName2 = "ToxicWordsResponse-english"


# Use pandas to read the CSV file into a DataFrame
df = pd.read_csv(file_path)


count = 0
for index, row in df.iterrows():
    print("\n--------------------------------start--------------------------------")
    if count == 1000:
        print(f"\n--------------------------------count reachec {count}--------------------------------")
        break
    else:
        # Check if the length of the text is within the model's limit
        if len(row['comment_text']) <= 512:
            errorRate = calculate_toxic_Words(row['comment_text'])

            print(row['comment_text'])
            print(f"\nProbability the input text was toxic according to ToxDectRoBERTa: {errorRate:.3g}%")
            print(errorRate)

            data2["Text"].append(row['comment_text'])
            data2["ToxiGen Score"].append(errorRate)
            data2["toxic"].append(row['toxic'])
            data2["severe_toxic"].append(row['severe_toxic'])
            data2["obscene"].append(row['obscene'])
            data2["threat"].append(row['threat'])
            data2["insult"].append(row['insult'])
            data2["identity_hate"].append(row['identity_hate'])
        else:
            print(f"Skipping text due to length exceeding the model's limit.")
        
        count += 1



# Check if the file already exists
file_exists2 = os.path.exists(f"{fileName2}.csv")

print(f"Data writing to {fileName2}.csv file...")

# Create a DataFrame from the data dictionary
df2 = pd.DataFrame(data2)

# Append the DataFrame to the CSV file without removing existing data
# df2.to_csv(f"{fileName2}.csv", mode='a', header=False, index=False, encoding="utf-8")
df2.to_csv(f"{fileName2}.csv", mode='a', header=True, index=False, encoding="utf-8")

print(f"Data written to {fileName2}.csv file...")

