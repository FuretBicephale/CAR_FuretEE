/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package book.service;

import java.util.List;
import javax.ejb.Remote;

/**
 * Initialize the database with some books and allow the user to see the authors' list 
 * @author cachera - brabant
 */
@Remote
public interface bookManager {

    /**
     * Initialize the database with some books.
     */
    public void init();
    
    public List<String> getAuthorsList();
    
}
