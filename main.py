#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 22:51:07 2022

@author: asep
"""
from __future__ import unicode_literals, print_function, division
import argparse
import re

schema = {
            "Allah": "Allah", 
            "Throne-of-Allah": "Throne", 
            "Artifact":"Artifact", 
            "Astronomical-body":"AstronomicalBody",
            "Event":"Event",
            "False-deity":"False-deity",
            "Holy-book":"HolyBook",
            "Language":"Language",
            "Angel":"Angel",
            "Person":"Person",
            "Messenger":"Messenger",
            "Prophet":"Prophet",
            "Sentient":"Sentient",
            "Afterlife-location":"AfterlifeLocation",
            "Geographical-location":"GeographicalLocation",
            "Color":"Color",
            "Religion":"Religion",
            "O":"O"
        }

def main(filename, output, schema):
    prev_word = ""
    prev_tag = "O"
    empty_space = False
    with open(output, "w+",  encoding="utf8") as f:
        f.write("")
    with open(filename, "r" , encoding="utf8") as reader:
        for line in reader:
            values = line.split("\t")
            sentence = values[0].strip()
            sentence = sentence.replace("\n", "")
            
            tag = "None"
            if len(values)>1:
                tag = values[1].replace("\n", "").strip()
            if sentence != " ":
                words = sentence.split(" ")
            if tag == "None":
                tag="O"
            for i, word in enumerate(words):
                regex = re.compile(r"""["'“’;@_!#$%,^&*()<>?/\|\-\.}{~:]""")
                search = regex.findall(word) 
                if len(search)>0:
                    sub_words = word
                    for item in search:
                        sub_words = sub_words.replace(item, f" {item} ").strip()
                    sub_words = sub_words.split(" ")
                else:
                    sub_words = [word]
                for sub_word in sub_words:
                    if tag != "O" and i==0:
                        tag_ = "B-"+schema[tag]
                    elif tag != "O" and i>0:
                        tag_ = "I-"+schema[tag]
                    else:
                        tag_ = schema[tag]                    
                    
                    if sub_word != "":
                        print(sub_word, tag_)
                        with open(output, "a",  encoding="utf8") as f:
                            f.write("{}\t{}\n".format(sub_word.strip(), tag_))
                        if sub_word =="." and i==0:
                            with open(output, "a",  encoding="utf8") as f:
                                f.write("\n")
                            empty_space = True
                        elif sub_word=="." and i>0:
                            if prev_word.isnumeric()==False:
                                with open(output, "a",  encoding="utf8") as f:
                                    f.write("\n")
                                empty_space = True
                            else:
                                next_i = i+1
                                if next_i < len(words):
                                    next_word = words[next_i]
                                else:
                                    next_word=""
                                    
                                if next_word !="" and next_word.isnumeric()==False:
                                    with open(output, "a",  encoding="utf8") as f:
                                        f.write("\n")
                                    empty_space = True
                    prev_word = sub_word
                    prev_tag = tag
            
            if len(values)==1:
                if empty_space==False:
                    with open(output, "a",  encoding="utf8") as f:
                        f.write("\n")
            empty_space=False
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("--filename", type=str, default="", help="")
    parser.add_argument("--output", type=str, default="output.txt", help="")
    args = parser.parse_args()
    main(args.filename, args.output, schema)