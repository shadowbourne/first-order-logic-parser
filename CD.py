#N.B. ALL INDEXING IN ERRORS STARTS AT 0 !!!!!!!!!!!!!!!!!!!!!!
import re
import os
import sys
from anytree import Node
from anytree.exporter import UniqueDotExporter
try:
    os.remove("tree.png")
except:
    pass
try:
    os.remove("log.txt")
except:
    pass
try:
    os.remove("grammar.txt")
except:
    pass
log = open("log.txt", 'w')
grammar_output = open("grammar.txt", 'w')
categories = ["variables", "constants", "equality", "connectives", "quantifiers"]
grammar = {}
visited = {}
for i in ["variables", "constants", "equality", "connectives", "quantifiers","formula", "predicates"]:
    grammar[i] = []
    visited[i] = 0
all_tokens = set()
arities = {}

part_of_formula = 0
#for loop to read in file into the "grammar" dictionary, with lots of error checks contained within
try:
    with open(sys.argv[1], "r") as file:
        for line in file:
            if line.strip() == '':
                log.write("Error, blank line contained in input file.")
                exit()
            category = line.split(":")
            if len(category) != 2:
                if len(category) == 1 and part_of_formula == 1:
                    category[0] = category[0].replace("(", " ( ")
                    category[0] = category[0].replace(")", " ) ")
                    category[0] = category[0].replace(",", " , ")
                    grammar["formula"] +=  re.split(r'\s+|\t+' , category[0].strip())
                    continue
                log.write("Error, too many colons in line.")
                exit()
            part_of_formula = 0
            if category[0] in categories:
                if visited[category[0]] != 0:
                    log.write("Error, {0} section given more than once in input file.".format(category[0]))
                    exit()
                visited[category[0]] = 1
                tokens = category[1].split(' ')
                if tokens[0] == "\n":
                    if category[0] in {"variables", "constants", "predicates"}:
                        continue
                    else:
                        log.write("Error, no definitions in \"{0}\".".format(category[0]))
                        exit()
                elif tokens[0] == '':
                    if len(tokens) == 1 or (len(tokens) == 2 and tokens[1] == ''):
                        if category[0] not in {"variables", "constants"}:
                            log.write("Error, no definitions supplied in \"{0}\".".format(category[0]))
                            exit()
                        continue
                    elif tokens[1] == "\n":
                        if category[0] not in {"variables", "constants"}:
                            log.write("Error, no definitions supplied in \"{0}\".".format(category[0]))
                            exit()
                        continue
                    tokens.pop(0)
                else:
                    log.write("Error, There is no space between \"{0}:\" and its definitions within.".format(category[0]))
                    exit()
                if tokens[-1][-1] == "\n":
                    tokens[-1] = tokens[-1][:-1]
                for h in range(len(tokens)):
                    k = tokens[h]
                    if k == '':
                        if h == 0:
                            log.write("Error, too much whitespace after \"{0}:\"".format(category[0]))
                            exit()
                        log.write("Error, too much whitespace after \"{0}\" in \"{1}\" definitions".format(tokens[h-1], category[0]))
                        exit()
                    if k not in all_tokens:
                        all_tokens.add(k)
                    else:
                        log.write("Error, symbol \"{0}\" defined multiple times".format(k))
                        exit()
                grammar[category[0]] = tokens
            elif category[0] == "formula":
                if visited[category[0]] != 0:
                    log.write("Error,{0} section given more than once in input file".format(category[0]))
                    exit()
                visited[category[0]] = 1
                if category[1].strip() == '':
                    log.write("Error, no formula supplied.")
                    exit()
                category[1] = category[1].replace("(", " ( ")
                category[1] = category[1].replace(")", " ) ")
                category[1] = category[1].replace(",", " , ")
                tokens = re.split(r'\s+|\t+' , category[1].strip())
                grammar[category[0]] = tokens
                part_of_formula = 1
            elif category[0] == "predicates":
                if visited[category[0]] != 0:
                    log.write("Error, {0} section given more than once in input file.".format(category[0]))
                    exit()
                visited[category[0]] = 1
                tokens = category[1].split(' ')
                if tokens[0] == "\n":
                        continue
                elif tokens[0] == '':
                    if len(tokens) == 1 or (len(tokens) == 2 and tokens[1] == ''):
                        continue
                    elif tokens[1] == "\n":
                        continue
                    tokens.pop(0)
                else:
                    log.write("Error, there is no space between \"{0}:\" and its definitions within.".format(category[0]))
                    exit()
                if tokens[-1][-1] == "\n":
                    tokens[-1] = tokens[-1][:-1]
                for k in range(len(tokens)):
                    if tokens[k] == '':
                        if k == 0:
                            log.write("Error, too much whitespace after \"{0}:\"".format(category[0]))
                            exit()
                        log.write("Error, too much whitespace after \"{0}\" in \"{1}\" definitions".format(tokens[k-1], category[0]))
                        exit()
                    predicate = tokens[k].split("[")
                    if len(predicate) != 2:
                        log.write("Error, too many \"[\"s in predicate definition of \"{0}\".".format(predicate[0]))
                        exit()
                    grammar["predicates"].append(predicate[0])
                    if predicate[0] not in all_tokens:
                        all_tokens.add(predicate[0])
                    else:
                        log.write("Error, symbol \"{0}\" defined multiple times.".format(predicate[0]))
                        exit()
                    predicate[1] = predicate[1].split("]")
                    if len(predicate[1]) != 2:
                        log.write("Error, too many \"]\"s in predicate definition of \"{0}\".".format(predicate[0]))
                        exit()
                    if predicate[1][0].isdigit():
                        if int(predicate[1][0]) != 0:
                            arities[predicate[0]] = predicate[1][0]
                        else:
                            log.write("Error, arity (\"{1}\") of \"{0}\" is not a positive integer.".format(predicate[0], predicate[1][0]))
                            exit()
                    else:
                        log.write("Error, arity (\"{1}\") of \"{0}\" is not a positive integer.".format(predicate[0], predicate[1][0]))
                        exit()
            else:
                log.write("Error, {0} is not a valid category. Categories should be from the following list:".format() + r'["variables", "constants", "equality", "connectives", "quantifiers","formula", "predicates"]')
                exit()
