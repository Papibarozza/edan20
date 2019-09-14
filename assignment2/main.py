import regex as re
with open('Selma.txt', 'r',encoding="utf-8") as file:
  text = file.read()
  #for m in re.finditer(r'([\p{Lu}][^\.\n]+\.)', text):

  txt2 = (re.sub(r'[^\P{P}.]+','',text)) #Removes every punctuation character that is not a dot
  txt3 = re.sub(r'([\p{Lu}\p{L}]+[^\.]+\.)',r'<s> \1 </s>',txt2) #Find all sentences which begins with uppercase letter and ends with dot.
  txt4 = re.sub(r'\.','',txt3).lower() #Removes the dot and makes the text lowercase.
  print(txt4[-500:])
