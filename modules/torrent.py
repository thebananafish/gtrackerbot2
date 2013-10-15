import MySQLdb as mdb
import sys, urllib

downloadLink = "http://tracker.installgentoo.com/download.php?"


class dbQuery:
    def __init__(self, host, user, passwd, db, query):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.query = query
        self.conn = self.conn()

    def conn(self):
        try:
            conn = mdb.connect(self.host, self.user, self.passwd, self.db)
        except mdb.Error:
            sys.exit("couldn't connect!")
        return conn

    def search(self, title):
        search = "%s \"%%%s%%\" LIMIT 10" % (self.query, title)

        cur = self.conn.cursor()
        cur.execute(title)

        results = cur.fetchall(search)

        if not results:
            return
        else:
            return results

        self.conn.close()


def torrent(phenny, input):
    query = input.group(2)

    if not query:
        return phenny.reply(".torrent-search title")

    sql = "SELECT name, size, seeders, leechers, id, filename FROM \
            torrents WHERE title LIKE"

    myDb = dbQuery("host", "user", "passwd", "db", sql)
    results = myDb.search(query)

    phenny.msg(input.nick,"%s results found for %s " % (len(results)), query)

    if not len(results):
        return phenny.msg(input.nick, "No results found for %s" % query)

    for row in results:
        phenny.msg(input.nick, ' ')
        phenny.msg(input.nick, "title: %s %skb \u21e7[%s]\u21e9[%s]" \
                   % (row[0], fileSize(row[1]), row[2], row[3]))
        phenny.msg(input.nick, "Download: %sid=%s&name=%s" \
                   %(downloadLink, row[4], urllib.quote(row[5])))

torrent.commands = ['torrent-search']
torrent.priority = 'high'


def fileSize(size):
    if size <= 1024:
        size = str(size) + 'B'
    elif size <= 1048576:
        size = str(size/1024) + 'KiB'
    elif size <=1073741824:
        size = str(size/1024**2) + 'MiB'
    else:
        size = str(size/1024**3) + 'GiB'
    return size