except Exception:
    log.write("Error, cannot read input file.")
    exit()

#some post reading in error checks


for i in ["variables", "constants", "equality", "connectives", "quantifiers","formula", "predicates"]:
    if visited[i] != 1:
        log.write("Error, {0} not defined in input file. Even if you are not defining any {0}'s, please enter a line simply containing \"{0}:\"".format(i))
        exit()

for current_category in ["variables", "constants", "predicates"]:
    for i in range(len(grammar[current_category])):
        for j in range(len(grammar[current_category][i])):
            if not grammar[current_category][i][j].isalnum() and grammar[current_category][i][j] != "_":
                log.write("Error, definition of {1} symbol \"{0}\" includes invalid characters; Variable, constant and predicate definition characters must be either alphanumeric or \"_\" only.".format(grammar[current_category][i], current_category[:-1]))
                exit()
if len(grammar["connectives"]) != 5:
    log.write("Error, more/less than 5 connectives symbols defined.")
    exit()
if len(grammar["quantifiers"]) != 2:
    log.write("Error, more/less than 2 quantifier symbols defined.")
    exit()
for current_category in ["connectives", "quantifiers"]:
    for i in range(len(grammar[current_category])):
        for j in range(len(grammar[current_category][i])):
            if not grammar[current_category][i][j].isalnum() and grammar[current_category][i][j] not in {"_", "\\"}:
                log.write("Error, definition of {1} symbol \"{0}\" includes invalid characters; Connectives and quantifiers definition characters must be either alphanumeric or \"_\" or \"\\\" only.".format(grammar[current_category][i], current_category[:-1]))
                exit()
if len(grammar["equality"]) != 1:
    log.write("Error, more/less than one equality symbol defined.")
    exit()
for j in range(len(grammar["equality"][0])):
    if not grammar["equality"][0][j].isalnum() and grammar["equality"][0][j] not in {"_", "\\", "="}:
        log.write("Error, definition of equality symbol \"{0}\" includes invalid characters; Equality definition characters must be either alphanumeric or \"_\", \"\\\" or \"=\" only.".format(grammar["equality"][0]))
        exit()
