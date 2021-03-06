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
            `password` TEXT,
            PRIMARY KEY(mobilephone));
            ''')

    today = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")

    result = db.execute("SELECT DISTINCT projectname FROM workingdiary order by projectname asc;").fetchall()
    allprojects = [item[0] for item in result]

    result = db.execute("SELECT DISTINCT location FROM workingdiary order by location asc;").fetchall()
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

        result = db.execute("SELECT DISTINCT projectname FROM workingdiary order by projectname asc;").fetchall()
        allprojects = [item[0] for item in result]

        projectname = bottle.request.forms.getunicode("projectname").strip()
        if len(projectname):
            if projectname.isdecimal():
                if (int(projectname) > 0) and (int(projectname) <= len(allprojects)):
                    projectname = allprojects[int(projectname) - 1]
                else:
                    return "输入的项目名称：{}好像不正确。".format(projectname)
        else:
            return "输入的项目名称：{}好像不正确。".format(projectname)

        taskname = bottle.request.forms.getunicode("taskname").strip()
        if not len(taskname):
            return "输入的任务名称不能为空。"

        timeinhour = bottle.request.forms.get("timeinhour").strip()
        try:
            timeinhour = float(timeinhour)
        except ValueError:
            return "输入的耗费时间：{}好像不正确。".format(timeinhour)
        if timeinhour % 0.5:
            return "输入的耗费时间：{}好像不正确。".format(timeinhour)

        result = db.execute("SELECT DISTINCT location FROM workingdiary order by location asc;").fetchall()
        alllocations = [item[0] for item in result]

        location = bottle.request.forms.getunicode("location").strip()
        if len(location):
            if location.isdecimal():
                if (int(location) > 0) and (int(location) <= len(alllocations)):
                    location = alllocations[int(location) - 1]
                else:
                    return "输入的地点：{}好像不正确。".format(location)
        else:
            return "输入的地点：{}好像不正确。".format(location)

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

        with open(os.path.join(os.path.split(os.path.realpath(__file__))[0], "download", mobilephone + ".csv"), "wt") as csvfile:
            csvfile.write("\"记录号\",\"日期\",\"项目名称\",\"任务名称\",\"耗费时间\",\"地点\",\"交通\",\"住宿\",\"餐饮\",\"其他\",\n")

            for record in result:
                for index, item in enumerate(record):
                    if index == 1:
                        pass
                    elif index == 7:
                        item = item.split("$")
                        for subitem in item:
                            subitem = subitem.strip().split("|")
                            if len(subitem) == 2:
                                csvfile.write("\"{}\",".format(subitem[1].strip()))
                            else:
                                csvfile.write("\"\",")
                    else:
                        csvfile.write("\"{}\",".format(item))

                csvfile.write("\n")

        result = db.execute("SELECT * FROM workingdiary WHERE mobilephone = ? order by date(timestamp) desc", (mobilephone,))

        return bottle.template("show_record", records = result, filename = mobilephone + ".csv")

    elif bottle.request.forms.get("adduser", "").strip():
        mobilephone = bottle.request.forms.get("mobilephone").strip()
        if (len(mobilephone) != 11) or (not mobilephone.isdecimal()) or (mobilephone[0] != '1'):
            return "输入的手机号：{}好像不正确，请重新输入。".format(mobilephone)

        checkphone = db.execute("SELECT COUNT(*) FROM mobilephone_dict WHERE mobilephone = ?", (mobilephone,)).fetchone()
        if 1 == checkphone[0]:
            return "手机号：{}已经注册过。".format(mobilephone)

        password = bottle.request.forms.get("password").strip()
        if len(password) < 4:
            return "输入的密码太短，应该大于4位。"

        code = hashlib.md5()
        code.update(password.encode())
        value = code.hexdigest()

        db.execute("INSERT INTO mobilephone_dict (mobilephone, password) VALUES (?, ?)", (mobilephone, value))
        return "手机号：{}注册成功。".format(mobilephone)

@bottle.route('/download/<filename:path>')
def download(filename):
    return bottle.static_file(filename, os.path.join(os.path.split(os.path.realpath(__file__))[0], "download"))

@bottle.route("/edit/<id:int>")
def edit(id, db):
    result = db.execute("SELECT DISTINCT projectname FROM workingdiary order by projectname asc;").fetchall()
    allprojects = [item[0] for item in result]

    result = db.execute("SELECT DISTINCT location FROM workingdiary order by location asc;").fetchall()
    alllocations = [item[0] for item in result]

    result = db.execute("SELECT * FROM workingdiary where id = ?", (id,)).fetchone()
    if type(result) == type(None):
        return "非法查询。".format(id)

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

        result = db.execute("SELECT DISTINCT projectname FROM workingdiary order by projectname asc;").fetchall()
        allprojects = [item[0] for item in result]

        projectname = bottle.request.forms.getunicode("projectname").strip()
        if len(projectname):
            if projectname.isdecimal():
                if (int(projectname) > 0) and (int(projectname) <= len(allprojects)):
                    projectname = allprojects[int(projectname) - 1]
                else:
                    return "输入的项目名称：{}好像不正确。".format(projectname)
        else:
            return "输入的项目名称：{}好像不正确。".format(projectname)

        taskname = bottle.request.forms.getunicode("taskname").strip()
        if not len(taskname):
            return "输入的任务名称不能为空。"

        timeinhour = bottle.request.forms.get("timeinhour").strip()
        try:
            timeinhour = float(timeinhour)
        except ValueError:
            return "输入的耗费时间：{}好像不正确。".format(timeinhour)
        if timeinhour % 0.5:
            return "输入的耗费时间：{}好像不正确。".format(timeinhour)

        result = db.execute("SELECT DISTINCT location FROM workingdiary order by location asc;").fetchall()
        alllocations = [item[0] for item in result]

        location = bottle.request.forms.getunicode("location").strip()
        if len(location):
            if location.isdecimal():
                if (int(location) > 0) and (int(location) <= len(alllocations)):
                    location = alllocations[int(location) - 1]
                else:
                    return "输入的地点：{}好像不正确。".format(location)
        else:
            return "输入的地点：{}好像不正确。".format(location)

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
