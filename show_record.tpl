查到记录：
<table border="1">
%for row in records:
  <tr>
  %for col in row:
    <td>{{col}}</td>
  %end
  <td><a href="/edit/{{row[0]}}">编辑</a></td>
  </tr>
%end
</table>
