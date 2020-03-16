import java.util.ArrayList;
import com.google.gson.GsonBuilder;

public class Assignment2 {
	
	public static ArrayList<Block> blockchain = new ArrayList<Block>(); 

	public static void main(String[] args) {	
		//add our blocks to the blockchain ArrayList:
		//initialising the dataname into blocks 

			blockchain.add(new Block(1,"Mabel Lim Pei Xuan", "0"));		
			blockchain.add(new Block(2,"Lee Shi Jia",blockchain.get(blockchain.size()-1).hash)); 
			blockchain.add(new Block(3,"Cheston Wong",blockchain.get(blockchain.size()-1).hash));
			blockchain.add(new Block(4,"Sabrina",blockchain.get(blockchain.size()-1).hash));
			String blockchainJson = new GsonBuilder().setPrettyPrinting().create().toJson(blockchain);		
			System.out.println(blockchainJson);
	
		
	}
	
	//checking the hash value of previous and current 
	public static Boolean isChainValid() {
		Block currentBlock; 
		Block previousBlock;
		
		//loop through blockchain to check hashes:
		for(int i=1; i < blockchain.size(); i++) {
			currentBlock = blockchain.get(i);
			previousBlock = blockchain.get(i-1);
			//compare registered hash and calculated hash:
			if(!currentBlock.hash.equals(currentBlock.calculateHash()) ){
				System.out.println("Current Hashes not equal");			
				return false;
			}
			//compare previous hash and registered previous hash
			if(!previousBlock.hash.equals(currentBlock.previousHash) ) {
				System.out.println("Previous Hashes not equal");
				return false;
			}
		}
		return true;
	}

}