if len(grammar["predicates"]) > 0 and len(grammar["variables"]) == 0:
    log.write("WARNING: Predicates defined, but no variables defined, therefore predicates will not be included in grammar production rules. See documentation for more details.\n\n")
#section to work out terminals and non terminals

terminals = []
for i in ["variables", "constants", "predicates", "equality", "connectives", "quantifiers"]:
    for j in range(len(grammar[i])):
        terminals.append(grammar[i][j])
terminals += ["(", ",", ")"]

for i in grammar["formula"]:
    if i not in terminals:
        log.write("Error, undefined symbol \"{0}\" in formula.".format(i))
        exit()

non_terminals = ["<S>", "<K>"]
for objct in [["<C>", "constants"], ["<V>", "variables"], ["<Q>", "quantifiers"], ["<L>", "connectives"], ["<P>", "predicates"]]:
    if len(grammar[objct[1]]) != 0:
        
        non_terminals.append(objct[0])
if len(grammar["variables"]) == 0:
    non_terminals.pop(-1)

#Section to write grammar to file

P = {}
grammar_output.write("Grammar = {*Vt*, *Vn*, *P*, <S>}\n")
grammar_output.write("*Vt* = {"+"{0}".format(terminals)[1:-1]+"}\n")
grammar_output.write("*Vn* = {"+"{0}".format(non_terminals)[1:-1]+"}\n")
grammar_output.write("*P* = { ")
grammar_output.write("<L> -> ")
for i in range(len(grammar["connectives"])-1):
    if i == len(grammar["connectives"])-2:
        grammar_output.write(grammar["connectives"][i]+"\n")
    else:
        grammar_output.write("{0} | ".format(grammar["connectives"][i]))
for objct in [["<Q> -> ", "quantifiers"], ["<C> -> ", "constants"], ["<V> -> ", "variables"]]:# ["<E> -> ", "equality"]]:
    if len(grammar[objct[1]]) > 0:
        grammar_output.write("        " + objct[0])
        for i in range(len(grammar[objct[1]])):
            if i == len(grammar[objct[1]])-1:
                grammar_output.write(grammar[objct[1]][i]+"\n")
            else:
                grammar_output.write("{0} | ".format(grammar[objct[1]][i]))
if len(grammar["predicates"]) > 0 and len(grammar["variables"]) > 0:
    grammar_output.write("        <P> -> ")
    for i in range(len(grammar["predicates"])):
        if i == len(grammar["predicates"])-1:
            grammar_output.write("{0}(".format(grammar["predicates"][i]))
            for j in range(int(arities[grammar["predicates"][i]])-1):
                grammar_output.write("V,")
            grammar_output.write("V)\n")
        else:
            grammar_output.write("{0}(".format(grammar["predicates"][i]))
            for j in range(int(arities[grammar["predicates"][i]]) -1):
                grammar_output.write("V,")
            grammar_output.write("V) | ")

const = "<C>"
var = "<V>"
if len(grammar["constants"]) == 0 and len(grammar["variables"]) == 0:
    grammar_output.write("        <S> -> ( <S> <L> <S> ) | {1} <S>\n".format(grammar["equality"][0], grammar["connectives"][-1]))
elif len(grammar["constants"]) == 0:
    if len(grammar["predicates"]) > 0:
        grammar_output.write("        <S> -> (<K> {0} <K>) | <P> | ( <S> <L> <S> ) | <Q> <V> <S> | {1} <S>\n".format(grammar["equality"][0], grammar["connectives"][-1]))
        grammar_output.write("        <K> -> <V>\n")
    else:
        grammar_output.write("        <S> -> (<K> {0} <K>) | ( <S> <L> <S> ) | <Q> <V> <S> | {1} <S>\n".format(grammar["equality"][0], grammar["connectives"][-1]))
        grammar_output.write("        <K> -> <V>\n")
elif len(grammar["variables"]) == 0:
    grammar_output.write("        <S> -> (<K> {0} <K>) | ( <S> <L> <S> ) | {1} <S>\n".format(grammar["equality"][0], grammar["connectives"][-1], const))
    grammar_output.write("        <K> -> <C>\n")
