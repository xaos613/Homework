'''
Implement a function which search for most common words in the file.
Use data/lorem_ipsum.txt file as a example.
'''

def most_common_words(filepath, number_of_words=3):

    result_dict = {}

    with open('data/lorem_ipsum.txt') as file:
        for row in file:
            row = row.replace(".", "").replace(",", "").lower()
            for word in row.split():
                if word in result_dict:
                    result_dict[word] +=1
                else:
                    result_dict[word] = 1


    sorted_keys = sorted(result_dict, key=result_dict.get, reverse=True)

    return sorted_keys[:number_of_words]

print(most_common_words('Homework/data/lorem_ipsum.txt'))


