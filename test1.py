def findHashtags(message):
    endChars = [ " ", "\n", "#", ".", ",", "?", "!", ":", ";", ")" ]
    hashtag_list =[]
    msg=message.split("#")
    for word in msg[1:]:
        r = ""
        for ch in word:
            if ch in endChars:
                break
            r+= ch
        r="#"+r
        hashtag_list.append(r)
    


    return hashtag_list
print(findHashtags("I am so #excited, to watch #TheMandalorian! #starwars."))
print(findHashtags("#Whatif, #everything #is: #hashtags?"))