package book.servlet;

import book.service.bookManager;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;
import javax.ejb.EJB;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Is a servlet which call getAuthorsList fonction from bookManager and return the list to the user.
 * @author cachera - brabant
 */
@WebServlet(name = "listAuthorsBookServlet", urlPatterns = "/listAuthorsBookServlet")
public class listAuthorsBookServlet extends HttpServlet {
    
    @EJB
    private bookManager bm;
    
    @Override
    public void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();
                
        List<String> list = bm.getAuthorsList();
        
        out.println("<html><body><h1>Authors:</h1><ul>");
        
        for(int i = 0; i < list.size(); i++) {
            out.println("<li>" + list.get(i) + "</li>");
        }   
        
        out.println("</ul></html></body>");
    }
    
}
