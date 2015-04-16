/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package book.service;

import book.entity.Book;
import java.util.List;
import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.Query;

/**
 * Implements bookManager interface.
 * @author cachera - brabant
 */
@Stateless
public class bookManagerImpl implements bookManager {

    @PersistenceContext
    private EntityManager em;
            
    @Override
    public void init() {
                        
        Book b1 = new Book("Ferret Power", "Ferret Master", 2016);
        Book b2 = new Book("Ferret Kingdom", "Ferret Master", 2012);
        Book b3 = new Book("Le fleau, T1", "Stephen King", 1990);
        
        em.persist(b1);
        em.persist(b2);
        em.persist(b3);
    }

    @Override
    public List<String> getAuthorsList() {        
        List<String> list;
        
        Query q = em.createQuery("select b.author from Book b");
        list = (List<String>) q.getResultList();
        
        return list;
    }
    
}
