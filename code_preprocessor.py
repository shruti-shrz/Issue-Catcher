import re
# function to remove unnecessary punctuation marks to get the words out of code
def code_preprocess(text):
    result=[]
    pure_text = ''
    for char in text:
        if char.isalnum():
            pure_text += char
        else:
            pure_text += ' '
    pure_text = re.sub(' +', ' ', pure_text)
    pure_txt = pure_text.strip()
    #print(pure_txt)
    result = pure_txt.split(' ')
    print('----------WORDS---------')
    print(result)
    return result