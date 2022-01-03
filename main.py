#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 22:51:07 2022

@author: asep
"""
from __future__ import unicode_literals, print_function, division
import argparse

schema = {"location": "LOC", "organization": "ORG", "person":"PER", "o":"O"}

def main(filename, schema):
    prev_word = ""
    prev_tag = "o"
    empty_space = False
    with open("results.txt", "w+",  encoding="utf8") as f:
        f.write("")
    with open(filename, "r" , encoding="utf8") as reader:
        for line in reader:
            values = line.split("\t")
            sentence = values[0].strip()
            sentence = sentence.replace("\n", "")
            
            tag = "None"
            if len(values)>1:
                tag = values[1].replace("\n", "").strip().lower()
            if sentence != " ":
                words = sentence.split(" ")
            if tag == "None":
                tag="o"
            
            for i, word in enumerate(words):
                if tag != "o" and i==0:
                    tag_ = "B-"+schema[tag]
                elif tag != "o" and i>0:
                    tag_ = "I-"+schema[tag]
                else:
                    tag_ = schema[tag]                    
                
                if word == "" and tag =="o":
                    print("OK")
                    #if prev_word =="." and prev_tag=="o":
                    #    with open("results.txt", "a",  encoding="utf8") as f:
                    #        f.write("empty space\n")
                else:
                    print(word, tag_)
                    with open("results.txt", "a",  encoding="utf8") as f:
                        f.write("{}\t{}\n".format(word.strip(), tag_))
                    if word =="." and i==0:
                        with open("results.txt", "a",  encoding="utf8") as f:
                            f.write("empty space\n")
                        empty_space = True
                    
                prev_word = word
                prev_tag = tag
            
            if len(values)==1:
                if empty_space==False:
                    with open("results.txt", "a",  encoding="utf8") as f:
                        f.write("empty space\n")
            empty_space=False
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("--filename", type=str, default="", help="")
    args = parser.parse_args()
    main(args.filename, schema)