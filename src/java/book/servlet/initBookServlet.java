package book.servlet;

import book.service.bookManager;
import java.io.IOException;
import java.io.PrintWriter;
import javax.ejb.EJB;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Is a servlet which call init fonction from bookManager in order to initialize the database with some books
 * @author cachera - brabant
 */
@WebServlet(name = "initBookServlet", urlPatterns = "/initBookServlet")
public class initBookServlet extends HttpServlet {
    
    @EJB
    private bookManager bm;
    
    @Override
    public void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();
        
        bm.init();
        
        out.println("<html><body><h1>Successful initialisation!</h1></html></body>");
    }
    
}
