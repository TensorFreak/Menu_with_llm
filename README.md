Simple project that automates restaurant menu translation and extends it with dishes descriptions.

Outline:

data: json file in Spain with dishes categories, names and prices.

model: Mixtral-8x7b-32768 + Groq API

process:

1) parse json and make txt menu file

2) translate via llm and write to new txt

3) ask llm to generate short description

4) construct new json with all generated data.


Possible improvements:
1) In case of long menu text items should be processed "in batches" to prevent "lost in the middle" model behavior

2) Add assertions and checks on initial items count and length of the description

3) Add more refined details about style of dishes description.

