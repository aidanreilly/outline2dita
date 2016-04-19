# outline2dita
Python script to generate a DITA project from a text outline

Create a DITA project structure for oXygen XML Editor, starting from a simple content outline.

## Prerequirements

For outline2dita v1.0 you need:
* oXygen Editor (tested with v16.1, v17.1)
* python 3 (tested with python 3.4.4 on windows). Make sure that you add the Python install dir to your system path.

## Initial setup

Unzip the outline2map folder to C:/outline2map. The unzipped folder contains the following sub-folders and files:

- *_outlines*  
    - *outline2ditamap.py*
      *map-model.txt* is a sample outline. 
- *projects*  
	- *_topic-templates*  
    		- *en*  
    		- *stub-py-Project.xpr*  

## Writing the content outline

Based on your information model for a new project, write the outline in a .txt file and save it in the *_outlines* folder.  
Until further development, the outline files must start by specifying the three parameters for language, repository and folder name:   
```
language=en  
projects repository=C:/DITA/outline2dita/projects/  
project folder name=test-project
```

Make sure your DITA-OT contains the corresponding language strings. Otherwise it will report a series of errors. 

Starting with the 4th line, each line in the outline text file must contain a topic title and topic type.  
Use **tabs** before the topic title, to give the proper nesting level.  
To specify the topic type, insert a space followed by double hash and the type prefix for concept ##c, task ##t, reference ##r. Eventually, add *_ov* for overview topics.  

Example:  
```
language=en
projects repository=C:/DITA/outline2dita/projects/
project folder name=test-project
Introduction ##c_ov
	About this manual ##c_ov
		Scope ##c
		Qualifications ##r
		Liability ##c
	Product overview ##c_ov
		System requirements ##r
		Support ##r
Installing the product ##t_ov
	Installing the server ##t
	Installing the client ##t
Imprint ##c
```

## Creating the DITA project

1. Double-click *generate_outline.bat* to generate the files and open the output folder.
2. The script creates the stub project structure in the C:\outline2dita\projects\ folder.
4. Topic files are generated in *en/source/*. The file name and the `title` element are assigned as given in the outline.  
5. The ditamap is generated in *en* and contains `conref` elements to the topic files.  
4. Open the .xpr project in oXygen and check if the new *test-project.ditamap* is valid.

## Known issues

1. The map should end with a topic on the first level (such as *Imprint*). This issue will be fixed asap.
2. Need to implement support for special characters (normalize titles when used in filepaths).
3. If the previous output folder or any files are open, the script won't complete. Close all files and folders to regenerate the output.
 
