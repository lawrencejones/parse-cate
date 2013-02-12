package cate;

import java.text.Format;
import java.text.SimpleDateFormat;
import java.util.*;

public class Exercise implements Comparable<Exercise> {

	private final String id;
	private final String name;
	private final String specLocation;
	private final Module module;
	private final String givenURLs;
	private final Date setDate, dueDate;
	private final ExType assessType;
	private final int duration;

	public Exercise(String id, String name, Module module, String specLocation, String givenURLs,
			Date setDate, Date dueDate, ExType assessType, int duration) {
		assert (id.length() < 3)
		: "Exercise ID is too large: invalid id";
		this.id = id;
		this.name = name;
		this.specLocation = specLocation;
		this.givenURLs = givenURLs;
		this.module = module;
		this.setDate = setDate;
		this.dueDate = dueDate;
		this.assessType = assessType;
		this.duration = duration;
	}

	public String getOnlyIntId() {
		if (Character.isDigit(id.charAt(1))) {
			return id.substring(0,2);
		} else {
			return id.substring(0,1);
		}
	}
	public int getDuration() {
		return duration;
	}
	
	public String getId() {
		return id;
	}

	public String getName() {
		return name;
	}

	public String getSpecURL() {
		return specLocation;
	}

	public String getGivenURLs() {
		return givenURLs;
	}

	public Date getSetDate() {
		return setDate;
	}

	public Date getDueDate() {
		return dueDate;
	}


	public ExType getAssessType() {
		return assessType;
	}
	
	 @Override
	  public int compareTo(Exercise e) {
	    if (getDueDate() == null || e.getDueDate() == null)
	      return 0;
	    return getDueDate().compareTo(e.getDueDate());
	  }
	 
	 public String toString() {
		 Format formatter = new SimpleDateFormat("dd/MM/yyyy");
		 String setDateStr = formatter.format(setDate);
		 String dueDateStr = formatter.format(dueDate);
		 return "Exercise ID : " + id
				 + "\nExercise name : " + name
				 + "\nSpec location : " + specLocation
				 + "\nBelongs to Module : " + module
				 + "\nSet date : " + setDateStr + " due date " + dueDateStr;
	 }

}

enum ExType {
	UNASSESSED, UNASSESSED_SUBMISSION, ASSESSED_INDIVIDUAL, ASSESSED_GROUP
}
