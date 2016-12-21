<form action="/edit/{{record[0]}}" method="post">
<table width="500">
<tr>
    <td width="100">记录号：</td>
    <td><input name="id" type="text" value="{{record[0]}}" style="width:400px;" readonly="readonly" /></td>
</tr>
<tr>
    <td width="100">手机号：</td>
    <td><input name="mobilephone" type="text" value="{{record[1]}}" style="width:400px;" readonly="readonly" /></td>
</tr>
<tr>
    <td width="100">日期：</td>
    <td><input name="timestamp" type="text" value="{{record[2]}}" style="width:400px;" /></td>
</tr>
<tr>
    <td width="100">现有项目：</td>
    <td><table>
%for id, item in enumerate(projects):
        <tr><td>{{id+1}}. {{item}}</td></tr>
%end
    </table></td>
</tr>
<tr>
    <td width="100">项目名称：</td>
    <td><input name="projectname" type="text" value="{{record[3]}}" style="width:400px;" /></td>
</tr>
<tr>
    <td width="100">任务名称：</td>
    <td><input name="taskname" type="text" value="{{record[4]}}" style="width:400px;" /></td>
</tr>
<tr>
    <td width="100">耗费时间：</td>
    <td><input name="timeinhour" type="text" value="{{record[5]}}" style="width:400px;" /></td>
</tr>
<tr>
    <td width="100">现有地点：</td>
    <td><table>
%for id, item in enumerate(locations):
        <tr><td>{{id+1}}. {{item}}</td></tr>
%end
    </table></td>
</tr>
<tr>
    <td width="100">地点：</td>
    <td><input name="location" type="text" value="{{record[6]}}" style="width:400px;" /></td>
</tr>
<tr>
    <td width="100">备注：</td>
    <td><textarea name="summary" type="text" value="" style="width:400px;height:100px;">{{record[7]}}</textarea></td>
</tr>
</table>
密码：<input name="password" value="" type="password" style="width:150px" />
<input name="save" value="提交" type="submit" />
<input name="delete" value="删除" type="submit" />
</form>
