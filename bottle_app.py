import os, datetime, bottle, bottle_sqlite

dbfilepath = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'workingdiary.db')
bottle.install(bottle_sqlite.SQLitePlugin(dbfile = dbfilepath))

GlobalDebugMode = True

@bottle.route("/")
def hello(db):
    checkexist = db.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name = 'mobilephone_dict';").fetchone()
    if 1 != checkexist[0]:
        db.execute('''CREATE TABLE `workingdiary` (
            `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            `mobilephone` INTEGER NOT NULL,
            `timestamp` TEXT NOT NULL,
            `projectname` TEXT NOT NULL,
            `taskname` TEXT NOT NULL,
            `timeinhour` REAL NOT NULL,
            `location` TEXT NOT NULL,
            `commit` TEXT);
            ''')
        db.execute('''CREATE TABLE `mobilephone_dict` (
            `mobilephone`	INTEGER NOT NULL,
            PRIMARY KEY(mobilephone));
            ''')

    today = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")

    result = db.execute("SELECT DISTINCT projectname FROM workingdiary;").fetchall()
    allprojects = [item[0] for item in result]

    result = db.execute("SELECT DISTINCT location FROM workingdiary;").fetchall()
    alllocations = [item[0] for item in result]

    return bottle.template("submit_record", timestamp = today, projects = allprojects, locations = alllocations)

@bottle.post('/')
def hello(db):
    mobilephone = bottle.request.forms.get("mobilephone").strip()
    if (len(mobilephone) != 11) or (not mobilephone.isdecimal()) or (mobilephone[0] != '1'):
        return "输入的手机号：{}好像不正确，请重新输入。".format(mobilephone)
    checkphone = db.execute("SELECT COUNT(*) FROM mobilephone_dict WHERE mobilephone = ?", (mobilephone,)).fetchone()
    if 1 != checkphone[0]:
        return "输入的手机号：{}好像还未注册过。".format(mobilephone)

    timestamp = bottle.request.forms.get("timestamp").strip()
    try:
        check = datetime.datetime.strptime(timestamp, "%Y-%m-%d").date()
    except ValueError:
        return "输入的日期：{}好像不正确。".format(timestamp)

    projectname = bottle.request.forms.getunicode("projectname").strip()

    taskname = bottle.request.forms.getunicode("taskname").strip()

    timeinhour = bottle.request.forms.get("timeinhour").strip()
    try:
        timeinhour = float(timeinhour)
    except ValueError:
        return "输入的耗费时间：{}好像不正确。".format(timeinhour)
    if timeinhour % 0.5:
        return "输入的耗费时间：{}好像不正确。".format(timeinhour)

    location = bottle.request.forms.getunicode("location").strip()

    commit = bottle.request.forms.getunicode("commit").strip()
    commit = commit.split('(')[0].strip()

    db.execute("INSERT INTO workingdiary (mobilephone, timestamp, projectname, taskname, timeinhour, location) VALUES (?,?,?,?,?,?)", (mobilephone, timestamp, projectname, taskname, timeinhour, location))
    result = db.execute("SELECT MAX(id) FROM workingdiary where mobilephone = ?", (mobilephone,)).fetchone()
    newid = result[0]

    return "新纪录：{}创建成功。".format(newid)

@bottle.route("/add_user")
def add_user():
    return '''
        <form action="/add_user" method="post">
            手机号: <input name="mobilephone" type="text" />
            <input value="提交" type="submit" />
        </form>
    '''

@bottle.post("/add_user")
def do_add_user(db):
    newmobilephone = bottle.request.forms.get("mobilephone").strip()
    checkphone = db.execute("SELECT COUNT(*) FROM mobilephone_dict WHERE mobilephone = ?", (newmobilephone,)).fetchone()
    if 1 == checkphone[0]:
        return "手机号：{}已经注册过。".format(newmobilephone)

    if (len(newmobilephone) != 11) or (not newmobilephone.isdecimal()) or (newmobilephone[0] != '1'):
        return "输入的手机号：{}好像不正确，请重新输入。".format(newmobilephone)

    db.execute("INSERT INTO mobilephone_dict (mobilephone) VALUES (?)", (newmobilephone,))
    return "手机号：{}注册成功。".format(newmobilephone)

if GlobalDebugMode:
    bottle.debug(True)
    bottle.run()
else:
    application = bottle.default_app()
