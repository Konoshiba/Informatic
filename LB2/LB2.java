
package informatic;
import java.util.Scanner;
public class inf2 {
	public static void main(String[] args) {
    	Scanner sc = new Scanner(System.in);
    	String massopt = sc.next();
    	String[] a = {"R1", "R2", "I1", "R3", "I2", "I3", "I4"};
        int mass = Integer.parseInt(massopt);
        if(massopt.length() != 7) {
        	System.out.println("Poshel otsuda");
        	return;
        }
        int[] message = new int[7];
        int[] s = new int[3];
        int len = 6;
        while(mass > 0){
        	message[len] = mass%10;
            mass /=10;
            len--;
        }
        System.out.print("Message: ");
        for(int i = 0; i < 7; i++) {
            System.out.printf("%d", message[i]);
        }
        System.out.printf("\n");
        s[0] = message[0] ^ message[2] ^ message[4] ^ message[6];
        s[1]  = message[1] ^ message[2] ^ message[5] ^ message[6];
        s[2] = message[3] ^ message[4] ^ message[5] ^ message[6];
        System.out.printf("Syndrom: %d%d%d\n", s[0], s[1], s[2]);
        System.out.printf("Byt: %d, %s\n", s[0] + s[1]*2 + s[2] * 4, a[s[0] + s[1]*2 + s[2] * 4-1]);
        int fakebit = (s[0]*1 + s[1]*2 + s[2] * 4) - 1;
        System.out.print("Message: ");
        for(int i = 0; i < 7; i++) {
        	if (i != fakebit) {
        		System.out.print(message[i]);
        		}
        	else {
        		System.out.print(message[fakebit] ^ 1);
        	}
        }
}
}
