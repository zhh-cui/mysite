import os, hashlib, datetime, bottle, bottle_sqlite

dbfilepath = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'workingdiary.db')
bottle.install(bottle_sqlite.SQLitePlugin(dbfile = dbfilepath))

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
            `summary` TEXT);
            ''')
        db.execute('''CREATE TABLE `mobilephone_dict` (
            `mobilephone` INTEGER NOT NULL,
            `password` TEXT NOT NULL,
            PRIMARY KEY(mobilephone));
            ''')

    today = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")

    result = db.execute("SELECT DISTINCT projectname FROM workingdiary;").fetchall()
    allprojects = [item[0] for item in result]

    result = db.execute("SELECT DISTINCT location FROM workingdiary;").fetchall()
    alllocations = [item[0] for item in result]

    return bottle.template("submit_record", timestamp = today, projects = allprojects, locations = alllocations)

@bottle.post("/")
def do_hello(db):
    if bottle.request.forms.get("save", "").strip():
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

        summary = bottle.request.forms.getunicode("summary").strip()
        summary = summary.split('(')[0].strip()

        db.execute("INSERT INTO workingdiary (mobilephone, timestamp, projectname, taskname, timeinhour, location, summary) VALUES (?,?,?,?,?,?,?)", (mobilephone, timestamp, projectname, taskname, timeinhour, location, summary))
        result = db.execute("SELECT MAX(id) FROM workingdiary where mobilephone = ?", (mobilephone,)).fetchone()
        newid = result[0]

        return "新纪录：{}创建成功。".format(newid)

    elif bottle.request.forms.get("query", "").strip():
        mobilephone = bottle.request.forms.get("mobilephone").strip()
        if (len(mobilephone) != 11) or (not mobilephone.isdecimal()) or (mobilephone[0] != '1'):
            return "输入的手机号：{}好像不正确，请重新输入。".format(mobilephone)
        checkphone = db.execute("SELECT COUNT(*) FROM mobilephone_dict WHERE mobilephone = ?", (mobilephone,)).fetchone()
        if 1 != checkphone[0]:
            return "输入的手机号：{}好像还未注册过。".format(mobilephone)

        password = bottle.request.forms.get("password").strip()
        code = hashlib.md5()
        code.update(password.encode())
        value = code.hexdigest()

        check = db.execute("SELECT password FROM mobilephone_dict WHERE mobilephone = ?", (mobilephone,)).fetchone()
        if value != check[0]:
            return "输入的手机号：{}好像与密码不匹配。".format(mobilephone)

        result = db.execute("SELECT * FROM workingdiary WHERE mobilephone = ? order by date(timestamp) desc", (mobilephone,))
        return bottle.template("show_record", records = result)

    elif bottle.request.forms.get("adduser", "").strip():
        mobilephone = bottle.request.forms.get("mobilephone").strip()
        checkphone = db.execute("SELECT COUNT(*) FROM mobilephone_dict WHERE mobilephone = ?", (mobilephone,)).fetchone()
        if 1 == checkphone[0]:
            return "手机号：{}已经注册过。".format(mobilephone)

        if (len(mobilephone) != 11) or (not mobilephone.isdecimal()) or (mobilephone[0] != '1'):
            return "输入的手机号：{}好像不正确，请重新输入。".format(mobilephone)

        password = bottle.request.forms.get("password").strip()
        if len(password) < 4:
            return "输入的密码太短，应该大于4位。"

        code = hashlib.md5()
        code.update(password.encode())
        value = code.hexdigest()

        db.execute("INSERT INTO mobilephone_dict (mobilephone, password) VALUES (?, value)", (mobilephone, value))
        return "手机号：{}注册成功。".format(mobilephone)

@bottle.route("/edit/<id:int>")
def edit(id, db):
    result = db.execute("SELECT DISTINCT projectname FROM workingdiary;").fetchall()
    allprojects = [item[0] for item in result]

    result = db.execute("SELECT DISTINCT location FROM workingdiary;").fetchall()
    alllocations = [item[0] for item in result]

    result = db.execute("SELECT * FROM workingdiary where id = ?", (id,)).fetchone()
    return bottle.template("edit_record", record = result, projects = allprojects, locations = alllocations)

@bottle.post("/edit/<id:int>")
def do_edit(id, db):
    mobilephone = bottle.request.forms.get("mobilephone").strip()
    if (len(mobilephone) != 11) or (not mobilephone.isdecimal()) or (mobilephone[0] != '1'):
        return "输入的手机号：{}好像不正确，请重新输入。".format(mobilephone)
    checkphone = db.execute("SELECT COUNT(*) FROM mobilephone_dict WHERE mobilephone = ?", (mobilephone,)).fetchone()
    if 1 != checkphone[0]:
        return "输入的手机号：{}好像还未注册过。".format(mobilephone)

    password = bottle.request.forms.get("password").strip()
    code = hashlib.md5()
    code.update(password.encode())
    value = code.hexdigest()

    check = db.execute("SELECT password FROM mobilephone_dict WHERE mobilephone = ?", (mobilephone,)).fetchone()
    if value != check[0]:
        return "输入的手机号：{}好像与密码不匹配。".format(mobilephone)

    if bottle.request.forms.get("save", "").strip():
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

        summary = bottle.request.forms.getunicode("summary").strip()
        summary = summary.split('(')[0].strip()

        db.execute("UPDATE workingdiary SET mobilephone = ?, timestamp = ?, projectname = ?, taskname = ?, timeinhour = ?, location = ?, summary = ? WHERE id = ?", (mobilephone, timestamp, projectname, taskname, timeinhour, location, summary, id))

        return "纪录：{}修改成功。".format(id)

    elif bottle.request.forms.get("delete", "").strip():
        db.execute("DELETE FROM workingdiary WHERE id = ?", (id,))

        return "纪录：{}删除成功。".format(id)

bottle.debug(True)
bottle.run()
#application = bottle.default_app()
