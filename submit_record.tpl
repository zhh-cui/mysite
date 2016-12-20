<form action="/" method="post">
<table width="500">
<tr>
    <td width="100">手机号：</td>
    <td><input name="mobilephone" type="text" value="" style="width:250px;" /></td>
    <td><input name="query" value="查询" type="submit" /></td>
    <td><input disabled name="adduser" value="添加" type="submit" /></td>
</tr>
<tr>
    <td width="100">日期：</td>
    <td colspan=3><input name="timestamp" type="text" value="{{timestamp}}" style="width:400px;" /></td>
</tr>
<tr>
    <td width="100">现有项目：</td>
    <td colspan=3><table>
%for item in projects:
        <tr><td>{{item}}</td></tr>
%end
    </table></td>
</tr>
<tr>
    <td width="100">项目名称：</td>
    <td colspan=3><input name="projectname" type="text" value="" style="width:400px;" /></td>
</tr>
<tr>
    <td width="100">任务名称：</td>
    <td colspan=3><input name="taskname" type="text" value="" style="width:400px;" /></td>
</tr>
<tr>
    <td width="100">耗费时间：</td>
    <td colspan=3><input name="timeinhour" type="text" value="（以0.5小时为最小单位）" style="width:400px;" /></td>
</tr>
<tr>
    <td width="100">现有地点：</td>
    <td colspan=3><table>
%for item in locations:
        <tr><td>{{item}}</td></tr>
%end
    </table></td>
</tr>
<tr>
    <td width="100">地点：</td>
    <td colspan=3><input name="location" type="text" value="公司" style="width:400px;" /></td>
</tr>
<tr>
    <td width="100">备注：</td>
    <td colspan=3><textarea name="summary" type="text" value="" style="width:400px;height:100px;">交通：，住宿：，餐饮：，其他：(这里列出的关键字和标点符号不要改动)</textarea></td>
</tr>
</table>
<input name="save" value="提交" type="submit" />
</form>