else:
    if len(grammar["predicates"]) > 0:
        grammar_output.write("        <S> -> (<K> {0} <K>) | <P> | ( <S> <L> <S> ) | <Q> <V> <S> | {1} <S>\n".format(grammar["equality"][0], grammar["connectives"][-1]))
    else:
        grammar_output.write("        <S> -> (<K> {0} <K>) | ( <S> <L> <S> ) | <Q> <V> <S> | {1} <S>\n".format(grammar["equality"][0], grammar["connectives"][-1]))
    grammar_output.write("        <K> -> <C> | <V>\n")
grammar_output.write("      }")


# section to produce the production rules dictionary, depending upon the current nonterminal and the current lookahead symbol from the formula ( effectively the parse table entries )

P["<L>"] = {}
P["<Q>"] = {}
P["<V>"] = {}
P["<C>"] = {}
P["<P>"] = {}
P["<K>"] = {}
P["<S>"] = {}

for i in range(len(grammar["connectives"])-1):
    P["<L>"][grammar["connectives"][i]] = [grammar["connectives"][i]]

for i in grammar["quantifiers"]:
    P["<Q>"][i] = [i]
    P["<S>"][i] = ["<Q>", "<V>", "<S>"]

for i in grammar["variables"]:
    P["<V>"][i] = [i]
    P["<K>"][i] = ["<V>"]


for i in grammar["constants"]:
    P["<C>"][i] = [i]
    P["<K>"][i] = ["<C>"]

for i in grammar["predicates"]:
    P["<P>"][i] = [i, "("]
    for _ in range(int(arities[i])-1):
        P["<P>"][i] += ["<V>", ","]
    P["<P>"][i] += ["<V>", ")"]
    P["<S>"][i] = ["<P>"]

P["<S>"][grammar["connectives"][-1]] = [grammar["connectives"][-1], "<S>"]

Vt = set(terminals)
Vn = set(non_terminals)

# section to validate formula and construct parse tree

root = Node("<S>")
ri = 0
parse_tree = {}
def add_to_tree(x, j, ri):
    for i in x:
        ri += 1
        i = i.replace("\\","\\\\")
        parse_tree[ri] = Node(i, parent= parse_formula[j][1])
    return ri
