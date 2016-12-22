查到记录：
<table style="width:1000px" rules=rows frame=hsides>
<tr>
<td style="width:40px" />
<td style="width:40px" />
<td style="width:40px" />
<td style="width:40px" />
<td style="width:40px" />
<td style="width:40px" />
<td style="width:40px" />
<td style="width:40px" />
<td style="width:40px" />
<td style="width:40px" />
<td style="width:40px" />
<td style="width:400px" />
<td style="width:30px" />
<td style="width:130px" />
</tr>
%for row in records:
  <tr>
  %for index, col in enumerate(row):
    %if index == 0:
    <td rowspan=2 style="width:40px">{{col}}</td>
    %elif index == 1:
      %pass
    %elif index == 2:
    <td colspan=2 style="width:80px">{{col}}</td>
    %elif index == 3:
    <td colspan=8 style="width:320px">{{col}}</td>
    %elif index == 4:
    <td style="width:400px">{{col}}</td>
    %elif index == 5:
    <td style="width:30px">{{col}}</td>
    %elif index == 6:
    <td style="width:130px">{{col}}</td>
    %elif index == 7:
      </tr>
      <tr>
      <td style="width:40px"><a href="/edit/{{row[0]}}">编辑</a></td>
      %item = col.split("$")
      %for subindex, subitem in enumerate(item):
        %if subindex == 0:
          %subitem = subitem.strip().split("|")
          %if len(subitem) == 2:
          <td colspan=3 style="width:120px" >{{subitem[1]}}</td>
          %else:
          <td colspan=3 style="width:120px" />
          %end
        %elif subindex == 1:
          %subitem = subitem.strip().split("|")
          %if len(subitem) == 2:
          <td colspan=3 style="width:120px" >{{subitem[1]}}</td>
          %else:
          <td colspan=3 style="width:120px" />
          %end
        %elif subindex == 2:
          %subitem = subitem.strip().split("|")
          %if len(subitem) == 2:
          <td colspan=3 style="width:120px" >{{subitem[1]}}</td>
          %else:
          <td colspan=3 style="width:120px" />
          %end
        %elif subindex == 3:
          %subitem = subitem.strip().split("|")
          %if len(subitem) == 2:
          <td colspan=3 style="width:560px" >{{subitem[1]}}</td>
          %else:
          <td colspan=3 style="width:560px" />
          %end
        %end
      %end
    %end
  %end
  </tr>
%end
</table>
<br />
<a href="/download/{{filename}}">下载文件(.csv)</a><br />
