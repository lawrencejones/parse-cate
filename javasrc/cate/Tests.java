package cate;

import java.io.IOException;
import java.io.InputStreamReader;
import java.text.ParseException;
import java.util.Scanner;
import java.io.Console;

public class Tests {

	/**
	 * @param args
	 * @throws ParseException 
	 */
	public static void main(String[] args) throws IOException, ParseException {
		Scanner sc = new Scanner(new InputStreamReader(System.in));
		System.out.println("Please enter your username...");
		String user = sc.next();
		System.out.println("Please enter your password...");
		Console cons = System.console();
		String pass ="";
		if (cons != null) {
			char[] p = cons.readPassword();
			for (char c : p) {
				pass += Character.toString(c);
			}
		} else {
			pass = sc.next();
		}
    System.out.println(pass);
		//pass = "109E00a248";
		String tmp = sc.next();
		String optionalPeriod = "";
		if (tmp.equals("AUTUMN")) {
			optionalPeriod = "1";
		} else if (tmp.equals("SPRING")) {
			optionalPeriod = "3";
		}
		System.out.println();
		//String pass = sc.next();
		Parser parser = new Parser(user, pass, optionalPeriod);
		//HashMap<Module,Exercise[]> moduleExercises = parser.getModuleExercises();
		for (int i = 0; i < parser.moduleArray.length; i++) {
			Module m = parser.moduleArray[i];
			if (parser.moduleHasExercises(m)) {
				if (parser.getExercises(m).length != 0) {
					System.out.println("\n**********************************************\n" + m + "\n**********************************************\n");
					Exercise[] exs = /*Util.sortExercise*/(parser.getExercises(m));
					for (int j = 0; j < exs.length; j++) {
						System.out.println(j+ "  -  " + exs[j]+"\n");
					}
				}
			}
		}
	}

}
