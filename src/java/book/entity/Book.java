package book.entity;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

/**
 * Is a database entity which represents a book with a title, the primary key, an author and a publication year
 * @author cachera - brabant
 */
@Entity
@Table(name="Book")
public class Book {
    
    /**
     * Primary key of Book
     */
    private String author;
    
    private String title;
    private int publicationYear;
    
    public Book(String title, String author, int year) {
        this.title = title; 
        this.author = author;
        this.publicationYear = year;
    }
    
    @Id
    public String getTitle() { 
        return this.title; 
    }
    
    public void setTitle(String title) { 
        this.title = title; 
    }
    
    public String getAuthor() { 
        return this.author; 
    }
    
    public void setAuthor(String author) { 
        this.author = author; 
    }
    
    public int getPublicationYaer() {
        return this.publicationYear;
    }
    
    public void setPublicationYear(int year) {
        this.publicationYear = year;
    }
    
}
