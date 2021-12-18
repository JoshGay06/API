import psycopg2
import psycopg2.extras
from pydantic import errors

# WINDOWS SPECIFIC LOGIN
conn = psycopg2.connect(host='localhost', dbname='Jitter Database', user='postgres', password='pwd')

cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

# ALTER SEQUENCE posts_id_seq RESTART WITH 1      --   RESET INDEX AUTO INCREMENT

def getValues():
    cursor.execute("""SELECT * FROM "posts" """)
    return cursor.fetchall()

def deleteAll():
    cursor.execute("""DELETE FROM "posts" """)
    conn.commit()

def find_post_by_id(id):

    cursor.execute("""SELECT * FROM "posts" WHERE id=(%s) """, (str(id)))
        
    returner = cursor.fetchone()

    if returner != None:
        return returner
    
    return '404'


def add_post(post):
    cursor.execute("""INSERT INTO "posts" (username, content, date, votes)
                      VALUES (%s, %s, %s, %s);""", (str(post.name), post.description, post.date_published, post.votes))

    conn.commit()


def delete_post_by_id(id):
    

    try:

        cursor.execute("""DELETE FROM "posts" WHERE id = %s """ % (str(id),))

        conn.commit()

        return 0

    
    except (Exception, psycopg2.DatabaseError) as error:
        return (error)



def update(id, post):

    final_parser = []

    prev_post = find_post_by_id(id)

    prev_post_values = list(prev_post.values())
    current_post_values = list(dict(post).values())

    for i in range(len(prev_post)):
        if current_post_values[i] != None:
            final_parser.append(current_post_values[i])
        else:
            final_parser.append(prev_post_values[i])

    try:

        cursor.execute("""UPDATE "posts" SET username = %s, content = %s, date=%s, votes='%s' WHERE id = %s """, (str(final_parser[1]), str(final_parser[2]), str(final_parser[3]), (final_parser[4]), str(final_parser[0])))

        conn.commit()

        return 0


    except ValueError:
        return '404'


