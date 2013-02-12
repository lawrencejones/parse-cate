package cate;

public class Module {

	private final String moduleId;
	//restriction to size 4
	private final String name;
	//private final URL[] noteURLs;

	public Module(String moduleId, String name) { //, URL[] noteURLs) {
		assert (moduleId.length() < 8)
		: "Module ID is too large: invalid moduleId";
		this.moduleId = moduleId;
		this.name = name;
		//this.noteURLs = noteURLs;
	}

	public String getModuleId() {
		return moduleId;
	}

	public String getName() {
		return name;
	}

	@Override
	public String toString() {
		return moduleId + " - " + name;
	}
	
	/*public URL[] getNotes() {
		return noteURLs;
	} */

}
