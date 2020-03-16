
import java.util.Date;
import java.sql.*;

public class Block {

	public String hash;
	public String previousHash;
	private String data; //our data will be a simple message.
	public String timeStamp;
	public int index;
	

	public String calculateHash() {
		
		Timestamp ts = new Timestamp(10000);
		String calculatedhash = StringUtil.applySha256( 
				previousHash +
				ts.toString() +
				data 
				);
		return calculatedhash;
	}
	
	public Block(int index, String data,String previousHash ) {
		this.index = index;
		this.data = data;
		this.previousHash = previousHash;
		this.timeStamp = new Date().toString();
		this.hash = calculateHash(); //Making sure we do this after we set the other values.
	}


}


/*import java.sql.*; 

class GFG { 
    public static void main(String args[]) 
    { 
        // Create two timestamp objects 
        Timestamp ts = new Timestamp(10000); 
  
        // Display the timestamp object 
        System.out.println("Timestamp time : "
                           + ts.toString()); 
        System.out.println("Time in milliseconds : "
                           + ts.getTime()); 
    } 
} 
*/