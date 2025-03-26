import requests
import pathlib
import os
import re

unwanted_phrases = ["<Media omitted>", "This message was deleted", "You deleted this message", "<Video note omitted>"]
kq_chat = "chatlog\cleaned_whatsapp_chat_kq.txt"
jl_chat = "chatlog\cleaned_whatsapp_chat_jl.txt"
cs_chat = "chatlog\cleaned_whatsapp_chat_cs.txt"
jr_chat = "chatlog\cleaned_whatsapp_chat_jr.txt"
dennis_chat = "chatlog\cleaned_whatsapp_chat_dennis.txt"
hursh_chat = "chatlog\cleaned_whatsapp_chat_hursh.txt"

# To convert list of something into text file, used for the wordle part
def convert_to_txt(lst, path):
    with open(path, "w", encoding="utf-8") as file:
        for word in lst:
            file.write(word + "\n")

    return 

# Remove away audio omit and message deleted from whatsapp chat log
def clean_chat(input_file, output_file):
    counter = 0
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            if counter < 4:
                counter += 1
                continue
            if not any(phrase in line for phrase in unwanted_phrases):
                outfile.write(line)

# Only take chat log from a specific person
def specify_person(input_file, person, output_file):
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        speaker = None 
        message = []  
        
        for line in infile:
            if not line.strip():
                continue
            
            if line[0].isdigit():
                if message and speaker:
                    if speaker == person:
                        outfile.write(f"{speaker}: {''.join(message)}\n")
                
                parts = line.split(" - ", 1)  
                if len(parts) > 1:
                    message_part = parts[1]
                    if ":" in message_part:
                        speaker, message_content = message_part.split(":", 1)
                        speaker = speaker.strip()  
                        message = [message_content.strip()] 
                    else:
                        continue
            else:
                if speaker and line.strip():
                    message.append(line.strip())
        
        if message and speaker:
            if speaker == person:
                outfile.write(f"{speaker}: {''.join(message)}\n")


# Convert specified chat log to openai format {'speaker':'____', 'message': '______'}
def process_chat_logs(file_path):
    """Converts the cleaned chat data into a structured format."""
    conversation = []

    # Open the file and read it line by line
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        # Match pattern "Speaker: Message"
        '''
        Regex breakdown: ^ indicates start of string
                         \w to match any word character, for single names
                         \s to match whitespace character, for names with spaces
                          + for more than one occurrence
                         () to capture the entire group                       
        '''
        match = re.match(r"^([\w\s]+): (.*)", line.strip()) # regex to capture the speaker and message
        if match:
            speaker, message = match.groups()
            conversation.append({"speaker": speaker, "message": message})

    return conversation

        

            