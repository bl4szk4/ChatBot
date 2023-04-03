import morfeusz2

morf = morfeusz2.Morfeusz(analyse=True)


def morph_word(word):
    global morf
    analiza = morf.analyse(word)
    out = []
    for i, j, interp in analiza:
        out.append([interp][0])

    xd = [list(item)[0:2] for item in out]
    xd = [item for sublist in xd for item in sublist]
    xd = [item.lower() for item in xd]

    # Usuniecie wszystkiego po : (czasem wystepuje)
    try:
        xd[1] = xd[1].split(":", 1)[0]
    except IndexError as e:
        raise IndexError("Given string must be single word")

    try:
        xd[0] = xd[0].split(":", 1)[0]
    except IndexError as e:
        raise IndexError("Given string must be single word")

    try:
        return xd[1]
    except IndexError as e:
        return xd[0]


def morph_phrase(phrase):
    if phrase:
        text = []
        for x in phrase.split():
            text.append(morph_word(x))
        lambda_join = lambda x: ' '.join(x)
        return lambda_join(text)
    else:
        return 0