<form action="/" method="post">
<table width="500">
<tr>
    <td width="100">手机号：</td>
    <td><input name="mobilephone" type="text" value="" style="width:150px;" /></td>
    <td><input name="query" value="查询" type="submit" /></td>
    <td><input disabled name="adduser" value="添加" type="submit" /></td>
    <td><input name="password" value="" type="password" style="width:150px" /></td>
</tr>
<tr>
    <td width="100">日期：</td>
    <td colspan=4><input name="timestamp" type="text" value="{{timestamp}}" style="width:400px;" /></td>
</tr>
<tr>
    <td width="100">现有项目：</td>
    <td colspan=4><table>
%for id, item in enumerate(projects):
        <tr><td>{{id+1}}. {{item}}</td></tr>
%end
    </table></td>
</tr>
<tr>
    <td width="100">项目名称：</td>
    <td colspan=4><input name="projectname" type="text" value="" style="width:400px;" /></td>
</tr>
<tr>
    <td width="100">任务名称：</td>
    <td colspan=4><input name="taskname" type="text" value="" style="width:400px;" /></td>
</tr>
<tr>
    <td width="100">耗费时间：</td>
    <td colspan=4><input name="timeinhour" type="text" value="（以0.5小时为最小单位）" style="width:400px;" /></td>
</tr>
<tr>
    <td width="100">现有地点：</td>
    <td colspan=4><table>
%for id, item in enumerate(locations):
        <tr><td>{{id+1}}. {{item}}</td></tr>
%end
    </table></td>
</tr>
<tr>
    <td width="100">地点：</td>
    <td colspan=4><input name="location" type="text" value="公司" style="width:400px;" /></td>
</tr>
<tr>
    <td width="100">备注：</td>
    <td colspan=4><textarea name="summary" type="text" value="" style="width:400px;height:100px;">交通|$住宿|$餐饮|$其他|(这里列出的关键字不要改动，"|"符号后面添加对应项的内容，"$"符号表示对应项结束。自行添加的内容也不要包含它们，本括号的内容会自动删除。)</textarea></td>
</tr>
</table>
<input name="save" value="提交" type="submit" />
</form>
