package cate;

import java.io.*;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;
import java.net.*;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import com.sun.org.apache.xerces.internal.impl.dv.util.Base64;


public class Parser {

	private String webPage; 
	private String login, pass, optionalPeriod;
	public Module[] moduleArray;
	private HashMap<Module,Exercise[]> moduleExs = new HashMap<Module,Exercise[]>();

	public Parser(String login, String pass) throws IOException, ParseException {
		this.login = login; this.pass = pass;
		try {
			this.webPage = generateURL();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		processExs();
	}
	
	public Parser(String login, String pass, String optionalPeriod) throws IOException, ParseException {
		this.login = login; this.pass = pass; this.optionalPeriod = optionalPeriod;
		try {
			this.webPage = generateURL();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		processExs();
	}
	
	public boolean moduleHasExercises(Module m) {
		return moduleExs.containsKey(m);
	}
	
	public Exercise[] getExercises(Module m) {
		if (moduleExs.containsKey(m)) {
			return moduleExs.get(m);
		} else {
			return null;
		
		}
	}
	
	private String getKeyp() {
		return "20" + Character.toString(login.charAt(login.length()-2)) + Character.toString(login.charAt(login.length()-1));
	}
	
	public String generateURL() throws IOException {
		URL url = new URL("https://cate.doc.ic.ac.uk/personal.cgi?keyp=" + getKeyp() +":"+login);
		URLConnection uc = url.openConnection();
		String userpass = login + ":" + pass;
		@SuppressWarnings("static-access")
		String basicAuth = "Basic " + new String(new Base64().encode(userpass.getBytes()));
		uc.setRequestProperty ("Authorization", basicAuth);
		InputStream input = uc.getInputStream();
		Scanner sc = new Scanner(input);
		String classHtml ="", periodHtml="", keyHtml="", html="";
		while (sc.hasNext()) {
			html = sc.nextLine();
			//System.out.println(html);
			if (html.contains("<input type=hidden name=keyt value=")) {
				keyHtml = html;
			}
			if (html.contains("checked")) {
				if (periodHtml.equals("")) {
					periodHtml = html;
				} else if (classHtml.equals("")){
					System.out.println("WE FOUND IT");
					classHtml = html;
				}
			}
		}
		//System.out.println(keyHtml +"\n"+ periodHtml +"\n"+ classHtml+"\n\n");
		String classValue = "", periodValue = "";
		for (int i = 0; i < classHtml.length() - "value=".length(); i++) {
			if (classHtml.substring(i,i+"value=".length()).equals("value=")) {
				classValue = classHtml.substring(i+"value=".length(),i+"value=".length()+2);
			}
		}
		for (int i = 0; i + "value=".length() < periodHtml.length(); i++) {
			if (periodHtml.substring(i,i+"value=".length()).equals("value=")) {
				periodValue = periodHtml.substring(i+"value=".length()+1,i+"value=".length()+2);
			}
		}
		
		for (int i = 0; i < keyHtml.length(); i++) {
			if (keyHtml.charAt(i)=='2') {
			}
		}
		//System.out.println("Period value : " + periodValue + "\nClass value : " + classValue);
		return "https://cate.doc.ic.ac.uk/timetable.cgi?keyt=" + getKeyp() + ":" + ((optionalPeriod != null) ? optionalPeriod :periodValue.trim()) + ":" + classValue.trim() + ":" + login;
	}
	
	public void processExs() throws IOException, ParseException {
		URL url = new URL(webPage);
		URLConnection uc = url.openConnection();
		String userpass = login + ":" + pass;
		@SuppressWarnings("static-access")
		String basicAuth = "Basic " + new String(new Base64().encode(userpass.getBytes()));
		uc.setRequestProperty ("Authorization", basicAuth);
		InputStream input = uc.getInputStream();
		Scanner sc = new Scanner(input);
		String htmlSrc = "";
		while (sc.hasNextLine()) {
			htmlSrc += sc.nextLine();
		}
		Document doc = Jsoup.parse(htmlSrc);
		Elements tableRows = doc.getElementsByTag("tr");
		//System.out.println(tableRows);
		String[][] rowCols = new String[100][100];
		for (int i = 0; i < tableRows.size(); i++) {
			Elements cells = tableRows.get(i).getElementsByTag("td");
			for (int j = 0; j < cells.size(); j++) {
				//System.out.println(cells.get(j).html());
				rowCols[i][j] = cells.get(j).html();
			} //System.out.println();
		}
		ArrayDeque<Integer[]> moduleRowIndexes = new ArrayDeque<Integer[]>();
		ArrayDeque<Integer> rowIndexes = new ArrayDeque<Integer>();
		ArrayDeque<Module> modules = new ArrayDeque<Module>();
		for (int i = 0; i<100; i++) {
			if (rowCols[i][1] != null) if (rowCols[i][1].length() > 8) 
			if (rowCols[i][1].substring(0,8).equals("<b><font")) {
				//System.out.println("FUCKITPLEASEWORK : " +extractInt(tableRows.get(i).html().split("\\r?\\n")[0]));
				//System.out.println("Select LINE: " + Arrays.toString(rowCols[i]));
				int noOfRows = extractInt(tableRows.get(i).html().split("\\r?\\n")[0]);
				for (int x = 0; x < noOfRows; x++) {
					rowIndexes.add(x+i);
				}
				String id = removeFont(rowCols[i][1].substring(22));
				String name = removeFont(removeHeadUntil(rowCols[i][1],'-'));
				modules.add(new Module(id,name));
				moduleRowIndexes.add(rowIndexes.toArray(new Integer[0]));
				i+=noOfRows;
				//System.out.println("HITME");
			}
			rowIndexes.clear();
		} 
		/*for (Integer[] is : moduleRowIndexes) {
			System.out.println(Arrays.toString(is));
		} //*/
		for (Module mod : modules) {
			System.out.println(mod);
		}
		System.out.println("\n");
		//System.out.println(rowIndexes + "\n");
		//Exercise[] exercises = null;
		Date startDate = processDate(7,"January");
		//System.out.println(startDate);
		moduleArray = modules.toArray(new Module[0]); int moduleCount = 0;
		for (Integer[] is : moduleRowIndexes) {
			ArrayDeque<String> exerciseHtml = new ArrayDeque<String>();
			for (int i : is) {
				//System.out.println(tableRows.get(i).html() + "\n\n");
				
				//while (tableRows.get(i).html().contains("<b>")) {
				BufferedReader br = new BufferedReader(new StringReader(tableRows.get(i).html()));
				int x = 0; String s = null;
				while ((s = br.readLine()) != null) {
					//System.out.println(x+ " - " +s);
					if (x > 3) exerciseHtml.add(s);
					x++;
				} 
				//i++;
				//}
				//System.out.println(exerciseHtml+"\n");
			}
			Module crrtModule = moduleArray[moduleCount];
			//System.out.println("analysing crrtModule name : " + crrtModule.getName());
			moduleExs.put(crrtModule, parseExercises(exerciseHtml, startDate, crrtModule));
			moduleCount++;
		}

	}
	
	int extractRowspan(String s) {
		for (int i = 0; i < s.length() -"rowspan=".length(); i++) {
			if (s.substring(i,i+"rowspan=".length()).equals("rowspan=")) {
				return extractInt(s.substring(i+"rowspan=".length(),i+"rowspan=".length()+3));  
			}
		}
		return 1;
	}
	
	Exercise[] parseExercises(ArrayDeque<String> html, Date startDate, Module module) {
		//System.out.println(html);
		int counter = -2; ArrayDeque<Exercise> exercises = new ArrayDeque<Exercise>();
		while (!html.isEmpty()) {
			String snippet = html.pop();
			if (snippet.equals("<td></td>")) {
				counter++;
			} else if (snippet.contains("<td colspan=")) {
				counter += extractInt(snippet);
			} else if (snippet.contains("LightSkyBlue")) {
				counter++;
			} else if (snippet.contains("<td bgcolor=")) {
				exercises.add(processExercise(snippet, startDate, counter, module));
				counter += exercises.getLast().getDuration();
			}
		}
		
		return exercises.toArray(new Exercise[0]);
	}
	
	Exercise processExercise(String html, Date startDate, int counter, Module module) {
		int duration = 0;
		//System.out.println("*****"+html+"*****");
		Document doc = Jsoup.parse(html);
		for (int i = 0; i+13 < html.length(); i++) {
			if (html.substring(i,i+9).contains("colspan=")) {
				//System.out.println("Substring " + html.substring(i,i+13) + "\nRemove alphas : " + html.substring(i,i+13).replaceAll( "[^\\d]", "" ));
				duration = Integer.parseInt(html.substring(i,i+13).replaceAll( "[^\\d]", "" ));
			}
		}  
		//System.out.println("Duration : " + duration);
		Calendar cal = Calendar.getInstance();
        cal.setTime(startDate);
        cal.add(Calendar.DATE, counter); //minus number would decrement the days
        Date setDate = cal.getTime();
        //System.out.println("Set date : " + setDate);
        int tmp = duration-1;
        cal.add(Calendar.DATE, tmp);
        Date dueDate = cal.getTime();
        //System.out.println("Due date : " + dueDate);
        doc = Jsoup.parse(html);
        Element idTag = doc.getElementsByTag("b").first();
        String exId = idTag.text(), exTitle;
        if (doc.text().length() == exId.length()) {
        	exTitle = "";
        } else {
        	exTitle = doc.text().substring(exId.length()+1);
        }
        //got id, title, setDate, dueDate, module, gonna pass givens null and assessType AssessedIndv
        //need specLocation
        String specLocation = null; String givenLink = null;
        Elements hyperlinks = doc.getElementsByTag("a");
        for (Element link : hyperlinks) {
        	if (link.attr("href").contains("SPECS")) {
        		//System.out.println("contains href");
        		specLocation = link.attr("href");
        	}
        	if (link.attr("href").contains("given")) givenLink = link.attr("href");
        }
        Exercise ex = new Exercise(exId,exTitle,module,specLocation,givenLink,setDate,dueDate,null, duration ); 
        //System.out.println(ex + "\n");
        return ex;
	}
	
	String removeFont(String s) {
		for (int i = 0; i < s.length(); i++) {
			if (s.charAt(i+1)=='<') return s.substring(0,(i+1));
		} return null;
	}
	
	String removeHeadUntil(String s, char a) {
		for (int i=0; i < s.length(); i++) {
			if (s.charAt(i)=='-') return s.substring(i+1);
		} return null;
	}
	
	String extractFromTags(String s, String tag) {
		int startOfTag = 0, startOfEndTag = 0;
		for (int i = 0; i < s.length() - tag.length(); i++) {
			if (s.substring(i,i+tag.length()).equals(tag)) startOfTag = i; 
		}
		String endTag = "</" + tag.substring(1);
		for (int i = startOfTag; i < s.length() - endTag.length(); i++) {
			if (s.substring(i,i+endTag.length()).equals(endTag)) startOfEndTag = i;
		}
		return s.substring(startOfTag+tag.length(),startOfEndTag-1);
	}
	
	private int extractInt(String s) {
		//System.out.println("Extract case: " + s);
		return Integer.parseInt(s.replaceAll("[\\D]", ""));
	}
	
	private Date processDate(int day, String month) {
		String[] monthNames = {"JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY"
				, "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"};
		month = month.toUpperCase();
		//System.out.println("Passed in month name: " + month);
		int i = 0; 
		while (!monthNames[i].equals(month.substring(0,monthNames[i].length())) && i<monthNames.length-1) {
			i++;
		}
		SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy");
		Date d = new Date();
		try {
			d = sdf.parse(String.format("%d/%d/%d",day,(i+1),
					Calendar.getInstance().get(Calendar.YEAR)));
		} catch (ParseException e) {
			e.printStackTrace();
		}
		//System.out.println(d);
		return d;
	}

}
