import nltk
import re
import operator


def extract_candidates(comparison_object, sentences):
    unique_candidates = {}
    print(len(sentences))
    for sentence in sentences:
        taglist = tag_sentence(sentence)
        for tag in taglist:
            if tag[1].startswith('NN'):
                candidate = tag[0].lower()
                if candidate not in [comparison_object, 'vs', 'vs.'] and is_candidate(candidate, comparison_object, sentence):

                    if candidate in unique_candidates:
                        unique_candidates[candidate] += 1
                    else:
                        unique_candidates[candidate] = 1

    unique_candidates = sorted(unique_candidates.items(), key=operator.itemgetter(1), reverse=True)
    return unique_candidates


def is_candidate(candidate, comparison_object, sentence):
    vs = ' (vs|vs.) '
    candidate = re.escape(candidate)
    pattern = '(' + candidate + vs + comparison_object + '|' + comparison_object + vs + candidate + ')'
    if re.match(pattern, sentence, re.IGNORECASE) is not None:
        # print(sentence)
        return True

def tag_sentence(sentence):
    '''
    Returns a list of tags for each word of the sentence. A tag is a combination of the word and
    its part of speech coded as an NLTK tag, for example ('apple', 'NN').
    '''
    # remove special characters
    # sentence = re.sub('[^a-zA-Z0-9 ]', ' ', sentence)
    # find all words in the sentence
    wordlist = nltk.word_tokenize(sentence)
    taglist = nltk.pos_tag(wordlist)
    return taglist