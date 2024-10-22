import sqlite3 as sq


def sql_start():
    global base_meme, cur1, base_anecdote, cur2, base_riddle, cur3, base_words, cur4, russia_vs_world, cur5
    base_meme = sq.connect('meme.db')
    base_anecdote = sq.connect('anecdote.db')
    base_riddle = sq.connect('riddle.db')
    # base_words = sq.connect('words.db')
    # russia_vs_world = sq.connect('russia_vs_world.db')
    cur1 = base_meme.cursor()
    cur2 = base_anecdote.cursor()
    cur3 = base_riddle.cursor()
    # cur4=base_words.cursor()
    # cur5=russia_vs_world.cursor()
    base_meme.execute(
        'CREATE TABLE IF NOT EXISTS menu(img TEXT)')
    base_anecdote.execute(
        'CREATE TABLE IF NOT EXISTS menu(joke TEXT)')
    base_riddle.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT,answer TEXT)')
    # base_words.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT,info TEXT)')
    # russia_vs_world.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT,info TEXT)')
    base_meme.commit()
    base_anecdote.commit()
    base_riddle.commit()
    # base_knowledge.commit()
    # russia_vs_world.commit()


async def sql_add_meme(data):
    cur1.execute('INSERT INTO menu VALUES (?)', tuple(data.values()))
    base_meme.commit()


def sql_read_meme():
    return cur1.execute('SELECT * FROM menu').fetchall()


async def sql_add_anecdote(data):
    cur2.execute('INSERT INTO menu VALUES (?)', tuple(data.values()))
    base_anecdote.commit()


def sql_read_anecdote():
    return cur2.execute('SELECT * FROM menu').fetchall()

async def sql_add_riddle(data):
    cur3.execute('INSERT INTO menu VALUES (?,?)', tuple(data.values()))
    base_riddle.commit()

def sql_read_riddle():
    return cur3.execute('SELECT * FROM menu').fetchall()

#
# async def sql_add_component_words(data):
#     cur4.execute('INSERT INTO menu VALUES (?,?)', tuple(data.values()))
#     base_words.commit()
#
# async def sql_add_russia_vs_world(data):
#     cur5.execute('INSERT INTO menu VALUES (?,?)', tuple(data.values()))
#     russia_vs_world.commit()




# def sql_read_words():
#     return cur4.execute('SELECT * FROM menu').fetchall()
#
#
# def sql_read_russia_vs_world():
#     return cur5.execute('SELECT * FROM menu').fetchall()
