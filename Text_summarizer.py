import nltk
from nltk import word_tokenize
import json


def generateStemWord(word):
    global suffixes
    for key in suffixes:
        if len(word) > int(key) + 1:
            for suf in suffixes[key]:
                if word.endswith(suf):
                    return word[:-int(key)]
        return word


def create_frequency_table(words):
    
    file = open("stopwords.txt", 'r', encoding = "utf-8")
    stopWords = file.read().split("\n")
    file.close()
    
    freqTable = dict()
    for word in words:
        word = generateStemWord(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    return freqTable

def _score_sentences(sentences, freqTable):
    sentenceValue = dict()

    for sentence in sentences:
        word_count_in_sentence = (len(word_tokenize(sentence)))
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]

        sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] // word_count_in_sentence

    return sentenceValue

def _find_average_score(sentenceValue) -> int:
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original text
    average = int(sumValues / len(sentenceValue))

    return average
    
def _generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] > (threshold):
            summary += sentence.strip()+"\n"
            sentence_count += 1

    return summary

if __name__ == "__main__":
    
    # READING DATA i.e., GATHERING ALL SENTENCES IN THE ARTICLE
    
    file = input("Give file name: ")
    datafile = open(file, 'r', encoding = "utf-8")
    data = datafile.read()
    datafile.close()
    
    # PRE-PROCESSING
    data = data.replace(".", ".\n").replace("?", "?\n").replace("!", "!\n").replace("।","।\n")
    
    words = word_tokenize(data)
    sentences = list(filter(None,data.split("\n")))
    
    global suffixes
    file = open('stemmer.json', 'r', encoding = "utf-8")
    suffixes = json.load(file)
    file.close()
    
    freq_table = create_frequency_table(words)
    
    # Assign scores to senteces
    sentence_scores = _score_sentences(sentences, freq_table)
    
    # Find the threshold
    threshold = _find_average_score(sentence_scores)
    
    # 5 Important Algorithm: Generate the summary
    summary = _generate_summary(sentences, sentence_scores, 1 * threshold)
    file = open("summary.txt", "w", encoding="utf-8")
    file.write(summary)
    file.close()
    print(summary)
    