parse_formula = [["<S>",root]]
finished = False
while not finished:
    finished = True
    for j in range(len(parse_formula)):
        if parse_formula[j][0] in Vn:
            finished = False
            i = j
            if parse_formula[j][0] == "<P>" and grammar["formula"][i] in grammar["predicates"]:
                if len(grammar["formula"]) > i+1+2*int(arities[grammar["formula"][i]]):
                    if grammar["formula"][i+1] != "(":
                        for k in range(len(parse_formula)):
                            parse_formula[k] = parse_formula[k][0]
                        log.write("Error, symbol number {1} of formula cannot be parsed.\nPreview of formula symbols {2} to {3}: \"{0}\" .\nDid you mean to put something of the format {5}(<V>{4}) ? (Symbol \"{6}\" is not a \"(\" ).".format(" ".join(grammar["formula"][i:i+2+2*int(arities[grammar["formula"][i]])]), i+1+2*int(arities[grammar["formula"][i]]), i, i+1+2*int(arities[grammar["formula"][i]]), ",<V>"*(-1+int(arities[grammar["formula"][i]])), grammar["formula"][i], grammar["formula"][i+1]))
                        exit()
                    for n in range(int(arities[grammar["formula"][i]])):
                        if grammar["formula"][i+2+2*n] not in grammar["variables"]:
                            for k in range(len(parse_formula)):
                                parse_formula[k] = parse_formula[k][0]
                            log.write("Error, symbol number {1} of formula cannot be parsed.\nPreview of formula symbols {2} to {3}: \"{0}\" .\nDid you mean to put something of the format {5}(<V>{4}) ? (Symbol \"{6}\" is not a variable ).".format(" ".join(grammar["formula"][i:i+2+2*int(arities[grammar["formula"][i]])]), i+2+2*n, i, i+1+2*int(arities[grammar["formula"][i]]), ",<V>"*(-1+int(arities[grammar["formula"][i]])), grammar["formula"][i], grammar["formula"][i+2+2*n]))
                            exit()
                    for n in range(int(arities[grammar["formula"][i]])-1):
                        if grammar["formula"][i+3+2*n] != ",":
                            for k in range(len(parse_formula)):
                                parse_formula[k] = parse_formula[k][0]
                            log.write("Error, symbol number {1} of formula cannot be parsed.\nPreview of formula symbols {2} to {3}: \"{0}\" .\nDid you mean to put something of the format {5}(<V>{4}) ? (Symbol \"{6}\" is not a \",\" ).".format(" ".join(grammar["formula"][i:i+2+2*int(arities[grammar["formula"][i]])]), i+3+2*n, i, i+1+2*int(arities[grammar["formula"][i]]), ",<V>"*(-1+int(arities[grammar["formula"][i]])), grammar["formula"][i], grammar["formula"][i+3+2*n]))
                            exit()
                    if grammar["formula"][i+1+2*int(arities[grammar["formula"][i]])] != ")":
                        for k in range(len(parse_formula)):
                            parse_formula[k] = parse_formula[k][0]
                        log.write("Error, symbol number {1} of formula cannot be parsed.\nPreview of formula symbols {2} to {3}: \"{0}\" .\nDid you mean to put something of the format {5}(<V>{4}) ? (Symbol \"{6}\" is not a \")\" ).".format(" ".join(grammar["formula"][i:i+2+2*int(arities[grammar["formula"][i]])]), i+1+2*int(arities[grammar["formula"][i]]), i, i+1+2*int(arities[grammar["formula"][i]]), ",<V>"*(-1+int(arities[grammar["formula"][i]])), grammar["formula"][i], grammar["formula"][i+1+2*int(arities[grammar["formula"][i]])]))
                        exit()
                else:
                    for k in range(len(parse_formula)):
                        parse_formula[k] = parse_formula[k][0]
                    log.write("Error, missing parts of \"{1}(<V>{0})\" at the very end of the inputted formula ( requires {2} variable parameters, seperated by commas, ending in a \")\" ).\nPlease add on these missing components.".format(",<V>"*(-1+int(arities[grammar["formula"][i]])), grammar["formula"][i], int(arities[grammar["formula"][i]])))
                    exit()
            if parse_formula[j][0] == "<S>" and grammar["formula"][i] == "(":
                if grammar["formula"][i+1] in grammar["variables"] or grammar["formula"][i+1] in grammar["constants"]:
                    if i + 4 > len(grammar["formula"]) - 1:
                        for k in range(len(parse_formula)):
                            parse_formula[k] = parse_formula[k][0]
                        parse_formula[j:j+1] = ["(", "<K>", grammar["equality"][0], "<K>", ")"]
                        log.write("Error, formula cannot be parsed correctly as parser tries to produce a semi-complete formula:\n\"{0}\"\nwhich already has greater length than the inputted formula:\n\"{1}\"\nPlease inspect the two above formulas and refer to the grammar production rules to see the types of valid expressions, and their formats.".format(" ".join(parse_formula), " ".join(grammar["formula"])))
                        exit()
                    else:
                        if grammar["formula"][i+2] == grammar["equality"][0]:
                            if grammar["formula"][i+3] in grammar["variables"] or grammar["formula"][i+3] in grammar["constants"]:
                                if grammar["formula"][i+4] == ")":
                                    ri = add_to_tree(["(", "<K>", grammar["equality"][0], "<K>", ")"], j , ri)
                                    parse_formula[j:j+1] = [["(", parse_tree[ri-4]], ["<K>", parse_tree[ri-3]], [grammar["equality"][0], parse_tree[ri-2]], ["<K>", parse_tree[ri-1]], [")", parse_tree[ri]]]
                                else:
                                    if len(grammar["formula"]) > i+4:
                                        for k in range(len(parse_formula)):
                                            parse_formula[k] = parse_formula[k][0]
                                        log.write("Error, symbol number {1} of formula cannot be parsed.\nPreview of formula symbols {2} to {3}: \"{0}\" .\nDid you mean to put something of the format (<K> = <K>) ? (Missing final bracket of the atom)".format(" ".join(grammar["formula"][i:i+5]), i+4, i, i+4))
                                        exit()
                                    else:
                                        for k in range(len(parse_formula)):
                                            parse_formula[k] = parse_formula[k][0] 
                                        log.write("Error, symbol number {1} of formula cannot be parsed.\nPreview of formula symbols {2} to {3}: \"{0}\" .\nDid you mean to put something of the format (<K> = <K>) ? (Missing final bracket of the atom)".format(" ".join(grammar["formula"][i:]), i+4, i, len(grammar["formula"])-1))
                                        exit()
                            else:
                                if len(grammar["formula"]) > i+4:
                                    for k in range(len(parse_formula)):
                                        parse_formula[k] = parse_formula[k][0]
                                    log.write("Error, symbol number {1} of formula cannot be parsed.\nPreview of formula symbols {2} to {3}: \"{0}\" .\nDid you mean to put something of the format (<K> = <K>) ? (Symbol \"{4}\" after equality symbol is neither a variable nor a constant)".format(" ".join(grammar["formula"][i:i+5]), i+3, i, i+4, grammar["formula"][i+3]))
                                    exit()
                                else:
                                    for k in range(len(parse_formula)):
                                        parse_formula[k] = parse_formula[k][0]
                                    log.write("Error, symbol number {1} of formula cannot be parsed.\nPreview of formula symbols {2} to {3}: \"{0}\" .\nDid you mean to put something of the format (<K> = <K>) ? (Symbol \"{4}\" after equality symbol is neither a variable nor a constant)".format(" ".join(grammar["formula"][i:]), i+3, i, len(grammar["formula"])-1, grammar["formula"][i+3]))
                                    exit()
                        else:
                            if len(grammar["formula"]) > i+4:
                                for k in range(len(parse_formula)):
                                    parse_formula[k] = parse_formula[k][0]
                                log.write("Error, symbol number {1} of formula cannot be parsed.\nPreview of formula symbols {2} to {3}: \"{0}\" .\nDid you mean to put something of the format (<K> = <K>) ? (Symbol \"{4}\" is not an equality symbol)".format(" ".join(grammar["formula"][i:i+5]), i+2, i, i+4, grammar["formula"][i+2]))
                                exit()
                            else:
                                for k in range(len(parse_formula)):
                                    parse_formula[k] = parse_formula[k][0]
                                log.write("Error, symbol number {1} of formula cannot be parsed.\nPreview of formula symbols {2} to {3}: \"{0}\" .\nDid you mean to put something of the format (<K> = <K>) ? (Symbol \"{4}\" is not an equality symbol)".format(" ".join(grammar["formula"][i:]), i+2, i, len(grammar["formula"])-1, grammar["formula"][i+2]))
                                exit()
                    
                else:
                    ri = add_to_tree(["(", "<S>", "<L>", "<S>", ")"], j , ri)
                    parse_formula[j:j+1] = [["(", parse_tree[ri-4]], ["<S>", parse_tree[ri-3]], ["<L>", parse_tree[ri-2]], ["<S>", parse_tree[ri-1]], [")", parse_tree[ri]]]
            elif parse_formula[j][0] == "<S>" and grammar["formula"][i] in grammar["quantifiers"]:
                if grammar["formula"][i+1] in grammar["variables"]:
                    ri = add_to_tree(P[parse_formula[j][0]][grammar["formula"][i]], j , ri)
                    parse_formula[j:j+1] = [[P[parse_formula[j][0]][grammar["formula"][i]][k], parse_tree[ri - len(P[parse_formula[j][0]][grammar["formula"][i]]) + k + 1]] for k in range(len(P[parse_formula[j][0]][grammar["formula"][i]]))]
                else:
                    if len(grammar["formula"]) > i+2:
                        for k in range(len(parse_formula)):
                            parse_formula[k] = parse_formula[k][0]
                        log.write("Error, symbol number {1} of formula cannot be parsed.\nPreview of formula symbols {2} to {3}: \"{0}\" .\n(Symbol \"{4}\" after quantifier \"{5}\" is not a variable )\nDid you mean to put something of the format <Q> <V> <S> ?".format(" ".join(grammar["formula"][i:i+3]), i+1, i, i+2, grammar["formula"][i+1], grammar["formula"][i]))
                        exit()
                    else:
                        for k in range(len(parse_formula)):
                            parse_formula[k] = parse_formula[k][0]
                        log.write("Error, symbol number {1} of formula cannot be parsed.\nPreview of formula symbols {2} to {3}: \"{0}\" .\n(Symbol \"{4}\" after quantifier \"{5}\" is not a variable )\nDid you mean to put something of the format <Q> <V> <S> ?".format(" ".join(grammar["formula"][i:]), i+1, i, len(grammar["formula"])-1, grammar["formula"][i+1], grammar["formula"][i]))
                        exit()
        
            else:
                try:
                    ri = add_to_tree(P[parse_formula[j][0]][grammar["formula"][i]], j , ri)
                    parse_formula[j:j+1] = [[P[parse_formula[j][0]][grammar["formula"][i]][k], parse_tree[ri - len(P[parse_formula[j][0]][grammar["formula"][i]]) + k + 1]] for k in range(len(P[parse_formula[j][0]][grammar["formula"][i]]))]
                except:
                    for k in range(len(parse_formula)):
                        parse_formula[k] = parse_formula[k][0]
                    log.write("Error, formula not consistent with grammar, as this formula cannot be parsed using the grammar's production rules.\nError reached at the parsing of the {1}'th symbol \"{3}\" ( as \"{3}\" can never be produced from \"{2}\" ). Did you perhaps forget a bracket?\nPlease refer to the grammar production rules to see the types of valid expressions, and their format, parsable from \"{2}\".\nSemi-parsed formula: \"{0}\"".format(" ".join(parse_formula), j, parse_formula[j], grammar["formula"][i]))
                    exit()

                break
        else:
            if j > len(grammar["formula"]) - 1:
                for k in range(len(parse_formula)):
                    parse_formula[k] = parse_formula[k][0]
                log.write("Error, formula cannot be parsed correctly as parser tries to produce a semi-complete formula:\n\"{0}\"\nwhich already has greater length than the inputted formula:\n\"{1}\"\nPlease inspect the two above formulas and refer to the grammar production rules to see the types of valid expressions, and their formats.".format(" ".join(parse_formula), " ".join(grammar["formula"])))
                exit()
            if parse_formula[j][0] != grammar["formula"][j]:
                for k in range(len(parse_formula)):
                    parse_formula[k] = parse_formula[k][0]
                log.write("Error, formula cannot be parsed correctly as parser produces semi-complete formula:\n\"{0}\"\nwhich mismatches the inputted formula:\n\"{1}\"\nupon reaching symbol \"{2}\" in the {3}'th position ( \"{2}\" != \"{4}\" ).\nPlease inspect the two above formulas and refer to the grammar production rules to see the types of valid expressions, and their formats.".format(" ".join(parse_formula), " ".join(grammar["formula"]), grammar["formula"][j], j, parse_formula[j]))
                exit()
                
#check formula isnt longer than completed parsed formula

if len(parse_formula) != len(grammar["formula"]):
    for k in range(len(parse_formula)):
        parse_formula[k] = parse_formula[k][0]
    log.write("Error, formula cannot be parsed correctly as parser produces a complete formula:\n\"{0}\"\nwhich has unequal length to therefore mismatches the inputted formula:\n\"{1}\"\n(and may proceed no further using the production rules of the grammar, as no non-terminals remain).\nPlease inspect the two above formulas and refer to the grammar production rules to see the types of valid expressions, and their formats.".format(" ".join(parse_formula), " ".join(grammar["formula"])))
    exit()


#Once formula has been validated and tree constructed, render tree to file and write success to log
UniqueDotExporter(root).to_picture("tree.png")
log.write("Success, both the input file format and formula are valid. Check \"tree.png\" for the produced parse tree.")




#N.B. ALL INDEXING IN ERRORS STARTS AT 0 !!!!!!!!!!!!!!!!!!!!!!
