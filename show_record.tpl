查到如下记录：
<table border="1">
%for row in records:
  <tr>
  %for col in row:
    <td>{{col}}</td>
  %end
  </tr>
%end
</table>
