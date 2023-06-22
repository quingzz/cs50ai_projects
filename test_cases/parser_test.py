from parser import preprocess, np_chunk, parser
def test_0():
    # Convert input into list of words
    s = preprocess("Holmes sat.")

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    assert trees
    
    
def test_1():
    # Convert input into list of words
    s = preprocess("Holmes lit a pipe.")

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    assert trees
    
def test_2():
    # Convert input into list of words
    s = preprocess("We arrived the day before Thursday.")

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    assert trees
    
def test_3():
    # Convert input into list of words
    s = preprocess("Holmes sat in the red armchair and he chuckled.")

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    assert trees
    
def test_4():
    # Convert input into list of words
    s = preprocess("My companion smiled an enigmatical smile.")

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    assert trees
    
def test_5():
    # Convert input into list of words
    s = preprocess("Holmes chuckled to himself.")

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    assert trees
    
def test_6():
    # Convert input into list of words
    s = preprocess("She never said a word until we were at the door here.")

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    assert trees
    
def test_7():
    # Convert input into list of words
    s = preprocess("Holmes sat down and lit his pipe.")

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    assert trees
    
def test_8():
    # Convert input into list of words
    s = preprocess("I had a country walk on Thursday and came home in a dreadful mess.")

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    assert trees
    
def test_9():
    # Convert input into list of words
    s = preprocess("I had a little moist red paint in the palm of my hand.")

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    assert trees

