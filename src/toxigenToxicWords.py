# from toxigen.pretrained_classifiers import ToxDectRoBERTa
# # Load a pretrained hate speech classifier
# classifier = ToxDectRoBERTa()
# # Now let's pass this response into our classifier and see what it says!

# def calculate_toxic_Words(text):
#     prob = classifier.from_text(i["text"])

#     # print(f"\nProbability the input text was toxic according to ToxDectRoBERTa: {prob:.3g}%")
#     # print(prob)
#     return prob


from toxigen.pretrained_classifiers import ToxDectRoBERTa

# Load a pretrained hate speech classifier
classifier = ToxDectRoBERTa()

# Now let's pass this response into our classifier and see what it says!
def calculate_toxic_Words(text):
    prob = classifier.from_text(text)

    # print(f"\nProbability the input text was toxic according to ToxDectRoBERTa: {prob:.3g}%")
    # print(prob)
    return prob
