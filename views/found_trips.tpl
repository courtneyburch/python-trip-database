<html> <body>
<h4>Trip Results</H4>
<table>
    <tr>
        <th>Trip ID</th>
        <th>Username</th>
        <th>Date</th>
        <th>Destination</th>
        <th>Miles</th>
        <th>Gallons</th>
    </tr>

    %for row in rows:
    <tr>
        %for col in row:
            <td>{{col}}</td>
        %end
    </tr>
    %end    

</table>


<a href='/'>Go Home</a> 
      
</body></html>