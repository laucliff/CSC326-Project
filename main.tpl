RushedSearch
<form action="/" method="GET">
<input type="text" name="query">
<input type="submit" value="Search">
</form>
%if results:
  %for result in results:
    <div> {{result}} <br> </div>
