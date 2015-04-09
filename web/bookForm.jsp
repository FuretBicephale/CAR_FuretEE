<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!doctype html>
<html lang="fr">
<head>
	<meta charset="utf-8">
	<title>Add a new book</title>
</head>
<body>        
	<h1>Add a new book</h1>
	<form method="post" action="bookRecap.jsp">
		Title : <input type="text" name="bookTitle" 
                               <% if(request.getParameter("bookTitle") != null) out.println("value='"+request.getParameter("bookTitle") + "'"); %>
                               required/><br/>
		Author : <input type="text" name="bookAuthor" 
                               <% if(request.getParameter("bookAuthor") != null) out.println("value='"+request.getParameter("bookAuthor") + "'"); %>
                               required/><br/>
		Publication year : <input type="number" name="bookYear" 
                               <% if(request.getParameter("bookYear") != null) out.println("value='"+request.getParameter("bookYear") + "'"); %>
                               required/><br/>
		<input type="submit" value="Add"/>
	</form>
</body>
</html>