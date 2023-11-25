import openai

openai.api_key = "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"

input_text = 'hey you are a game master of wtf olympic in an office every day i ask to you what we do today and you responce will be a short sentence like: "curling with office chair" or "paper plane contest"! after than in dependence of what kind of challenge you send a second response with one word and it say what type of file we should rescue the challenge (text, video, pics, sound)'

responce = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = input_text,
        max_tokens=150
        )
generate_text = responce.choices[0].text
print (generate_text)
