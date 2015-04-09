<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!doctype html>
<html lang="fr">
<head>
	<meta charset="utf-8">
	<title>Input summary</title>
</head>
<body>
    	<%
	String title = request.getParameter("bookTitle");
	String author = request.getParameter("bookAuthor");
	String year = request.getParameter("bookYear");
	%>
    
	<h1>Input summary</h1>	
	<div>Title : <%= title %></div><br/>
	<div>Author : <%= author %></div><br/>
	<div>Publication year :  <%= year %></div><br/>
        <%@include file="bookForm.jsp"%>
</body>
</html>