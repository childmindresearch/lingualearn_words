#!/usr/bin/env python                                                                                                       
'''                                                                                                                        
Main program to run Linguamorph software (see README.md).

Copyright 2023, Arno Klein, MIT License

'''
import argparse
import re
from process_phonemes import phoneme_list, consonant_list, words_to_sounds, separate_consonants, generate_homophones
from check_grammar import check_grammar_twice, grammar_tool, grammar_tool2
from io_files import display_save_output

#-----------------------------------------------------------------------------                                              
# Command-line arguments                                                                                               
#-----------------------------------------------------------------------------                                              
parser = argparse.ArgumentParser(description="""                                                                            
                    Run Linguamorph software.""",
                     formatter_class = lambda prog:
                     argparse.HelpFormatter(prog, max_help_position=40))
parser.add_argument('text', type=str, help='Enter a string of text')
parser.add_argument("-c", "--convert", type=int, help="Convert text to (1) homophones (same sounds), (2) consonances (same consonants), or (3) consonant permutations", default=0)
parser.add_argument("-g", "--grammar", type=int, help="Check grammar (0=no (default), 1=once, 2=twice)", default=0)
parser.add_argument("-s", "--save", action='store_true', help="Save output files")
parser.add_argument("-q", "--quiet", action='store_false', help="Do not generate output on the command line")
args = parser.parse_args()

input_text = args.text
do_convert = args.convert 
do_grammar = args.grammar   
do_save = args.save
verbose = args.quiet

do_generate_homophones = False  # Generate homophones (same sounds)
do_generate_consonances = False  # Generate consonances (same consonants)
do_permute_consonants = False  # Generate swap-consonances (permute consonants)
if do_convert == 1:
    do_generate_homophones = True
elif do_convert == 2:
    do_generate_consonances = True
elif do_convert == 3:
    do_permute_consonants = True

do_check_grammar = False
do_check_grammar_again = False
cap_and_punc = False
if do_grammar > 0:
    do_check_grammar = True  # Check grammar
    cap_and_punc = True
    if do_check_grammar == 2:
        do_check_grammar_again = True  # Check grammar with a second tool

#-----------------------------------------------------------------------------                                              
# Settings
#-----------------------------------------------------------------------------                                              
ignore_inputs = []  # Don't use any of these words
do_ignore_inputs = False  # Don't use any of the original words
do_split_up_consonants = True  # Split up consonant compounds ("I scream" => "ice cream")?
if do_split_up_consonants:
    max_phonemes_per_word = 25
else:
    max_phonemes_per_word = 11      

verbose2 = False

#-----------------------------------------------------------------------------                                              
# Process input text
#-----------------------------------------------------------------------------                                              
if verbose:
    print("Entered text: {0}".format(input_text))

if ' ' in input_text.strip():
    words = input_text.split()
    nwords = len(words)
else:
    words = input_text
    nwords = 1

max_phonemes = nwords * max_phonemes_per_word

# Convert words to phonemes
phonemes, consonants, stresses, nsyllables = words_to_sounds(words, phoneme_list, consonant_list)

# Split up consonant compounds ("I scream" => "ice cream")
if do_split_up_consonants:
    phonemes = separate_consonants(phonemes)

# Set parameters
if do_ignore_inputs:
    ignore_inputs = words

filename_base = None
if do_save:
    if isinstance(words, list):
        filename_base = 'output/' + '_'.join(words)
    elif isinstance(words, str):
        filename_base = 'output/' + words

#-----------------------------------------------------------------------------                                              
# Convert input text to homophones, consonances, or swap-consonances
#-----------------------------------------------------------------------------                                              
# Homophones
if do_generate_homophones:
    homophones = generate_homophones(phonemes, max_phonemes, max_phonemes_per_word, False, False, ignore_inputs, verbose2)
    if do_grammar:
        homophones = check_grammar_twice(homophones, grammar_tool, grammar_tool2, cap_and_punc, do_check_grammar_again, verbose2)
    display_save_output(homophones, 'homophones', input_text, do_save, filename_base, verbose)

# Consonances
if do_generate_consonances:
    consonances = generate_homophones(phonemes, max_phonemes, max_phonemes_per_word, True, False, ignore_inputs, verbose2)
    if do_grammar:
        consonances = check_grammar_twice(consonances, grammar_tool, grammar_tool2, cap_and_punc, do_check_grammar_again, verbose2)
    display_save_output(consonances, 'consonances', input_text, do_save, filename_base, verbose)

# Swap-consonances
if do_permute_consonants:
    swap_consonants = generate_homophones(phonemes, max_phonemes, max_phonemes_per_word, True, True, ignore_inputs, verbose2)
    if do_grammar:
        swap_consonants = check_grammar_twice(consonances, grammar_tool, grammar_tool2, cap_and_punc, do_check_grammar_again, verbose2)
    display_save_output(swap_consonants, 'swap_consonants', input_text, do_save, filename_base, verbose)

if verbose:
    print('\nDone')