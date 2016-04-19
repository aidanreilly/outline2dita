#!/usr/bin/env python3
#OUTLINE TO DITAMAP TRANSFORMATION
#version 1.0
#author @thinkDITA
#tweaked aidanreilly
#Copy topic templates for each language in <outline2dita folder>/_topic-templates/<language>.
#This  script takes a .txt file as argument. Make sure the .txt has the following structure:
#language=en|de
#projects repository=<projects folder>
#project folder name=<project name>
#[tabs]<Title> ##<prefix>
#Example:
#----------------
#language=en
#projects repository=C:/DITA/projects/
#project folder name=test-project
#General ##c_ov
#	Information about the manual ##c_ov
#		Scope ##c
#----------------
#Set the nesting via tabs
#Specify the topic type by space+hash+hash+prefix
#
#
import sys
import os
import shutil
import glob

'txt_filepath' in vars()
os.listdir()[0]
#OPEN AND PROCESS THE TXT LINES:
for filename in glob.glob('*.txt'):
    txt_file=open(filename,'r',encoding='UTF-8')
    lines=txt_file.readlines()
    #["General ##c_ov\n", "\tInformation about the manual ##c_ov\n", "\t\tScope ##c\n"]
    line_pairs=[]
    for line in lines:
        if 'language=' in line:
            lang=line.split('=')[1].strip()
            print("Language: ",lang)
            if lang=='en':
                xml_lang='en-US'
            elif lang=='de':
                xml_lang='de-DE'
        elif 'projects repository' in line:
            proj_homedir=line.split('=')[1].strip()
            print("Projects repository: ",proj_homedir)
        elif 'project folder name' in line:
            proj_name=line.split('=')[1].strip()
            print("Project name: ",proj_name)
        elif '##' in line:
            line_level=line.count('\t')
            line_text_type=line.strip()
            line_text_pair=line_text_type.split('##')
            text=line_text_pair[0].strip().replace('\ufeff', '')
            topic_type=line_text_pair[1]
            line_pair=[line_level,text,topic_type]
            #[4, 'Show balance', 'c']
            line_pairs.append(line_pair)
        else:
            print('\tMake sure the ##type is specified for each topic \n\tCheck line ',len(line_pairs)+1)
            sys.exit()
    print(line_pairs)
    #collect a list of following topics to check for nesting
    following_lines=line_pairs[1:len(line_pairs)]
    following_lines.append([-1,'End of map',''])
    msg='Number of entries: '
    print(msg,len(line_pairs))
    #print(following_lines)
    txt_file.close()


#create proj dir
proj_dir=proj_homedir+'/'+proj_name
#clean previous output
dir = proj_dir
if os.path.exists(dir):
    shutil.rmtree(dir)
os.makedirs(proj_dir)
#create proj_name.xpr in proj_dir, if does not exist
xpr_templ=proj_homedir+'_topic-templates/stub-py-'+lang+'-Project.xpr'
xpr_file=proj_dir+'/'+proj_name+'.xpr'
if not os.path.isfile(xpr_file):
    shutil.copy(xpr_templ, xpr_file)
#create source dir
source_dir=proj_dir+'/'+lang+'/source'
os.makedirs(source_dir)
templ_path=proj_homedir+'_topic-templates/'+lang
#
#
#PROCESSING THE LEVELS:
#Read the name and type of the topic, create topic file and write topicref in ditamap
new_ditalines=''
x=0
for x in range(len(line_pairs)):
    (line_level,line_navtitle,topic_type)=line_pairs[x]
    (f_line_level,f_line_navtitle,f_topic_type)=following_lines[x]
    #print(line_level,'followed by',f_line_level)
    #construct topic type, title and filename
    topicname=str.casefold(line_navtitle).replace(' ','-')
    topicfile=topicname+'.dita'
    if topic_type.startswith('trbl'):
        att_type='troubleshooting'
    elif topic_type.startswith('c'):
        att_type='concept'
    elif topic_type.startswith('t'):
        att_type='task'
    elif topic_type.startswith('r'):
        att_type='reference'
    else:
        att_type='topic'
    #replace id and title in template, and create new topic file
    templ_name=att_type.title()+'.xml'
    templ_srcname = os.path.join(templ_path, templ_name)
    templ_dstname = os.path.join(source_dir, topicfile)
    read_templ=open(templ_srcname,'r',encoding='UTF-8')
    new_topic=open(templ_dstname,'w',encoding='UTF-8')
    for line in read_templ:
        if '${id}' in line:
            new_topic.write(line.replace('${id}',topicname))
        elif '${caret}' in line:
            new_topic.write(line.replace('${caret}',line_navtitle))
        else:
            new_topic.write(line)
    new_topic.close()
    read_templ.close()
    print('Created topic ',templ_dstname)
    #
    #
    #write topicrefs in ditamap:
    if f_line_level == -1:
        #last topic in map (should be Impressum on first level)
        line_topicref='<topicref href="source/'+topicfile+'" navtitle="'+line_navtitle+'" format="dita" type="'+att_type+'"/></map>\n'
    elif line_level < f_line_level:
        #topic followed by children (stays open)
        line_topicref='<topicref href="source/'+topicfile+'" navtitle="'+line_navtitle+'" format="dita" type="'+att_type+'">\n'
    elif line_level == f_line_level:
        #topic followed by sibling (close tag)
        line_topicref='<topicref href="source/'+topicfile+'" navtitle="'+line_navtitle+'" format="dita"  type="'+att_type+'"/>\n'
    elif line_level == f_line_level + 1:
        #topic followed by parent (close tag and close parent)
        line_topicref='<topicref href="source/'+topicfile+'" navtitle="'+line_navtitle+'" format="dita" type="'+att_type+'"/></topicref>\n'
    elif line_level == f_line_level + 2:
        #topic followed by grand-parent (close tag and close 2 x parent)
        line_topicref='<topicref href="source/'+topicfile+'" navtitle="'+line_navtitle+'" format="dita" type="'+att_type+'"/></topicref></topicref>\n'
    elif line_level == f_line_level + 3:
        #topic followed by great-grand-parent (close tag and close 3 x parent)
        line_topicref='<topicref href="source/'+topicfile+'" navtitle="'+line_navtitle+'" format="dita" type="'+att_type+'"/></topicref></topicref></topicref>\n'
    elif line_level == f_line_level + 4:
        #topic followed by great-great-grand-parent (close tag and close 4 x parent)
        line_topicref='<topicref href="source/'+topicfile+'" navtitle="'+line_navtitle+'" format="dita" type="'+att_type+'"/></topicref></topicref></topicref></topicref>\n'
    #else:
        #line_topicref='<!-- Too many levels! Cannot add '+line_navtitle+'. Please use submaps. -->'
    new_dline=line_topicref
    new_ditalines=new_ditalines+new_dline
print(new_ditalines)
#WRITE NEW DITAMAP
dita_filepath2=proj_dir+'/'+lang+'/'+proj_name+'.ditamap'
dita_file2=open(dita_filepath2,'w',encoding='UTF-8')
dita_file2.write('<?xml version="1.0" encoding="UTF-8"?> \n<!DOCTYPE map PUBLIC "-//OASIS//DTD DITA Map//EN" "map.dtd"> \n<map xml:lang="'+xml_lang+'">\n<title>'+proj_name+'</title>\n')
dita_file2.write(new_ditalines)
dita_file2.close()
print('New ditamap created as ',dita_filepath2)
print(msg,len(line_pairs))
print('You can open the project file: ',xpr_file)



