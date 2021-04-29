
# function to remove unnecessary punctuation marks to get the words out of code
def code_preprocess(text):
    result=[]
    pure_text = ''
    for char in text:
        if char.isalnum():
            pure_text += char
        else:
            pure_text += ' '
    result = pure_text.split(' ')
    print('----------WORDS---------')
    print(result)
    return result