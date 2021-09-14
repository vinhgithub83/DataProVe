"""
Created on  August 2020
Last update August 2021

@author: Vinh Thong Ta (vinhthongt@gmail.com, Tav@edgehill.ac.uk) and the DataProVe team.

NOTE: 
This code was written besides limited resources (time and man power) mainly to demonstrate what the 
approach and the tool in the paper can be used for, and how the proposed approach can be implemented as an example.

The code is still in its "prototype/infancy stage". Hence, it has not been properly optimised (regarding 
code efficiency and length). 

This code will be constantly improved and optimised in the future on the GitHub 
page of the tool (https://github.com/Dataprove/Dataprovetool/), which will be made publicly available.  

Python was chosen for the prototype due to its large community and great support (inc. GUI libraries). 
Possible changes also include switching to other programming langauge to improve efficiency. 

"""



import webbrowser
from tkinter import * 
import re
import itertools
from tkinter import scrolledtext
from tkinter.colorchooser import *
 
import json
from tkinter.filedialog import askopenfile 
from tkinter.filedialog import asksaveasfile 
import time



def objectinfo(comp): 
    coordi = canvas.coords(comp)
    return [coordi,canvas.itemcget(comp, 'fill'),canvas.itemcget(comp, 'activefill')]   

def textboxinfo(tbox): 
    coordi = canvas.coords(tbox[0]) 
    return [coordi,tbox[1],tbox[2]]  


def removebracketsfromtuple(tup): 
        return ",".join(tup)


def extractparamConsent(consterm) : 
    global CConsDataE 
    global UConsDataE
    global SConsDataE
    global FwConsDataE
    
        
    if str(consterm.predicate) == "cconsent" :    
        if str(consterm.arguments[0]) not in CConsDataE: 
            CConsDataE[str(consterm.arguments[0])] = set()
            CConsDataE[str(consterm.arguments[0])].add(str(consterm.arguments[1]))
        else: 
            CConsDataE[str(consterm.arguments[0])].add(str(consterm.arguments[1]))
            
        
    elif str(consterm.predicate) == "uconsent" :  
        if str(consterm.arguments[0]) not in UConsDataE: 
            UConsDataE[str(consterm.arguments[0])] = set()
            UConsDataE[str(consterm.arguments[0])].add(str(consterm.arguments[1]))
        else: 
            UConsDataE[str(consterm.arguments[0])].add(str(consterm.arguments[1]))
    
    
    elif str(consterm.predicate) == "sconsent" :  
        
        if str(consterm.arguments[0]) not in SConsDataE: 
            SConsDataE[str(consterm.arguments[0])] = set()
            SConsDataE[str(consterm.arguments[0])].add(str(consterm.arguments[1]))
        else: 
            SConsDataE[str(consterm.arguments[0])].add(str(consterm.arguments[1]))
            
            
    elif str(consterm.predicate) == "fwconsent" :  
        if str(consterm.arguments[0]) not in FwConsDataE: 
            FwConsDataE[str(consterm.arguments[0])] = set()
            FwConsDataE[str(consterm.arguments[0])].add(str(consterm.arguments[1]))
        else: 
            FwConsDataE[str(consterm.arguments[0])].add(str(consterm.arguments[1])) 


def dictsetTOdictlistVALKEY(dictionary) :
    tempdict = {}
    for k in dictionary.keys(): 
        tempdict[removebracketsfromtuple(k)] = list(dictionary[k])
    return tempdict

def dictsetTOdictlistKEY(dictionary) :
    tempdict = {}
    for k in dictionary.keys(): 
        tempdict[removebracketsfromtuple(k)] = dictionary[k]
    return tempdict

def dictsetTOdictlistVAL(dictionary) :
    for k in dictionary.keys():
        dictionary[k] = list(dictionary[k])
    return dictionary

############################################# SAVE A POLICY FILE ########################################

def savepolicyfileas(): 
    files = [('Policy', '*.pol')] 
    file = asksaveasfile(mode='w', filetypes = files, defaultextension = files)
    
    if file:
        policyfilelist = [entityrec,
                          dictsetTOdictlistVAL(datatypesrec),
                          dictsetTOdictlistKEY(collectionpolicytosave),
                          dictsetTOdictlistKEY(usagepolicytosave),
                          dictsetTOdictlistKEY(storagepolicytosave),
                          dictsetTOdictlistKEY(deletionpolicytosave),
                          dictsetTOdictlistKEY(transferpolicytosave),
                          dictsetTOdictlistKEY(haspolicytosave),
                          dictsetTOdictlistKEY(linkpermitpolicytosave),
                          dictsetTOdictlistKEY(linkforbidpolicytosave),
                          storagemodepol,
                          dictsetTOdictlistKEY(storeoptionrec),
                          list(map(tostring, queryLinkUnique)),
                          list(map(tostring, queryLink)),
                          list(map(tostring, queryNotLinkUnique)),
                          list(map(tostring, queryNotLink)),
                          datagroupoftypes,
                          list(UniqueData),
                          dictsetTOdictlistKEY(lastCQuery),
                          dictsetTOdictlistKEY(lastUQuery),
                          dictsetTOdictlistKEY(lastSQuery),
                          dictsetTOdictlistKEY(lastDQuery),
                          dictsetTOdictlistVALKEY(lastTQuery),
                          dictsetTOdictlistKEY(lastHQuery),
                          dictsetTOdictlistVALKEY(lastLinkPer),
                          dictsetTOdictlistVALKEY(lastLinkFor),
                          dictsetTOdictlistVAL(datatypesrec1)] 
        json.dump(policyfilelist, file)
        file.close()
    else: 
        return 0


    
def convertstrtupletotuple(stringkey) : 
    return  (stringkey.split(',')[0],",".join(stringkey.split(',')[1:])) 
    

def dictlistTOdictsetVALKEY(dictionary) :
    tempdict = {}
    for k in dictionary.keys():
        tempdict[convertstrtupletotuple(k)] = set(dictionary[k])
    return tempdict

def dictlistTOdictsetVALKEYcuPURP(dictionary) :
    tempdict = {}
    for k in dictionary.keys():
        tempdict[convertstrtupletotuple(k)] = set(map(tuple,dictionary[k]))
    return tempdict

def dictlistTOdictsetKEY(dictionary) :
    tempdict = {}
    for k in dictionary.keys():
        tempdict[convertstrtupletotuple(k)] = dictionary[k]
    return tempdict

def dictlistTOdictsetVAL(dictionary) :
    for k in dictionary.keys():
        dictionary[k] = set(dictionary[k])
    return dictionary

############################################# OPEN A POLICY FILE ########################################
    
def open_policyfile(): 
    global entityrec
    global datagroupoftypes
    global datatypesrec
    global collectionpolicytosave
    global usagepolicytosave
    global storagepolicytosave
    global deletionpolicytosave 
    global transferpolicytosave 
    global haspolicytosave 
    global linkpermitpolicytosave 
    global linkforbidpolicytosave
    global storagemodepol   
    global storeoptionrec
    global queryLinkUnique
    global queryLink
    global queryNotLinkUnique
    global queryNotLink
    global UniqueData   
    global lastCQuery 
    global lastUQuery 
    global lastSQuery 
    global lastDQuery 
    global lastTQuery 
    global lastHQuery 
    global lastLinkPer 
    global lastLinkFor
    global datatypesrec1
    global transferThirdRec
    global queryHas
    global entityHasListRec
    global entityHasRec
    global queryCConsent
    global cpurposesRecPol
    global setcpurposesRecPol
    global queryUConsent
    global upurposesRecPol
    global setupurposesRecPol
    global querySConsent
    global storagemodepol    
    global storePolRec 
    global queryHasAfter
    global queryFWConsent
    
    
    try:
        with askopenfile(mode ='r', filetypes =[('Policy', '*.pol')]) as file :
            queryHas.clear()
            entityHasListRec.clear()
            entityHasRec.clear()
            queryCConsent.clear()
            cpurposesRecPol.clear()
            setcpurposesRecPol.clear()
            queryUConsent.clear()
            upurposesRecPol.clear()
            setupurposesRecPol.clear()
            querySConsent.clear()
            storagemodepol.clear()    
            queryHasAfter.clear()
            queryFWConsent.clear()
            transferThirdRec.clear()
            
            policylist =  json.load(file)
            entityrec = policylist[0].copy()
            datatypesrec = dictlistTOdictsetVAL(policylist[1]).copy()
        
            datagroupoftypes = policylist[16]
            UniqueData = set(policylist[17])
        
        
            collectionpolicytosave = dictlistTOdictsetKEY(policylist[2]).copy()
        
            for (term11,term22) in collectionpolicytosave.keys(): 
          
                content1 = collectionpolicytosave[(term11,term22)][0]
                content2 = collectionpolicytosave[(term11,term22)][1]
            
                save_colpolicy_noframe(content1,content2,term11,term22)
        
        
            usagepolicytosave = dictlistTOdictsetKEY(policylist[3]).copy()
            for (term11,term22) in usagepolicytosave.keys():
                ucontent1 = usagepolicytosave[(term11,term22)][0]
                ucontent2 = usagepolicytosave[(term11,term22)][1]
                save_usepolicy_noframe(ucontent1,ucontent2,term11,term22)
        
        
            storagepolicytosave = dictlistTOdictsetKEY(policylist[4]).copy()
            storagemodepol = policylist[10]
            storeoptionrec = dictlistTOdictsetKEY(policylist[11]).copy()
            for (who1, what1) in storagepolicytosave.keys():
                scontent1 = storagepolicytosave[(who1, what1)][0]
                scontent2 = storagepolicytosave[(who1, what1)][1]
                save_storepolicy_noframe(scontent1,scontent2, who1, what1)
        
        
        
            deletionpolicytosave = dictlistTOdictsetKEY(policylist[5]).copy()
            for (who1, what1) in deletionpolicytosave.keys():
                deloption = deletionpolicytosave[(who1, what1)][0]
                dcontent1 = deletionpolicytosave[(who1, what1)][1]
                dcontent2 = deletionpolicytosave[(who1, what1)][2]
                save_deletepolicy_noframe(dcontent1,dcontent2,deloption,who1,what1)
        
        
            transferpolicytosave = dictlistTOdictsetKEY(policylist[6]).copy()
            for (who1, what1) in transferpolicytosave.keys():
                tcontent1 = transferpolicytosave[(who1, what1)][0]
                tcontent2 = transferpolicytosave[(who1, what1)][1]
                save_transferpolicy_noframe(tcontent1,tcontent2, who1, what1)
        
        
            haspolicytosave = dictlistTOdictsetKEY(policylist[7]).copy()
            for (term11, term22) in haspolicytosave.keys(): 
            
                hcontent = haspolicytosave[(term11, term22)][0]
            
                save_haspolicy_noframe(hcontent, term11, term22)
        
        
            linkpermitpolicytosave = dictlistTOdictsetKEY(policylist[8]).copy()
        
        
            if len(policylist[12]) > 0: 
                queryLinkUnique = list(map(strtoterm,policylist[12]))
            elif len(policylist[12]) == 0: 
                queryLinkUnique = []
        
            if len(policylist[13]) > 0: 
                queryLink = list(map(strtoterm,policylist[13]))
            elif len(policylist[13]) == 0: 
                queryLink = []
        
        
        
            linkforbidpolicytosave = dictlistTOdictsetKEY(policylist[9]).copy()
        
        
            if len(policylist[14]) > 0: 
                queryNotLinkUnique = list(map(strtoterm,policylist[14]))
            elif len(policylist[14]) == 0: 
                queryNotLinkUnique = []
        
            if len(policylist[15]) > 0: 
                queryNotLink = list(map(strtoterm,policylist[15]))
            elif len(policylist[15]) == 0: 
                queryNotLink = []
        
        
            lastCQuery = dictlistTOdictsetKEY(policylist[18]).copy()
            lastUQuery = dictlistTOdictsetKEY(policylist[19]).copy()
            lastSQuery = dictlistTOdictsetKEY(policylist[20]).copy()
            lastDQuery = dictlistTOdictsetKEY(policylist[21]).copy()
            lastTQuery = dictlistTOdictsetVALKEY(policylist[22]).copy()
            lastHQuery = dictlistTOdictsetKEY(policylist[23]).copy()
            lastLinkPer = dictlistTOdictsetVALKEY(policylist[24]).copy()
            lastLinkFor = dictlistTOdictsetVALKEY(policylist[25]).copy()
        
            datatypesrec1 = dictlistTOdictsetVAL(policylist[26]).copy()
        
            show_policy_window()
        
    except Exception: 
        pass 
             


def savetextarchitecturefileas(): 
    files = [('Actions Text File', '*.txt')]  
    file = asksaveasfile(mode='w', filetypes = files, defaultextension = files) 
    if file:
        file.write(texteditorcontent + "\n" + relationboxcontent)
        file.close()
    else:       
        return 0


############################################# OPEN AN ARCHITECTURE FILE ########################################
        
def savearchitecturefileas(): 
    files = [('Architecture', '*.arch')] 
    file = asksaveasfile(mode='w', filetypes = files, defaultextension = files) 
    if file:
        archfilelist = [list(Arch), 
                        list(ArchPseudo),
                        list(ArchMeta),
                        list(ArchTime),
                        dictsetTOdictlistVALKEY(cpurposesRecArch),
                        dictsetTOdictlistVALKEY(upurposesRecArch),
                        dictsetTOdictlistVAL(storeArchRec),
                        dictsetTOdictlistVAL(HasAccessTo),
                        dictsetTOdictlistVAL(entityRelationRec),
                        dictsetTOdictlistVALKEY(recvdOwnArgRec),
                        dictsetTOdictlistVALKEY(recvdStoreArgRec),
                        list(map(tostring, SetlistofbasicsLink)),
                        list(map(tostring, SetlistofbasicsHAS)),
                        list(map(objectinfo, all_main_comp)), 
                        list(map(objectinfo, all_sub_comp)),
                        list(map(objectinfo, all_lines)),
                        list(map(textboxinfo, all_textboxes)),
                        nameboxcontent,
                        relationbox, 
                        dictsetTOdictlistVAL(entityRelationListRec)]  
        json.dump(archfilelist, file)
        file.close()
    else: 
        return 0

############################################# OPEN AN ARCHITECTURE FILE (GUI) ########################################        

def open_architecturefile(): 
    global Arch
    global ArchPseudo
    global ArchMeta
    global ArchTime
    global cpurposesRecArch
    global upurposesRecArch
    global storeArchRec
    global HasAccessTo
    global entityRelationRec
    global recvdOwnArgRec
    global recvdStoreArgRec
    global SetlistofbasicsLink 
    global SetlistofbasicsHAS
    global info_list_main
    global info_list_sub
    global info_list_lines
    global info_list_box
    global all_main_comp
    global all_sub_comp 
    global all_lines 
    global all_textboxes
    global nameboxcontent
    global relationbox
    global globalidofbuttontxted
    global globalidoftexteditor
    global globalidoflabeltxted
    global globalidoflabeltxted2
    global entityRelationListRec
    global texteditorcontent
    
    
    try:
        with askopenfile(mode ='r', filetypes =[('Architecture', '*.arch')]) as file :
            canvas.delete("all")  
            all_main_comp  = []
            all_sub_comp = []
            all_lines = []
            all_textboxes = []
            nameboxcontent = {}
            texteditorcontent = ""
            
    
            if globalidofbuttontxted !=-1 and globalidoftexteditor !=-1 and globalidoflabeltxted !=-1 and globalidoflabeltxted2 !=-1: 
                globalidofbuttontxted.destroy()
                globalidoftexteditor.destroy()
                globalidoflabeltxted.destroy()  
                globalidoflabeltxted2.destroy()
                globalidofbuttontxted = -1
                globalidoftexteditor = -1
                globalidoflabeltxted = -1
                globalidoflabeltxted2 = -1
            else:
                pass
            
            archfilelist =  json.load(file)
            Arch = set(archfilelist[0])
            ArchPseudo = set(archfilelist[1])
            ArchMeta = set(archfilelist[2])
            ArchTime = set(archfilelist[3])
            cpurposesRecArch = dictlistTOdictsetVALKEYcuPURP(archfilelist[4]).copy()
            upurposesRecArch = dictlistTOdictsetVALKEYcuPURP(archfilelist[5]).copy()
            storeArchRec = dictlistTOdictsetVAL(archfilelist[6]).copy()
            HasAccessTo = dictlistTOdictsetVAL(archfilelist[7]).copy()
            entityRelationRec = dictlistTOdictsetVAL(archfilelist[8]).copy()
            recvdOwnArgRec  = dictlistTOdictsetVALKEY(archfilelist[9]).copy()
            recvdStoreArgRec = dictlistTOdictsetVALKEY(archfilelist[10]).copy()
            SetlistofbasicsLink = set(map(strtoterm,archfilelist[11]))  
            SetlistofbasicsHAS = set(map(strtoterm,archfilelist[12]))
            info_list_main = archfilelist[13]
            info_list_sub = archfilelist[14]
            info_list_lines = archfilelist[15]
            info_list_box = archfilelist[16]
            nameboxcontent = archfilelist[17]
            relationbox = archfilelist[18]
            entityRelationListRec = dictlistTOdictsetVAL(archfilelist[19])
            
            for info in info_list_main : 
                if len(info[0]) > 0: 
                    create_rectangle(info[0][0], info[0][1], info[0][2], info[0][3], info[1], info[2])
                    
        
            for info in info_list_sub : 
                if len(info[0]) > 0: 
                    nextsub = canvas.create_oval(info[0][0], info[0][1], info[0][2], info[0][3],outline=info[1],fill=info[1], activefill=info[2], tags ="token")
                    all_sub_comp.append(nextsub)
        
            for info in info_list_lines : 
                if len(info[0]) > 0:
                    nextline = canvas.create_line(info[0][0], info[0][1], info[0][2], info[0][3],fill=info[1], activefill=info[2], width=1,arrow=LAST, tags ="token")
                    all_lines.append(nextline)
                
            for info in info_list_box : 
                if len(info[0]) > 0: 
                    create_namebox_open(info[2],info[1],info[0][0],info[0][1])   
            
            updatearchitecture_noframe()
    except Exception: 
        pass   
        

############################################# OPEN AN ARCHITECTURE FILE (text mode) ########################################

def open_textarchitecturefile(): 
    global texteditorcontent

    try:
        with askopenfile(mode ='r', filetypes =[('Actions Text File', '*.txt')]) as file : 
            clear_archpane()
            alllines = file.read() 
            alllinesarray = alllines.split("\n")
            for e in alllinesarray : 
                if len(e) == 0:
                    alllinesarray.remove(e)
            if len(alllinesarray) > 0 :
                for i in range(len(alllinesarray)) : 
                    if alllinesarray[i] == "Relationship:" :
                        j=i
                texteditorcontent = "\n".join(alllinesarray[:j])        
                relation = "\n".join(alllinesarray[j+1:])
                opentexteditorfile()
                save_relation_noframetext(relation)
            else :
                texteditorcontent = alllines
                opentexteditorfile()
    except Exception: 
        pass

    
    
def numberofvar(term) : 
    num = 0
    if len(term.arguments) > 0 : 
        for arg in term.arguments : 
            if isVariable(arg) : 
                if "!" not in str(arg) : 
                    num = num + 1
            else :
                num = num + numberofvar(arg) 
        return num        
    else : 
        return 0



def replacearg(data,argnum,witharg) :  
    strdataargs = list(map(tostring, data.arguments))
    if argnum > 0 : 
        return DataOrFact(str(data.predicate) + "(" + ",".join(strdataargs[:argnum]) + "," + witharg + "," + ",".join(strdataargs[argnum+1:]) + ")")
    else : 
        return DataOrFact(str(data.predicate) + "(" + ",".join(strdataargs[:argnum]) + witharg + "," + ",".join(strdataargs[argnum+1:]) + ")")




def returnBasicEncSet(data,setofkeys) : 
    forreplace = set()
    originalkeyset = setofkeys.copy()
    
    if len(str(data).split("senc(")) == 1 and len(str(data).split("aenc(")) == 1:  
        return forreplace #set()
    else : 
        if len(data.arguments) > 0 : 
            if str(data.predicate) in ["senc","aenc"] : 
                if len(data.arguments[0].arguments) == 0 :
                    forreplace.add((str(data.arguments[0]),str(data.arguments[1]))) 
                    if len(setofkeys) > 0 : 
                        for key in setofkeys : 
                            forreplace.add((str(data.arguments[0]),key))
                    return forreplace
                else : 
                    forreplace.add((str(data.arguments[0]),str(data.arguments[1])))
                    if len(setofkeys) > 0 : 
                        for key in setofkeys : 
                            forreplace.add((str(data.arguments[0]),key))
                    setofkeys.add(str(data.arguments[1]))
                    forreplace = forreplace.union(returnBasicEncSet(data.arguments[0],setofkeys))
                    return forreplace
            else: 
                for i in range(len(data.arguments)) : 
                    setofkeys = originalkeyset.copy()
                    for witharg in returnBasicEncSet(data.arguments[i],setofkeys) : 
                        unlayereddata = replacearg(data,i,witharg[0]) 
                        forreplace.add((str(unlayereddata),witharg[1]))
                        setofkeys.add(witharg[1])
                        forreplace = forreplace.union(returnBasicEncSet(unlayereddata,setofkeys))
                return forreplace

   
    


def addBasicStrEncToRec(entity,data) : 
    global basicEncRec 
    
    for pair in returnBasicEncSet(data,set()) : 
        if str(entity) not in basicEncRec.keys() :  
            basicEncRec[str(entity)] = {}
            basicEncRec[str(entity)][pair[0]] = set()
            basicEncRec[str(entity)][pair[0]].add(pair[1])
        else : 
            if pair[0] not in basicEncRec[str(entity)].keys() :  
                basicEncRec[str(entity)][pair[0]] = set()
                basicEncRec[str(entity)][pair[0]].add(pair[1])
            else:     
                basicEncRec[str(entity)][pair[0]].add(pair[1])
            
            
            
def addBasicStrEncToRecAttEx(data) : 
     global basicEncRecAttEx 
     
     for pair in returnBasicEncSet(data,set()) : 
        if ("att",pair[0]) not in basicEncRecAttEx.keys() : 
            basicEncRecAttEx[("att",pair[0])] = set()
            basicEncRecAttEx[("att",pair[0])].add(pair[1])
        else : 
            basicEncRecAttEx[("att",pair[0])].add(pair[1])
                  

def addBasicStrEncToRecAttIn(data) : 
     global basicEncRecAttIn 
     
     for pair in returnBasicEncSet(data,set()) : 
        if ("att",pair[0]) not in basicEncRecAttIn.keys() : 
            basicEncRecAttIn[("att",pair[0])] = set()
            basicEncRecAttIn[("att",pair[0])].add(pair[1])
        else : 
            basicEncRecAttIn[("att",pair[0])].add(pair[1])


def addBasicStrEncToRecAttHyb(data) : 
     global basicEncRecAttHyb 
     
     for pair in returnBasicEncSet(data,set()) : 
        if ("att",pair[0]) not in basicEncRecAttHyb.keys() : 
            basicEncRecAttHyb[("att",pair[0])] = set()
            basicEncRecAttHyb[("att",pair[0])].add(pair[1])
        else : 
            basicEncRecAttHyb[("att",pair[0])].add(pair[1])            


            
def checkinbasicsEncRecKeys(strentity,strkey) :
    StringsetofbasicsHAS = set()
    
    if len(basicEncRec[strentity]) > 0 and len(basicEncRec[strentity][strkey]) > 0 :
        for strkeyforkey in basicEncRec[strentity][strkey] : 
            if  strkeyforkey not in basicEncRec[strentity].keys() :  
                if  strentity in ReclistofbasicsHAS.keys() and (len(ReclistofbasicsHAS[strentity]) > 0) :
                    StringsetofbasicsHAS = set(map(tostring, ReclistofbasicsHAS[strentity]))
                    strhaskey = "Has(" + strentity + "," + strkeyforkey + ")" 
                    if strhaskey not in StringsetofbasicsHAS :  
                        return 0
                    
            else : 
                if checkinbasicsEncRecKeys(strentity,strkeyforkey) == 0 :
                    return 0
        return 1    
                

def checkinbasicsEncRecKeysAttEx(strkey) : 
    
    StringsetofbasicsHAS = set()
    
    if len(basicEncRecAttEx[("att",strkey)]) > 0 :
        for strkeyforkey in basicEncRecAttEx[("att",strkey)] : 
            if  ("att",strkeyforkey) not in basicEncRecAttEx.keys() :   
                if  "att" in ReclistofbasicsHASAttEx.keys() and (len(ReclistofbasicsHASAttEx["att"]) > 0) :
                    StringsetofbasicsHAS = set(map(tostring, ReclistofbasicsHASAttEx["att"]))
                    strhaskey = "Has(" + "att" + "," + strkeyforkey + ")" 
                    if strhaskey not in StringsetofbasicsHAS : 
                       return 0
            else : 
                if checkinbasicsEncRecKeysAttEx(strkeyforkey)  == 0  : 
                    return 0 
        return 1   
    

def checkinbasicsEncRecKeysAttIn(strkey) : 
    StringSetofbasicsHASATTIN = set()
    
    if len(basicEncRecAttIn[("att",strkey)]) > 0 :
        for strkeyforkey in basicEncRecAttIn[("att",strkey)] : 
            if  ("att",strkeyforkey) not in basicEncRecAttIn.keys() :   
                if  len(SetlistofbasicsHASATTIN) > 0 : 
                    StringSetofbasicsHASATTIN = set(map(tostring, SetlistofbasicsHASATTIN))
                    strhaskey = "Has(" + "att" + "," + strkeyforkey + ")" 
                    if strhaskey not in StringSetofbasicsHASATTIN : 
                       return 0
            else : 
                if checkinbasicsEncRecKeysAttIn(strkeyforkey) == 0  : 
                    return 0
        return 1



def checkinbasicsEncRecKeysAttHyb(strkey) : 
    StringSetofbasicsHASATTHyb = set()
    
    if len(basicEncRecAttHyb[("att",strkey)]) > 0 :
        for strkeyforkey in basicEncRecAttHyb[("att",strkey)] : 
            if  ("att",strkeyforkey) not in basicEncRecAttHyb.keys() :   
                if  len(SetlistofbasicsHASATTHYB) > 0 : 
                    StringSetofbasicsHASATTHyb = set(map(tostring, SetlistofbasicsHASATTHYB))
                    strhaskey = "Has(" + "att" + "," + strkeyforkey + ")" 
                    if strhaskey not in StringSetofbasicsHASATTHyb : 
                       return 0
            else : 
                if checkinbasicsEncRecKeysAttHyb(strkeyforkey) == 0  : 
                    return 0
        return 1



def checkinAccessToEncRecKeys(entaccto,strkey) : 
    if len(basicEncRec[(entaccto,strkey)]) > 0 :
        for strkeyforkey in basicEncRec[(entaccto,strkey)] : 
            if  (entaccto,strkeyforkey) not in basicEncRec.keys() :   
                if  entaccto in ReclistofbasicsHAS.keys() and (len(ReclistofbasicsHAS[entaccto]) > 0) :
                    StringsetofbasicsHAS = set(map(tostring, ReclistofbasicsHAS[entaccto]))
                    strhaskey = "Has(" + entaccto + "," + strkeyforkey + ")" 
                    if strhaskey not in StringsetofbasicsHAS : 
                       return 0
            else : 
                if checkinAccessToEncRecKeys(entaccto,strkeyforkey) == 0 : 
                    return 0    
        return 1    
    




def checkinbasicsEncRec(strentity,strdata,strdataroot,allkeyOK) : 
    if len(basicEncRec[strentity]) > 0 and len(basicEncRec[strentity][strdata]) > 0 :
        for strkey in basicEncRec[strentity][strdata] : 
            if  strkey not in basicEncRec[strentity].keys() :   
              
                if  strentity in ReclistofbasicsHAS.keys() and (len(ReclistofbasicsHAS[strentity]) > 0) : 
                    StringsetofbasicsHAS = set(map(tostring, ReclistofbasicsHAS[strentity]))
                    strhaskey = "Has(" + strentity + "," + strkey + ")" 
                    if strhaskey not in StringsetofbasicsHAS : 
                        allkeyOK = 0 
                        
                        break
                    else : 
                        allkeyOK = 1
                else : 
                    allkeyOK = 0   
                    break                                                
            else : 
                allkeyOK = checkinbasicsEncRecKeys(strentity,strkey)
                if allkeyOK == 0 : 
                    break
               
        if allkeyOK == 1 :         
            hasterm = DataOrFact("Has(" + strentity + "," + strdataroot + ")")
            
            generatebasics(hasterm)            



def checkinbasicsEncRecAttEx(strdata,strdataroot,allkeyOK) : 
    if len(basicEncRecAttEx[("att",strdata)]) > 0 :
        for strkey in basicEncRecAttEx[("att",strdata)] : 
            if  ("att",strkey) not in basicEncRecAttEx.keys() :   
                strhaskey = "Has(" + "att" + "," + strkey + ")" 
                
                if  "att" in ReclistofbasicsHASAttEx.keys() and (len(ReclistofbasicsHASAttEx["att"]) > 0) : 
                    StringsetofbasicsHAS = set(map(tostring, ReclistofbasicsHASAttEx["att"]))
                    
                    if strhaskey not in StringsetofbasicsHAS : 
                        allkeyOK = 0 
                        
                        break
                    else : 
                        allkeyOK = 1
                else :                    
                    allkeyOK = 0   
                    break
            else : 
               allkeyOK = checkinbasicsEncRecKeysAttEx(strkey)
               if allkeyOK == 0 : 
                    break
       
        if allkeyOK == 1 :         
            hasterm = DataOrFact("Has(" + "att" + "," + strdataroot + ")")
            
            generatebasics(hasterm)   



def checkinbasicsEncRecAttIn(strdata,strdataroot,allkeyOK) : 
    global SetlistofbasicsHASATTIN
    
    if len(basicEncRecAttIn[("att",strdata)]) > 0 :
        for strkey in basicEncRecAttIn[("att",strdata)] : 
            if  ("att",strkey) not in basicEncRecAttIn.keys() :   
                strhaskey = "Has(" + "att" + "," + strkey + ")" 
                if  len(SetlistofbasicsHASATTIN) > 0 : 
                    StringSetofbasicsHASATTIN = set(map(tostring, SetlistofbasicsHASATTIN))
                    if strhaskey not in StringSetofbasicsHASATTIN : 
                        allkeyOK = 0 
                        break
                    else : 
                        allkeyOK = 1
                else : 
                    allkeyOK = 0   
                    break
            else : 
               allkeyOK = checkinbasicsEncRecKeysAttIn(strkey)
               if allkeyOK == 0 : 
                    break
                
        if allkeyOK == 1 :         
            hasterm = DataOrFact("Has(" + "att" + "," + strdataroot + ")")
            generatebasicsAttIn(hasterm)  


def checkinbasicsEncRecAttHyb(strdata,strdataroot,allkeyOK) : 
    global SetlistofbasicsHASATTHYB

    if len(basicEncRecAttHyb[("att",strdata)]) > 0 :
        for strkey in basicEncRecAttHyb[("att",strdata)] : 
            if  ("att",strkey) not in basicEncRecAttHyb.keys() :   
                strhaskey = "Has(" + "att" + "," + strkey + ")" 
                if  len(SetlistofbasicsHASATTHYB) > 0 : 
                    StringSetofbasicsHASATTHyb = set(map(tostring, SetlistofbasicsHASATTHYB))
                    if strhaskey not in StringSetofbasicsHASATTHyb : 
                        allkeyOK = 0 
                        break
                    else : 
                        allkeyOK = 1
                else : 
                    allkeyOK = 0   
                    break
            else : 
               allkeyOK = checkinbasicsEncRecKeysAttHyb(strkey)
               if allkeyOK == 0 : 
                    break
                
        if allkeyOK == 1 :         
            hasterm = DataOrFact("Has(" + "att" + "," + strdataroot + ")")
            generatebasicsAttHyb(hasterm)    
            


    
def cleanbasicsEncRec() : 
    global allkeyOK
    allkeyOK = 1
    
    for strentity in basicEncRec :
        for strdata in basicEncRec[strentity].keys() : 
            checkinbasicsEncRec(strentity,strdata,strdata,allkeyOK) 



def cleanbasicsEncRecAttEx() : 
    global allkeyOK
    allkeyOK = 1
    
    for (strentity,strdata) in basicEncRecAttEx.keys() : 
        checkinbasicsEncRecAttEx(strdata,strdata,allkeyOK)             



def cleanbasicsEncRecAttIn() : 
    global allkeyOK
    allkeyOK = 1
    
    for (strentity,strdata) in basicEncRecAttIn.keys() : 
        checkinbasicsEncRecAttIn(strdata,strdata,allkeyOK)  
 
 


def cleanbasicsEncRecAttHyb() : 
    global allkeyOK
    allkeyOK = 1
    
    for (strentity,strdata) in basicEncRecAttHyb.keys() : 
        checkinbasicsEncRecAttHyb(strdata,strdata,allkeyOK)  
                       
        
                    
def generatebasicsEnc(archterm) : 
    
    if len(str(archterm).split("senc(")) > 1 or len(str(archterm).split("aenc(")) > 1 :  
        addBasicStrEncToRec(archterm.arguments[0],archterm.arguments[1])


def generatebasicsEncAttEx(archterm) : 
    
    if str(archterm.predicate) in ["receive", "receiveat"] : 
        if len(str(archterm).split("senc(")) > 1 or len(str(archterm).split("aenc(")) > 1 : 
            addBasicStrEncToRecAttEx(archterm.arguments[1])
    else : 
        if str(archterm.arguments[0]) == "att" : 
            addBasicStrEncToRecAttEx(archterm.arguments[1])

            
def generatebasicsEncAttIn(archterm)  :
    if len(str(archterm).split("senc(")) > 1 or len(str(archterm).split("aenc(")) > 1 :   
        addBasicStrEncToRecAttIn(archterm.arguments[1])              

            
def generatebasicsEncAttHyb(archterm)  :
    if len(str(archterm).split("senc(")) > 1 or len(str(archterm).split("aenc(")) > 1 :  
        addBasicStrEncToRecAttHyb(archterm.arguments[1])  



def cleanSetbasicHas() : 
    global SetlistofbasicsHAS
    CopiedSetbasicHAS = SetlistofbasicsHAS.copy()
    
    for hasterm in CopiedSetbasicHAS : 
        if len(hasterm.arguments[1].arguments) > 0 : 
            for arg in hasterm.arguments[1].arguments : 
                if str(arg) == str(hasterm.arguments[1].predicate) : 
                    SetlistofbasicsHAS.remove(hasterm)
    return SetlistofbasicsHAS



def cleanSetbasicHasATTEX() : 
    global SetlistofbasicsHASATTEX
    CopiedSetbasicHAS = SetlistofbasicsHASATTEX.copy()
    
    for hasterm in CopiedSetbasicHAS : 
        if len(hasterm.arguments[1].arguments) > 0 : 
            for arg in hasterm.arguments[1].arguments : 
                if str(arg) == str(hasterm.arguments[1].predicate) : 
                    SetlistofbasicsHASATTEX.remove(hasterm)
    return SetlistofbasicsHASATTEX



def cleanSetbasicHasATTIN() : 
    global SetlistofbasicsHASATTIN
    CopiedSetbasicHAS = SetlistofbasicsHASATTIN.copy()
    
    for hasterm in CopiedSetbasicHAS : 
        if len(hasterm.arguments[1].arguments) > 0 : 
            for arg in hasterm.arguments[1].arguments : 
                if str(arg) == str(hasterm.arguments[1].predicate) : 
                    SetlistofbasicsHASATTIN.remove(hasterm)
    return SetlistofbasicsHASATTIN



def cleanSetbasicHasATTHyb() : 
    global SetlistofbasicsHASATTHYB
    CopiedSetbasicHAS = SetlistofbasicsHASATTHYB.copy()
    
    for hasterm in CopiedSetbasicHAS : 
        if len(hasterm.arguments[1].arguments) > 0 : 
            for arg in hasterm.arguments[1].arguments : 
                if str(arg) == str(hasterm.arguments[1].predicate) : 
                    SetlistofbasicsHASATTHYB.remove(hasterm)
    return SetlistofbasicsHASATTHYB




def addtoArchRec(archterm) : 
    global Recofactions 
    
    if str(archterm.arguments[0]) not in Recofactions.keys() :  
        Recofactions[str(archterm.arguments[0])] = set() 
        Recofactions[str(archterm.arguments[0])].add(archterm)
    else : 
        Recofactions[str(archterm.arguments[0])].add(archterm)



def generatebasicsAttIn(archterm) : 
    global SetlistofbasicsHASATTIN     
    global SetlistofbasicsLinkATTIN    
    global SetlistofbasicsLinkATTINUnique
    
    argpredsetattin = []
    
    if len(str(archterm).split("time(")) == 2 : 
        strarchtermargs = list(map(tostring, archterm.arguments[:-1])) 
    elif len(str(archterm).split("time(")) == 1 :     
        strarchtermargs = list(map(tostring, archterm.arguments))
    
    if (str(archterm.predicate) in ["receive","own","create","calculate", "calculatefrom", "store", "storeat", "createat", "calculateat", "calculatefromat"]) :   #wE ONLY NEED TO INCLUDE RECEIVE/OWN due to the well-formedness property there must be at least 1 receive/own.
        strarchtermargsattin =  strarchtermargs[1:]
        basicquerytermattin = DataOrFact("Has(" + "att," + ",".join(strarchtermargsattin) + ")")  
        SetlistofbasicsHASATTIN.add(basicquerytermattin)
            
        for arg in archterm.arguments[1:]:
             if (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                 basicqueryterm2attin = DataOrFact("Has(" + "att" + "," + str(arg.predicate) + ")")
                 SetlistofbasicsHASATTIN.add(basicqueryterm2attin) 
                 addtoHasAttIn(basicqueryterm2attin.arguments[0],arg)
                 addtoLink(arg,argpredsetattin) 
        
        permutedpairs=set(itertools.permutations(argpredsetattin, 2))  
        for pair in permutedpairs : 
                 
            basicSubHasattin = DataOrFact("Has(" + "att" + "," + str(archterm.arguments[1].predicate) + "(" + pair[0] + "," + pair[1] + ")" + ")")
            SetlistofbasicsHASATTIN.add(basicSubHasattin)
             
            
            basicquerytermLinkAttIn = DataOrFact("Link(" + "att" + "," + pair[0] + "," + pair[1] + ")")
            SetlistofbasicsLinkATTIN.add(basicquerytermLinkAttIn)
            basicquerytermLinkUniqueAttIn = DataOrFact("LinkUnique(" + "att" + "," + pair[0] + "," + pair[1] + ")")
            SetlistofbasicsLinkATTINUnique.add(basicquerytermLinkUniqueAttIn)
        
    elif str(archterm.predicate) in ["receiveat", "Has"] : 
        if str(archterm.arguments[1].predicate) not in ["cconsent","uconsent","sconsent","fwconsent"] : 
            strarchtermargsattin =  strarchtermargs[1:]
            basicquerytermattin = DataOrFact("Has(" + "att," + ",".join(strarchtermargsattin) + ")")  
            SetlistofbasicsHASATTIN.add(basicquerytermattin)
            
            for arg in archterm.arguments[1:]:
                 if (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                     basicqueryterm2attin = DataOrFact("Has(" + "att" + "," + str(arg.predicate) + ")")
                     SetlistofbasicsHASATTIN.add(basicqueryterm2attin) 
                     addtoHasAttIn(basicqueryterm2attin.arguments[0],arg)
                     addtoLink(arg,argpredsetattin) 
            
            permutedpairs=set(itertools.permutations(argpredsetattin, 2))  
            for pair in permutedpairs : 
                     
                basicSubHasattin = DataOrFact("Has(" + "att" + "," + str(archterm.arguments[1].predicate) + "(" + pair[0] + "," + pair[1] + ")" + ")")
                SetlistofbasicsHASATTIN.add(basicSubHasattin)
                 
                
                basicquerytermLinkAttIn = DataOrFact("Link(" + "att" + "," + pair[0] + "," + pair[1] + ")")
                SetlistofbasicsLinkATTIN.add(basicquerytermLinkAttIn)
                basicquerytermLinkUniqueAttIn = DataOrFact("LinkUnique(" + "att" + "," + pair[0] + "," + pair[1] + ")")
                SetlistofbasicsLinkATTINUnique.add(basicquerytermLinkUniqueAttIn)
     

        

def generatebasicsAttHyb(archterm) : 
    global SetlistofbasicsHASATTHYB     
    global SetlistofbasicsLinkATTHYB    
    global SetlistofbasicsLinkATTHYBUnique 
    
    argpredsetatthyb = [] 
    
    strarchtermargs = list(map(tostring, archterm.arguments))
    strarchtermargsatthyb =  strarchtermargs[1:]
       
    basicquerytermatthyb = DataOrFact("Has(" + "att," + ",".join(strarchtermargsatthyb) + ")")  
    SetlistofbasicsHASATTHYB.add(basicquerytermatthyb)
   
    
    for arg in archterm.arguments[1:]:
        if (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
            basicqueryterm2atthyb = DataOrFact("Has(" + "att" + "," + str(arg.predicate) + ")")
            SetlistofbasicsHASATTHYB.add(basicqueryterm2atthyb) 
            addtoHasAttHyb(basicqueryterm2atthyb.arguments[0],arg)
            addtoLink(arg,argpredsetatthyb) 
    
            
    permutedpairs=set(itertools.permutations(argpredsetatthyb, 2))  
    
    for pair in permutedpairs : 
                 
            basicSubHasatthyb = DataOrFact("Has(" + "att" + "," + str(archterm.arguments[1].predicate) + "(" + pair[0] + "," + pair[1] + ")" + ")")
            SetlistofbasicsHASATTHYB.add(basicSubHasatthyb)
             
            
            basicquerytermLinkAttHyb = DataOrFact("Link(" + "att" + "," + pair[0] + "," + pair[1] + ")")
            SetlistofbasicsLinkATTHYB.add(basicquerytermLinkAttHyb)
            basicquerytermLinkUniqueAttHyb = DataOrFact("LinkUnique(" + "att" + "," + pair[0] + "," + pair[1] + ")")
            SetlistofbasicsLinkATTHYBUnique.add(basicquerytermLinkUniqueAttHyb)
   
    
    

    
    
def generatebasics(archterm): 
    
    global ReclistofbasicsHAS
    global ReclistofbasicsLink
    global ReclistofbasicsLinkUnique
   
    global ReclistofbasicsHASAttEx
    global ReclistofbasicsLinkAttEx
    global ReclistofbasicsLinkAttExUnique
    
    argpredset = []
    argpredsetattex =[] 
     
   
    if len(str(archterm).split("time(")) == 2 : 
        strarchtermargs = list(map(tostring, archterm.arguments[:-1])) 
    elif len(str(archterm).split("time(")) == 1 :     
        strarchtermargs = list(map(tostring, archterm.arguments))
        
    if (str(archterm.predicate) in ["receive","own","create","calculate", "calculatefrom", "store", "storeat", "createat", "calculateat", "calculatefromat"]) :   #wE ONLY NEED TO INCLUDE RECEIVE/OWN due to the well-formedness property there must be at least 1 receive/own.
        basicqueryterm = DataOrFact("Has(" + ",".join(strarchtermargs) + ")")  
        
        if str(archterm.arguments[0]) not in ReclistofbasicsHAS.keys() :  
            ReclistofbasicsHAS[str(archterm.arguments[0])] = set() 
            ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicqueryterm)
        else : 
            ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicqueryterm)
        
            
        for arg in archterm.arguments[1:]:
             if (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                 basicqueryterm2 = DataOrFact("Has(" + str(archterm.arguments[0]) + "," + str(arg.predicate) + ")")
                 
                 if str(archterm.arguments[0]) not in ReclistofbasicsHAS.keys() :  
                     ReclistofbasicsHAS[str(archterm.arguments[0])] = set() 
                     ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicqueryterm2)
                 else : 
                     ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicqueryterm2)
                 
                 
                 addtoHas(archterm.arguments[0],arg)
                 addtoLink(arg,argpredset)   
                 
    
        permutedpairs=set(itertools.permutations(argpredset, 2))
        
        
        for pair in permutedpairs : 
                     
                basicquerytermSubHas = DataOrFact("Has(" + str(archterm.arguments[0]) + "," + str(archterm.arguments[1].predicate) + "(" + pair[0] + "," + pair[1] + ")" + ")")
                
                if str(archterm.arguments[0]) not in ReclistofbasicsHAS.keys() :  
                     ReclistofbasicsHAS[str(archterm.arguments[0])] = set() 
                     ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicquerytermSubHas)
                else : 
                     ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicquerytermSubHas)
                
                
                
                basicquerytermLink = DataOrFact("Link(" + str(archterm.arguments[0]) + "," + pair[0] + "," + pair[1] + ")")
                
                if str(archterm.arguments[0]) not in ReclistofbasicsLink.keys() :  
                    ReclistofbasicsLink[str(archterm.arguments[0])] = set() 
                    ReclistofbasicsLink[str(archterm.arguments[0])].add(basicquerytermLink)
                else : 
                    ReclistofbasicsLink[str(archterm.arguments[0])].add(basicquerytermLink)
                    
                
                basicquerytermLinkUnique = DataOrFact("LinkUnique(" + str(archterm.arguments[0]) + "," + pair[0] + "," + pair[1] + ")")
                
                if str(archterm.arguments[0]) not in ReclistofbasicsLinkUnique.keys() :  
                    ReclistofbasicsLinkUnique[str(archterm.arguments[0])] = set() 
                    ReclistofbasicsLinkUnique[str(archterm.arguments[0])].add(basicquerytermLinkUnique)
                else : 
                    ReclistofbasicsLinkUnique[str(archterm.arguments[0])].add(basicquerytermLinkUnique)
        
        
        if str(archterm.predicate) == "receive" :  
            strarchtermargsattex =  strarchtermargs[1:]
            basicquerytermattex = DataOrFact("Has(" + "att," + ",".join(strarchtermargsattex) + ")")  
            
            if "att" not in ReclistofbasicsHASAttEx.keys() :  
                ReclistofbasicsHASAttEx["att"] = set() 
                ReclistofbasicsHASAttEx["att"].add(basicquerytermattex)
            else : 
                ReclistofbasicsHASAttEx["att"].add(basicquerytermattex)
    
            for arg in archterm.arguments[1:]:
                 if (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                     basicqueryterm2attex = DataOrFact("Has(" + "att" + "," + str(arg.predicate) + ")")
                     if  "att" not in ReclistofbasicsHASAttEx.keys() : 
                         ReclistofbasicsHASAttEx["att"] = set() 
                         ReclistofbasicsHASAttEx["att"].add(basicqueryterm2attex)
                        
                     else : 
                         ReclistofbasicsHASAttEx["att"].add(basicqueryterm2attex)
                         
                     addtoHasAttEx(basicqueryterm2attex.arguments[0],arg)
                     addtoLink(arg,argpredsetattex) 
                     
            permutedpairs=set(itertools.permutations(argpredsetattex, 2))  
            
            for pair in permutedpairs : 
                     
                basicSubHasattex = DataOrFact("Has(" + "att" + "," + str(archterm.arguments[1].predicate) + "(" + pair[0] + "," + pair[1] + ")" + ")")
                
                if "att" not in ReclistofbasicsHASAttEx.keys() :  
                    ReclistofbasicsHASAttEx["att"] = set() 
                    ReclistofbasicsHASAttEx["att"].add(basicSubHasattex)
                else : 
                    ReclistofbasicsHASAttEx["att"].add(basicSubHasattex)
                
                 
                
                basicquerytermLinkAttEx = DataOrFact("Link(" + "att" + "," + pair[0] + "," + pair[1] + ")")
                
                if "att" not in ReclistofbasicsLinkAttEx.keys() :  
                    ReclistofbasicsLinkAttEx["att"] = set() 
                    ReclistofbasicsLinkAttEx["att"].add(basicquerytermLinkAttEx)  
                else : 
                    ReclistofbasicsLinkAttEx["att"].add(basicquerytermLinkAttEx)
                             
                basicquerytermLinkUniqueAttEx = DataOrFact("LinkUnique(" + "att" + "," + pair[0] + "," + pair[1] + ")")    
                
                if "att" not in ReclistofbasicsLinkAttExUnique.keys() :  
                    ReclistofbasicsLinkAttExUnique["att"] = set() 
                    ReclistofbasicsLinkAttExUnique["att"].add(basicquerytermLinkUniqueAttEx)
                else : 
                    ReclistofbasicsLinkAttExUnique["att"].add(basicquerytermLinkUniqueAttEx)
    
        
        elif (str(archterm.predicate) in ["own","create","calculate", "calculatefrom", "store", "storeat", "createat", "calculateat", "calculatefromat"]) and (str(archterm.arguments[0]) == "att") :  
            
            strarchtermargsattex =  strarchtermargs[1:]
            basicquerytermattex = DataOrFact("Has(" + "att," + ",".join(strarchtermargsattex) + ")")  
            
            if "att" not in ReclistofbasicsHASAttEx.keys() :  
                ReclistofbasicsHASAttEx["att"] = set() 
                ReclistofbasicsHASAttEx["att"].add(basicquerytermattex)
            else : 
                ReclistofbasicsHASAttEx["att"].add(basicquerytermattex)
    
            for arg in archterm.arguments[1:]:
                 if (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                     basicqueryterm2attex = DataOrFact("Has(" + "att" + "," + str(arg.predicate) + ")")
                     if  "att" not in ReclistofbasicsHASAttEx.keys() : 
                         ReclistofbasicsHASAttEx["att"] = set() 
                         ReclistofbasicsHASAttEx["att"].add(basicqueryterm2attex)
                        
                     else : 
                         ReclistofbasicsHASAttEx["att"].add(basicqueryterm2attex)
                         
                     addtoHasAttEx(basicqueryterm2attex.arguments[0],arg)
                     addtoLink(arg,argpredsetattex) 
                     
            permutedpairs=set(itertools.permutations(argpredsetattex, 2))  
            
            for pair in permutedpairs : 
                     
                basicSubHasattex = DataOrFact("Has(" + "att" + "," + str(archterm.arguments[1].predicate) + "(" + pair[0] + "," + pair[1] + ")" + ")")
                
                if "att" not in ReclistofbasicsHASAttEx.keys() :  
                    ReclistofbasicsHASAttEx["att"] = set() 
                    ReclistofbasicsHASAttEx["att"].add(basicSubHasattex)
                else : 
                    ReclistofbasicsHASAttEx["att"].add(basicSubHasattex)
                
                
                
                basicquerytermLinkAttEx = DataOrFact("Link(" + "att" + "," + pair[0] + "," + pair[1] + ")")
                
                if "att" not in ReclistofbasicsLinkAttEx.keys() :  
                    ReclistofbasicsLinkAttEx["att"] = set() 
                    ReclistofbasicsLinkAttEx["att"].add(basicquerytermLinkAttEx)
                else : 
                    ReclistofbasicsLinkAttEx["att"].add(basicquerytermLinkAttEx)
                  
                basicquerytermLinkUniqueAttEx = DataOrFact("LinkUnique(" + "att" + "," + pair[0] + "," + pair[1] + ")")  
                
                if "att" not in ReclistofbasicsLinkAttExUnique.keys() :  
                    ReclistofbasicsLinkAttExUnique["att"] = set() 
                    ReclistofbasicsLinkAttExUnique["att"].add(basicquerytermLinkUniqueAttEx)
                else : 
                    ReclistofbasicsLinkAttExUnique["att"].add(basicquerytermLinkUniqueAttEx)
          
        
        
    
    elif str(archterm.predicate) == "receiveat" : 
        if str(archterm.arguments[1].predicate) not in ["cconsent","uconsent","sconsent","fwconsent"] :  
             basicqueryterm = DataOrFact("Has(" + ",".join(strarchtermargs) + ")") 
             
             if str(archterm.arguments[0]) not in ReclistofbasicsHAS.keys() :  
                 ReclistofbasicsHAS[str(archterm.arguments[0])] = set() 
                 ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicqueryterm)
             else : 
                 ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicqueryterm)
             
             for arg in archterm.arguments[1:]:
                 if (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                     basicqueryterm2 = DataOrFact("Has(" + str(archterm.arguments[0]) + "," + str(arg.predicate) + ")")  
                     
                     if str(archterm.arguments[0]) not in ReclistofbasicsHAS.keys() :  
                         ReclistofbasicsHAS[str(archterm.arguments[0])] = set() 
                         ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicqueryterm2)
                     else : 
                         ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicqueryterm2)
                         
                     addtoHas(archterm.arguments[0],arg)
                     addtoLink(arg,argpredset) 
                     
        
             permutedpairs=set(itertools.permutations(argpredset, 2))  
            
             for pair in permutedpairs : 
                      
                 basicquerytermSubHas = DataOrFact("Has(" + str(archterm.arguments[0]) + "," + str(archterm.arguments[1].predicate) + "(" + pair[0] + "," + pair[1] + ")" + ")")
                 
                 if str(archterm.arguments[0]) not in ReclistofbasicsHAS.keys() :  
                     ReclistofbasicsHAS[str(archterm.arguments[0])] = set() 
                     ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicquerytermSubHas)
                 else : 
                     ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicquerytermSubHas)
                 
                
                 
                 basicquerytermLink = DataOrFact("Link(" + str(archterm.arguments[0]) + "," + pair[0] + "," + pair[1] + ")")
                 
                 if str(archterm.arguments[0]) not in ReclistofbasicsLink.keys() :  
                     ReclistofbasicsLink[str(archterm.arguments[0])] = set() 
                     ReclistofbasicsLink[str(archterm.arguments[0])].add(basicquerytermLink)
                 else : 
                     ReclistofbasicsLink[str(archterm.arguments[0])].add(basicquerytermLink)
                     
                 basicquerytermLinkUnique = DataOrFact("LinkUnique(" + str(archterm.arguments[0]) + "," + pair[0] + "," + pair[1] + ")")    
                 
                 if str(archterm.arguments[0]) not in ReclistofbasicsLinkUnique.keys() :  
                     ReclistofbasicsLinkUnique[str(archterm.arguments[0])] = set() 
                     ReclistofbasicsLinkUnique[str(archterm.arguments[0])].add(basicquerytermLinkUnique)
                 else : 
                     ReclistofbasicsLinkUnique[str(archterm.arguments[0])].add(basicquerytermLinkUnique)
  
            
             strarchtermargsattex =  strarchtermargs[1:]
             basicquerytermattex = DataOrFact("Has(" + "att," + ",".join(strarchtermargsattex) + ")")  
            
             if "att" not in ReclistofbasicsHASAttEx.keys() :  
                 ReclistofbasicsHASAttEx["att"] = set() 
                 ReclistofbasicsHASAttEx["att"].add(basicquerytermattex)
             else : 
                 ReclistofbasicsHASAttEx["att"].add(basicquerytermattex)
    
             for arg in archterm.arguments[1:]:
                 if (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                     basicqueryterm2attex = DataOrFact("Has(" + "att" + "," + str(arg.predicate) + ")")
                     if  "att" not in ReclistofbasicsHASAttEx.keys() : 
                         ReclistofbasicsHASAttEx["att"] = set() 
                         ReclistofbasicsHASAttEx["att"].add(basicqueryterm2attex)
                     else : 
                         ReclistofbasicsHASAttEx["att"].add(basicqueryterm2attex)
                     addtoHasAttEx(basicqueryterm2attex.arguments[0],arg)
                     addtoLink(arg,argpredsetattex) 
                     
             permutedpairs=set(itertools.permutations(argpredsetattex, 2))  
            
             for pair in permutedpairs : 
                    
                 basicSubHasattex = DataOrFact("Has(" + "att" + "," + str(archterm.arguments[1].predicate) + "(" + pair[0] + "," + pair[1] + ")" + ")")
                
                 if "att" not in ReclistofbasicsHASAttEx.keys() :  
                     ReclistofbasicsHASAttEx["att"] = set() 
                     ReclistofbasicsHASAttEx["att"].add(basicSubHasattex)
                 else : 
                     ReclistofbasicsHASAttEx["att"].add(basicSubHasattex)
                
                
                 basicquerytermLinkAttEx = DataOrFact("Link(" + "att" + "," + pair[0] + "," + pair[1] + ")")
                
                 if "att" not in ReclistofbasicsLinkAttEx.keys() :  
                     ReclistofbasicsLinkAttEx["att"] = set() 
                     ReclistofbasicsLinkAttEx["att"].add(basicquerytermLinkAttEx)
                 else : 
                     ReclistofbasicsLinkAttEx["att"].add(basicquerytermLinkAttEx)
                     
                 basicquerytermLinkUniqueAttEx = DataOrFact("LinkUnique(" + "att" + "," + pair[0] + "," + pair[1] + ")")
                 
                 if "att" not in ReclistofbasicsLinkAttExUnique.keys() :  
                    ReclistofbasicsLinkAttExUnique["att"] = set() 
                    ReclistofbasicsLinkAttExUnique["att"].add(basicquerytermLinkUniqueAttEx)
                 else : 
                    ReclistofbasicsLinkAttExUnique["att"].add(basicquerytermLinkUniqueAttEx)
             
               
                  
    
    elif str(archterm.predicate) == "Has" and str(archterm.arguments[0]) != "att" : 
         
        if str(archterm.arguments[1].predicate) not in ["cconsent","uconsent","sconsent","fwconsent"] :  
             basicqueryterm = DataOrFact("Has(" + ",".join(strarchtermargs) + ")")  
             
             if str(archterm.arguments[0]) not in ReclistofbasicsHAS.keys() :  
                 ReclistofbasicsHAS[str(archterm.arguments[0])] = set() 
                 ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicqueryterm)
             else : 
                 ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicqueryterm)
             
             
             for arg in archterm.arguments[1:]:
                 if (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["meta","p"]) : 
                     basicqueryterm2 = DataOrFact("Has(" + str(archterm.arguments[0]) + "," + str(arg.predicate) + ")")  
                     
                     if str(archterm.arguments[0]) not in ReclistofbasicsHAS.keys() :  
                         ReclistofbasicsHAS[str(archterm.arguments[0])] = set() 
                         ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicqueryterm2)
                     else : 
                         ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicqueryterm2) 
                     
                     addtoHas(archterm.arguments[0],arg)
                     addtoLink(arg,argpredset) 
                     
        
             permutedpairs=set(itertools.permutations(argpredset, 2))  
            
             for pair in permutedpairs : 
                   
                 basicquerytermSubHas = DataOrFact("Has(" + str(archterm.arguments[0]) + "," + str(archterm.arguments[1].predicate) + "(" + pair[0] + "," + pair[1] + ")" + ")")
                 
                 if str(archterm.arguments[0]) not in ReclistofbasicsHAS.keys() :  
                     ReclistofbasicsHAS[str(archterm.arguments[0])] = set() 
                     ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicquerytermSubHas)
                 else : 
                     ReclistofbasicsHAS[str(archterm.arguments[0])].add(basicquerytermSubHas)
                 
                 
                 basicquerytermLink = DataOrFact("Link(" + str(archterm.arguments[0]) + "," + pair[0] + "," + pair[1] + ")")
                  
                 if str(archterm.arguments[0]) not in ReclistofbasicsLink.keys() :  
                    ReclistofbasicsLink[str(archterm.arguments[0])] = set() 
                    ReclistofbasicsLink[str(archterm.arguments[0])].add(basicquerytermLink)
                 else : 
                    ReclistofbasicsLink[str(archterm.arguments[0])].add(basicquerytermLink)
                
                 basicquerytermLinkUnique = DataOrFact("LinkUnique(" + str(archterm.arguments[0]) + "," + pair[0] + "," + pair[1] + ")")
                    
                 if str(archterm.arguments[0]) not in ReclistofbasicsLinkUnique.keys() :  
                     ReclistofbasicsLinkUnique[str(archterm.arguments[0])] = set() 
                     ReclistofbasicsLinkUnique[str(archterm.arguments[0])].add(basicquerytermLinkUnique)
                 else : 
                     ReclistofbasicsLinkUnique[str(archterm.arguments[0])].add(basicquerytermLinkUnique)
             
      
    elif str(archterm.predicate) == "Has" and str(archterm.arguments[0]) == "att" : 
        strarchtermargsattex =  strarchtermargs[1:]
        basicquerytermattex = DataOrFact("Has(" + "att," + ",".join(strarchtermargsattex) + ")")  
       
        if "att" not in ReclistofbasicsHASAttEx.keys() :  
            ReclistofbasicsHASAttEx["att"] = set() 
            ReclistofbasicsHASAttEx["att"].add(basicquerytermattex)
        else : 
            ReclistofbasicsHASAttEx["att"].add(basicquerytermattex)
   
        for arg in archterm.arguments[1:]:
            if (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                basicqueryterm2attex = DataOrFact("Has(" + "att" + "," + str(arg.predicate) + ")")
                if  "att" not in ReclistofbasicsHASAttEx.keys() : 
                    ReclistofbasicsHASAttEx["att"] = set() 
                    ReclistofbasicsHASAttEx["att"].add(basicqueryterm2attex)
                else : 
                    ReclistofbasicsHASAttEx["att"].add(basicqueryterm2attex)
                
                addtoHasAttEx(basicqueryterm2attex.arguments[0],arg)
                addtoLink(arg,argpredsetattex) 
                
        permutedpairs=set(itertools.permutations(argpredsetattex, 2))  
       
        for pair in permutedpairs : 
               
            basicSubHasattex = DataOrFact("Has(" + "att" + "," + str(archterm.arguments[1].predicate) + "(" + pair[0] + "," + pair[1] + ")" + ")")
           
            if "att" not in ReclistofbasicsHASAttEx.keys() :  
                ReclistofbasicsHASAttEx["att"] = set() 
                ReclistofbasicsHASAttEx["att"].add(basicSubHasattex)
            else : 
                ReclistofbasicsHASAttEx["att"].add(basicSubHasattex)
           
           
            basicquerytermLinkAttEx = DataOrFact("Link(" + "att" + "," + pair[0] + "," + pair[1] + ")")
           
            if "att" not in ReclistofbasicsLinkAttEx.keys() :  
                ReclistofbasicsLinkAttEx["att"] = set() 
                ReclistofbasicsLinkAttEx["att"].add(basicquerytermLinkAttEx)
            else : 
                ReclistofbasicsLinkAttEx["att"].add(basicquerytermLinkAttEx)
                
       
            basicquerytermLinkUniqueAttEx = DataOrFact("LinkUnique(" + "att" + "," + pair[0] + "," + pair[1] + ")")
                 
            if "att" not in ReclistofbasicsLinkAttExUnique.keys() :  
               ReclistofbasicsLinkAttExUnique["att"] = set() 
               ReclistofbasicsLinkAttExUnique["att"].add(basicquerytermLinkUniqueAttEx)
            else : 
               ReclistofbasicsLinkAttExUnique["att"].add(basicquerytermLinkUniqueAttEx) 
                



def generatenewlinkbasics(hasterm): 
     global SetlistofnewLink
     
     argpredset = []
     CopySetlistofnewLink = set()
    
     for arg in hasterm.arguments[1:]: 
             if (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                 
                 addtoLink(arg,argpredset) 
     
     permutedpairs=set(itertools.permutations(argpredset, 2))  
     for pair in permutedpairs :
                basicquerytermLink = DataOrFact("Link(" + str(hasterm.arguments[0]) + "," + pair[0] + "," + pair[1] + ")")
                SetlistofnewLink.add(basicquerytermLink) 
                basicquerytermLinkUnique = DataOrFact("LinkUnique(" + str(hasterm.arguments[0]) + "," + pair[0] + "," + pair[1] + ")")
                SetlistofnewLink.add(basicquerytermLinkUnique) 
     
     CopySetlistofnewLink = SetlistofnewLink.copy()      
     for basiclinkterm in CopySetlistofnewLink : 
        if (str(basiclinkterm.arguments[0]) in entityRelationRec) and  len(entityRelationRec[str(basiclinkterm.arguments[0])]) > 0 : 
            for ent in entityRelationRec[str(basiclinkterm.arguments[0])] : 
                parentquerylinkterm = replaceentity(basiclinkterm, ent)
                SetlistofnewLink.add(parentquerylinkterm)               
     
                     
                
        
def addtoNewHas(entity,data) :  
    global SetlistofnewHAS
    
    if len(data.arguments) > 0 and (str(data.predicate) not in CryptoPred) and (str(data.predicate) not in ["time","meta","p"])  : 
        for arg in data.arguments : 
            if str(arg.predicate) not in ["time","meta"] :  
                t1 = DataOrFact("Has(" + str(entity) + "," + str(arg) + ")")  
                SetlistofnewHAS.add(t1)
                if len(arg.arguments) > 0 and (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                    t2 = DataOrFact("Has(" + str(entity) + "," + str(arg.predicate) + ")")  
                    SetlistofnewHAS.add(t2)
                    if len(arg.arguments) > 1 : 
                        for arg2 in arg.arguments : 
                            if (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                                t4 = DataOrFact("Has(" + str(entity) + "," + str(arg.predicate) + "(" + str(arg2) + ")" + ")")  
                                SetlistofnewHAS.add(t4)
            addtoNewHas(entity,arg)       



def addtoHasAttEx(entity,data) : 
    global ReclistofbasicsHASAttEx
    
    if len(data.arguments) > 0 and (str(data.predicate) not in CryptoPred) and (str(data.predicate) not in ["time","meta","p"])  : 
        for arg in data.arguments :
            if str(arg.predicate) not in ["time","meta"] :  
                t1 = DataOrFact("Has(" + "att" + "," + str(arg) + ")")  
                
                if  "att" not in ReclistofbasicsHASAttEx.keys() : 
                    ReclistofbasicsHASAttEx[str(entity)] = set() 
                    ReclistofbasicsHASAttEx[str(entity)].add(t1)
                else : 
                    ReclistofbasicsHASAttEx[str(entity)].add(t1)
                
                if len(arg.arguments) > 0 and (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                    t2 = DataOrFact("Has(" + "att" + "," + str(arg.predicate) + ")")  
                    
                    if  "att" not in ReclistofbasicsHASAttEx.keys() : 
                        ReclistofbasicsHASAttEx[str(entity)] = set() 
                        ReclistofbasicsHASAttEx[str(entity)].add(t2)
                    else : 
                        ReclistofbasicsHASAttEx[str(entity)].add(t2)
                    
                    if len(arg.arguments) > 1 : 
                        for arg2 in arg.arguments : 
                            if (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                                t4 = DataOrFact("Has(" + "att" + "," + str(arg.predicate) + "(" + str(arg2) + ")" + ")")         
                                if  "att" not in ReclistofbasicsHASAttEx.keys() : 
                                     ReclistofbasicsHASAttEx[str(entity)] = set() 
                                     ReclistofbasicsHASAttEx[str(entity)].add(t4)
                                else : 
                                    ReclistofbasicsHASAttEx[str(entity)].add(t4)
            addtoHasAttEx(entity,arg)                    
    

def addtoHasAttIn(entity,data) : 
    global SetlistofbasicsHASATTIN
    
    if len(data.arguments) > 0 and (str(data.predicate) not in CryptoPred) and (str(data.predicate) not in ["time","meta","p"])  : 
        for arg in data.arguments :
            if str(arg.predicate) not in ["time","meta"] :  
                t1 = DataOrFact("Has(" + "att" + "," + str(arg) + ")")  
                SetlistofbasicsHASATTIN.add(t1)
                if len(arg.arguments) > 0 and (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                    t2 = DataOrFact("Has(" + "att" + "," + str(arg.predicate) + ")")  
                    SetlistofbasicsHASATTIN.add(t2)
                    if len(arg.arguments) > 1 : 
                        for arg2 in arg.arguments : 
                            if (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                                t4 = DataOrFact("Has(" + "att" + "," + str(arg.predicate) + "(" + str(arg2) + ")" + ")")  
                                SetlistofbasicsHASATTIN.add(t4)
            addtoHasAttIn(entity,arg) 
            


def addtoHasAttHyb(entity,data) : 
    global SetlistofbasicsHASATTHYB
    
    if len(data.arguments) > 0 and (str(data.predicate) not in CryptoPred) and (str(data.predicate) not in ["time","meta","p"])  : 
        for arg in data.arguments :
            if str(arg.predicate) not in ["time","meta"] :  
                t1 = DataOrFact("Has(" + "att" + "," + str(arg) + ")")  
                SetlistofbasicsHASATTHYB.add(t1)
                if len(arg.arguments) > 0 and (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                    t2 = DataOrFact("Has(" + "att" + "," + str(arg.predicate) + ")")  
                    SetlistofbasicsHASATTHYB.add(t2)
                    if len(arg.arguments) > 1 : 
                        for arg2 in arg.arguments : 
                            if (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                                t4 = DataOrFact("Has(" + "att" + "," + str(arg.predicate) + "(" + str(arg2) + ")" + ")")  
                                SetlistofbasicsHASATTHYB.add(t4)
            addtoHasAttHyb(entity,arg) 
    

    
def addtoHas(entity,data) :  
    global ReclistofbasicsHAS
    
    if len(data.arguments) > 0 and (str(data.predicate) not in CryptoPred) and (str(data.predicate) not in ["time","meta","p"])  : 
        for arg in data.arguments :
            if str(arg.predicate) not in ["time","meta"] :  
                t1 = DataOrFact("Has(" + str(entity) + "," + str(arg) + ")") 
                
                if str(entity) not in ReclistofbasicsHAS.keys() :  
                    ReclistofbasicsHAS[str(entity)] = set() 
                    ReclistofbasicsHAS[str(entity)].add(t1)
                else : 
                    ReclistofbasicsHAS[str(entity)].add(t1)
                
                
                if len(arg.arguments) > 0 and (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                    t2 = DataOrFact("Has(" + str(entity) + "," + str(arg.predicate) + ")")  
                    
                    if str(entity) not in ReclistofbasicsHAS.keys() :  
                        ReclistofbasicsHAS[str(entity)] = set() 
                        ReclistofbasicsHAS[str(entity)].add(t2)
                    else : 
                        ReclistofbasicsHAS[str(entity)].add(t2)
                    
                    
                    if len(arg.arguments) > 1 : 
                        for arg2 in arg.arguments : 
                            if (str(arg.predicate) not in CryptoPred) and (str(arg.predicate) not in ["time","meta","p"]) : 
                                t4 = DataOrFact("Has(" + str(entity) + "," + str(arg.predicate) + "(" + str(arg2) + ")" + ")")  
                                
                                if str(entity) not in ReclistofbasicsHAS.keys() :  
                                    ReclistofbasicsHAS[str(entity)] = set() 
                                    ReclistofbasicsHAS[str(entity)].add(t4)
                                else : 
                                    ReclistofbasicsHAS[str(entity)].add(t4)
                                
            addtoHas(entity,arg)                
            
   
            
          
def addtoLink(nextdata,argpredset) : 
    if len(nextdata.arguments) > 0 and (str(nextdata.predicate) not in CryptoPred) and (str(nextdata.predicate) not in ["time","meta","p"]) : 
        argpredset.append(str(nextdata.predicate))
        for arg2 in nextdata.arguments : 
            if len(arg2.arguments) == 0: 
                argpredset.append(str(arg2))  
            else :     
                addtoLink(arg2,argpredset)   
    elif len(nextdata.arguments) > 0 and (str(nextdata.predicate) in CryptoPred) or (str(nextdata.predicate) == "p") :         
        argpredset.append(str(nextdata))   
    elif len(nextdata.arguments) == 0 :         
       argpredset.append(str(nextdata))   
            
           

def extractmsginsidecrypto(term) :
    global msginsidecrypto
    for data in term.arguments : 
        if str(data.predicate) in ["senc","aenc"] : 
            for arg in data.arguments[:-1] : 
                if str(arg.predicate) not in ["senc","aenc","mac", "homenc"] : 
                    msginsidecrypto.add(str(arg))
                else : 
                    extractmsginsidecrypto(arg) 
        elif str(data.predicate) == "homenc" : 
            for arg in data.arguments : 
                if str(arg.predicate) not in ["senc","aenc","mac", "homenc"] :
                    msginsidecrypto.add(str(arg)) 
                else : 
                    extractmsginsidecrypto(arg)


########################################### DELETION DELAY CALCULATION ################################################

def evaltime(timestr) :
    if len(timestr.split("+")) >= 2 : 
        return sum(list(map(evaltime,timestr.split("+")))) 
    elif len(timestr.split("+")) == 1 : 
        if len(timestr.split("y")) == 2 : 
            return eval(timestr.split("y")[0] + "*" + "y" + timestr.split("y")[1])   
        elif len(timestr.split("w"))== 2 : 
            return eval(timestr.split("w")[0] + "*" + "w" + timestr.split("w")[1])
        elif len(timestr.split("mo")) == 2 : 
            return eval(timestr.split("mo")[0] + "*" + "mo" + timestr.split("mo")[1])
        elif len(timestr.split("d")) == 2 : 
            return eval(timestr.split("d")[0] + "*" + "d" + timestr.split("d")[1])
        elif len(timestr.split("h")) == 2 : 
            return eval(timestr.split("h")[0] + "*" + "h" + timestr.split("h")[1])
        elif len(timestr.split("m")) == 2 : 
            return eval(timestr.split("m")[0] + "*" + "m" + timestr.split("m")[1])
        else : return -1
    else : return -1


def semicolsep(dataorfactstr):
     listofdata = []
     subcomplexdata = 0
     straftersemicol = []
     for character in dataorfactstr + ";":
         if character == ";" and subcomplexdata == 0:
             listofdata.append("".join(straftersemicol))
             straftersemicol = []
         else:
             if character == "(":
                 subcomplexdata += 1
             elif character == ")":
                 subcomplexdata -= 1
             straftersemicol.append(character)
     return listofdata


def commasep(dataorfactstr):
     listofdata = []
     subcomplexdata = 0
     straftercomma = []
     for character in dataorfactstr + ",":
         if character == "," and subcomplexdata == 0:
             listofdata.append("".join(straftercomma))
             straftercomma = []
         else:
             if character == "(":
                 subcomplexdata += 1
             elif character == ")":
                 subcomplexdata -= 1
             straftercomma.append(character)
     return listofdata


########################################### CLASS OF DATATYPE/FACT #######################################################

class DataOrFact :  #A data type or a logic fact 
    def __init__ (self, datatypestr, arguments=None) :
        if arguments :  
            self.predicate = datatypestr
            self.arguments = arguments
        elif len(datatypestr) > 0 and datatypestr[-1] == ')' :  #if complex data type or a logic fact
            predargsseparation = datatypestr.split("(", 1)
            self.arguments = list(map(DataOrFact, commasep(predargsseparation[1][:-1])))
            self.predicate = predargsseparation[0]
        else : 
            self.predicate = datatypestr          
            self.arguments = []

    def __repr__ (self) :
        if self.arguments : 
            return "%s(%s)" % (self.predicate, ",".join(map(str,self.arguments)))     
        else : return self.predicate 

########################################### CLASS OF INFERENCE RULES #############################################
        
class InfRule :
    def __init__ (self, rulestr) :   
        headgoalsseparation = rulestr.split(":-")
        self.head = DataOrFact(headgoalsseparation[0])
        self.goals = []
        if len(headgoalsseparation) == 2 :
            goalsseparation = semicolsep(re.sub("\),",");",headgoalsseparation[1]))  
            for goal in goalsseparation : self.goals.append(DataOrFact(goal))

    def __repr__ (self) :
        rep = str(self.head)
        sep = ":-"  
        for goal in self.goals :
            rep += sep + str(goal)
            sep = ","
        return rep  


       
        
def isVariable(data) : return data.arguments == [] and     data.predicate[0:1] in capital  
def isConstant(data) : return data.arguments == [] and not data.predicate[0:1] in capital  
def startUnderline(data) : return str(data.predicate)[0] == "_" and len(data.arguments) == 0   



def isCryptHasInGoal(goalslist) : 
    
    if len(goalslist) > 0 :
        if str(goalslist[-1].predicate) == "CryptHas" : 
            return 1 
        else : return 0 
    else: return 0

def iscontainingcrypto(strterm,strarg) : 
    if str(DataOrFact(strterm)) == strarg :   
        return 1  
    for arg in DataOrFact(strterm).arguments : 
        if iscontainingcrypto(str(arg),strarg) == 1 : 
            return 1
    return 0

def extractcryptoarg(strterm,cryptoset) : 
    if str(DataOrFact(strterm).predicate) in ["senc", "mac", "aenc"] : 
        cryptoset.add(str(DataOrFact(strterm)))   
    for arg in DataOrFact(strterm).arguments : 
        extractcryptoarg(str(arg),cryptoset)
    return cryptoset

def isargincryptofunc(strterm,strarg) : 
    c=set() 
    for e in extractcryptoarg(strterm,c) : 
        if iscontainingcrypto(e,strarg) == 1 : 
            return 1 
    return 0


def iscontainingarg(strterm,strarg) :  
    if str(DataOrFact(strterm).predicate) == strarg and len(DataOrFact(strterm).arguments) == 0 :   
        return 1  
    for arg in DataOrFact(strterm).arguments : 
        if iscontainingarg(str(arg),strarg) == 1 : 
            return 1
    return 0



def reorder(term,commonelement) :   
    argtupleincmeta ="" 
    for arg in term.arguments : 
        if (str(arg.predicate) != commonelement) :   
            argtupleincmeta = argtupleincmeta + str(arg) + ","
    argtupleincmeta = argtupleincmeta[:-1]  
    argtuple = str(term.predicate) + "(" + commonelement + "," + argtupleincmeta + ")"   
    return DataOrFact(argtuple) 


########################################### THE UNIFICATION PROCEDURE ###############################################
    
def unification(fact1, fact2, MAPRECORD, cryptopred) :
    uIsInsideCrypto = 0  
    uIsInsideCrypto2 = 0  
    
    if isVariable(fact1) and isConstant(fact2) :  
       
        fact1Val = evfact(fact1, MAPRECORD) 
        if not fact1Val : 
            
            MAPRECORD[fact1.predicate] = DataOrFact(fact2.predicate)
            return [1, 1]   
        else :
            
            return [0, 1]   
           
    
    
    
    if isVariable(fact1) and (not isConstant(fact2)) and (not isVariable(fact2)) : 
        
        if str(fact2.predicate)[0] =="_" :
            return [0, 1] 
        else:     
            fact1Val = evfact(fact1, MAPRECORD)  
            if not fact1Val :  
                MAPRECORD[fact1.predicate] = evfact(fact2, MAPRECORD)
              
                return [1, 1]   
            else : return [0, 1] 
    
    
    
    if isVariable(fact1) and isVariable(fact2) and (fact1!=fact2): 
        fact1Val = evfact(fact1, MAPRECORD)  
        
        if not fact1Val :  
            MAPRECORD[fact1.predicate] = DataOrFact(fact2.predicate)
            
            return [1, 1]   
        else : return [0, 1]  
            
    
    
    if  (not isVariable(fact1)) and isVariable(fact2) :  
        fact2Val = evfact(fact2, MAPRECORD)           
       
        if fact2Val : return unification(fact1, fact2Val, MAPRECORD, cryptopred)   
        else :        
            MAPRECORD[fact2.predicate] = evfact(fact1, MAPRECORD)   
            return [1, 1]  
        
       
    if  len(str(fact2).split("@")) == 1 and len(str(fact2).split("!")) == 1 and (not isVariable(fact1)) and (not isConstant(fact1)) and (str(fact2.predicate)[0] =="_") and  (str(fact1.predicate)[0] !="_") and (str(fact1.predicate) not in cryptopred) :  
        
        if len(fact1.arguments) != len(fact2.arguments) : return [0, 1] 
        else : 
           
            for i in range(len(fact1.arguments)) :
                if unification(fact1.arguments[i], fact2.arguments[i], MAPRECORD, cryptopred)[0] == 0 :  
                        return [0, 1] 
            fact2Val = evfact(DataOrFact(fact2.predicate), MAPRECORD)      
           
            if not fact2Val : 
                MAPRECORD[fact2.predicate] = DataOrFact(fact1.predicate)
                
                return [1, 1] 
            else :
                
                return [0, 1] 
    
    
    if len(str(fact1).split("@")) == 1 and len(str(fact1).split("!")) == 1 and (not isVariable(fact2)) and (not isConstant(fact2)) and (str(fact1.predicate)[0] =="_") and  (str(fact2.predicate)[0] !="_") and (str(fact2.predicate) not in cryptopred):     
           
        if len(fact1.arguments) != len(fact2.arguments) : return [0, 1]   
        else : 
            for i in range(len(fact2.arguments)) : 
                
                unificationoutput = unification(fact1.arguments[i], fact2.arguments[i], MAPRECORD, cryptopred)
                if unificationoutput[0] == 0 : 
                        
                        return [0, 1] 
                elif unificationoutput == [1, 0] : 
                    uIsInsideCrypto2 = 1
                    
            fact1Val = evfact(DataOrFact(fact1.predicate), MAPRECORD)      
            if not fact1Val :  
                MAPRECORD[fact1.predicate] = DataOrFact(fact2.predicate)
                
                if uIsInsideCrypto2 == 1 : 
                    return [1, 0]  
                else: 
                    return [1, 1]  
            else :
                
                return [0, 1]  
    
    
    if len(str(fact2).split("!")) == 2 and len(str(fact2).split("@")) == 1 and len(str(fact2).split("meta(")) == 2 and len(str(fact1).split("meta(")) == 2 and (not isVariable(fact1)) and (not isConstant(fact1)) and (str(fact2.predicate)[0] =="_") and  (str(fact1.predicate)[0] !="_") and (str(fact1.predicate) not in cryptopred):      
       fact1args = list(map(tostring, fact1.arguments))  
       fact2args = list(map(tostring, fact2.arguments)) 
       setfact1 = set(fact1args)  
       setfact2 = set(fact2args) 
       common = setfact1.intersection(setfact2) 
       
       commonlist = list(common)  
       
       if (len(common) == 1 and len(str(commonlist[0]).split("meta(")) == 1) or len(common) > 1 :  
           
           argtuple = ""
           argendwithplus = DataOrFact("a")  
           for arg in fact1.arguments : 
               
               if (str(arg) not in commonlist) and  (str(arg.predicate) != "meta") : 
                   argtuple = argtuple + str(arg.predicate) + "," 
           argtuple = argtuple[:-1]  
         
           if (argtuple =="") : 
               for arg in fact2.arguments : 
                   if "!" in str(arg.predicate) : 
                       argendwithplus = arg  
               fact2split = str(fact2).split(str(argendwithplus))
            
               if len(fact2split[0]) > 0 and fact2split[0][-1] == ",": 
                    fact2split[0]= fact2split[0][:-1] 
               
               if len(fact2split[0]) > 0 and fact2split[0][-1] == "(" and  fact2split[1][0] == ",":   
                   fact2split[1] = fact2split[1][1:] 
                
               shortenfact2 = fact2split[0] + fact2split[1] 
               shortenfact2term = DataOrFact(shortenfact2)
               
               if unification(fact1, shortenfact2term, MAPRECORD, cryptopred)[0] == 0 :  
                   return [0, 1] 
               else : return [1, 1] 
           else : 
               termargtuple =  DataOrFact(argtuple)
               for arg in fact2.arguments : 
                   if "!" in str(arg.predicate) : 
                       argendwithplus = arg  
                       fact2Val = evfact(DataOrFact(arg.predicate), MAPRECORD)
                       if not fact2Val : 
                           MAPRECORD[arg.predicate] = termargtuple
                          
               fact1split = str(fact1).split(argtuple)
                
               if len(fact1split[0]) > 0 and fact1split[0][-1] == ",":   
                   fact1split[0]= fact1split[0][:-1] 
               
               
               if len(fact1split[0]) > 0 and fact1split[0][-1] == "(" and fact1split[1][0] == ",":   
                         fact1split[1] = fact1split[1][1:]  
                        
               shortenfact1 = fact1split[0] + fact1split[1]
                
               shortenfact1term = DataOrFact(shortenfact1)
                
               fact2split = str(fact2).split(str(argendwithplus))
                
               if len(fact2split[0]) > 0 and fact2split[0][-1] == ",": 
                   fact2split[0]= fact2split[0][:-1] 
                    
               
               if len(fact2split[0]) > 0 and fact2split[0][-1] == "(" and fact2split[1][0] == ",":   
                   fact2split[1] = fact2split[1][1:]  
                
               shortenfact2 = fact2split[0] + fact2split[1] 
               shortenfact2term = DataOrFact(shortenfact2)
                
               if unification(shortenfact1term, shortenfact2term, MAPRECORD, cryptopred)[0] == 0 :    
                   return [0, 1] 
               else : return [1, 1] 
       else :    
           return [0, 1] 
        
    """
    if len(str(fact2).split("!")) == 2 and len(str(fact2).split("@")) == 1 and len(str(fact2).split("meta(")) == 1 and len(str(fact1).split("meta(")) == 1 and (not isVariable(fact1)) and (not isConstant(fact1)) and (str(fact2.predicate)[0] =="_") and  (str(fact1.predicate)[0] !="_") and (str(fact1.predicate) not in cryptopred):
       print("THI IS IT 0000")
       fact1args = list(map(tostring, fact1.arguments))  
       fact2args = list(map(tostring, fact2.arguments)) 
       setfact1 = set(fact1args)  
       setfact2 = set(fact2args) 
       common = setfact1.intersection(setfact2) 
      
       if len(common) > 0 :  
           commonlist = list(common)  
           
           argtuple = ""
           argendwithplus = DataOrFact("a")  
           for arg in fact1.arguments : 
               if (str(arg) not in commonlist) :  
                   argtuple = argtuple + str(arg.predicate) + "," 
           if len(argtuple) > 0 and argtuple[-1] == "," :          
               argtuple = argtuple[:-1]  
           if (argtuple =="") : 
               for arg in fact2.arguments : 
                   if "!" in str(arg.predicate) :  
                       argendwithplus = arg  
               fact2split = str(fact2).split(str(argendwithplus))
               
               if len(fact2split[0]) > 0 and fact2split[0][-1] == ",": 
                    fact2split[0]= fact2split[0][:-1] 
               
               if len(fact2split[0]) > 0 and fact2split[0][-1] == "(" and fact2split[1][0] == ",":   
                   fact2split[1] = fact2split[1][1:] 
                
               shortenfact2 = fact2split[0] + fact2split[1] 
               shortenfact2term = DataOrFact(shortenfact2)
               if unification(fact1, shortenfact2term, MAPRECORD, cryptopred)[0] == 0 :  
                   return [0, 1] #0
               else : return [1, 1] #1
           else : 
               termargtuple =  DataOrFact(argtuple)
               for arg in fact2.arguments : 
                   if "!" in str(arg.predicate) : 
                       argendwithplus = arg  
                       fact2Val = evfact(DataOrFact(arg.predicate), MAPRECORD)
                       if not fact2Val : 
                           MAPRECORD[arg.predicate] = termargtuple
                          
               fact1split = str(fact1).split(argtuple)
               if len(fact1split[0]) > 0 and fact1split[0][-1] == ",":   
                   fact1split[0]= fact1split[0][:-1] 
               
              
               if len(fact1split[0]) > 0 and fact1split[0][-1] == "(" and fact1split[1][0] == ",":  
                         fact1split[1] = fact1split[1][1:]  
                        
               shortenfact1 = fact1split[0] + fact1split[1]
                
               shortenfact1term = DataOrFact(shortenfact1)
               
               fact2split = str(fact2).split(str(argendwithplus))
               
               if len(fact2split[0]) > 0 and fact2split[0][-1] == ",": 
                   fact2split[0]= fact2split[0][:-1] 
                    
              
               if len(fact2split[0]) > 0 and fact2split[0][-1] == "(" and fact2split[1][0] == ",":  
                   fact2split[1] = fact2split[1][1:]  
                
               shortenfact2 = fact2split[0] + fact2split[1] 
               shortenfact2term = DataOrFact(shortenfact2)
                
               if unification(shortenfact1term, shortenfact2term, MAPRECORD, cryptopred)[0] == 0 :
                   return [0, 1] 
               else : return [1, 1] 
       else :    
           return [0, 1] #0    
    """
    
    if len(str(fact1).split("!")) == 2 and len(str(fact1).split("@")) == 1 and len(str(fact1).split("meta(")) == 2 and len(str(fact2).split("meta(")) == 2 and (not isVariable(fact2)) and (not isConstant(fact2)) and (str(fact1.predicate)[0] =="_") and  (str(fact2.predicate)[0] !="_") and (str(fact2.predicate) not in cryptopred):
       
       fact1args = list(map(tostring, fact1.arguments))
       fact2args = list(map(tostring, fact2.arguments))
       setfact1 = set(fact1args)  
       setfact2 = set(fact2args) 
       common = setfact1.intersection(setfact2) 
       commonlist = list(common)  
       
       if (len(common) == 1 and len(str(commonlist[0]).split("meta(")) == 1) or len(common) > 1 : 
           argtuple = ""
           argendwithplus = DataOrFact("a")  
           for arg in fact2.arguments : 
               
               if (str(arg) not in commonlist) and  (str(arg.predicate) != "meta") : 
                   argtuple = argtuple + str(arg.predicate) + "," 
           argtuple = argtuple[:-1] 
            
           if (argtuple =="") : 
               for arg in fact1.arguments : 
                   if "!" in str(arg.predicate) :  
                       argendwithplus = arg  
               fact1split = str(fact1).split(str(argendwithplus))
            
               if len(fact1split[0]) > 0 and fact1split[0][-1] == ",":
                    fact1split[0]= fact1split[0][:-1] 
               
               if len(fact1split[0]) > 0 and fact1split[0][-1] == "(" and fact1split[1][0] == ",":  
                   fact1split[1] = fact1split[1][1:]  
                
               shortenfact1 = fact1split[0] + fact1split[1] 
               shortenfact1term = DataOrFact(shortenfact1)
               
               if unification(fact2, shortenfact1term, MAPRECORD, cryptopred)[0] == 0 :  
                   return [0, 1] 
               else : return [1, 1] 
           else : 
               termargtuple =  DataOrFact(argtuple)
               for arg in fact1.arguments : 
                   if "!" in str(arg.predicate) : 
                       argendwithplus = arg  
                       fact1Val = evfact(DataOrFact(arg.predicate), MAPRECORD)
                       if not fact1Val : 
                           MAPRECORD[arg.predicate] = termargtuple
                           
              
               fact2split = str(fact2).split(argtuple)
               
               if len(fact2split[0]) > 0 and fact2split[0][-1] == ",":  
                   fact2split[0]= fact2split[0][:-1] 
               
               
               if len(fact2split[0]) > 0 and fact2split[0][-1] == "(" and fact2split[1][0] == ",":  
                         fact2split[1] = fact2split[1][1:]  
                        
               shortenfact2 = fact2split[0] + fact2split[1]
               
               shortenfact2term = DataOrFact(shortenfact2)
               
               
               
                
               fact1split = str(fact1).split(str(argendwithplus))
                
               if len(fact1split[0]) > 0 and fact1split[0][-1] == ",": 
                   fact1split[0]= fact1split[0][:-1] 
                    
                
               if len(fact1split[0]) > 0 and fact1split[0][-1] == "(" and fact1split[1][0] == ",":   
                   fact1split[1] = fact1split[1][1:]  
    
    
               shortenfact1 = fact1split[0] + fact1split[1] 
               shortenfact1term = DataOrFact(shortenfact1)
               if unification(shortenfact1term, shortenfact2term, MAPRECORD, cryptopred)[0] == 0 :  
                   return [0, 1] 
               else : return [1, 1] 
       else :    
           return [0, 1] 
    
    
    """
    if len(str(fact1).split("!")) == 2 and len(str(fact1).split("@")) == 1 and len(str(fact1).split("meta(")) == 1 and len(str(fact2).split("meta(")) == 1 and (not isVariable(fact2)) and (not isConstant(fact2)) and (str(fact1.predicate)[0] =="_") and  (str(fact2.predicate)[0] !="_") and (str(fact2.predicate) not in cryptopred):     # If fact2 contains "!". unification DataOrFact("sickness(name,photo,phone,address,meta(ip))") with DataOrFact("_anypred1(name,W!,meta(Z))")
       print("THI IS IT 2222")
       fact2args = list(map(tostring, fact2.arguments))  
       fact1args = list(map(tostring, fact1.arguments))
       setfact2 = set(fact2args)  
       setfact1 = set(fact1args) 
       common = setfact2.intersection(setfact1) 
       print("COMMON:")
       print(common)
       
       if len(common) > 0 :  
           commonlist = list(common)  
           
           argtuple = ""
           argendwithplus = DataOrFact("a")  
           for arg in fact2.arguments : 
               if (str(arg) not in commonlist) :   
                   argtuple = argtuple + str(arg.predicate) + "," 
           if len(argtuple) > 0 and argtuple[-1] == "," :
               argtuple = argtuple[:-1]  
           if (argtuple =="") : 
               for arg in fact1.arguments : 
                   if "!" in str(arg.predicate) :  
                       argendwithplus = arg  
               fact1split = str(fact1).split(str(argendwithplus))
               
               if len(fact1split[0]) > 0 and fact1split[0][-1] == ",": 
                   fact1split[0]= fact1split[0][:-1] 
               
               if len(fact1split[0]) > 0 and fact1split[0][-1] == "(" and fact1split[1][0] == ",":   
                   fact1split[1] = fact1split[1][1:] 
                
               shortenfact1 = fact1split[0] + fact1split[1] 
               shortenfact1term = DataOrFact(shortenfact1)
               if unification(fact2, shortenfact1term, MAPRECORD, cryptopred)[0] == 0 :  
                   return [0, 1] #0
               else : return [1, 1] #1
           else :
               termargtuple =  DataOrFact(argtuple)
               for arg in fact1.arguments : 
                   if "!" in str(arg.predicate) : 
                       argendwithplus = arg  
                       fact1Val = evfact(DataOrFact(arg.predicate), MAPRECORD)
                       if not fact1Val : 
                           MAPRECORD[arg.predicate] = termargtuple
                          
               fact2split = str(fact2).split(argtuple)
               if len(fact2split[0]) > 0 and fact2split[0][-1] == ",":   
                   fact2split[0]= fact2split[0][:-1] 
               
               
               if len(fact2split[0]) > 0 and fact2split[0][-1] == "(" and fact2split[1][0] == ",":   
                         fact2split[1] = fact2split[1][1:] 
                        
               shortenfact2 = fact2split[0] + fact2split[1]
               
               shortenfact2term = DataOrFact(shortenfact2)
              
               
               
              
               fact1split = str(fact1).split(str(argendwithplus))
               
               if len(fact1split[0]) > 0 and fact1split[0][-1] == ",": 
                   fact1split[0]= fact1split[0][:-1] 
                    
               
               if len(fact1split[0]) > 0 and fact1split[0][-1] == "(" and fact1split[1][0] == ",":   
                   fact1split[1] = fact1split[1][1:]  
                
               shortenfact1 = fact1split[0] + fact1split[1] 
               shortenfact1term = DataOrFact(shortenfact1)
                
               if unification(shortenfact1term, shortenfact2term, MAPRECORD, cryptopred)[0] == 0 :    
                   return [0, 1] 
               else : return [1, 1] 
       else :    
           return [0, 1]   
    
      """  
    
    if len(str(fact2).split("@")) == 2 and len(str(fact2).split("!")) == 1 and (not isVariable(fact1)) and (not isConstant(fact1)) and (str(fact2.predicate)[0] =="_") and  (str(fact1.predicate)[0] !="_") and (str(fact1.predicate) not in cryptopred) : 
        if len(fact1.arguments) > 1 and len(fact2.arguments) > 0 : 
            
            fact1args = list(map(tostring, fact1.arguments))  
            fact2args = list(map(tostring, fact2.arguments)) 
            setfact1 = set(fact1args)  
            setfact2 = set(fact2args) 
            common = setfact1.intersection(setfact2) 
           
            if len(common) > 0 : 
                commonlist = list(common)  
                
                argtuple = ""
                for arg in fact1.arguments : 
                    if (str(arg) not in commonlist) : 
                        argtuple = argtuple + str(arg.predicate) + "," 
                if len(argtuple) > 0 and argtuple[-1] == "," : 
                    argtuple = argtuple[:-1]  
            
                
                termargtuple =  DataOrFact(argtuple)
                for arg in fact2.arguments : 
                    if "@" in str(arg.predicate) : 
                        
                        fact2Val = evfact(DataOrFact(arg.predicate), MAPRECORD)
                        if not fact2Val : 
                            MAPRECORD[arg.predicate] = termargtuple
                            
                fact2Pred = evfact(DataOrFact(fact2.predicate), MAPRECORD)      
                
                if not fact2Pred :  
                    MAPRECORD[fact2.predicate] = DataOrFact(fact1.predicate)
                   
                    return [1, 1] 
                else : 
                    
                    return [0, 1] 
            else : 
                return [0, 1] 
        else : 
            return [0, 1]          
    
  
    if len(str(fact1).split("@")) == 2 and len(str(fact1).split("!")) == 1 and (not isVariable(fact2)) and (not isConstant(fact2)) and (str(fact1.predicate)[0] =="_") and  (str(fact2.predicate)[0] !="_") and (str(fact2.predicate) not in cryptopred) : 
        if len(fact2.arguments) > 1 and len(fact1.arguments) > 0 : 
            
            fact2args = list(map(tostring, fact2.arguments))  
            fact1args = list(map(tostring, fact1.arguments)) 
            setfact2 = set(fact2args)  
            setfact1 = set(fact1args) 
            common = setfact2.intersection(setfact1) 
            
            if len(common) > 0 :  
                commonlist = list(common)  
                
                argtuple = ""
                for arg in fact2.arguments : 
                    if (str(arg) not in commonlist) : 
                        argtuple = argtuple + str(arg.predicate) + "," 
                
                if len(argtuple) > 0 and argtuple[-1] == "," : 
                    argtuple = argtuple[:-1]  
                
               
                termargtuple =  DataOrFact(argtuple)
                for arg in fact1.arguments : 
                    if "@" in str(arg.predicate) : 
                        
                        fact1Val = evfact(DataOrFact(arg.predicate), MAPRECORD)
                        if not fact1Val : 
                            MAPRECORD[arg.predicate] = termargtuple
                            
                fact1Pred = evfact(DataOrFact(fact1.predicate), MAPRECORD)      
                
                if not fact1Pred :  
                    MAPRECORD[fact1.predicate] = DataOrFact(fact2.predicate)
                    
                    return [1, 1] 
                else : 
                    
                    return [0, 1]  
            else : 
                return [0, 1] 
        else :    
            return [0, 1]  
        
    if str(fact1.predicate) == "time" and str(fact2.predicate) == "time" : 
        
        if isConstant(fact1.arguments[0]) and  isVariable(fact2.arguments[0]) :  
            fact2Val = evfact(fact2.arguments[0], MAPRECORD)  
            if not fact2Val :  
                MAPRECORD[fact2.arguments[0].predicate] = DataOrFact(fact1.arguments[0].predicate)
                return [1, 1]  
            else : return [0, 1]  
        elif isVariable(fact1.arguments[0]) and  isConstant(fact2.arguments[0]) : 
            fact1Val = evfact(fact1.arguments[0], MAPRECORD)  
            if not fact1Val : 
                MAPRECORD[fact1.arguments[0].predicate] = DataOrFact(fact2.arguments[0].predicate)
                return [1, 1]   
            else : return [0, 1]  
        elif isConstant(fact1.arguments[0]) and  isConstant(fact2.arguments[0]) : 
            if len(str(fact1.arguments[0]).split("t")) == 2 and len(str(fact2.arguments[0]).split("t")) == 2 : 
                if str(fact1.arguments[0]) == str(fact2.arguments[0]) : 
                    return [1, 1] 
                else : return [0, 1] 
            elif len(str(fact1.arguments[0]).split("t")) == 1 and len(str(fact2.arguments[0]).split("t")) == 1 :     
               
                if evaltime(str(fact1.arguments[0])) >= evaltime(str(fact2.arguments[0])) : 
                    
                    return [1, 1] 
                else : return [0, 1]  
    
    if ((fact1.predicate == "Anytypeinccrypto") or  (fact1.predicate == "Anytypeinccrypto1") or (fact1.predicate == "Anytypeinccrypto2")) : 
        
        if isargincryptofunc(str(fact2),str(fact1.arguments[0])) == 1: 
            return [1, 0] 
        else: 
            if iscontainingarg(str(fact2),str(fact1.arguments[0])) == 1:  
                return [1, 1] 
            else: 
                return [0, 1] 
    

    if ((fact2.predicate == "Anytypeinccrypto") or  (fact2.predicate == "Anytypeinccrypto1") or (fact2.predicate == "Anytypeinccrypto2")) : 
        if isargincryptofunc(str(fact1),str(fact2.arguments[0])) == 1: 
            return [1, 0] 
        else: 
            if iscontainingarg(str(fact1),str(fact2.arguments[0])) == 1:  
                return [1, 1]
            else: 
                return [0, 1] 
        
        
    
    elif fact1.predicate      != fact2.predicate      :  
        return [0, 1] 
    elif len(fact1.arguments) != len(fact2.arguments) : return [0, 1] 
    else : 
        for i in range(len(fact1.arguments)) :    
            unificationoutput = unification(fact1.arguments[i], fact2.arguments[i], MAPRECORD, cryptopred)
            if unificationoutput[0] == 0 : 
                return [0, 1] 
            elif unificationoutput == [1, 0] : 
                uIsInsideCrypto = 1
        if uIsInsideCrypto == 1 :
            return [1, 0]
        else : 
            return [1, 1]  


        
def evfact(fact, mapping) :      
    if isConstant(fact) and not startUnderline(fact) : return fact   
    if isVariable(fact) or startUnderline(fact) :   
        ans = mapping.get(fact.predicate)  
        if not ans : return None  
        else : 
            return evfact(ans,mapping)   
    args = [] 
    for arg in fact.arguments :  
        
        a = evfact(arg, mapping)  
        if not a : a = arg   
        args.append(a)         
    if str(fact.predicate)[0] == "_" :
        boundfactpred = evfact(DataOrFact(fact.predicate),mapping) 
        if not boundfactpred : 
            return DataOrFact(fact.predicate, args)
        else :  
            return DataOrFact(boundfactpred, args)    
    else :
        return DataOrFact(fact.predicate, args)  
    


def appendnumtovariableinterm(term, num) : 
    ind = 1
    newterm = str(term.predicate) + '(' 
    for arg in term.arguments : 
        if  not isConstant(arg): 
            if (len(arg.arguments) == 0) and (ind == len(term.arguments)) : 
                argnew = str(arg) + str(num) + ')'
                newterm = newterm + argnew
               
            elif (len(arg.arguments) == 0) and (ind < len(term.arguments)) :
                argnew = str(arg) + str(num) + ','
                newterm = newterm + argnew
               
                ind = ind + 1
            elif (len(arg.arguments) > 0) and (ind == len(term.arguments)) : 
                newterm = newterm + str(appendnumtovariableinterm(arg, num)) + ')'
               
            elif (len(arg.arguments) > 0) and (ind < len(term.arguments)) : 
                newterm = newterm + str(appendnumtovariableinterm(arg, num)) + ','
                ind = ind + 1
        else: 
            if (ind == len(term.arguments)): 
                argnew = str(arg) + ')'
                newterm = newterm + argnew
            elif (ind < len(term.arguments)) :
                argnew = str(arg) + ','
                newterm = newterm + argnew
                ind = ind + 1       
    return DataOrFact(newterm)


def searchfirstvar(term): 
    if len(term.arguments) > 0: 
        for arg in term.arguments: 
            if isVariable(arg) : 
                return str(arg) 
            else: 
                if searchfirstvar(arg) != 0: 
                    return searchfirstvar(arg)
    elif len(term.arguments) == 0:
        if isVariable(term) :
            return str(term)
        else: 
            return 0
                    

def renameterm(term):
    if len(term.arguments) > 0 :  
        convertedstr = str(term).replace(";",",")  
        convertedterm = DataOrFact(convertedstr)
        variablestr = searchfirstvar(convertedterm) 
        strextractednumber = ''.join(character for character in variablestr if character.isdigit())
        if not strextractednumber : 
            return appendnumtovariableinterm(convertedterm, 1)
        else : 
            strincreasednumber = str(int(strextractednumber)+1)
            return DataOrFact(str(convertedterm).replace(strextractednumber,strincreasednumber))   

            
def renamerule(rule) : 
    j = 1
    newrule = str(renameterm(rule.head)) + ':-'
    for goal in rule.goals : 
        if j == len(rule.goals) :  
            newrule = newrule + str(renameterm(goal))
        elif j < len(rule.goals) : 
            newrule = newrule + str(renameterm(goal)) + ','
            j = j+1
    return InfRule(newrule)   


def tostring(tm):
    return str(tm)

def replaceentity(term,tothis) :  
    strtermargs = list(map(tostring, term.arguments))
    return DataOrFact(str(term.predicate) + "(" + tothis + "," + ",".join(strtermargs[1:]) + ")") 


##########################################################################################################################################
########################################### CHECK A GOAL/SUB-GOAL AGAINST THE ARCHITECTURE ###############################################
##########################################################################################################################################
    
def checkInArchComplete(bterm, architecture, archmeta, archpseudo, archtime, MAPRECORD, cryptopred) : 
    
    listofMAPRECORD = [] 
    MAPRECORDORIGIN = MAPRECORD.copy()
    
    entity = bterm.arguments[0] 
    strbterm = str(bterm)
    
    timesplit = str(strbterm).split("time(")
    metasplit = str(strbterm).split("meta(")   
    pseudosplit = str(strbterm).split("p(")
    
    # ================================ PSEUDO ======================================================
    
    if len(pseudosplit) == 2 :  
        for arch in archpseudo : 
            MAPRECORD = MAPRECORDORIGIN.copy()
            
            if unification(arch, bterm, MAPRECORD, cryptopred)[0] == 1 :
                listofMAPRECORD.append(MAPRECORD) 
        
        return listofMAPRECORD         
            
    
    elif len(metasplit) == 2 :  
        for arch in archmeta : 
            MAPRECORD = MAPRECORDORIGIN.copy()
            
            if unification(arch, bterm, MAPRECORD, cryptopred)[0] == 1 :
                listofMAPRECORD.append(MAPRECORD) 
        
        return listofMAPRECORD         
    
    
    # ================================ TIME ======================================================    
    elif len(timesplit) == 2 : 
        for arch in archtime :
            MAPRECORD = MAPRECORDORIGIN.copy()
            
            if unification(arch, bterm, MAPRECORD, cryptopred)[0] == 1 :
                listofMAPRECORD.append(MAPRECORD) 
                
        return listofMAPRECORD             

    else: 
    # ================================ architecture ======================================================    
        for arch in architecture :
            MAPRECORD = MAPRECORDORIGIN.copy()
            
            if unification(arch, bterm, MAPRECORD, cryptopred)[0] == 1 :
                listofMAPRECORD.append(MAPRECORD) 
                
            
        return listofMAPRECORD    
        
    

############################# Check the goal/sub-goal against the architecture ##################################
def checkInArch(bterm, architecture, archmeta, archpseudo, archtime, MAPRECORD, cryptopred) : 
   
    strbterm = str(bterm)
    
    metasplit = str(strbterm).split("meta(")   
    pseudosplit = str(strbterm).split("p(")
    timesplit = str(strbterm).split("time(")
    strarchitecture = list(map(tostring, architecture))    
    
    strarchmeta = map(tostring, archmeta)    
    strarchpseudo = map(tostring, archpseudo)    
    strarchtime = map(tostring, archtime)    
    
    if len(pseudosplit) == 2 : 
        if strbterm in strarchpseudo : 
            return [1, 1] 
        else : 
            for arch in archpseudo : 
               if unification(arch, bterm, MAPRECORD, cryptopred)[0] == 1 : 
                   return [1, 1] 
                
            
            return [0, 1]   
        
    elif len(metasplit) == 2 :   
        if strbterm in strarchmeta : 
            return [1, 1] 
        else : 
            for arch in archmeta : 
                if unification(arch, bterm, MAPRECORD, cryptopred)[0] == 1 : 
                    return [1, 1] 
                
            
            return [0, 1]  
        
    elif len(timesplit) == 2 : 
        if strbterm in strarchtime : 
            return [1, 1] 
        else : 
            for arch in archtime : 
                if unification(arch, bterm, MAPRECORD, cryptopred)[0] == 1 : 
                    return [1, 1]
            
            
            return [0, 1]    

             
    else :
        if strbterm in strarchitecture : 
            return [1, 1] 
        else: 
            for arch in architecture : 
                 
                unificationoutput = unification(bterm, arch, MAPRECORD, cryptopred)
                if unificationoutput == [1, 1]: 
                    return [1, 1] 
                else :
                    if unificationoutput == [1, 0]: 
                        return [1, 0] 
            
            return [0, 1] 



def checkInBasicHasComplete(listofMAPRECORD, bterm, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) : 
    
    unificationOK1 = 0
    
    MAPRECORDORIGIN = MAPRECORD.copy()
    
    
    # NO ATTACKER CASE
    if verifmode ==  1 :  
        for hasterm in SetlistofbasicsHAS : 
            MAPRECORD = MAPRECORDORIGIN.copy()
            if unification(bterm, hasterm, MAPRECORD, cryptopred)[0] == 1 : 
                listofMAPRECORD.append(MAPRECORD)
                unificationOK1 = 1
            
    # EXTERNAL ATTACKER CASE             
    elif verifmode ==  2 : 
        for hasterm in SetlistofbasicsHASATTEX : 
            MAPRECORD = MAPRECORDORIGIN.copy()
            if unification(bterm, hasterm, MAPRECORD, cryptopred)[0] == 1 : 
                listofMAPRECORD.append(MAPRECORD)
                unificationOK1 = 1
    
    # INSIDER ATTACKER CASE                    
    elif verifmode ==  3 : 
        for hasterm in SetlistofbasicsHASATTIN : 
            MAPRECORD = MAPRECORDORIGIN.copy()
            if unification(bterm, hasterm, MAPRECORD, cryptopred)[0] == 1 : 
                listofMAPRECORD.append(MAPRECORD)
                unificationOK1 = 1
    
    # Hybrid ATTACKER CASE                    
    elif verifmode ==  4 : 
        for hasterm in SetlistofbasicsHASATTHYB : 
            MAPRECORD = MAPRECORDORIGIN.copy()
            if unification(bterm, hasterm, MAPRECORD, cryptopred)[0] == 1 : 
                listofMAPRECORD.append(MAPRECORD)
                unificationOK1 = 1            
            
    MAPRECORD = MAPRECORDORIGIN.copy()
   
    proofOKnotOK = checkAgainstAbilitySet(listofMAPRECORD, MAPRECORD, bterm, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) 
    
    
    if (unificationOK1 == 0) and (proofOKnotOK == 0) : 
        return 0
    else : 
        return 1
        

    


def checkInBasicHas(listofMAPRECORD, bterm, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) : 
    
    strbterm = str(bterm)
    
    if verifmode ==  1 : # NO ATTACKER CASE
        strbasichas = list(map(tostring, SetlistofbasicsHAS))   
         
        if strbterm in strbasichas :
        
            return 1 
    
        else: 
            for hasterm in SetlistofbasicsHAS : 
                if unification(bterm, hasterm, MAPRECORD, cryptopred)[0] == 1 :            
                    return 1
            
    # EXTERNAL ATTACKER CASE
    elif verifmode ==  2 :  
        strbasichasattex = list(map(tostring, SetlistofbasicsHASATTEX)) 
        if strbterm in strbasichasattex : 
             return 1
        else: 
            for hasterm in SetlistofbasicsHASATTEX : 
                if unification(bterm, hasterm, MAPRECORD, cryptopred)[0] == 1 :  
                   return 1 
        
    # INSIDER ATTACKER CASE                    
    elif verifmode ==  3 : 
        strbasichasattin = list(map(tostring, SetlistofbasicsHASATTIN)) 
        if strbterm in strbasichasattin : 
            return 1
        else: 
            for hasterm in SetlistofbasicsHASATTIN : 
                if unification(bterm, hasterm, MAPRECORD, cryptopred)[0] == 1 :  
                   return 1 
               
    # Hybrid ATTACKER CASE                    
    elif verifmode ==  4 : 
        strbasichasatthyb = list(map(tostring, SetlistofbasicsHASATTHYB)) 
        if strbterm in strbasichasatthyb : 
            return 1
        else: 
            for hasterm in SetlistofbasicsHASATTHYB : 
                if unification(bterm, hasterm, MAPRECORD, cryptopred)[0] == 1 :  
                   return 1             
         
        
    if checkAgainstAbilitySet(listofMAPRECORD, MAPRECORD, bterm, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
        return 1
    
    return 0


#################################### In case of data types containing crypto elements ########################################### 
def checkInBasicHasCompleteCrypto(listofMAPRECORDCrypto, bterm, MAPRECORDCrypto, ruleindex, cryptopred, nestenc, verifmode) : 
    global AbilitySetCrypto
    
    unificationOK1 = 0
    unificationOK2 = 0
    unificationOK3 = 0
    
    MAPRECORDORIGINCrypto = MAPRECORDCrypto.copy()
    
    entity = bterm.arguments[0]   
    
    if verifmode ==  1 : # NO ATTACKER CASE
        for hasterm in SetlistofbasicsHAS : 
            MAPRECORDCrypto = MAPRECORDORIGINCrypto.copy()
            if unification(bterm, hasterm, MAPRECORDCrypto, cryptopred)[0] == 1 : 
                listofMAPRECORDCrypto.append(MAPRECORDCrypto)
                unificationOK1 = 1
         
    
        if str(entity) in HasAccessTo.keys():  
            for ent in HasAccessTo[str(entity)] :  
                for hasterm in SetlistofbasicsHAS : 
                    MAPRECORDCrypto = MAPRECORDORIGINCrypto.copy()
                    if unification(hasterm, replaceentity(bterm,ent), MAPRECORDCrypto, cryptopred)[0] == 1 : 
                        listofMAPRECORDCrypto.append(MAPRECORDCrypto)
                        unificationOK2 = 1
 
            
        if str(entity) in entityRelationRec.keys():  
            for ent in entityRelationRec[str(entity)] : 
                for hasterm in SetlistofbasicsHAS : 
                    MAPRECORDCrypto = MAPRECORDORIGINCrypto.copy()
                    if unification(hasterm, replaceentity(bterm,ent), MAPRECORDCrypto, cryptopred)[0] == 1 : 
                        listofMAPRECORDCrypto.append(MAPRECORDCrypto)
                        unificationOK3 = 1
    
    # EXTERNAL ATTACKER CASE                    
    elif verifmode ==  2 :  
        for hasterm in SetlistofbasicsHASATTEX : 
            MAPRECORDCrypto = MAPRECORDORIGINCrypto.copy()
            if unification(bterm, hasterm, MAPRECORDCrypto, cryptopred)[0] == 1 : 
                listofMAPRECORDCrypto.append(MAPRECORDCrypto)
                unificationOK1 = 1                
    
    # INSIDER ATTACKER CASE                    
    elif verifmode ==  3 : 
         for hasterm in SetlistofbasicsHASATTIN : 
            MAPRECORDCrypto = MAPRECORDORIGINCrypto.copy()
            if unification(bterm, hasterm, MAPRECORDCrypto, cryptopred)[0] == 1 : 
                listofMAPRECORDCrypto.append(MAPRECORDCrypto)
                unificationOK1 = 1  
                
    
    # HYBRID ATTACKER CASE                    
    elif verifmode ==  4 : 
         for hasterm in SetlistofbasicsHASATTHYB : 
            MAPRECORDCrypto = MAPRECORDORIGINCrypto.copy()
            if unification(bterm, hasterm, MAPRECORDCrypto, cryptopred)[0] == 1 : 
                listofMAPRECORDCrypto.append(MAPRECORDCrypto)
                unificationOK1 = 1  
                
      
    MAPRECORDCrypto = MAPRECORDORIGINCrypto.copy()
    
    proofOKnotOK = checkAgainstAbilitySetCrypto(listofMAPRECORDCrypto, MAPRECORDCrypto, bterm, ruleindex, cryptopred, nestenc, verifmode) 
    
    if (unificationOK1 == 0) and (unificationOK2 == 0) and (unificationOK3 == 0) and (proofOKnotOK == 0) :  
        return 0 
    else : 
        return 1
    
    
    
    

def checkInBasicHasCrypto(listofMAPRECORDCrypto, bterm, MAPRECORDCrypto, ruleindex, cryptopred, nestenc, verifmode) : 
    
    global AbilitySetCrypto
    
    entity = bterm.arguments[0]
    strbterm = str(bterm)
    
    if verifmode ==  1 : # NO ATTACKER CASE 
    
        strbasichas = list(map(tostring, SetlistofbasicsHAS))   
    
        if strbterm in strbasichas : 
            return 1 
    
        else: 
            for hasterm in SetlistofbasicsHAS : 
                if unification(bterm, hasterm, MAPRECORDCrypto, cryptopred)[0] == 1 : 
                    return 1
            
        if str(entity) in HasAccessTo:  
            for ent in HasAccessTo[str(entity)] :  
                if str(replaceentity(bterm,ent)) in strbasichas : 
                    return 1
                else : 
                    for hasterm in SetlistofbasicsHAS : 
                        if unification(hasterm, replaceentity(bterm,ent), MAPRECORDCrypto, cryptopred)[0] == 1 : 
                            return 1   
            
        if str(entity) in entityRelationRec:  
            for ent in entityRelationRec[str(entity)] : 
                if str(replaceentity(bterm,ent)) in strbasichas : 
                    return 1
                else : 
                    for hasterm in SetlistofbasicsHAS : 
                        if unification(hasterm, replaceentity(bterm,ent), MAPRECORDCrypto, cryptopred)[0] == 1 : 
                            return 1       
    
    # EXTERNAL ATTACKER CASE                    
    elif verifmode ==  2 :  
        strbasichasattex = list(map(tostring, SetlistofbasicsHASATTEX))    
        if strbterm in strbasichasattex : 
            return 1 
        else: 
            for hasterm in SetlistofbasicsHASATTEX : 
                if unification(bterm, hasterm, MAPRECORDCrypto, cryptopred)[0] == 1 : 
                    return 1
    
    # INSIDER ATTACKER CASE                    
    elif verifmode ==  3 : 
        strbasichasattin = list(map(tostring, SetlistofbasicsHASATTIN)) 
        if strbterm in strbasichasattin : 
            return 1
        else: 
            for hasterm in SetlistofbasicsHASATTIN : 
                if unification(bterm, hasterm, MAPRECORDCrypto, cryptopred)[0] == 1 :  
                   return 1 
               
    # HYBRID ATTACKER CASE                    
    elif verifmode ==  4 : 
        strbasichasatthyb = list(map(tostring, SetlistofbasicsHASATTHYB)) 
        if strbterm in strbasichasatthyb : 
            return 1
        else: 
            for hasterm in SetlistofbasicsHASATTHYB : 
                if unification(bterm, hasterm, MAPRECORDCrypto, cryptopred)[0] == 1 :  
                   return 1             
                
    
    if checkAgainstAbilitySetCrypto(listofMAPRECORDCrypto, MAPRECORDCrypto, bterm, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
        return 1
    
    return 0



def checkInUnique(bterm, uniquedata, MAPRECORD, cryptopred) : 
    strbterm = str(bterm)
    struniquedata = list(map(tostring, uniquedata))    
    
    if strbterm in struniquedata : 
        return 1 
    
    else: 
        for uniterm in uniquedata : 
            if unification(bterm, uniterm, MAPRECORD, cryptopred)[0] == 1 :  
                return 1
    
    return 0
   
   
    
def pred(architecture) :
    predlist = []
    for act in architecture : 
        predlist.append(act.predicate)
    return predlist



def convertHasAfter(term) : 
    if str(term.predicate) == "HasAfter" : 
        for arg in term.arguments : 
            if str(arg.predicate) == "time" : 
                return DataOrFact("HasUpTo(" + ",".join(list(map(tostring,term.arguments[:-1]))) + "," + "time(" + str(arg.arguments[0]) + "+1m)" + ")")
    else : return term




def reverselink(linkterm) :
    return "Link(" + str(linkterm.arguments[0]) + "," + str(linkterm.arguments[2]) + "," + str(linkterm.arguments[1]) + ")"


def reverselinkunique(linkterm) :
    return "LinkUnique(" + str(linkterm.arguments[0]) + "," + str(linkterm.arguments[2]) + "," + str(linkterm.arguments[1]) + ")"






def checkAgainstAbilitySet(listofMAPRECORD, VMAPRECORD, query, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) : 
    
    nextgoalslist = [query]
    
    if checkAgainstAbilitySetComplete(listofMAPRECORD, nextgoalslist, VMAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 :
        return 1
    else: 
       
        return 0    

################################ CHECK AGAINST THE INFERENCE RULESET and ARCHITECTURE #################################################    
def checkAgainstAbilitySetComplete(listofMAPRECORD, nextgoalslist, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) : 
    global AbilitySetConsent
    global AbilitySetHasUpto
    global AbilitySetHas
    global AbilitySetLink
    global AbilitySetLinkUnique
    global AbilitySetAttackerHas  
    global AbilitySetAttackerLink
    global AbilitySetAttackerLinkUnique 
    
    global crypthasnotneeded 
    
    MapRecordOrigin = MAPRECORD.copy()
    listofMAPRECORDOrigin = listofMAPRECORD.copy()
    
    if verifmode == 1 : # NO ATTACKER CASE
        if len(nextgoalslist) == 1 : 
            if str(nextgoalslist[0].predicate) in ["fwconsentcollected", "cconsentcollected", "uconsentcollected", "strconsentcollected"] :
                for i in range(len(AbilitySetConsent)) :
                    MAPRECORD = MapRecordOrigin.copy()
                    listofMAPRECORD = listofMAPRECORDOrigin.copy()
                    if proofTree(listofMAPRECORD, nextgoalslist[0], i, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
                        return 1 
                return 0
            elif  str(nextgoalslist[0].predicate) in ["HasUpTo", "HasAfter"] :
                for i in range(len(AbilitySetHasUpto)) :
                    MAPRECORD = MapRecordOrigin.copy()
                    listofMAPRECORD = listofMAPRECORDOrigin.copy()
                    if proofTree(listofMAPRECORD, nextgoalslist[0], i, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
                        return 1 
                return 0
            elif  str(nextgoalslist[0].predicate) == "Has" :
                for i in range(len(AbilitySetHas)) :
                    MAPRECORD = MapRecordOrigin.copy()
                    if proofTree(listofMAPRECORD, nextgoalslist[0], i, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
                        return 1 
                return 0
            elif  str(nextgoalslist[0].predicate) == "Link" :
                for i in range(len(AbilitySetLink)) :
                    MAPRECORD = MapRecordOrigin.copy()
                    listofMAPRECORD = listofMAPRECORDOrigin.copy()
                    if proofTree(listofMAPRECORD, nextgoalslist[0], i, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
                        return 1 
                return 0
            elif  str(nextgoalslist[0].predicate) == "LinkUnique" :
                for i in range(len(AbilitySetLinkUnique)) :
                    MAPRECORD = MapRecordOrigin.copy()
                    listofMAPRECORD = listofMAPRECORDOrigin.copy()
                    if proofTree(listofMAPRECORD, nextgoalslist[0], i, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
                        return 1 
                return 0
        elif len(nextgoalslist) > 1 : # at least two goals
            if str(nextgoalslist[0].predicate) in ["fwconsentcollected", "cconsentcollected", "uconsentcollected", "strconsentcollected"] :
                for i in range(len(AbilitySetConsent)) :
                    MAPRECORD = MapRecordOrigin.copy()
                    listofMAPRECORD = listofMAPRECORDOrigin.copy()
                    if proofTree(listofMAPRECORD, nextgoalslist[0], i, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
                        if checkAgainstAbilitySetComplete(listofMAPRECORD, nextgoalslist[1:], MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 :
                            return 1
                return 0 #if no rule can be used in the proof.
            elif str(nextgoalslist[0].predicate) in ["HasUpTo", "HasAfter"] :
                for i in range(len(AbilitySetHasUpto)) :
                    MAPRECORD = MapRecordOrigin.copy()
                    listofMAPRECORD = listofMAPRECORDOrigin.copy()
                    if proofTree(listofMAPRECORD, nextgoalslist[0], i, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
                        if checkAgainstAbilitySetComplete(listofMAPRECORD, nextgoalslist[1:], MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 :
                            return 1
                return 0 #if no rule can be used in the proof.
            elif str(nextgoalslist[0].predicate) == "Has" :
                for i in range(len(AbilitySetHas)) :
                    MAPRECORD = MapRecordOrigin.copy()
                    listofMAPRECORD = listofMAPRECORDOrigin.copy()
                    if proofTree(listofMAPRECORD, nextgoalslist[0], i, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
                        if checkAgainstAbilitySetComplete(listofMAPRECORD, nextgoalslist[1:], MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 :
                            return 1
                return 0 #if no rule can be used in the proof.
            elif str(nextgoalslist[0].predicate) == "Link" :
                for i in range(len(AbilitySetLink)) :
                    MAPRECORD = MapRecordOrigin.copy()
                    listofMAPRECORD = listofMAPRECORDOrigin.copy()
                    if proofTree(listofMAPRECORD, nextgoalslist[0], i, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
                        if checkAgainstAbilitySetComplete(listofMAPRECORD, nextgoalslist[1:], MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 :
                            return 1
                return 0 #if no rule can be used in the proof.
            elif str(nextgoalslist[0].predicate) == "LinkUnique" :
                for i in range(len(AbilitySetLinkUnique)) :
                    MAPRECORD = MapRecordOrigin.copy()
                    listofMAPRECORD = listofMAPRECORDOrigin.copy()
                    if proofTree(listofMAPRECORD, nextgoalslist[0], i, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
                        if checkAgainstAbilitySetComplete(listofMAPRECORD, nextgoalslist[1:], MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 :
                            return 1
                return 0 #if no rule can be used in the proof.
        else: 
            print("ERROR: len(nextgoalslist) == 0")    
    # ALL ATTACKER CASES
    else : 
        if len(nextgoalslist) == 1 : 
            if  str(nextgoalslist[0].predicate) == "Has" :
                for i in range(len(AbilitySetAttackerHas)) :
                    MAPRECORD = MapRecordOrigin.copy()
                    if proofTree(listofMAPRECORD, nextgoalslist[0], i, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
                        return 1 
                return 0
            elif  str(nextgoalslist[0].predicate) == "Link" :
                for i in range(len(AbilitySetAttackerLink)) :
                    MAPRECORD = MapRecordOrigin.copy()
                    listofMAPRECORD = listofMAPRECORDOrigin.copy()
                    if proofTree(listofMAPRECORD, nextgoalslist[0], i, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
                        return 1 
                return 0
            elif  str(nextgoalslist[0].predicate) == "LinkUnique" :
                for i in range(len(AbilitySetAttackerLinkUnique)) :
                    MAPRECORD = MapRecordOrigin.copy()
                    listofMAPRECORD = listofMAPRECORDOrigin.copy()
                    if proofTree(listofMAPRECORD, nextgoalslist[0], i, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
                        return 1 
                return 0
        elif len(nextgoalslist) > 1 : # at least two goals
            if str(nextgoalslist[0].predicate) == "Has" :
                for i in range(len(AbilitySetAttackerHas)) :
                    MAPRECORD = MapRecordOrigin.copy()
                    listofMAPRECORD = listofMAPRECORDOrigin.copy()
                    if proofTree(listofMAPRECORD, nextgoalslist[0], i, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
                        if checkAgainstAbilitySetComplete(listofMAPRECORD, nextgoalslist[1:], MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 :
                            return 1
                return 0 #if no rule can be used in the proof.
            elif str(nextgoalslist[0].predicate) == "Link" :
                for i in range(len(AbilitySetAttackerLink)) :
                    MAPRECORD = MapRecordOrigin.copy()
                    listofMAPRECORD = listofMAPRECORDOrigin.copy()
                    if proofTree(listofMAPRECORD, nextgoalslist[0], i, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
                        if checkAgainstAbilitySetComplete(listofMAPRECORD, nextgoalslist[1:], MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 :
                            return 1
                return 0 #if no rule can be used in the proof.
            elif str(nextgoalslist[0].predicate) == "LinkUnique" :
                for i in range(len(AbilitySetAttackerLinkUnique)) :
                    MAPRECORD = MapRecordOrigin.copy()
                    listofMAPRECORD = listofMAPRECORDOrigin.copy()
                    if proofTree(listofMAPRECORD, nextgoalslist[0], i, MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
                        if checkAgainstAbilitySetComplete(listofMAPRECORD, nextgoalslist[1:], MAPRECORD, uniquedata, archMeta, architecture, archPseudo, archTime, ruleindex, cryptopred, nestenc, verifmode) == 1 :
                            return 1
                return 0 #if no rule can be used in the proof.
        else: 
            print("ERROR: len(nextgoalslist) == 0")    
    
       
def termsLength(term) :
    length = 0
    if len(str(term)) > 0 : 
        length += 1
        for tm in term.arguments : 
            length += termsLength(tm) 
        return length

############################################ Building the proof tree for a goal/sub-goal #################################################
def proofTree(listofMAPRECORD, query, i, MAPRECORD, unique, Meta, arch, Pseudo, Time, ruleindex, crypto, nest, verifmode) : 
    global AbilitySetConsent
    global AbilitySetHasUpto
    global AbilitySetHas
    global AbilitySetLink
    global AbilitySetLinkUnique
    setofMapRecunificationOK = []
    hasgoalslist = []
    archgoalslist = []

    queryvalid = 1
    
    if verifmode == 1 : # NO ATTACKER CASE 
        if str(query.predicate) in ["fwconsentcollected", "cconsentcollected", "uconsentcollected", "strconsentcollected"] : 
            AbilitySet = AbilitySetConsent
        elif str(query.predicate) in ["HasUpTo", "HasAfter"] : 
            AbilitySet = AbilitySetHasUpto
        elif str(query.predicate) == "Has" : 
            AbilitySet = AbilitySetHas
        elif str(query.predicate) == "Link" : 
            AbilitySet = AbilitySetLink
        elif str(query.predicate) == "LinkUnique" : 
            AbilitySet = AbilitySetLinkUnique
    # ALL ATTACKER CASES
    else : 
        if str(query.predicate) == "Has" : 
            AbilitySet = AbilitySetAttackerHas
        elif str(query.predicate) == "Link" : 
            AbilitySet = AbilitySetAttackerLink
        elif str(query.predicate) == "LinkUnique" : 
            AbilitySet = AbilitySetAttackerLinkUnique
    
    convertedstr = str(query).replace(";",",")  
    convertedterm = DataOrFact(convertedstr)
    currterm = evfact(convertedterm,MAPRECORD)      
           
    
    goalstring = str(AbilitySet[i].goals)
    headstring = str(AbilitySet[i].head)
    currstring = str(currterm)
        
    ######################################## TO AVOID INFINITE LOOP LIMIT THE NUMBER OF NESTED CRYPTO FUNC. #################################################                                                                                                       
    if (len(headstring.split("senc("))==1 and len(headstring.split("aenc("))==1 and len(headstring.split("mac("))==1) and (len(goalstring.split("senc(")) + len(goalstring.split("aenc(")) + len(goalstring.split("mac(")) >= 4) and (len(currstring.split("senc(")) + len(currstring.split("aenc(")) + len(currstring.split("mac(")) > nest + 1) :   
        return 0    
        
        
    if AbilitySet[i].head.predicate != currterm.predicate : 
        return 0
            
    if len(AbilitySet[i].head.arguments) != len(currterm.arguments) : 
        return 0 
    
    if unification(currterm, AbilitySet[i].head, MAPRECORD, crypto)[0] == 1 : 
            
        goalslist = AbilitySet[i].goals
            
        if len(str(AbilitySet[i]).split("Anytypeinccrypto(")) == 1 and len(str(AbilitySet[i]).split("Anytypeinccrypto1(")) == 1 and len(str(AbilitySet[i]).split("Anytypeinccrypto2(")) == 1 :  
                goalslist.sort(reverse = True, key=termsLength)   
                
        AbilitySet[i] = renamerule(AbilitySet[i])   
        
         
        if len(goalslist) == 3 :  
           for termarg in goalslist : 
                if queryvalid == 0 :  
                    return 0 
            
                convertstr = str(termarg).replace(";",",")  
                convertterm = DataOrFact(convertstr)
                boundterm = evfact(convertterm,MAPRECORD)
                
                
                if goalslist.index(termarg) == 0 : 
                    if checkInBasicHasComplete(listofMAPRECORD, boundterm, MAPRECORD, unique, Meta, arch, Pseudo, Time, ruleindex, crypto, nest, verifmode) == 0 :
                       
                        queryvalid = queryvalid * 0
                       
                elif goalslist.index(termarg) == 1 : 
                    if len(listofMAPRECORD) > 0 :
                        usedmaprecslist = []
                        for maprec in listofMAPRECORD : 
                            convertstr = str(boundterm).replace(";",",")  
                            convertterm = DataOrFact(convertstr)
                            boundlastarch = evfact(convertterm,maprec)
                            if numberofvar(boundlastarch) == 0 :  
                                hasgoalslist.append(boundlastarch)
                                usedmaprecslist.append(maprec)
                        
                        for i in range(len(hasgoalslist)) :
                           
                            checkinhas = checkInBasicHas(listofMAPRECORD, hasgoalslist[i], MAPRECORD, unique, Meta, arch, Pseudo, Time, ruleindex, crypto, nest, verifmode) 
                            if checkinhas == 1 : 
                                convertstr = str(goalslist[2]).replace(";",",")  
                                convertterm = DataOrFact(convertstr)
                                boundterm = evfact(convertterm,usedmaprecslist[i])
                               
                                if str(boundterm.predicate) == "Unique" : 
                                    queryvalid = queryvalid * checkInUnique(boundterm, unique, MAPRECORD, crypto)
                                    
                                    break
                                else: 
                                    
                                    queryvalid = queryvalid * checkinhas 
                                    
                                    break
                            elif (i == len(hasgoalslist)-1) and checkinhas == 0 : 
                                queryvalid = queryvalid * checkinhas
                                
                    else: 
                        queryvalid = 0
                else: 
                    pass
           if (queryvalid == 1)  :     
               return 1
           else : 
               return 0  
        elif len(goalslist) == 2 :   
            if str(goalslist[1].predicate) == "Unique" :   
                convertstr2 = str(goalslist[1]).replace(";",",")  
                convertterm2 = DataOrFact(convertstr2)
                boundunique = evfact(convertterm2,MAPRECORD)   
            
            for termarg in goalslist : 
                if queryvalid == 0 :  
                    return 0 
            
                convertstr = str(termarg).replace(";",",")  
                convertterm = DataOrFact(convertstr)
                boundterm = evfact(convertterm,MAPRECORD)
                
                if str(boundterm.predicate) in predefinedarchpred :  
                    if  goalslist.index(termarg) == 0 : 
                        
                        setofMapRecunificationOK = checkInArchComplete(boundterm, arch, Meta, Pseudo, Time, MAPRECORD, crypto)    
                       
                        if len(setofMapRecunificationOK) == 0 : 
                            queryvalid = queryvalid * 0
                    else :  
                            
                        for maprec in setofMapRecunificationOK : 
                            convertstr = str(boundterm).replace(";",",")  
                            convertterm = DataOrFact(convertstr)
                            boundlastarch = evfact(convertterm,maprec)
                            archgoalslist.append(boundlastarch)
                        for archgoal in archgoalslist : 
                            checkinarch = checkInArch(archgoal, arch, Meta, Pseudo, Time, MAPRECORD, crypto) 
                            if checkinarch[0] == 1 : 
                                queryvalid = queryvalid * checkinarch[0]                    
                                break
                            elif (archgoalslist.index(archgoal) == len(archgoalslist)-1) and checkinarch[0] == 0 : 
                                queryvalid = queryvalid * checkinarch[0]
                elif str(boundterm.predicate) == "Link" : 
                     if goalslist.index(termarg) == 0 : 
                         nextgoalslist = [boundterm]    
                         checkinunique = checkAgainstAbilitySetComplete(listofMAPRECORD, nextgoalslist, MAPRECORD, unique, Meta, arch, Pseudo, Time, ruleindex, crypto, nest, verifmode)  
                         if checkinunique == 1 : 
                             queryvalid = queryvalid * checkInUnique(boundunique, unique, MAPRECORD, crypto)    
                               
                         else : 
                             queryvalid = queryvalid * 0
                     else :
                         pass
                elif str(boundterm.predicate) == "Has" :   
                    if goalslist.index(termarg) == 0 : 
                        if checkInBasicHasComplete(listofMAPRECORD, boundterm, MAPRECORD, unique, Meta, arch, Pseudo, Time, ruleindex, crypto, nest, verifmode) == 0 :                    
                            queryvalid = queryvalid * 0
                       
                    else: 
                        if len(listofMAPRECORD) > 0 :
                            for maprec in listofMAPRECORD : 
                                convertstr = str(boundterm).replace(";",",")  
                                convertterm = DataOrFact(convertstr)
                                boundlastarch = evfact(convertterm,maprec)
                                if numberofvar(boundlastarch) == 0 :  
                                    hasgoalslist.append(boundlastarch)
                            
                            for archgoal in hasgoalslist : 
                                checkinhas = checkInBasicHas(listofMAPRECORD, archgoal, MAPRECORD, unique, Meta, arch, Pseudo, Time, ruleindex, crypto, nest, verifmode) 
                                if checkinhas == 1 : 
                                    queryvalid = queryvalid * checkinhas 
                                    break
                                elif (hasgoalslist.index(archgoal) == len(hasgoalslist)-1) and checkinhas == 0 : 
                                    queryvalid = queryvalid * checkinhas
                        else: 
                            queryvalid = 0
            if (queryvalid == 1)  :     
                return 1
            else : 
                return 0     
            
        elif len(goalslist) == 1 :
            for termarg in goalslist : 
                if queryvalid == 0 :  
                    return 0 
            
                convertstr = str(termarg).replace(";",",")  
                convertterm = DataOrFact(convertstr)
                boundterm = evfact(convertterm,MAPRECORD)
                
                if str(boundterm.predicate) in predefinedarchpred :  
                    checkinarch = checkInArch(listofMAPRECORD, boundterm, arch, Meta, Pseudo, Time, MAPRECORD, crypto)
                    queryvalid = queryvalid * checkinarch[0]
                    
                else:   
                    queryvalid = queryvalid * checkInBasicHas(listofMAPRECORD, boundterm, MAPRECORD, unique, Meta, arch, Pseudo, Time, ruleindex, crypto, nest, verifmode)
                    
            if (queryvalid == 1)  :     
                return 1
            else : 
                return 0           
                  
    else : 
        AbilitySet[i] = renamerule(AbilitySet[i])
        return 0      
     



def checkAgainstAbilitySetCrypto(listofMAPRECORDCrypto, VMAPRECORDCrypto, query, ruleindex, cryptopred, nestenc, verifmode) : 
    nextgoalslist = [query]
    
    if checkAgainstAbilitySetCryptoComplete(listofMAPRECORDCrypto, nextgoalslist, VMAPRECORDCrypto, ruleindex, cryptopred, nestenc, verifmode) == 1 :
       
        return 1
    else: 
       
        return 0    


def checkAgainstAbilitySetCryptoComplete(listofMAPRECORDCrypto, nextgoalslist, MAPRECORDCrypto, ruleindex, cryptopred, nestenc, verifmode) : 
    global AbilitySetCrypto
     
    MapRecordOriginCrypto = MAPRECORDCrypto.copy()
    listofMAPRECORDCryptoOrigin = listofMAPRECORDCrypto.copy()
    
    if len(nextgoalslist) == 1 : 
       
        for i in range(len(AbilitySetCrypto)) :
            MAPRECORDCrypto = MapRecordOriginCrypto.copy()
            listofMAPRECORDCrypto = listofMAPRECORDCryptoOrigin.copy()
            
            if proofTreeCrypto(listofMAPRECORDCrypto, nextgoalslist[0], i, MAPRECORDCrypto, ruleindex, cryptopred, nestenc, verifmode) == 1 : 
                return 1 
        return 0
    elif len(nextgoalslist) > 1 :
        for i in range(len(AbilitySetCrypto)) :
            MAPRECORDCrypto = MapRecordOriginCrypto.copy()
            listofMAPRECORDCrypto = listofMAPRECORDCryptoOrigin.copy()
            
            if proofTreeCrypto(listofMAPRECORDCrypto, nextgoalslist[0], i, MAPRECORDCrypto, ruleindex, cryptopred, nestenc, verifmode) == 1 :  
                if checkAgainstAbilitySetCryptoComplete(listofMAPRECORDCrypto, nextgoalslist[1:], MAPRECORDCrypto, ruleindex, cryptopred, nestenc, verifmode) == 1 :
                    return 1
        return 0 
    else: 
        print("ERROR: len(nextgoalslist) == 0")
    


    
def proofTreeCrypto(listofMAPRECORDCrypto, query, i, MAPRECORD, ruleindex, cryptopred, nestenc, verifmode) :     
    global AbilitySetCrypto

    queryvalidcrypto = 1
    
    goalslist = []
    goalslistcrypto = []
    
   
    convertedstr = str(query).replace(";",",") 
    convertedterm = DataOrFact(convertedstr)
    currterm = evfact(convertedterm, MAPRECORD)     
    
    
    goalstring = str(AbilitySetCrypto[i].goals)
    headstring = str(AbilitySetCrypto[i].head)
    currstring = str(currterm)
        
    
    if (len(headstring.split("senc("))==1 and len(headstring.split("aenc("))==1 and len(headstring.split("mac("))==1) and (len(goalstring.split("senc(")) + len(goalstring.split("aenc(")) + len(goalstring.split("mac(")) >= 4) and (len(currstring.split("senc(")) + len(currstring.split("aenc(")) + len(currstring.split("mac(")) > nestenc + 1) :   # nestenc = 3 then 2 + 1 + 1 = 3 + 1, namely, only 1 crypto func is allowed.  
        return 0   

    if len(AbilitySetCrypto[i].head.arguments) != len(currterm.arguments) : 
        return 0 
        
    if unification(currterm, AbilitySetCrypto[i].head, MAPRECORD, cryptopred)[0] == 1 :   
        goalslist = AbilitySetCrypto[i].goals
        goalslist.sort(reverse = True, key=termsLength)   
        
        AbilitySetCrypto[i] = renamerule(AbilitySetCrypto[i])   
        
           
        for termarg in goalslist : 
            if queryvalidcrypto == 0 :  
                return 0 
                        
            convertstr = str(termarg).replace(";",",")  
            convertterm = DataOrFact(convertstr)
            boundterm = evfact(convertterm, MAPRECORD)
                
            if len(goalslist) > 1 : 
                if goalslist.index(termarg) == 0 :  
                    if checkInBasicHasCompleteCrypto(listofMAPRECORDCrypto, boundterm, MAPRECORD, 0, cryptopred, nestenc, verifmode) == 0:  
                        queryvalidcrypto = queryvalidcrypto * 0
                else :    
                    for maprec in listofMAPRECORDCrypto : 
                        convertstr = str(boundterm).replace(";",",")  
                        convertterm = DataOrFact(convertstr)
                        boundlast = evfact(convertterm,maprec)
                        goalslistcrypto.append(boundlast)
                    for goal in goalslistcrypto : 
                        checkinhas = checkInBasicHasCrypto(listofMAPRECORDCrypto, goal, MAPRECORD, 0, cryptopred, nestenc, verifmode) 
                        if checkinhas == 1 : 
                            queryvalidcrypto = queryvalidcrypto * checkinhas 
                            break
                        elif (goalslistcrypto.index(goal) == len(goalslistcrypto)-1) and checkinhas == 0 : 
                            queryvalidcrypto = queryvalidcrypto * checkinhas
            elif len(goalslist) == 1 : 
                queryvalidcrypto = queryvalidcrypto * checkInBasicHasCrypto(listofMAPRECORDCrypto, boundterm, MAPRECORD, 0, cryptopred, nestenc, verifmode) 
                     
        if queryvalidcrypto == 1 : 
            return 1
        else : 
            return 0  
        
    else : 
        AbilitySetCrypto[i] = renamerule(AbilitySetCrypto[i])   
        return 0


################################ RESET THE SET OF UNIFIERS AND THE INFERENCE RULES (REQUIRED FOR CORRECT RESOLUTION) #################################################
def resetAbilitysetsMaprecords() : 
    global VARMAPRECORD
    global VARMAPRECORDCrypto
    global AbilitySetConsent
    global AbilitySetHasUpto
    global AbilitySetHas
    global AbilitySetLink
    global AbilitySetLinkUnique
    global AbilitySetCrypto
    global AbilitySetAttackerLinkUnique
    global AbilitySetAttackerLink
    global AbilitySetAttackerHas
    
    VARMAPRECORD = {}
    VARMAPRECORDCrypto = {}
    
    
    
    AbilitySetConsent = [InfRule("fwconsentcollected(EE,XX,Third):-receiveat(EE,fwconsent(XX,Third),time(TN)),receiveat(Third,XX,time(TN))"),
             InfRule("fwconsentcollected(EX,XE,Thi):-receiveat(EX,fwconsent(XE,Thi),time(TN)),receiveat(Thi,Anytypeinccrypto(XE),time(TN))"),
             InfRule("cconsentcollected(QQ,S):-receiveat(QQ,cconsent(S,QK),time(TM)),receiveat(QK,S,time(TM))"),  
             InfRule("cconsentcollected(QX,SX):-receiveat(QX,cconsent(SX,QZ),time(TM)),receiveat(QZ,Anytypeinccrypto(SX),time(TM))"),  
             InfRule("uconsentcollected(LX,UX):-receiveat(LX,uconsent(UX,LZ),time(TI)),createat(LZ,UX,time(TI))"),
             InfRule("uconsentcollected(LL,UU):-receiveat(LL,uconsent(UU,LK),time(TI)),createat(LK,Anytypeinccrypto(UU),time(TI))"), 
             InfRule("uconsentcollected(LB,UB):-receiveat(LB,uconsent(UB,BT),time(TA)),calculateat(BT,UB,time(TA))"), 
             InfRule("uconsentcollected(LA,UA):-receiveat(LA,uconsent(UA,LT),time(TA)),calculateat(LT,Anytypeinccrypto(UA),time(TA))"),
             InfRule("strconsentcollected(LS,US):-receiveat(LS,sconsent(US,UJ),time(TS)),storeat(UJ,US,time(TS))"), 
             InfRule("strconsentcollected(LP,UW):-receiveat(LP,sconsent(UW,UT),time(TW)),storeat(UT,Anytypeinccrypto(UW),time(TW))")]  
             
    AbilitySetHasUpto = [InfRule("HasUpTo(RR,NN,time(TT)):-store(RR,NN),deletewithin(RR,NN,time(TT))"), 
             InfRule("HasUpTo(RL,NL,time(TL)):-storeat(RL,NL,time(AT)),deletewithin(RL,NL,time(TL))")]

    AbilitySetHas = [InfRule("Has(trusted,_anypred(ds,M@)):-Has(trusted,_anypred(M@,p(ds)))"), 
             InfRule("Has(trusted,_anypred(M@,ds)):-Has(trusted,_anypred(M@,p(ds)))")]
             
             
    AbilitySetLink = [InfRule("Link(OKN,BZN,JMN):-calculatefrom(OKN,BZN,FRN),calculatefrom(OKN,JMN,FRN)"),
             InfRule("Link(OKM,BZM,JMM):-calculatefromat(OKM,BZM,FRM,time(TLM)),calculatefromat(OKM,JMM,FRM,time(TLM))"),
             InfRule("Link(OKL,BZL,JML):-own(OKL,BZL),own(OKL,JML)"), #
             InfRule("Link(C,V,W):-Has(C,_anypredA(V,Q!,meta(K))),Has(C,_anypredB(W,P!,meta(K)))"),
             InfRule("Link(O,B,J):-Has(O,_anypredC(B,U)),Has(O,_anypredD(J,U))")]

    AbilitySetLinkUnique = [InfRule("LinkUnique(OKE,BZE,JME):-calculatefrom(OKE,BZE,FRE),calculatefrom(OKE,JME,FRE)"),
             InfRule("LinkUnique(OKD,BZD,JMD):-calculatefromat(OKD,BZD,FRD,time(TLD)),calculatefromat(OKD,JMD,FRD,time(TLD))"),           
             InfRule("LinkUnique(OKC,BZC,JMC):-calculatefrom(OKC,BZC,FRC),calculatefrom(OKC,JMC,FRC)"), #
             InfRule("LinkUnique(OK,BZ,JM):-own(OK,BZ),own(OK,JM)"), #
             InfRule("LinkUnique(OOA,BOA,JOA):-Has(OOA,_anypreDA(BOA,UOA)),Has(OOA,_anypreDB(JOA,UOA)),Unique(UOA)"), 
             #InfRule("LinkUnique(OOB,BOB,JOB):-Has(OOB,_anypreDC(BOB,UOB)),Has(OOB,_anypreDD(JOB,Anytypeinccrypto(UOB))),Unique(UOB)"),      
             #InfRule("LinkUnique(OOC,BOC,JOC):-Has(OOC,_anypreDE(BOC,UOC)),Has(OOC,_anypreDF(Anytypeinccrypto(JOC),UOC)),Unique(UOC)"),      
             #InfRule("LinkUnique(OOD,BOD,JOD):-Has(OOD,_anypreDG(BOD,UOD)),Has(OOD,_anypreDH(Anytypeinccrypto1(JOD),Anytypeinccrypto2(UOD))),Unique(UOD)"),      
             InfRule("LinkUnique(OOE,BOE,JOE):-Has(OOE,_anypreDI(BOE,UOE)),Has(OOE,_anypreDJ(UOE,JOE)),Unique(UOE)"), 
             InfRule("LinkUnique(OOF,BOF,JOF):-Has(OOF,_anypreDK(UOF,BOF)),Has(OOF,_anypreDL(JOF,UOF)),Unique(UOF)"), 
             InfRule("LinkUnique(OOG,BOG,JOG):-Has(OOG,_anypreDM(UOG,BOG)),Has(OOG,_anypreDN(UOG,JOG)),Unique(UOG)"),
             InfRule("LinkUnique(KKA,BKA,JKA):-Link(KKA,BKA,JKA),Unique(BKA)"),
             InfRule("LinkUnique(KKB,BKB,JKB):-Link(KKB,BKB,JKB),Unique(JKB)")]
             

    AbilitySetAttackerHas =  [InfRule("Has(att,GATT):-Has(att,senc(GATT,IATT)),Has(att,IATT)"),
                          InfRule("Has(att,QATT):-Has(att,aenc(QATT,TATT)),Has(att,sk(TATT))")] 

    AbilitySetAttackerLink =  [InfRule("Link(att,VATT,WATT):-Has(att,_anypredA(VATT,QATT!,meta(KATT))),Has(att,_anypredB(WATT,PATT!,meta(KATT)))"),
             InfRule("Link(att,BATT,JATT):-Has(att,_anypredC(BATT,UATT)),Has(att,_anypredD(JATT,UATT))"),
             #InfRule("Link(att,BPATT,JPATT):-Has(att,_anypredE(BPATT,UPATT)),Has(att,_anypredF(JPATT,Anytypeinccrypto(UPATT)))"),
             #InfRule("Link(att,BAATT,JAATT):-Has(att,_anypredG(BAATT,UKATT)),Has(att,_anypredH(Anytypeinccrypto(JAATT),UKATT))"),
             #InfRule("Link(att,BSATT,JSATT):-Has(att,_anypredI(BSATT,ULATT)),Has(att,_anypredJ(Anytypeinccrypto1(JSATT),Anytypeinccrypto2(ULATT)))"),
             InfRule("Link(att,BDATT,JDATT):-Has(att,_anypredK(BDATT,UDATT)),Has(att,_anypredL(UDATT,JDATT))"), 
             InfRule("Link(att,BEATT,JEATT):-Has(att,_anypredM(UEATT,BEATT)),Has(att,_anypredN(JEATT,UEATT))"), 
             InfRule("Link(att,BFATT,JFATT):-Has(att,_anypredQ(UFATT,BFATT)),Has(att,_anypredP(UFATT,JFATT))")]

    AbilitySetAttackerLinkUnique =  [InfRule("LinkUnique(att,BOAA,JOAA):-Has(att,_anypreDA(BOAA,UOAA)),Has(att,_anypreDB(JOAA,UOAA)),Unique(UOAA)"), 
             #InfRule("LinkUnique(att,BOBA,JOBA):-Has(att,_anypreDC(BOBA,UOBA)),Has(att,_anypreDD(JOBA,Anytypeinccrypto(UOBA))),Unique(UOBA)"),     
             #InfRule("LinkUnique(att,BOCA,JOCA):-Has(att,_anypreDE(BOCA,UOCA)),Has(att,_anypreDF(Anytypeinccrypto(JOCA),UOCA)),Unique(UOCA)"),      
             #InfRule("LinkUnique(att,BODA,JODA):-Has(att,_anypreDG(BODA,UODA)),Has(att,_anypreDH(Anytypeinccrypto1(JODA),Anytypeinccrypto2(UODA))),Unique(UODA)"),      
             InfRule("LinkUnique(att,BOEA,JOEA):-Has(att,_anypreDI(BOEA,UOEA)),Has(att,_anypreDJ(UOEA,JOEA)),Unique(UOEA)"), 
             InfRule("LinkUnique(att,BOFA,JOFA):-Has(att,_anypreDK(UOFA,BOFA)),Has(att,_anypreDL(JOFA,UOFA)),Unique(UOFA)"), 
             InfRule("LinkUnique(att,BOGA,JOGA):-Has(att,_anypreDM(UOGA,BOGA)),Has(att,_anypreDN(UOGA,JOGA)),Unique(UOGA)"),
             InfRule("LinkUnique(att,BKAA,JKAA):-Link(att,BKAA,JKAA),Unique(BKAA)"),
             InfRule("LinkUnique(att,BKBA,JKBA):-Link(att,BKBA,JKBA),Unique(JKBA)")]            
    
    
    AbilitySetCrypto = [InfRule("Has(Z,Y):-Has(Z,senc(Y,X)),Has(Z,X)"), 
                        InfRule("Has(P,Q):-Has(P,aenc(Q,T)),Has(P,sk(T))")]  

    
    
def ReplaceEntitiesInSetHas(strent,strwithent) : 
    newset = set()
    
    for term in ReclistofbasicsHAS[strent] : 
        newset.add(replaceentity(term, strwithent))
        
    return newset


def ReplaceEntitiesInSetArch(strent,strwithent) : 
    newset = set()
    
    for term in Recofactions[strent] : 
        newset.add(replaceentity(term, strwithent))
        
    return newset

def ReplaceEntitiesInSetLink(strent,strwithent) : 
    newset = set()
    
    for term in ReclistofbasicsLink[strent] : 
        newset.add(replaceentity(term, strwithent))
        
    return newset    
         
    
################################ Verification in the benign (no attacker) case #################################################
def VerifyPolicy(queryfwconsent, querycconsent, queryuconsent, queryhas, querynothas, queryhasafter, querylink, querynotlink, querylinkunique, querynotlinkunique, querysconsent, uniquedata, archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc) : 
    global SetlistofbasicsHAS
    global SetlistofbasicsLink
    global SetlistofbasicsLinkUnique
    global cPurposePol
    global cPurposeArch
    global uPurposePol
    global uPurposeArch
    verifmode = 1 # no attakcer
    
    isThereRecvforCons = {}
    
    t = time.process_time()  #start measure time.
    
    resetAbilitysetsMaprecords() 
    
    SetlistofbasicsHAS.clear()  
    SetlistofbasicsLink.clear() 
    
    #StringSetlistofbasicsLink = set()
    StringSetlistofbasicsLinkUnique = set()
    
    #setnotwellformedarch = set()  
    isprivacyviolated = 0
    isdprviolated = 0
    isfunctionalviolated = 0
    vresult = ""
    vdetails = ""
    
    
    CopyarchPseudo = set()
    CopyarchMeta = set()
    CopyarchTime = set()
    Copyarch = set()
    UnionarchPseudo = set()
    UnionarchMeta = set()
    UnionarchTime = set()
    Unionarch = set()
    for ap in archpseudo : 
        if (str(ap.arguments[0]) in entityRelationRec) and  len(entityRelationRec[str(ap.arguments[0])]) > 0 : 
            for ent in entityRelationRec[str(ap.arguments[0])] : 
                parentarchpseudo = replaceentity(ap, ent) 
                CopyarchPseudo.add(parentarchpseudo)
    UnionarchPseudo = archpseudo.union(CopyarchPseudo)
    for am in archmeta : 
        if (str(am.arguments[0]) in entityRelationRec) and  len(entityRelationRec[str(am.arguments[0])]) > 0 : 
            for ent in entityRelationRec[str(am.arguments[0])] : 
                parentarchmeta = replaceentity(am, ent) 
                CopyarchMeta.add(parentarchmeta)
    UnionarchMeta = archmeta.union(CopyarchMeta)   
    for at in archtime : 
        if (str(at.arguments[0]) in entityRelationRec) and  len(entityRelationRec[str(at.arguments[0])]) > 0 : 
            for ent in entityRelationRec[str(at.arguments[0])] : 
                parentarchtime = replaceentity(at, ent) 
                CopyarchTime.add(parentarchtime)
    UnionarchTime = archtime.union(CopyarchTime)
    for ar in architecture : 
        if (str(ar.arguments[0]) in entityRelationRec) and  len(entityRelationRec[str(ar.arguments[0])]) > 0 : 
            for ent in entityRelationRec[str(ar.arguments[0])] : 
                parentarch = replaceentity(ar, ent) 
                Copyarch.add(parentarch)
    Unionarch = architecture.union(Copyarch)
    
    
    if len(cPurposePolAll - cPurposeArch) > 0 : 
        
        isfunctionalviolated = 1
        
        for cpurppol in cPurposePolAll.difference(cPurposeArch) : 
            if len(DataOrFact(cpurppol).arguments) == 3 :
                vdetails = vdetails + "- THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY: THE FOLLOWING COLLECTION PURPOSE IS SET IN THE POLICY, WHICH IS NOT IMPLEMENTED IN THE ARCH.:\n" + "  ===> FOR SOME ENTITY TO "  + "<< " + str(DataOrFact(cpurppol).arguments[1])  + " >> A PIECE OF DATA OF TYPE " + "<< " + str(DataOrFact(cpurppol).arguments[0])  + " >>"  + " THAT CONTAINS " + "<< " + str(DataOrFact(cpurppol).arguments[2]) + " >>" + "\n\n"
            else : 
                vdetails = vdetails + "- THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY: THE FOLLOWING COLLECTION PURPOSE IS SET IN THE POLICY, WHICH IS NOT IMPLEMENTED IN THE ARCH.:\n" + "  ===> FOR SOME ENTITY TO "  + "<< " + str(DataOrFact(cpurppol).arguments[1]) + " >> A PIECE OF DATA OF TYPE " + "<< " + str(DataOrFact(cpurppol).arguments[0])  + " >>"  + "\n\n"
        
    
    if len(cPurposeArch - cPurposePolAll) > 0 : 
        
        isdprviolated = 1
        
        if len(cPurposePolAll) == 0 : 
            for cpurparch in cPurposeArch.difference(cPurposePolAll) : 
                if len(DataOrFact(cpurparch).arguments) == 3 :
                    vdetails = vdetails + "- THE ARCHITECTURE <<MAY NOT>>  DPR CONFORM WITH THE POLICY: THE FOLLOWING COLLECTION PURPOSE MAY BE IMPLEMENTED IN THE ARCH, BUT COLLECTION PURPOSE IS NOT DEFINED IN THE POLICY:\n"  + "  ===> FOR SOME ENTITY TO "  + "<< " + str(DataOrFact(cpurparch).arguments[1]) + " >> A PIECE OF DATA OF TYPE " + "<< " + str(DataOrFact(cpurparch).arguments[0])  + " >>"  + " THAT CONTAINS " + "<< " + str(DataOrFact(cpurparch).arguments[2]) + " >>" + "\n\n"                                                                                                                    
                else :
                    vdetails = vdetails + "- THE ARCHITECTURE <<MAY NOT>>  DPR CONFORM WITH THE POLICY: THE FOLLOWING COLLECTION PURPOSE MAY BE IMPLEMENTED IN THE ARCH, BUT COLLECTION PURPOSE IS NOT DEFINED IN THE POLICY:\n" + "  ===> FOR SOME ENTITY TO "  + "<< " + str(DataOrFact(cpurparch).arguments[1]) + " >> A PIECE OF DATA OF TYPE " + "<< " + str(DataOrFact(cpurparch).arguments[0])  + " >>"  + "\n\n"
        else :
            for cpurparch in cPurposeArch.difference(cPurposePolAll) :
                vdetails = vdetails + "- THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY: THE FOLLOWING COLLECTION PURPOSE IS IMPLEMENTED IN THE ARCH, BUT NOT SET IN THE POLICY:\n" + "  ===> FOR SOME ENTITY TO " +  "<< " + str(DataOrFact(cpurparch).arguments[1]) + " >> A PIECE OF DATA OF TYPE " + "<< " + str(DataOrFact(cpurparch).arguments[0])  + " >>"  + "\n\n"
        
    
    
    if len(uPurposePolAll - uPurposeArch) > 0 : 
        
        isfunctionalviolated = 1
        
        for upurppol in uPurposePolAll.difference(uPurposeArch) :
            if len(DataOrFact(upurppol).arguments) == 3 :
                vdetails = vdetails + "- THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY: THE FOLLOWING COLLECTION PURPOSE IS SET IN THE POLICY, WHICH IS NOT IMPLEMENTED IN THE ARCH.:\n" + "  ===> FOR SOME ENTITY TO "  + "<< " + str(DataOrFact(upurppol).arguments[1])  + " >> A PIECE OF DATA OF TYPE " + "<< " + str(DataOrFact(upurppol).arguments[0])  + " >>"  + " THAT CONTAINS " + "<< " + str(DataOrFact(upurppol).arguments[2]) + " >>" + "\n\n"
            else : 
                vdetails = vdetails + "- THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY: THE FOLLOWING COLLECTION PURPOSE IS SET IN THE POLICY, WHICH IS NOT IMPLEMENTED IN THE ARCH.:\n" + "  ===> FOR SOME ENTITY TO "  + "<< " + str(DataOrFact(upurppol).arguments[1]) + " >> A PIECE OF DATA OF TYPE " + "<< " + str(DataOrFact(upurppol).arguments[0])  + " >>"  + "\n\n"
        
    if len(uPurposeArch - uPurposePolAll) > 0 :  
        
        isdprviolated = 1
        
        if len(uPurposePolAll) == 0 : 
            for upurparch in uPurposeArch.difference(uPurposePolAll) : 
                if len(DataOrFact(upurparch).arguments) == 3 :
                    vdetails = vdetails + "- THE ARCHITECTURE <<MAY NOT>>  DPR CONFORM WITH THE POLICY: THE FOLLOWING USAGE PURPOSE MAY BE IMPLEMENTED IN THE ARCH, BUT USAGE PURPOSE IS NOT DEFINED IN THE POLICY:\n" + "===> FOR SOME ENTITY TO "  + "<< " + str(DataOrFact(upurparch).arguments[1]) + " >> A PIECE OF DATA OF TYPE " + "<< " + str(DataOrFact(upurparch).arguments[0])  + " >>"  + " THAT CONTAINS " + "<< " + str(DataOrFact(upurparch).arguments[2]) + " >>" + "\n\n"
                else :   
                    vdetails = vdetails + "- THE ARCHITECTURE <<MAY NOT>>  DPR CONFORM WITH THE POLICY: THE FOLLOWING USAGE PURPOSE MAY BE IMPLEMENTED IN THE ARCH, BUT USAGE PURPOSE IS NOT DEFINED IN THE POLICY:\n" + "===> FOR SOME ENTITY TO " +  "<< " + str(DataOrFact(upurparch).arguments[1]) + " >> A PIECE OF DATA OF TYPE " + "<< " + str(DataOrFact(upurparch).arguments[0])  + " >>"  + "\n\n"
        else :
            for upurparch in uPurposeArch.difference(uPurposePolAll) :
                vdetails = vdetails + "- THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY: THE FOLLOWING USAGE PURPOSE IS IMPLEMENTED IN THE ARCH, BUT NOT SET IN THE POLICY:\n"  + "  ===> FOR SOME ENTITY TO " +  "<< " + str(DataOrFact(upurparch).arguments[1]) + " >> A PIECE OF DATA OF TYPE " + "<< " + str(DataOrFact(upurparch).arguments[0])  + " >>"  + "\n\n"        
        
   
      
    for cc in CConsDataE.keys() :  
        
        isThereRecvforCons[cc] = 0
        if cc in collectionpolconsent.keys() and collectionpolconsent[cc] == "Y" : 
            for ren in ReceiveDataE :
                if (cc == ren[0]) or (iscontainingarg(ren[0],cc) == 1) :  
                    if ren[1] not in CConsDataE[cc]  :  
                        isdprviolated = 1
                        isThereRecvforCons[cc] = 1
                        vdetails = vdetails + "- THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY: " + "<< " + ren[1]  + " >>" + " CAN RECEIVE (WITHOUT COLLENCTION CONSENT) " + "<< " + ren[0]  + " >>" + " THAT CONTAINS/IS EQUAL TO " + "<< " + cc  + " >>" + "\n\n"
                    else: 
                        isThereRecvforCons[cc] = 1
            if isThereRecvforCons[cc] == 0 : 
                isfunctionalviolated = 1 
                vdetails = vdetails + "- THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY AS: << " +  cc  + " >> CANNOT BE RECEIVED BY ANY ENTITY IN ARCH, DESPITE THE COLLECTION CONSENT IS  DEFINED (IN BOTH ARCH. AND POL.)\n\n" 
        
    for cc in UConsDataE.keys() :
        
        isThereRecvforCons[cc] = 0
        if cc in usagepolconsent.keys() and usagepolconsent[cc] == "Y" : 
            for ren in ReceiveDataE :
                if (cc == ren[0]) or (iscontainingarg(ren[0],cc) == 1) :  
                    if ren[1] not in UConsDataE[cc]  :  
                        isdprviolated = 1
                        isThereRecvforCons[cc] = 1
                        vdetails = vdetails + "- THE ARCHITECTURE MAY NOT DPR CONFORM WITH THE POLICY: " + "<< " + ren[1]  + " >>" + " CAN RECEIVE (WITHOUT USAGE CONSENT) " + "<< " + ren[0]  + " >>" + " THAT CONTAINS/IS EQUAL TO " + "<< " + cc  + " >>" + "\n\n"
                    else:  
                        isThereRecvforCons[cc] = 1
            if isThereRecvforCons[cc] == 0 : 
                isfunctionalviolated = 1  
                vdetails = vdetails + "- THE ARCHITECTURE MAY NOT FUNCTIONALLY CONFORM WITH THE POLICY AS: << " +  cc  + " >> CANNOT BE RECEIVED BY ANY ENTITY IN ARCH, DESPITE THE USAGE CONSENT IS DEFINED (IN BOTH ARCH. AND POL.)\n\n" 
            
            isThereRecvforCons[cc] = 0
            
            for ren in CalculateDataE : 
                if (cc == ren[0]) or (iscontainingarg(ren[0],cc) == 1) :  
                    if ren[1] not in UConsDataE[cc]  :  
                        isdprviolated = 1
                        isThereRecvforCons[cc] = 1
                        vdetails = vdetails + "- THE ARCHITECTURE MAY NOT DPR CONFORM WITH THE POLICY: " + "<< " + ren[1]  + " >>" + " CAN CALCULATE (WITHOUT USAGE CONSENT) " + "<< " + ren[0]  + " >>" + " THAT CONTAINS/IS EQUAL TO " + "<< " + cc  + " >>" + "\n\n"
                    else:    
                        isThereRecvforCons[cc] = 1
            if isThereRecvforCons[cc] == 0 :
                isfunctionalviolated = 1 
                vdetails = vdetails + "- THE ARCHITECTURE MAY NOT FUNCTIONALLY CONFORM WITH THE POLICY AS: << " +  cc  + " >> CANNOT BE CALCULATED BY ANY ENTITY IN ARCH, DESPITE THE USAGE CONSENT IS  DEFINED (IN BOTH ARCH. AND POL.)\n\n" 
            
            isThereRecvforCons[cc] = 0
            
            
            for ren in CreateDataE : 
                if (cc == ren[0]) or (iscontainingarg(ren[0],cc) == 1) :  
                    if ren[1] not in UConsDataE[cc]  :  
                        isdprviolated = 1
                        isThereRecvforCons[cc] = 1
                        vdetails = vdetails + "- THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY: " + "<< " + ren[1]  + " >>" + " CAN CREATE (WITHOUT USAGE CONSENT) " + "<< " + ren[0]  + " >>" + " THAT CONTAINS/IS EQUAL TO " + "<< " + cc  + " >>" + "\n\n"
             
                    else:  
                        isThereRecvforCons[cc] = 1
            if isThereRecvforCons[cc] == 0 : 
                isfunctionalviolated = 1 
                vdetails = vdetails + "- THE ARCHITECTURE MAY NOT FUNCTIONALLY CONFORM WITH THE POLICY AS: << " +  cc  + " >> CANNOT BE CREATED BY ANY ENTITY IN ARCH, DESPITE THE USAGE CONSENT IS  DEFINED (IN BOTH ARCH. AND POL.)\n\n" 
              
    
    for cc in SConsDataE.keys() :
        
        isThereRecvforCons[cc] = 0
        if cc in storepolconsent.keys() and storepolconsent[cc] == "Y" : 
            for ren in StoreDataE :
                if (cc == ren[0]) or (iscontainingarg(ren[0],cc) == 1) : 
                    if ren[1] not in SConsDataE[cc]  :  
                        isdprviolated = 1
                        isThereRecvforCons[cc] = 1
                        vdetails = vdetails + "- THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY: " + "<< " + ren[1]  + " >>" + " CAN STORE (WITHOUT STORAGE CONSENT) " + "<< " + ren[0]  + " >>" + " THAT CONTAINS/IS EQUAL TO " + "<< " + cc  + " >>" + "\n\n"
            
                    else:  
                        isThereRecvforCons[cc] = 1
            if isThereRecvforCons[cc] == 0 : 
                isfunctionalviolated = 1 
                vdetails = vdetails + "- THE ARCHITECTURE MAY NOT FUNCTIONALLY CONFORM WITH THE POLICY AS: << " +  cc  + " >> CANNOT BE STORED BY ANY ENTITY IN ARCH, DESPITE THE STORAGE CONSENT IS  DEFINED (IN BOTH ARCH. AND POL.).\n\n" 
        
    
    for cc in FwConsDataE.keys() : 
        
        if cc in transferThirdRec.keys() and (len(FwConsDataE[cc] - transferThirdRec[cc]) > 0) : 
            isdprviolated = 1
            for e in  (FwConsDataE[cc] - transferThirdRec[cc]) : 
                vdetails = vdetails + "- THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY: " + "<< " + e  + " >>" + " IS GIVEN CONSENT IN THE ARCH. TO RECEIVE THE TRANSFERED " + "<<" + cc  + " >> BUT NOT SPECIFIED IN THE POLICY.\n\n"  
        if cc in transferThirdRec.keys() and (len(transferThirdRec[cc] - FwConsDataE[cc]) > 0) : 
            isfunctionalviolated = 1
            for e in  (transferThirdRec[cc] - FwConsDataE[cc]) :
                vdetails = vdetails + "- THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY: " + "<< " + e  + " >>" + " IS GIVEN CONSENT IN POLICY TO RECEIVE THE TRANSFERED " + "<<" + cc  + " >> BUT NOT SPECIFIED IN THE ARCH.\n\n"  
        elif cc not in transferThirdRec.keys() : 
            isfunctionalviolated = 1 
            vdetails = vdetails + "- THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY: " + "<< " + cc  + " >>" + " ARE NOT GIVEN CONSENT TO BE TRANSFERRED TO ANY ENTITY IN THE POLICY, BUT FWCONSENT(" + cc   + ",...) CAN BE RECEIVED IN THE ARCH.\n\n" 
        
        
    for cc in transferThirdRec.keys() :
        
        if cc not in  FwConsDataE.keys() :
            isfunctionalviolated = 1 
            vdetails = vdetails + "- THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY: " + "<< " + cc  + " >>" + " CANNOT BE TRANSFERRED TO ANY ENTITY IN THE ARCH. DESPITE DATA TRANSFER IS DEFINED IN THE POLICY.\n\n"
        
    for cc in FwConsDataE.keys() :
       
        isThereRecvforCons[cc] = 0
        if cc in fwpolconsent.keys() and fwpolconsent[cc] == "Y" : 
            for ren in ReceiveDataE :
                if (cc == ren[0]) or (iscontainingarg(ren[0],cc) == 1) :  
                    if ren[1] not in FwConsDataE[cc]  :  
                        isdprviolated = 1
                        isThereRecvforCons[cc] = 1
                        vdetails = vdetails + "- THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY: " + "<< " + ren[1]  + " >>" + " CAN RECEIVE  (WITHOUT TRANSFER CONSENT) THE TRANSFERED DATA " + "<< " + ren[0]  + " >>" + " THAT CONTAINS/IS EQUAL TO " + "<< " + cc  + " >>" + "\n\n"
                    else:  
                        isThereRecvforCons[cc] = 1
            if isThereRecvforCons[cc] == 0 : 
                isfunctionalviolated = 1 
                vdetails = vdetails + "- THE ARCHITECTURE MAY NOT FUNCTIONALLY CONFORM WITH THE POLICY AS THE TRANSFERED: << " +  cc  + " >> CANNOT BE RECEIVED BY ANY ENTITY IN ARCH, DESPITE THE TRANSFER CONSENT IS  DEFINED (IN BOTH ARCH. AND POL.)\n\n"           
        
        
    for data in storagemodepol.keys():  
        
        if storagemodepol[data] == "centralmainbackup" :  
            if (data in storePolRec["mainstorage"]) and (data not in storeArchRec["mainstorage"]): 
                isfunctionalviolated = 1
                vdetails = vdetails + "- THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY: " + "<< " + data  + " >>" + " IS NOT STORED IN THE MAIN STORAGE\n\n"   
            if (data in storePolRec["backupstorage"]) and (data not in storeArchRec["backupstorage"]) :         
                isfunctionalviolated = 1
                vdetails = vdetails + "- THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY: " + "<< " + data  + " >>" + " IS NOT STORED IN THE BACKUP STORAGE\n\n"
        elif storagemodepol[data] == "centralmain" :  
            if (data in storePolRec["mainstorage"]) and  (data not in storeArchRec["mainstorage"]) : 
                isfunctionalviolated = 1
                vdetails = vdetails + "- THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY: " + "<< " + data  + " >>" + " IS NOT STORED IN THE MAIN STORAGE\n\n" 
            elif data in storeArchRec["backupstorage"] :
                isdprviolated = 1
                vdetails = vdetails + "- THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY: " + "<< " + data  + " >>" + " IS STORED IN THE BACKUP STORAGE (IT SHOULD BE STORED IN THE MAIN STORAGE ONLY) \n\n"     
        elif storagemodepol[data] == "decentral" :  
            if len(storeArchRec["mainstorage"]) > 0 or len(storeArchRec["backupstorage"]) > 0 : 
                isdprviolated = 1
                vdetails = vdetails + "- THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY: " + "<< " + data  + " >>" + " SHOULD NOT BE STORED IN THE MAIN OR BACKUP STORAGE AS IT WOULD BE CENTRALISED) \n\n"
        
    
    for q in querynothas : 
        
        
        if str(q.arguments[0]) in ReclistofbasicsHAS.keys() : 
            SetlistofbasicsHAS = ReclistofbasicsHAS[str(q.arguments[0])].copy()
        
        SetlistofbasicsHAS = cleanSetbasicHas().copy()
        StringSetofbasicsHAS = set(map(tostring, SetlistofbasicsHAS))
       
        
        if str(convertHasAfter(q)) in StringSetofbasicsHAS  : 
            isprivacyviolated = 1
            vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: " + str(q.arguments[0]) + " CAN HAVE THE DATA (OF TYPE) : " + str(q.arguments[1]) + "\n\n"
        else: 
             
            if VerifyAQuery(convertHasAfter(q),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1 : 
                isprivacyviolated = 1
                vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: " + str(q.arguments[0]) + " CAN HAVE THE DATA (OF TYPE) : " + str(q.arguments[1]) + "\n\n"   
        
        
    for q in queryhas :
        
        
        
        if str(q.arguments[0]) in ReclistofbasicsHAS.keys() : 
            SetlistofbasicsHAS = ReclistofbasicsHAS[str(q.arguments[0])].copy()
        
        SetlistofbasicsHAS = cleanSetbasicHas().copy()
        StringSetofbasicsHAS = set(map(tostring, SetlistofbasicsHAS))
        
        
        if str(convertHasAfter(q)) in StringSetofbasicsHAS :
            vdetails = vdetails + "- The architecture functionally conforms with the policy: " + str(q.arguments[0]) + " can have the data (of type) " + str(q.arguments[1]) + "\n\n"            
        elif VerifyAQuery(convertHasAfter(q), uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1 : 
            vdetails = vdetails + "- The architecture functionally conforms with the policy: " + str(q.arguments[0]) + " can have the data (of type) " + str(q.arguments[1]) + "\n\n" 
        else: 
            isfunctionalviolated = 1
            vdetails = vdetails + "- The architecture DOES NOT functionally conform with the policy: " + str(q.arguments[0]) + " CANNOT have the data (of type) " + str(q.arguments[1]) + "\n\n" 
        
    
    for q in queryhasafter :
        
        if VerifyAQuery(convertHasAfter(q),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1 : 
            isprivacyviolated = 1
            vdetails = vdetails + "- DPR VIOLATION OF THE POLICY << " + str(q.arguments[0]) + " >> CAN HAVE THE DATA (OF TYPE) << " + str(q.arguments[1]) + " >> AFTER << " + str(q.arguments[-1].arguments[0])  + " >> \n\n"   
        
       
    for q in querynotlink :
        
        if str(q.arguments[0]) in ReclistofbasicsLink.keys() : 
            SetlistofbasicsLink = ReclistofbasicsLink[str(q.arguments[0])].copy()
        
        StringSetofbasicsLink = set(map(tostring, SetlistofbasicsLink))
        
        
        if str(convertHasAfter(q)) in StringSetofbasicsLink : 
            isprivacyviolated = 1
            vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: " + str(q.arguments[0]) + " CAN LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"      
        else: 
            
            if VerifyAQuery(convertHasAfter(q),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1 or VerifyAQuery(convertHasAfter(DataOrFact(reverselink(q))),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1:
                isprivacyviolated = 1
                vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: " + str(q.arguments[0]) + " CAN LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n" 
            else: 
                if VerifyAQuery(convertHasAfter(DataOrFact(reverselink(q))),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1 : 
                    isprivacyviolated = 1
                    vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: " + str(q.arguments[0]) + " CAN LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
          
        
    for q in querynotlinkunique :
       
        if str(q.arguments[0]) in ReclistofbasicsLinkUnique.keys() : 
            SetlistofbasicsLinkUnique = ReclistofbasicsLinkUnique[str(q.arguments[0])].copy()
        
        StringSetlistofbasicsLinkUnique = set(map(tostring, SetlistofbasicsLinkUnique))
        
        
        if str(convertHasAfter(q)) in StringSetlistofbasicsLinkUnique : 
            isprivacyviolated = 1
            vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: " + str(q.arguments[0]) + " CAN !!! UNIQUELY !!! LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
        else: 
            if VerifyAQuery(convertHasAfter(q),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1 or VerifyAQuery(convertHasAfter(DataOrFact(reverselinkunique(q))),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1:
                isprivacyviolated = 1
                vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: " + str(q.arguments[0]) + " CAN !!! UNIQUELY !!! LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
            else: 
                if VerifyAQuery(convertHasAfter(DataOrFact(reverselinkunique(q))),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1 :
                    isprivacyviolated = 1
                    vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: " + str(q.arguments[0]) + " CAN !!! UNIQUELY !!! LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
        
    
    for q in querylink :
        
        if str(q.arguments[0]) in ReclistofbasicsLink.keys() : 
            SetlistofbasicsLink = ReclistofbasicsLink[str(q.arguments[0])].copy()
        
        StringSetofbasicsLink = set(map(tostring, SetlistofbasicsLink))
        
        
        if str(convertHasAfter(q)) in StringSetofbasicsLink : 
            vdetails = vdetails + "- The architecture functionally conforms with the policy: " + str(q.arguments[0]) + " can link two pieces of data (of type) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
        elif VerifyAQuery(convertHasAfter(q),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1 or VerifyAQuery(convertHasAfter(DataOrFact(reverselink(q))),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1: 
            vdetails = vdetails + "- The architecture functionally conforms with the policy: " + str(q.arguments[0]) + " can link two pieces of data (of type) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n" 
        else: 
            if VerifyAQuery(convertHasAfter(DataOrFact(reverselink(q))),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1 : 
                isprivacyviolated = 1
                vdetails = vdetails + "- The architecture functionally conforms with the policy: " + str(q.arguments[0]) + " can link two pieces of data (of type) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
            else:
                isfunctionalviolated = 1
                vdetails = vdetails + "- The architecture DOES NOT functionally conform with the policy: " + str(q.arguments[0]) + " CANNOT link two pieces of data (of type) " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
        
    
    for q in querylinkunique :
        
        if str(q.arguments[0]) in ReclistofbasicsLinkUnique.keys() : 
            SetlistofbasicsLinkUnique = ReclistofbasicsLinkUnique[str(q.arguments[0])].copy()
        
        
        StringSetlistofbasicsLinkUnique = set(map(tostring, SetlistofbasicsLinkUnique))
        
        
        if str(convertHasAfter(q)) in StringSetlistofbasicsLinkUnique : 
            vdetails = vdetails + "- The architecture functionally conforms with the policy: " + str(q.arguments[0]) + " can !!! UNIQUELY !!! link two pieces of data (of type) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
        elif VerifyAQuery(convertHasAfter(q),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1 or VerifyAQuery(convertHasAfter(DataOrFact(reverselinkunique(q))),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1: 
            vdetails = vdetails + "- The architecture functionally conforms with the policy: " + str(q.arguments[0]) + " can !!! UNIQUELY !!! link two pieces of data (of type) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n" 
        else:
            if VerifyAQuery(convertHasAfter(DataOrFact(reverselinkunique(q))),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1 : 
                isfunctionalviolated = 1
                vdetails = vdetails + "- The architecture functionally conforms with the policy: " + str(q.arguments[0]) + " can !!! UNIQUELY !!! link two pieces of data (of type) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
            else:
                isfunctionalviolated = 1
                vdetails = vdetails + "- The architecture DOES NOT functionally conform with the policy: " + str(q.arguments[0]) + " CANNOT !!! UNIQUELY !!! link two pieces of data (of type) " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
        
    
    for q in querycconsent : 
        if VerifyAQuery(convertHasAfter(q),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1 : 
            vdetails = vdetails + "- The architecture DPR CONFORMS with the policy: consent can be collected by << " + str(q.arguments[0]) + " >> before collecting the data (of type) : " + str(q.arguments[1]) + "\n\n" 
        else: 
            isdprviolated = 1
            vdetails = vdetails + "- THE ARCHITECTURE <<MAY>> NOT DPR CONFORM WITH THE POLICY: " + str(q.arguments[0]) + " <<MAY>> NOT COLLECT CONSENT BEFORE COLLECTING THE DATA (OF TYPE) " + str(q.arguments[1]) + "\n\n"
        
        
    for q in queryfwconsent : 
        if VerifyAQuery(convertHasAfter(q),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1 : 
            vdetails = vdetails + "- The architecture DPR CONFORMS with the policy: consent can be collected by <<  " + str(q.arguments[0]) + " >> before forwarding the data (of type) : " + str(q.arguments[1]) + "\n\n" 
        else: 
            isdprviolated = 1
            vdetails = vdetails + "- THE ARCHITECTURE <<MAY>> NOT DPR CONFORM WITH THE POLICY: " + str(q.arguments[0]) + " <<MAY>> NOT COLLECT CONSENT BEFORE FORWARDING THE DATA (OF TYPE) " + str(q.arguments[1]) + "\n\n"
        
        
    for q in queryuconsent : 
        if VerifyAQuery(convertHasAfter(q),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1 : 
            vdetails = vdetails + "- The architecture DPR CONFORMS with the policy: consent can be collected by << " + str(q.arguments[0]) + " >> before using the data (of type) : " + str(q.arguments[1]) + "\n\n" 
        else: 
            isdprviolated = 1
            vdetails = vdetails + "- THE ARCHITECTURE <<MAY>> NOT DPR CONFORM WITH THE POLICY: " + str(q.arguments[0]) + " <<MAY>> NOT COLLECT CONSENT BEFORE USING THE DATA (OF TYPE) " + str(q.arguments[1]) + "\n\n"
        
        
    for q in querysconsent : 
        
        if VerifyAQuery(convertHasAfter(q),  uniquedata, UnionarchMeta, Unionarch, UnionarchPseudo,  UnionarchTime, ruleindex, crytopred, nestenc, verifmode) == 1 : 
            vdetails = vdetails + "- The architecture DPR CONFORMS with the policy:  consent can be collected by << " + str(q.arguments[0]) + " >> before storing the data (of type) : " + str(q.arguments[1]) + "\n\n" 
        else: 
            isdprviolated = 1
            vdetails = vdetails + "- THE ARCHITECTURE <<MAY>> NOT DPR CONFORM WITH THE POLICY: " + str(q.arguments[0]) + " <<MAY>> NOT COLLECT CONSENT BEFORE STORING THE DATA (OF TYPE) " + str(q.arguments[1]) + "\n\n"
        
        
    if isprivacyviolated == 1 and isfunctionalviolated == 1 and isdprviolated == 1: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT PRIVACY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY (SEE DETAILS BELOW)"
    elif isprivacyviolated == 1 and isfunctionalviolated == 1 and isdprviolated == 0: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT PRIVACY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY (SEE DETAILS BELOW)"
    elif isprivacyviolated == 1 and isfunctionalviolated == 0 and isdprviolated == 1: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT PRIVACY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY (SEE DETAILS BELOW)"
    elif isprivacyviolated == 1 and isfunctionalviolated == 0 and isdprviolated == 0: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT PRIVACY CONFORM WITH THE POLICY (SEE DETAILS BELOW)" 
    elif isprivacyviolated == 0 and isfunctionalviolated == 0 and isdprviolated == 1: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY (SEE DETAILS BELOW)"
    elif isprivacyviolated == 0 and isfunctionalviolated == 1 and isdprviolated == 1: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY (SEE DETAILS BELOW)"  
    elif isprivacyviolated == 0 and isfunctionalviolated == 1 and isdprviolated == 0: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY (SEE DETAILS BELOW)" 
    elif isprivacyviolated == 0 and isfunctionalviolated == 0  and isdprviolated == 0: 
        vresult = vresult + "THE ARCHITECTURE PRIVACY CONFORMS WITH THE POLICY \n" + "THE ARCHITECTURE FUNCTIONALLY CONFORMS WITH THE POLICY \n" + "THE ARCHITECTURE DPR CONFORMS WITH THE POLICY (SEE DETAILS BELOW)"
    printresult(vresult, vdetails)   
    
    
    elapsed_time = time.process_time() - t               
    milliseconds = int(round(elapsed_time * 1000))   
    print("Verification time (entire policy): " + str(milliseconds) + " milliseconds") 
    
    
    
################################ Verification in the external attackers case ################################################# 
def VerifyPolicyEXATT(queryfwconsent, querycconsent, queryuconsent, queryhas, querynothas, queryhasafter, querylink, querynotlink, querylinkunique, querynotlinkunique, querysconsent, uniquedata, archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc) : 
    global SetlistofbasicsHAS
    global SetlistofbasicsLink
    global SetlistofbasicsLinkATTEXUnique
    global SetlistofbasicsHASATTEX
    global SetlistofbasicsLinkATTEX
    global ReclistofbasicsHASAttEx
    global ReclistofbasicsLinkAttEx
    global ReclistofbasicsLinkAttExUnique
    
    verifmode = 2 
    
    t = time.process_time()  #start measure time.
    
    resetAbilitysetsMaprecords() 
    
    SetlistofbasicsHAS.clear()  
    SetlistofbasicsLink.clear() 
    
    StringSetofbasicsLinkUnique = set()
      
    isprivacyviolated = 0
    isdprviolated = 0
    isfunctionalviolated = 0
    vresult = ""
    vdetails = "***NOTE: THE EXTERNAL ATTACKERS ARE NOT PART OF THE SYSTEM. THEY CAN EAVESDROP AND ANALYSE THE COMMUNICATIONS BETWEEN ENTITIES.*** \n\n"
    
    
    
    if "att" in ReclistofbasicsHASAttEx.keys() : 
        SetlistofbasicsHASATTEX = ReclistofbasicsHASAttEx["att"].copy()
    
    SetlistofbasicsHASATTEX = cleanSetbasicHasATTEX().copy()   
    
    StringSetofbasicsHASATTEX = set(map(tostring, SetlistofbasicsHASATTEX))  
   
    if "att" in ReclistofbasicsLinkAttEx.keys() : 
        SetlistofbasicsLinkATTEX = ReclistofbasicsLinkAttEx["att"].copy()
            
    StringSetofbasicsLinkATTEX = set(map(tostring, SetlistofbasicsLinkATTEX)) 
    
    if "att" in ReclistofbasicsLinkAttExUnique.keys() : 
        SetlistofbasicsLinkATTEXUnique = ReclistofbasicsLinkAttExUnique["att"].copy()
            
    StringSetofbasicsLinkUnique = set(map(tostring, SetlistofbasicsLinkATTEXUnique)) 
    
    for q in querynothas : 
        
         
        if str(q) in StringSetofbasicsHASATTEX  : 
            
            isprivacyviolated = 1
            vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The external " + str(q.arguments[0]) + "acker CAN HAVE THE DATA (OF TYPE) : " + str(q.arguments[1]) + "\n\n"
        else: 
            if VerifyAQuery(q,  uniquedata, archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1 : 
                isprivacyviolated = 1
                vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The external " + str(q.arguments[0]) + "acker CAN HAVE THE DATA (OF TYPE) : " + str(q.arguments[1]) + "\n\n"   # + str(q)
        
        
    for q in querynotlink :
        
        if str(q) in StringSetofbasicsLinkATTEX : 
            isprivacyviolated = 1
            vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The external " + str(q.arguments[0]) + "acker CAN LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"      
        else: 
            if VerifyAQuery(convertHasAfter(q),  uniquedata,  archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1 or VerifyAQuery(convertHasAfter(DataOrFact(reverselink(q))),  uniquedata, archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1:
                isprivacyviolated = 1
                vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The external " + str(q.arguments[0]) + "acker CAN LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n" 
            else: 
                if VerifyAQuery(convertHasAfter(DataOrFact(reverselink(q))),  uniquedata,  archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1 : 
                    isprivacyviolated = 1
                    vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The external " + str(q.arguments[0]) + "acker CAN LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
        
        
    for q in querynotlinkunique :
        
         
        if str(q) in StringSetofbasicsLinkUnique : 
            isprivacyviolated = 1
            vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The external " + str(q.arguments[0]) + "acker CAN !!! UNIQUELY !!! LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
        else: 
            if VerifyAQuery(convertHasAfter(q),  uniquedata,  archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1 or VerifyAQuery(convertHasAfter(DataOrFact(reverselinkunique(q))),  uniquedata, archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1:
                isprivacyviolated = 1
                vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The external " + str(q.arguments[0]) + "acker CAN !!! UNIQUELY !!! LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
            else: 
                if VerifyAQuery(convertHasAfter(DataOrFact(reverselinkunique(q))),  uniquedata,  archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1 :
                    isprivacyviolated = 1
                    vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The external " + str(q.arguments[0]) + "acker CAN !!! UNIQUELY !!! LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
        
    if isprivacyviolated == 1 and isfunctionalviolated == 1 and isdprviolated == 1: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT PRIVACY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY (SEE DETAILS BELOW)"
    elif isprivacyviolated == 1 and isfunctionalviolated == 1 and isdprviolated == 0: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT PRIVACY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY (SEE DETAILS BELOW)"
    elif isprivacyviolated == 1 and isfunctionalviolated == 0 and isdprviolated == 1: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT PRIVACY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY (SEE DETAILS BELOW)"
    elif isprivacyviolated == 1 and isfunctionalviolated == 0 and isdprviolated == 0: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT PRIVACY CONFORM WITH THE POLICY (SEE DETAILS BELOW)" 
    elif isprivacyviolated == 0 and isfunctionalviolated == 0 and isdprviolated == 1: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY (SEE DETAILS BELOW)"
    elif isprivacyviolated == 0 and isfunctionalviolated == 1 and isdprviolated == 1: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY (SEE DETAILS BELOW)"  
    elif isprivacyviolated == 0 and isfunctionalviolated == 1 and isdprviolated == 0: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY (SEE DETAILS BELOW)" 
    elif isprivacyviolated == 0 and isfunctionalviolated == 0  and isdprviolated == 0: 
        vresult = vresult + "THE ARCHITECTURE PRIVACY CONFORMS WITH THE POLICY \n" + "THE ARCHITECTURE FUNCTIONALLY CONFORMS WITH THE POLICY \n" + "THE ARCHITECTURE DPR CONFORMS WITH THE POLICY (SEE DETAILS BELOW)"
    printresult(vresult, vdetails)   
    
    
    elapsed_time = time.process_time() - t                
    milliseconds = int(round(elapsed_time * 1000))   
    print("Verification time (entire policy): " + str(milliseconds) + " milliseconds") 
    
 

    
def UnionArchInAtt(strent,rootstrent) :   
    global Recofactions
    global RecofUnionArch 
    for ent in HasAccessTo[strent] :  
        if ent in Recofactions.keys() : 
            if rootstrent not in RecofUnionArch.keys() : 
                if strent == "att" :
                    RecofUnionArch[rootstrent] = set()
                    RecofUnionArch[rootstrent] = RecofUnionArch[rootstrent].union(ReplaceEntitiesInSetArch(ent,rootstrent)) 
                else : 
                   
                    if rootstrent in Recofactions.keys() :
                        RecofUnionArch[rootstrent] = Recofactions[rootstrent]
                        RecofUnionArch[rootstrent] = RecofUnionArch[rootstrent].union(ReplaceEntitiesInSetArch(ent,rootstrent)) 
                    else : 
                        Recofactions[rootstrent] = set()
                        RecofUnionArch[rootstrent] = set()
                        RecofUnionArch[rootstrent] = RecofUnionArch[rootstrent].union(ReplaceEntitiesInSetArch(ent,rootstrent)) 
            else : 
                RecofUnionArch[rootstrent] = RecofUnionArch[rootstrent].union(ReplaceEntitiesInSetArch(ent,rootstrent))
            if (ent in HasAccessTo.keys()) and (len(HasAccessTo[ent]) > 0) :     
                UnionArchInAtt(ent,rootstrent)
        
       

def UnionArchAccessTo() : 
    global HasAccessTo 
    
    if len(HasAccessTo) > 0 : 
        for ent in HasAccessTo.keys() : 
            if len(HasAccessTo[ent]) > 0 :
                UnionArchInAtt(ent,ent) 
             


################################ Verification in the insider attackers case #################################################
def VerifyPolicyINATT(queryfwconsent, querycconsent, queryuconsent, queryhas, querynothas, queryhasafter, querylink, querynotlink, querylinkunique, querynotlinkunique, querysconsent, uniquedata, archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc) : 
    global SetlistofbasicsLinkATTIN
    global SetlistofbasicsHASATTIN
    global SetlistofbasicsLinkATTINUnique
   
    verifmode = 3 # insider attacker 
    
    t = time.process_time()  #start measure time.
    
    resetAbilitysetsMaprecords() 
      
    isprivacyviolated = 0
    isdprviolated = 0
    isfunctionalviolated = 0
    vresult = ""
    vdetails = "***NOTE: THE INSIDER ATTACKERS ARE PART OF THE SYSTEM. THEY ARE COMPROMISED ENTITIES AND HAVE FULL ACCESS TO THOSE.***\n\n"
    
    
    StringSetofbasicsHAS = set()
    StringSetofbasicsLink = set()
    StringSetofbasicsLinkUnique = set()
        
        
    StringSetofbasicsLink = set(map(tostring, SetlistofbasicsLinkATTIN))
    StringSetofbasicsHAS = set(map(tostring, SetlistofbasicsHASATTIN))
    StringSetofbasicsLinkUnique = set(map(tostring, SetlistofbasicsLinkATTINUnique))

    for q in querynothas : 
        
        if str(q) in StringSetofbasicsHAS  : 
           
            isprivacyviolated = 1
            vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The insider " + str(q.arguments[0]) + "acker(s), who compromised the entity(ies) " 
            for ent in HasAccessTo["att"] : 
                vdetails = vdetails + ent + ", "
            vdetails = vdetails + "CAN HAVE THE DATA (OF TYPE) : " + str(q.arguments[1]) + "\n\n"
        else: 
            if VerifyAQuery(convertHasAfter(q),  uniquedata, archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1 : 
                isprivacyviolated = 1
                vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The insider " + str(q.arguments[0]) + "acker(s), who compromised the entity(ies) " 
                for ent in HasAccessTo["att"] : 
                    vdetails = vdetails + ent + ", "
                vdetails = vdetails + "CAN HAVE THE DATA (OF TYPE) : " + str(q.arguments[1]) + "\n\n"
        
        
    for q in querynotlink :
        
        if str(q) in StringSetofbasicsLink : 
            isprivacyviolated = 1
            vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The insider " + str(q.arguments[0]) + "acker(s), who compromised the entity(ies) " 
            for ent in HasAccessTo["att"] : 
                vdetails = vdetails + ent + ", "
            vdetails = vdetails + "CAN LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
        else: 
            if VerifyAQuery(convertHasAfter(q),  uniquedata,  archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1 or VerifyAQuery(convertHasAfter(DataOrFact(reverselink(q))),  uniquedata, archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1:
                isprivacyviolated = 1
                vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The insider " + str(q.arguments[0]) + "acker(s), who compromised the entity(ies) " 
                for ent in HasAccessTo["att"] : 
                    vdetails = vdetails + ent + ", "
                vdetails = vdetails + "CAN LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
            else: 
                if VerifyAQuery(convertHasAfter(DataOrFact(reverselink(q))),  uniquedata,  archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1 : 
                    isprivacyviolated = 1
                    vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The insider " + str(q.arguments[0]) + "acker(s), who compromised the entity(ies) " 
                    for ent in HasAccessTo["att"] : 
                        vdetails = vdetails + ent + ", "
                    vdetails = vdetails + "CAN LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
        
        
    for q in querynotlinkunique :
        
        if str(q) in StringSetofbasicsLinkUnique : 
            isprivacyviolated = 1
            vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The insider " + str(q.arguments[0]) + "acker(s), who compromised the entity(ies) " 
            for ent in HasAccessTo["att"] : 
                vdetails = vdetails + ent + ", "
            vdetails = vdetails + "CAN !!! UNIQUELY !!! LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
        else: 
            if VerifyAQuery(convertHasAfter(q),  uniquedata,  archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1 or VerifyAQuery(convertHasAfter(DataOrFact(reverselinkunique(q))),  uniquedata, archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1:
                isprivacyviolated = 1
                vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The insider " + str(q.arguments[0]) + "acker(s), who compromised the entity(ies) " 
                for ent in HasAccessTo["att"] : 
                    vdetails = vdetails + ent + ", "
                vdetails = vdetails + "CAN !!! UNIQUELY !!! LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
            else: 
                if VerifyAQuery(convertHasAfter(DataOrFact(reverselinkunique(q))),  uniquedata,  archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1 :
                    isprivacyviolated = 1
                    vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The insider " + str(q.arguments[0]) + "acker(s), who compromised the entity(ies) " 
                    for ent in HasAccessTo["att"] : 
                        vdetails = vdetails + ent + ", "
                    vdetails = vdetails + "CAN !!! UNIQUELY !!! LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
        
    if isprivacyviolated == 1 and isfunctionalviolated == 1 and isdprviolated == 1: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT PRIVACY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY (SEE DETAILS BELOW)"
    elif isprivacyviolated == 1 and isfunctionalviolated == 1 and isdprviolated == 0: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT PRIVACY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY (SEE DETAILS BELOW)"
    elif isprivacyviolated == 1 and isfunctionalviolated == 0 and isdprviolated == 1: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT PRIVACY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY (SEE DETAILS BELOW)"
    elif isprivacyviolated == 1 and isfunctionalviolated == 0 and isdprviolated == 0: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT PRIVACY CONFORM WITH THE POLICY (SEE DETAILS BELOW)" 
    elif isprivacyviolated == 0 and isfunctionalviolated == 0 and isdprviolated == 1: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY (SEE DETAILS BELOW)"
    elif isprivacyviolated == 0 and isfunctionalviolated == 1 and isdprviolated == 1: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY (SEE DETAILS BELOW)"  
    elif isprivacyviolated == 0 and isfunctionalviolated == 1 and isdprviolated == 0: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY (SEE DETAILS BELOW)" 
    elif isprivacyviolated == 0 and isfunctionalviolated == 0  and isdprviolated == 0: 
        vresult = vresult + "THE ARCHITECTURE PRIVACY CONFORMS WITH THE POLICY \n" + "THE ARCHITECTURE FUNCTIONALLY CONFORMS WITH THE POLICY \n" + "THE ARCHITECTURE DPR CONFORMS WITH THE POLICY (SEE DETAILS BELOW)"
    printresult(vresult, vdetails)   
    
    
    elapsed_time = time.process_time() - t                
    milliseconds = int(round(elapsed_time * 1000))   
    print("Verification time (entire policy): " + str(milliseconds) + " milliseconds") 
    


################################ Verification in the hybrid attackers case #################################################
def VerifyPolicyHYBATT(queryfwconsent, querycconsent, queryuconsent, queryhas, querynothas, queryhasafter, querylink, querynotlink, querylinkunique, querynotlinkunique, querysconsent, uniquedata, archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc) : 
    global ReclistofbasicsHAS
    global ReclistofbasicsLink
    global ReclistofbasicsHASAttEx
    
    global SetlistofbasicsHASATTIN
    global SetlistofbasicsHASATTEX
    
    global SetlistofbasicsHASATTHYB
    global SetlistofbasicsLinkATTHYB
    global SetlistofbasicsLinkATTHYBUnique
    
    verifmode = 4 # hybrid attackers (atthyb)
    
    t = time.process_time()  #start measure time.
    
    resetAbilitysetsMaprecords() 
    
    
    setnotwellformedarch = set()  
    isprivacyviolated = 0
    isdprviolated = 0
    isfunctionalviolated = 0
    vresult = ""
    vdetails = "***NOTE: THE HYBRID ATTACKERS CASE SPECIFIES THE COLLUSION BETWEEN INSIDER AND EXTERNAL ATTACKERS.***\n\n"
    
    
    SetlistofbasicsHASATTEX.clear()  
    
    StringSetofbasicsHAS = set()
    StringSetofbasicsLink = set()
    StringSetofbasicsLinkUnique = set()
    SetofbasicsHAS = set()
    
        
    if "att" in ReclistofbasicsHASAttEx.keys() : 
        SetlistofbasicsHASATTEX = ReclistofbasicsHASAttEx["att"].copy() 
    
    SetlistofbasicsHASATTEX = cleanSetbasicHasATTEX().copy()  
    
        
    SetofbasicsHAS =  SetlistofbasicsHASATTEX.union(SetlistofbasicsHASATTIN)
    
    
    SetlistofbasicsHASATTHYB = SetofbasicsHAS.copy()
    
    for hasterm in SetofbasicsHAS : 
        generatebasicsEncAttHyb(hasterm)
    
    
    if len(basicEncRecAttHyb) > 0 : 
        cleanbasicsEncRecAttHyb()
    
    
    StringSetofbasicsHAS = set(map(tostring,  SetlistofbasicsHASATTHYB))
    StringSetofbasicsLink = set(map(tostring, SetlistofbasicsLinkATTHYB))
    StringSetofbasicsLinkUnique = set(map(tostring, SetlistofbasicsLinkATTHYBUnique))
    
    
    for q in querynothas : 
        
        if str(q) in StringSetofbasicsHAS  : 
            
            isprivacyviolated = 1
            vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The external attacker(s) AND the compromised entity(ies) " 
            if len(HasAccessTo) > 0 and "att" in HasAccessTo.keys() :
                for ent in HasAccessTo["att"] : 
                    vdetails = vdetails + ent + ", "
            vdetails = vdetails + "CAN HAVE THE DATA (OF TYPE) : " + str(q.arguments[1]) + "\n\n"
        else: 
            if VerifyAQuery(convertHasAfter(q),  uniquedata, archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1 : 
                isprivacyviolated = 1
                vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The external attacker(s) AND the compromised entity(ies) " 
                if len(HasAccessTo) > 0 and "att" in HasAccessTo.keys() :
                    for ent in HasAccessTo["att"] : 
                        vdetails = vdetails + ent + ", "
                vdetails = vdetails + "TOGETHER CAN HAVE THE DATA (OF TYPE) : " + str(q.arguments[1]) + "\n\n"
               
    for q in querynotlink : 
        
        if str(q) in StringSetofbasicsLink : 
            isprivacyviolated = 1
            vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The external attacker(s) AND the compromised entity(ies) "       
            if len(HasAccessTo) > 0 and "att" in HasAccessTo.keys() :
                for ent in HasAccessTo["att"] : 
                    vdetails = vdetails + ent + ", "
            vdetails = vdetails + "TOGETHER CAN LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
        else: 
            if VerifyAQuery(convertHasAfter(q),  uniquedata,  archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1 or VerifyAQuery(convertHasAfter(DataOrFact(reverselink(q))),  uniquedata, archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1:
                isprivacyviolated = 1
                vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The external attacker(s) AND the compromised entity(ies) "
                if len(HasAccessTo) > 0 and "att" in HasAccessTo.keys() :
                    for ent in HasAccessTo["att"] : 
                        vdetails = vdetails + ent + ", "
                vdetails = vdetails + "TOGETHER CAN LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
            else: 
                if VerifyAQuery(convertHasAfter(DataOrFact(reverselink(q))),  uniquedata,  archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1 : 
                    isprivacyviolated = 1
                    vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The external attacker(s) AND the compromised entity(ies) "
                    if len(HasAccessTo) > 0 and "att" in HasAccessTo.keys() :
                        for ent in HasAccessTo["att"] : 
                            vdetails = vdetails + ent + ", "
                    vdetails = vdetails + "TOGETHER CAN LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
              
    for q in querynotlinkunique :
        
        if str(q) in StringSetofbasicsLinkUnique : 
            isprivacyviolated = 1
            vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The external attacker(s) AND the compromised entity(ies) "
            if len(HasAccessTo) > 0 and "att" in HasAccessTo.keys() :
                for ent in HasAccessTo["att"] : 
                    vdetails = vdetails + ent + ", "
            vdetails = vdetails + "TOGETHER CAN !!! UNIQUELY !!! LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"  
        else: 
            if VerifyAQuery(convertHasAfter(q),  uniquedata,  archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1 or VerifyAQuery(convertHasAfter(DataOrFact(reverselinkunique(q))),  uniquedata, archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1:
                isprivacyviolated = 1
                vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The external attacker(s) AND the compromised entity(ies) "
                if len(HasAccessTo) > 0 and "att" in HasAccessTo.keys() :
                    for ent in HasAccessTo["att"] : 
                        vdetails = vdetails + ent + ", "
                vdetails = vdetails + "TOGETHER CAN !!! UNIQUELY !!! LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
            else: 
                if VerifyAQuery(convertHasAfter(DataOrFact(reverselinkunique(q))),  uniquedata,  archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1 :
                    isprivacyviolated = 1
                    vdetails = vdetails + "- PRIVACY VIOLATION OF THE POLICY: The external attacker(s) AND the compromised entity(ies) "
                    if len(HasAccessTo) > 0 and "att" in HasAccessTo.keys() :
                        for ent in HasAccessTo["att"] : 
                            vdetails = vdetails + ent + ", "
                    vdetails = vdetails + "TOGETHER CAN !!! UNIQUELY !!! LINK TWO PIECES OF DATA (OF TYPES) : " + str(q.arguments[1]) + " - and - " + str(q.arguments[2]) + "\n\n"
        
    
    if isprivacyviolated == 1 and isfunctionalviolated == 1 and isdprviolated == 1: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT PRIVACY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY (SEE DETAILS BELOW)"
    elif isprivacyviolated == 1 and isfunctionalviolated == 1 and isdprviolated == 0: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT PRIVACY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY (SEE DETAILS BELOW)"
    elif isprivacyviolated == 1 and isfunctionalviolated == 0 and isdprviolated == 1: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT PRIVACY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY (SEE DETAILS BELOW)"
    elif isprivacyviolated == 1 and isfunctionalviolated == 0 and isdprviolated == 0: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT PRIVACY CONFORM WITH THE POLICY (SEE DETAILS BELOW)" 
    elif isprivacyviolated == 0 and isfunctionalviolated == 0 and isdprviolated == 1: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY (SEE DETAILS BELOW)"
    elif isprivacyviolated == 0 and isfunctionalviolated == 1 and isdprviolated == 1: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY \n" + "THE ARCHITECTURE DOES NOT DPR CONFORM WITH THE POLICY (SEE DETAILS BELOW)"  
    elif isprivacyviolated == 0 and isfunctionalviolated == 1 and isdprviolated == 0: 
        vresult = vresult + "THE ARCHITECTURE DOES NOT FUNCTIONALLY CONFORM WITH THE POLICY (SEE DETAILS BELOW)" 
    elif isprivacyviolated == 0 and isfunctionalviolated == 0  and isdprviolated == 0: 
        vresult = vresult + "THE ARCHITECTURE PRIVACY CONFORMS WITH THE POLICY \n" + "THE ARCHITECTURE FUNCTIONALLY CONFORMS WITH THE POLICY \n" + "THE ARCHITECTURE DPR CONFORMS WITH THE POLICY (SEE DETAILS BELOW)"
    printresult(vresult, vdetails)   
    
    
    elapsed_time = time.process_time() - t                
    milliseconds = int(round(elapsed_time * 1000))   
    print("Verification time (entire policy): " + str(milliseconds) + " milliseconds") 
    


def HasAftertoHas(term) :
    strtermbody = "Has("
    for arg in term.arguments : 
        if str(arg.predicate) != "time" :  
            strtermbody = strtermbody + str(arg) + ","
    strtermbody = strtermbody[:-1]
    queryforhas = DataOrFact(strtermbody + ")")
    return queryforhas



def VerifyAQuery(query, uniquedata, archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) : 
    global VARMAPRECORD
    global VARMAPRECORDCrypto
    global listofMAPRECORD
    global listofMAPRECORDCrypto
    
    listofMAPRECORD = []
    listofMAPRECORDCrypto = []
      
    
    if checkAgainstAbilitySet(listofMAPRECORD, VARMAPRECORD, query, uniquedata, archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1 : 
        
        return 1 
    else : 
        return 0 


def iscontaining(strterm,strarg) : 
    if str(DataOrFact(strterm).predicate) == strarg :
        return 1  
    for arg in DataOrFact(strterm).arguments : 
        if iscontaining(str(arg),strarg) == 1 : 
            return 1
    return 0

 
# Discover embedded crypto functions during the verification.     
def VerifyCrypto(listofMAPRECORD, MAPRECORD, query, uniquedata, archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) :  
    global SetlistofnewHAS
    global SetlistofnewLink
    global SetlistofbasicsHAS
    global SetlistofbasicsHASATTEX
    global SetlistofbasicsHASATTIN
    global SetlistofbasicsHASATTHYB
    
    
    argpredsetcrypto = []
   
    
    for msg in msginsidecrypto :  
        for arg in query.arguments[1:] : 
            
            if iscontaining(msg,str(arg)) == 1 and (msg !=str(arg)):  
                
                newquery = DataOrFact("Has(" + str(query.arguments[0]) + "," + msg + ")")  
                
                if checkAgainstAbilitySet(listofMAPRECORD, MAPRECORD, newquery, uniquedata, archmeta, architecture, archpseudo, archtime, ruleindex, crytopred, nestenc, verifmode) == 1 :  
                    SetlistofnewHAS.add(newquery) 
                    
                    addtoNewHas(newquery.arguments[0],DataOrFact(msg))
                    
                    
                    addtoLink(DataOrFact(msg),argpredsetcrypto)
                    
                    permutedpairs=set(itertools.permutations(argpredsetcrypto, 2))
    
                    for pair in permutedpairs : 
                        basicquerytermSubHas = DataOrFact("Has(" + str(newquery.arguments[0]) + "," + str(newquery.arguments[1].predicate) + "(" + pair[0] + "," + pair[1] + ")" + ")")
                        SetlistofnewHAS.add(basicquerytermSubHas)
                    
                    for hasterm in SetlistofnewHAS: 
                        if len(hasterm.arguments) > 0  : 
                            generatenewlinkbasics(hasterm) 
                    
                    
                   
                    
    if verifmode == 1 : #No attacker
        Unionset = SetlistofbasicsHAS.union(SetlistofnewHAS)
        SetlistofbasicsHAS = Unionset.copy() 
    #EXTERNAL ATTACKER
    elif verifmode == 2 : #EXTERNAL ATTACKER
        Unionset = SetlistofbasicsHASATTEX.union(SetlistofnewHAS)
        SetlistofbasicsHASATTEX = Unionset.copy()
    elif verifmode == 3 : #INSIDER ATTACKER
        Unionset = SetlistofbasicsHASATTIN.union(SetlistofnewHAS)
        SetlistofbasicsHASATTIN = Unionset.copy()
    else : #HYBRID ATTACKER
        UnionINATT = SetlistofbasicsHASATTHYB
        Unionset = UnionINATT.union(SetlistofnewHAS)
        SetlistofbasicsHASATTHYB = Unionset.copy() 
        
    if str(query) in set(map(tostring, Unionset)) : 
        return 1
    else : 
        return 0


       

def VerifyCPurposes(details) : 
    for (entity,data) in cpurposesRecArch.keys() : 
        if (entity,data) not in cpurposesRecPol :  
              details = details + "THE ARCHITECTURE DOES NOT DPR CONFORMANCE WITH THE POLICY: " + entity + " COLLECTS DATA (OF TYPE): " + data + " IN THE ARCHITECTURE, BUT NOT IN THE POLICY" "\n\n"
        else : 
            if len(cpurposesRecArch[(entity,data)] - cpurposesRecPol[(entity,data)]) == 0 :
                details = details + "The Architecture DPR  Conforms with The Policy:  The Collection Purposes in the Archticture is a Subset of the Collection Purposes in the Policy \n\n"
            elif len(cpurposesRecArch[(entity,data)] - cpurposesRecPol[(entity,data)]) > 0 : 
               details = details + "THE ARCHITECTURE DOES NOT DPR CONFORMANCE WITH THE POLICY: " + entity + " ALSO COLLECTS DATA (OF TYPE): " + data + " IN THE ARCHITECTURE FOR THE FOLLOWING PURPOSES - " + str(cpurposesRecArch[(entity,data)] - cpurposesRecPol[(entity,data)]) + " - THAT IS NOT DEFINED IN THE POLICY \n\n"



def checkcomplexdatarecvown(strrootarchelement,strent,strcomplexdata,setnotwellformedarch) : 
    global atleastonenotwellformed
    if CheckIfAlreadyReceivedOwn(strent,strcomplexdata) == 0 : 
        for data in DataOrFact(strcomplexdata).arguments: 
            if len(data.arguments) == 0 :
                if CheckIfAlreadyReceivedOwn(strent,str(data)) == 0 :
                    atleastonenotwellformed = 1
                    setnotwellformedarch.add((strrootarchelement, str(data), strent)) 
            elif len(data.arguments) > 0 and str(data.predicate) not in ["time","meta"] : 
                checkcomplexdatarecvown(strrootarchelement,strent,str(data),setnotwellformedarch)



def CheckArchWellFormedness(arch, archpseudo, archmeta, archtime, SetNotWellFormedArch) : 
    global atleastonenotwellformed
    atleastonenotwellformed = 0
    verror = ""
    vlabel = ""
    unionofsets = arch.union(archpseudo,archmeta,archtime)  
    for a in unionofsets : 
        if str(a.predicate) in ["create", "calculate", "calculatefrom"] :   
            if len(a.arguments) > 1 :  
                for arg in a.arguments[1:] : 
                    if len(arg.arguments) > 0 and (str(arg.predicate) not in ["time","meta"]): 
                        
                        for arg2 in arg.arguments :   
                            if len(arg2.arguments) == 0 : 
                                if CheckIfAlreadyReceivedOwn(str(a.arguments[0]),str(arg2)) == 0 : 
                                    atleastonenotwellformed = 1
                                    SetNotWellFormedArch.add((str(a), str(arg2), str(a.arguments[0])))  
                            elif len(arg2.arguments) > 0 and  (str(arg2.predicate) not in ["time","meta"]) : 
                               checkcomplexdatarecvown(str(a),str(a.arguments[0]),str(arg2),SetNotWellFormedArch)
                    else: 
                         if CheckIfAlreadyReceivedOwn(str(a.arguments[0]),str(arg)) == 0 : 
                             atleastonenotwellformed = 1
                             SetNotWellFormedArch.add((str(a), str(arg), str(a.arguments[0]))) 
                             
        elif str(a.predicate) in ["createat","calculateat","calculatefromat"] :   
            if len(a.arguments) > 1 :  
                for arg in a.arguments[1:-1] : 
                    if len(arg.arguments) > 0 and (str(arg.predicate) not in ["time","meta"]): 
                        #print(str(arg.predicate))
                        for arg2 in arg.arguments :   
                            if len(arg2.arguments) == 0 : 
                                if CheckIfAlreadyReceivedOwn(str(a.arguments[0]),str(arg2)) == 0 : 
                                    atleastonenotwellformed = 1
                                    SetNotWellFormedArch.add((str(a), str(arg2), str(a.arguments[0])))  
                            elif len(arg2.arguments) > 0 and  (str(arg2.predicate) not in ["time","meta"]) : 
                               checkcomplexdatarecvown(str(a),str(a.arguments[0]),str(arg2),SetNotWellFormedArch)
                    else: 
                         if CheckIfAlreadyReceivedOwn(str(a.arguments[0]),str(arg)) == 0 : 
                             atleastonenotwellformed = 1
                             SetNotWellFormedArch.add((str(a), str(arg), str(a.arguments[0]))) 
        
        elif str(a.predicate) in ["delete", "deleteat"] :
              if len(a.arguments) > 1 :  
                for arg in a.arguments[1:] : 
                    if  (str(arg.predicate) != "time"):
                        if CheckIfAlreadyReceivedOwn(str(a.arguments[0]),str(arg)) == 0 and  CheckIfAlreadyStoredBeforeDelete(str(a.arguments[0]),str(arg)) == 1:  
                            atleastonenotwellformed = 1  
                            SetNotWellFormedArch.add((str(a), str(arg), str(a.arguments[0])))
                        elif CheckIfAlreadyReceivedOwn(str(a.arguments[0]),str(arg)) == 1 and  CheckIfAlreadyStoredBeforeDelete(str(a.arguments[0]),str(arg)) == 0: 
                            atleastonenotwellformed = 2  
                            SetNotWellFormedArch.add((str(a), str(arg), str(a.arguments[0])))
                        elif CheckIfAlreadyReceivedOwn(str(a.arguments[0]),str(arg)) == 0 and  CheckIfAlreadyStoredBeforeDelete(str(a.arguments[0]),str(arg)) == 0: 
                            atleastonenotwellformed = 3  
                            SetNotWellFormedArch.add((str(a), str(arg), str(a.arguments[0])))
                         
    
        elif str(a.predicate) in ["store", "storeat"] :            
            if len(a.arguments) > 1 :  
                for arg in a.arguments[1:] : 
                    if  (str(arg.predicate) not in ["time","cconsent","uconsent","sconsent","fwconsent"]): 
                        if CheckIfAlreadyReceivedOwn(str(a.arguments[0]),str(arg)) == 0 : 
                            atleastonenotwellformed = 1  
                            SetNotWellFormedArch.add((str(a), str(arg), str(a.arguments[0])))
                    elif (str(arg.predicate) in ["cconsent","uconsent","sconsent","fwconsent"]): 
                        if CheckIfAlreadyReceivedOwn(str(a.arguments[0]),str(arg.arguments[0])) == 0 :  
                            atleastonenotwellformed = 1  
                            SetNotWellFormedArch.add((str(a), str(arg.arguments[0]), str(a.arguments[0])))
                            
    if  atleastonenotwellformed == 1 : 
        vlabel = "WE FOUND NOT WELL-FORMED ARCHITECTURAL ELEMENTS (SEE DETAILS BELOW)"
        for (archelement, data, entity) in SetNotWellFormedArch : 
            if len(DataOrFact(data).arguments) == 0 :
                verror = verror + "THE ELEMENT << " + archelement + " >> IS NOT WELL-FORMED AS THE DATA << " + data + " >> HAS NOT BEEN RECEIVED OR OWNED BY THE ENTITY << " + entity + " >> BEFORE THE ACTION << " + str(DataOrFact(archelement).predicate) + " >> \n ===========> (HINT: DEFINE e.g. receive/receiveat(" + entity + "," + data + "), OR own(" + entity + "," + data + ")))" + "\n"  
            elif len(DataOrFact(data).arguments) > 0 :   
                verror = verror + "THE ELEMENT << " + archelement + " >> IS NOT WELL-FORMED AS THE DATA << " + data + " >> HAS NOT BEEN RECEIVED, OWNED, CREATED OR CALCULATED BY THE ENTITY << " + entity + " >> BEFORE THE ACTION << " + str(DataOrFact(archelement).predicate) + " >> \n ===========> (HINT: DEFINE e.g. receive/receiveat(" + entity + "," + data + "), OR \n ===========> own(" + entity + "," + data + "), OR \n ===========> create/createat(" + entity + "," + data + "), OR \n ===========> calculate/calculateat(" + entity + "," + data + ")))" + "\n" 
                         
        printwellformederror(verror,vlabel)
        return 0   
    
    elif atleastonenotwellformed == 2 : 
        vlabel = "WE FOUND NOT WELL-FORMED ARCHITECTURAL ELEMENTS (SEE DETAILS BELOW)"
        for (archelement, data, entity) in SetNotWellFormedArch : 
            verror = verror + "THE ELEMENT << " + archelement + " >> IS NOT WELL-FORMED AS THE DATA << " + data + " >> HAS NOT BEEN STORED IN << " + entity + " >> BEFORE THE ACTION << " + str(DataOrFact(archelement).predicate) + " >> \n ===========> (HINT: DEFINE e.g. store(" + entity + "," + data + ")" + "\n"  
        
        printwellformederror(verror,vlabel)
        return 0   
        
    elif atleastonenotwellformed == 3 : 
        vlabel = "WE FOUND NOT WELL-FORMED ARCHITECTURAL ELEMENTS (SEE DETAILS BELOW)"
        for (archelement, data, entity) in SetNotWellFormedArch : 
            verror = verror + "THE ELEMENT << " + archelement + " >> IS NOT WELL-FORMED AS THE DATA << " + data + " >> HAS NOT BEEN STORED IN << " + entity + " >> BEFORE THE ACTION << " + str(DataOrFact(archelement).predicate) + " >> \n ===========> (HINT: DEFINE e.g. store(" + entity + "," + data + ")" + "\n"   
            if len(DataOrFact(data).arguments) == 0 : 
                verror = verror + "THE ELEMENT << " + archelement + " >> IS NOT WELL-FORMED AS THE DATA << " + data + " >> HAS NOT BEEN RECEIVED OR OWNED BY THE ENTITY << " + entity + " >> BEFORE THE ACTION << " + str(DataOrFact(archelement).predicate) + " >> \n ===========> (HINT: DEFINE e.g. receive/receiveat(" + entity + "," + data + "), OR own(" + entity + "," + data + ")))" + "\n"  
            elif len(DataOrFact(data).arguments) > 0 :    
                verror = verror + "THE ELEMENT << " + archelement + " >> IS NOT WELL-FORMED AS THE DATA << " + data + " >> HAS NOT BEEN RECEIVED, OWNED, CREATED OR CALCULATED BY THE ENTITY << " + entity + " >> BEFORE THE ACTION << " + str(DataOrFact(archelement).predicate) + " >> \n ===========> (HINT: DEFINE e.g. receive/receiveat(" + entity + "," + data + "), OR \n ===========> own(" + entity + "," + data + "), OR \n ===========> create/createat(" + entity + "," + data + "), OR \n ===========> calculate/calculateat(" + entity + "," + data + ")))" + "\n" 
        
        printwellformederror(verror,vlabel)
        return 0  
    else: return 1



############################################################### WELL-FORMED ARCHITECTURE CHECK ###############################################################

def CheckIfAlreadyReceivedOwn(entity,simpledata) :  
      
    if ((entity,"receive") in recvdOwnArgRec) and (simpledata in recvdOwnArgRec[(entity,"receive")]) : 
        return 1 
    
    if entity in entityRelationRec : 
        for parent in entityRelationRec[entity] :
            if ((parent,"receive") in recvdOwnArgRec) and (simpledata in recvdOwnArgRec[(parent,"receive")]) : 
                return 1
    
    if entity in HasAccessTo :
        for comp in HasAccessTo[entity] :
            if ((comp,"receive") in recvdOwnArgRec) and (simpledata in recvdOwnArgRec[(comp,"receive")]) : 
                return 1
    
   
    
    if ((entity,"receiveat") in recvdOwnArgRec) and (simpledata in recvdOwnArgRec[(entity,"receiveat")]) :
        return 1
    
    if entity in entityRelationRec :
        for parent in entityRelationRec[entity] : 
            if ((parent,"receiveat") in recvdOwnArgRec) and (simpledata in recvdOwnArgRec[(parent,"receiveat")]) : 
                return 1
    
    if entity in HasAccessTo : 
        for comp in HasAccessTo[entity] : 
            if ((comp,"receiveat") in recvdOwnArgRec) and (simpledata in recvdOwnArgRec[(comp,"receiveat")]) : 
                return 1
    
   
    
    if ((entity,"own") in recvdOwnArgRec) and (simpledata in recvdOwnArgRec[(entity,"own")]) :
        return 1 
    
    if entity in entityRelationRec : 
        for parent in entityRelationRec[entity] : 
            if ((parent,"own") in recvdOwnArgRec) and (simpledata in recvdOwnArgRec[(parent,"own")]) : 
                return 1
    
    if entity in HasAccessTo :
        for comp in HasAccessTo[entity] : 
            if ((comp,"own") in recvdOwnArgRec) and (simpledata in recvdOwnArgRec[(comp,"own")]) : 
                return 1
            
    else : return 0



def CheckIfAlreadyStoredBeforeDelete(entity,simpledata) :  
    
       
    if ((entity,"store") in recvdStoreArgRec) and (simpledata in recvdStoreArgRec[(entity,"store")]) : 
        return 1 
    
    if entity in entityRelationRec : 
        for parent in entityRelationRec[entity] : 
            if ((parent,"store") in recvdStoreArgRec) and (simpledata in recvdStoreArgRec[(parent,"store")]) : 
                return 1
    
    if entity in HasAccessTo : 
        for comp in HasAccessTo[entity] : 
            if ((comp,"store") in recvdStoreArgRec) and (simpledata in recvdStoreArgRec[(comp,"store")]) : 
                return 1
    
    
    
    if ((entity,"storeat") in recvdStoreArgRec) and (simpledata in recvdStoreArgRec[(entity,"storeat")]) :
        return 1
    
    if entity in entityRelationRec : 
        for parent in entityRelationRec[entity] : 
            if ((parent,"storeat") in recvdStoreArgRec) and (simpledata in recvdStoreArgRec[(parent,"storeat")]) : 
                return 1
    
    if entity in HasAccessTo : 
        for comp in HasAccessTo[entity] : 
            if ((comp,"storeat") in recvdStoreArgRec) and (simpledata in recvdStoreArgRec[(comp,"storeat")]) : 
                return 1
    
    else : return 0


def printwellformederror(error,label) : 
    errorFrame = Toplevel()
    errorFrame.geometry("600x400")
    errorFrame.title("ARCHITECTURE WELL-FORMEDNESS ERROR")
    errorcanvas = Canvas(errorFrame, width = 600, height = 400, background="LightSalmon")
    lre = Label(errorFrame, text=label,font=("Arial", 12),bg="LightSalmon")
    lre.pack(pady=25)
    tre = scrolledtext.ScrolledText(errorFrame, width=500, heigh=50, bd=1,bg="LightSalmon") 
    tre.insert(END,error)
    tre.pack()


def printresult(result, details) : 
    resultFrame = Toplevel()
    resultFrame.geometry("600x400")
    resultFrame.title("VERIFICATION RESULT")
    resultcanvas = Canvas(resultFrame, width = 600, height = 400)
    lr1 = Label(resultFrame, text=result,font=("Arial", 12))
    lr1.pack(pady=25)
    tr1 = scrolledtext.ScrolledText(resultFrame, width=500, heigh=50, bd=1) 
    tr1.insert(END,details)
    tr1.pack()



def createNotHasTermsAttEx(listattexhasdata) :
    nothasattex = [] 
    
    attexnothas = set(datatypesrec.keys()) - set(listattexhasdata) 
        
    for data in attexnothas : 
        if data != "":
            nothasattex.append(DataOrFact("Has" + "(" + "att" + "," + data.lower() + ")"))     
    return nothasattex
            
def createNotHasTerms(entityhasrec):
    
    nothas = []
    for key, value in entityhasrec.items():
        nothasentities = set(entityrec.keys()) - set(value)     
        
        for entity in nothasentities :
            if entity != "":  
                nothas.append(DataOrFact("Has" + "(" + entity + "," + key.lower() + ")"))
    restdatagroups = set(datatypesrec.keys()) - set(entityhasrec.keys())
   
    for data in restdatagroups :
        for entity2 in entityrec.keys() : 
            if entity2 != "" and data != "" : 
                nothas.append(DataOrFact("Has" + "(" + entity2 + "," + data.lower() + ")"))
 
    return nothas




def components_cpurposesrecpol() : 
    tempRec = cpurposesRecPol.copy()  
    for (parent,simpledata) in tempRec.keys() : 
         if (parent in HasAccessTo) and  len(HasAccessTo[parent]) > 0 :  
            for component in HasAccessTo[parent] : 
               if (component,simpledata) not in setcpurposesRecPol :
                   setcpurposesRecPol[(component,simpledata)] = cpurposesRecPol[(parent,simpledata)]  
                   cpurposesRecPol[(component,simpledata)] = setcpurposesRecPol[(component,simpledata)]
               else : 
                setcpurposesRecPol[(component,simpledata)].union(cpurposesRecPol[(parent,simpledata)])  
                cpurposesRecPol[(component,simpledata)] = setcpurposesRecPol[(component,simpledata)]
                

def components_upurposesrecpol() : 
    tempRec = upurposesRecPol.copy()  
    for (parent,simpledata) in tempRec.keys() : 
         if (parent in HasAccessTo) and  len(HasAccessTo[parent]) > 0 :  
            for component in HasAccessTo[parent] : 
               if (component,simpledata) not in setupurposesRecPol :
                   setupurposesRecPol[(component,simpledata)] = upurposesRecPol[(parent,simpledata)]  
                   upurposesRecPol[(component,simpledata)] = setupurposesRecPol[(component,simpledata)]
               else :
                setupurposesRecPol[(component,simpledata)].union(upurposesRecPol[(parent,simpledata)])  
                upurposesRecPol[(component,simpledata)] = setupurposesRecPol[(component,simpledata)]


##########################################################################################################################################################
############################################################### GUI MODE #################################################################################
##########################################################################################################################################################
                
##########################################################################################################################################################
##########################################################################################################################################################
############################################################## THE POLICY LEVEL ##########################################################################
##########################################################################################################################################################
##########################################################################################################################################################                
                
##################################### GUI FEATURES, OPENING AND SAVING SUB-POLICY INPUTS #################################################################
 
def save_colpolicy_noframe(content1,content2,term11,term22): 
    global queryCConsent
    global setcpurposesRecPol
    global collectionpolconsent
    global cPurposePol
    global cPurposePolAll
    
    term1=term11.lower()
    term2=term22.lower()
    
    collectionpolconsent[term2] = content1[0]       
    
    if content1[0] == "Y": 
        queryCConsent.add("cconsentcollected" + "(" + term1.split(" (")[0] + "," + term2 + ")")
        
    cstringofrow2 = content2.splitlines()

    if lengthall(cstringofrow2) > 0: 
        cstringofrow = set(map(lambda e:e.lower(),cstringofrow2))  
        
        for cstring in cstringofrow :
                if len(cstring) != 0:
                    cseparation1 = cstring.split(":") 
                    cseparation2 = cseparation1[1].split(",")  
                    
                    if term2 not in setcpurposesRecPol :  
                        tempset = set()
                
                    for data in cseparation2 :  
                        cPurposePolAll.add("CPURPOSE(" + data + "," + cseparation1[0] + "," + term2 + ")")   
                        cPurposePolAll.add("CPURPOSE(" + data + "," + cseparation1[0] + ")")
                    
                        
                        tempset.add("CPURPOSE(" + data + "," + cseparation1[0] + "," + term2 + ")")
                        tempset.add("CPURPOSE(" + data + "," + cseparation1[0] + ")")
                    
                        setcpurposesRecPol[term2] = tempset
                        cPurposePol[term2] = setcpurposesRecPol[term2]
                    
                        del setcpurposesRecPol[term2]      
                
           
    
    
def save_usepolicy_noframe(ucontent1,ucontent2,term11,term22): 
    global queryUConsent
    global upurposesRecPol
    global setupurposesRecPol
    global usagepolconsent
    global uPurposePol
    global uPurposePolAll
    
    term1=term11.lower()
    term2=term22.lower()
    
    usagepolconsent[term2] = ucontent1[0]       
    
    if ucontent1[0] == "Y": 
        queryUConsent.add("uconsentcollected" + "(" + term1.split(" (")[0] + "," + term2 + ")")
    
        
    ustringofrow2 = ucontent2.splitlines() 
    
    if lengthall(ustringofrow2) > 0: 
        ustringofrow = set(map(lambda e:e.lower(),ustringofrow2))  
    
    for ustring in ustringofrow :
        if len(ustring) != 0:
            useparation1 = ustring.split(":") 
            useparation2 = useparation1[1].split(",")  
            
            if term2 not in setupurposesRecPol :  
                tempset = set()
                
            for data in useparation2 :  
                uPurposePolAll.add("UPURPOSE(" + data + "," + useparation1[0] + "," + term2 + ")")   
                uPurposePolAll.add("UPURPOSE(" + data + "," + useparation1[0] + ")")
                    
                
                tempset.add("UPURPOSE(" + data + "," + useparation1[0] + "," + term2 + ")")
                tempset.add("PURPOSE(" + data + "," + useparation1[0] + ")")
                    
                setupurposesRecPol[term2] = tempset
                uPurposePol[term2] = setupurposesRecPol[term2]
                    
                del setupurposesRecPol[term2]      
                
           

def save_storepolicy_noframe(scontent1,scontent2, who1, what1):
    global querySConsent
    global storagemodepol    
    global storePolRec 
    
    who=who1.lower()
    what=what1.lower()
    
    storepolconsent[what] = scontent1[0]       
    
    storeoptionrec[(who1, what1)] = scontent2   
    
    if scontent1[0] == "Y": 
        querySConsent.add("strconsentcollected" + "(" +  who.split(" (")[0] + "," + what + ")")    
    
    if scontent2 == "Service Provider (Main & Backup Storage)" : 
        storagemodepol[what] = "centralmainbackup"
        storePolRec["mainstorage"].add(what)  
        storePolRec["backupstorage"].add(what)
        
    elif scontent2 == "Service Provider (Only Main Storage)" : 
        storagemodepol[what] = "centralmain"
        storePolRec["mainstorage"].add(what)  
    else :     
        storagemodepol[what] = "decentral"
    

    
def save_deletepolicy_noframe(dcontent1,dcontent2,deloption,who1,what1):
    global queryHasAfter
    
    who=who1.lower()
    what=what1.lower()
    
    if dcontent1[-1] == "\n":
        dcontent1nobreakline = dcontent1[:-1]
    if dcontent2[-1] == "\n":
        dcontent2nobreakline = dcontent2[:-1]
    
    if dcontent2 != "Service Provider (Only Main Storage)" and dcontent2 != "Decentralised (Not Service Provider)" : 
        
        if evaltime(dcontent1nobreakline) > evaltime(dcontent2nobreakline) : 
            queryHasAfter.add(DataOrFact("HasAfter" + "(" + who.split(" (")[0] + "," + what + "," + "time(" + dcontent1nobreakline  + "))"))
        elif evaltime(dcontent1nobreakline) <= evaltime(dcontent2nobreakline) : 
            queryHasAfter.add(DataOrFact("HasAfter" + "(" + who.split(" (")[0] + "," + what + "," + "time(" + dcontent2nobreakline  + "))"))
    
    
    elif dcontent2 == "Service Provider (Only Main Storage)" : 
        queryHasAfter.add(DataOrFact("HasAfter" + "(" + who.split(" (")[0] + "," + what + "," + "time(" + dcontent1nobreakline  + "))"))
   
    
    elif dcontent2 == "Decentralised (Not Service Provider)" : 
        queryHasAfter.add(DataOrFact("HasAfter" + "(" + deloption.split(" (")[0] + "," + what + "," + "time(" + dcontent1nobreakline  + "))"))
    
    
def save_transferpolicy_noframe(tcontent1,tcontent2, who1, what1):
    global queryFWConsent
    global transferThirdRec
    
    who=who1.lower()
    what=what1.lower()
   
    fwpolconsent[what] = tcontent1[0]       
    
    if tcontent1[0] == "Y": 
        rowsofthird = tcontent2.splitlines()    
        for third in rowsofthird : 
            if len(third) != 0:
                queryFWConsent.add("fwconsentcollected" + "(" + who.split(" (")[0] + "," + what + "," + third + ")")
                for third in rowsofthird : 
                    if len(third) != 0:
                        if what not in transferThirdRec :
                            transferThirdRec[what] = {third}
                        else : 
                            transferThirdRec[what].add(third)
    
    
def save_haspolicy_noframe(hcontent, term11, term22):
    global entityHasListRec
    global entityHasRec
    global listAttExHasData
    
    
    term1=term11.lower()
    term2=term22.lower()
    
    if hcontent[0] == "Y":
        if term1.split(" (")[0] == "att" :  
            queryHasAttEx.append(DataOrFact("Has" + "(" + "att" + "," + term2 + ")"))
            listAttExHasData.append(term2)  
        
        else:  
            if term2 not in set(entityHasRec.keys()):   
                entitylist = []
                entitylist.append(term1.split(" (")[0]) 
                queryHas.append(DataOrFact("Has" + "(" + term1.split(" (")[0] + "," + term2 + ")"))
                
                entityHasListRec[term2] = entitylist
          
                entityHasRec[term2] = entityHasListRec[term2] 
            
            else :
                queryHas.append(DataOrFact("Has" + "(" + term1.split(" (")[0] + "," + term2 + ")"))
          
                entitylist = entityHasListRec[term2]
                entitylist.append(term1.split(" (")[0])
                entityHasListRec[term2] = entitylist
        
                entityHasRec[term2] = entityHasListRec[term2]   
          
    
  
def lengthall(strlist) : 
    length = 0 
    for string in strlist :
        length = length + len(string)
    return length


def save_colpolicy(colframe,content1,content2,term11,term22):  
    
    global setcpurposesRecPol  
    global queryCConsent
    global lastCQuery
    global collectionpolconsent  
    global cPurposePol
    global cPurposePolAll 
   
    
    term1=term11.lower()
    term2=term22.lower()
    
    if term2 in cPurposePol :
        cPurposePolAll = cPurposePolAll - cPurposePol[term2]
        del cPurposePol[term2]  
        
    
    collectionpolconsent[term2] = content1[0]       
    
    collectionpolicytosave[(term11,term22)] = [content1,content2]   
    
    if content1[0] == "Y": 
        if (term1.split(" (")[0],term2) not in lastCQuery :
            lastCQuery[(term1.split(" (")[0],term2)] = "cconsentcollected" + "(" + term1.split(" (")[0] + "," + term2 + ")"
            queryCConsent.add(lastCQuery[(term1.split(" (")[0],term2)])  
   
    cstringcontent1 = content1.splitlines()
    
    if content1[0] == "N" or (lengthall(cstringcontent1) ==0)  :  
        if (term1.split(" (")[0],term2) in lastCQuery : 
            queryCConsent.discard(lastCQuery[(term1.split(" (")[0],term2)])  
            del lastCQuery[(term1.split(" (")[0],term2)] 
        
    cstringofrow2 = content2.splitlines()  
     
        
    if lengthall(cstringofrow2) > 0: 
        cstringofrow = set(map(lambda e:e.lower(),cstringofrow2))  
    
        for cstring in cstringofrow :
            if len(cstring) != 0:
                cseparation1 = cstring.split(":") 
                cseparation2 = cseparation1[1].split(",")  
                
                if term2 not in setcpurposesRecPol : 
                    tempset = set()
                
                for data in cseparation2 :  
                    cPurposePolAll.add("CPURPOSE(" + data + "," + cseparation1[0] + "," + term2 + ")")   
                    cPurposePolAll.add("CPURPOSE(" + data + "," + cseparation1[0] + ")")
                    
                    tempset.add("CPURPOSE(" + data + "," + cseparation1[0] + "," + term2 + ")")
                    tempset.add("CPURPOSE(" + data + "," + cseparation1[0] + ")")
                    
                    setcpurposesRecPol[term2] = tempset
                    cPurposePol[term2] = setcpurposesRecPol[term2]
                    
                    
                    del setcpurposesRecPol[term2]      
            
           
    colframe.destroy()  



def save_usepolicy(useframe,ucontent1,ucontent2, term11, term22):
    
    global setupurposesRecPol
    global queryUConsent
    global lastUQuery
    global usagepolconsent  
    global uPurposePol
    global uPurposePolAll 
    
    term1=term11.lower()
    term2=term22.lower()
    
    if term2 in uPurposePol :
        uPurposePolAll = uPurposePolAll - uPurposePol[term2]
        del uPurposePol[term2]  
    
    usagepolconsent[term2] = ucontent1[0]       
    
    usagepolicytosave[(term11,term22)] = [ucontent1,ucontent2]   
    
    if ucontent1[0] == "Y": 
        if (term1.split(" (")[0],term2) not in lastUQuery :
            lastUQuery[(term1.split(" (")[0],term2)] = "uconsentcollected" + "(" + term1.split(" (")[0] + "," + term2 + ")"
            queryUConsent.add(lastUQuery[(term1.split(" (")[0],term2)]) 
   
    ustringcontent1 = ucontent1.splitlines()
     
    if ucontent1[0] == "N" or (lengthall(ustringcontent1) ==0) :  
        if (term1.split(" (")[0],term2) in lastUQuery : 
            queryUConsent.discard(lastUQuery[(term1.split(" (")[0],term2)])  
            del lastUQuery[(term1.split(" (")[0],term2)] 
    
      
    ustringofrow2 = ucontent2.splitlines()   
    
     
    if lengthall(ustringofrow2) > 0: 
        ustringofrow = set(map(lambda e:e.lower(),ustringofrow2))  
    
        for ustring in ustringofrow :
            if len(ustring) != 0: 
                useparation1 = ustring.split(":") 
                useparation2 = useparation1[1].split(",")  
                
                
                if term2 not in setupurposesRecPol :  
                    tempset = set()
                
                for data in useparation2 :  
                    uPurposePolAll.add("UPURPOSE(" + data + "," + useparation1[0] + "," + term2 + ")")   
                    uPurposePolAll.add("UPURPOSE(" + data + "," + useparation1[0] + ")")
                    
                    
                    tempset.add("UPURPOSE(" + data + "," + useparation1[0] + "," + term2 + ")")
                    tempset.add("UPURPOSE(" + data + "," + useparation1[0] + ")")
                    
                    setupurposesRecPol[term2] = tempset
                    uPurposePol[term2] = setupurposesRecPol[term2]
                
    useframe.destroy()

    
def save_storepolicy(storeframe,scontent1,scontent2, who1, what1):   
    global storagemodepol  
    global querySConsent
    global storePolRec
    global lastSQuery
    global storeoptionrec
    
    who=who1.lower()
    what=what1.lower()
    
    storepolconsent[what] = scontent1[0]       
    
    storeoptionrec[(who1, what1)] = scontent2  
    
    storagepolicytosave[(who1, what1)] = [scontent1,scontent2]  
    
    
    if scontent1[0] == "Y": 
        if (who.split(" (")[0],what) not in lastSQuery :
            lastSQuery[(who.split(" (")[0],what)] = "strconsentcollected" + "(" +  who.split(" (")[0] + "," + what + ")"
            querySConsent.add(lastSQuery[(who.split(" (")[0],what)])  
   
    sstringcontent1 = scontent1.splitlines()
     
    if scontent1[0] == "N" or (lengthall(sstringcontent1) ==0) :  
        if (who.split(" (")[0],what) in lastSQuery : 
            querySConsent.discard(lastSQuery[(who.split(" (")[0],what)])  
            del lastSQuery[(who.split(" (")[0],what)] 
      
    
    if what in storagemodepol : 
        if storagemodepol[what] == "centralmain" :
            if scontent2 == "Service Provider (Main & Backup Storage)" : 
                storagemodepol[what] = "centralmainbackup"
                storePolRec["mainstorage"].add(what)   
                storePolRec["backupstorage"].add(what)
            elif scontent2 == "Service Provider (Only Main Storage)" : 
                storagemodepol[what] = "centralmain"
            else :     
                storagemodepol[what] = "decentral"
                storePolRec["mainstorage"].discard(what)
        elif storagemodepol[what] == "centralmainbackup" : 
            if scontent2 == "Service Provider (Main & Backup Storage)" : 
                storagemodepol[what] = "centralmainbackup"
            elif scontent2 == "Service Provider (Only Main Storage)" : 
                storagemodepol[what] = "centralmain"
                storePolRec["backupstorage"].discard(what)
            else : # decentralised case     
                storagemodepol[what] = "decentral" 
                storePolRec["mainstorage"].discard(what)
                storePolRec["backupstorage"].discard(what)
        elif storagemodepol[what] == "decentral" : 
            if scontent2 == "Service Provider (Main & Backup Storage)" : 
                storagemodepol[what] = "centralmainbackup"
                storePolRec["mainstorage"].add(what)  
                storePolRec["backupstorage"].add(what)
            elif scontent2 == "Service Provider (Only Main Storage)" : 
                storagemodepol[what] = "centralmain"
                storePolRec["mainstorage"].add(what)  
            else :   
                storagemodepol[what] = "decentral"
    elif what not in storagemodepol : 
        if scontent2 == "Service Provider (Main & Backup Storage)" : 
            storagemodepol[what] = "centralmainbackup"
            storePolRec["mainstorage"].add(what)   
            storePolRec["backupstorage"].add(what)
            
        elif scontent2 == "Service Provider (Only Main Storage)" : 
            storagemodepol[what] = "centralmain"
            storePolRec["mainstorage"].add(what)   
        else :   
            storagemodepol[what] = "decentral"
    storeframe.destroy()


def removeterm(termset,term) :
    sstr=set(map(tostring, termset))
    sstr.discard(str(term))
    return(set(map(strtoterm, sstr)))


def save_deletepolicy(deleteframe,dcontent1,dcontent2,deloption,who1,what1):
    global queryHasAfter
    global lastDQuery
    
    who=who1.lower()
    what=what1.lower()
    
    deletionpolicytosave[(who1, what1)] = [deloption,dcontent1,dcontent2]
    
    dstringcontent1 = dcontent1.splitlines()
    dstringcontent2 = dcontent2.splitlines()
    
    if dcontent1[-1] == "\n":
        dcontent1nobreakline = dcontent1[:-1]
    if dcontent2[-1] == "\n":
        dcontent2nobreakline = dcontent2[:-1]
    
    
    if dcontent2 != "Service Provider (Only Main Storage)" and dcontent2 != "Decentralised (Not Service Provider)" : 
     
        if deloption != "Only From Main Storage" :
            if (who.split(" (")[0],what) not in lastDQuery : 
                if evaltime(dcontent1nobreakline) > evaltime(dcontent2nobreakline) : 
                    lastDQuery[(who.split(" (")[0],what)] = "HasAfter" + "(" + who.split(" (")[0] + "," + what + "," + "time(" + dstringcontent1[0] + "))" 
                    queryHasAfter.add(DataOrFact(lastDQuery[(who.split(" (")[0],what)]))
                elif evaltime(dcontent1nobreakline) <= evaltime(dcontent2nobreakline) : 
                    lastDQuery[(who.split(" (")[0],what)] = "HasAfter" + "(" + who.split(" (")[0] + "," + what + "," + "time(" + dstringcontent2[0] + "))" 
                    queryHasAfter.add(DataOrFact(lastDQuery[(who.split(" (")[0],what)]))
            elif (who.split(" (")[0],what) in lastDQuery :
                queryHasAfter = removeterm(queryHasAfter,DataOrFact(lastDQuery[(who.split(" (")[0],what)])) 
                if evaltime(dcontent1nobreakline) > evaltime(dcontent2nobreakline) : 
                    lastDQuery[(who.split(" (")[0],what)] = "HasAfter" + "(" + who.split(" (")[0] + "," + what + "," + "time("  + dstringcontent1[0] + "))"
                    queryHasAfter.add(DataOrFact(lastDQuery[(who.split(" (")[0],what)]))
                elif evaltime(dcontent1nobreakline) <= evaltime(dcontent2nobreakline) : 
                    lastDQuery[(who.split(" (")[0],what)] = "HasAfter" + "(" + who.split(" (")[0] + "," + what + "," + "time(" + dstringcontent2[0] + "))"
                    queryHasAfter.add(DataOrFact(lastDQuery[(who.split(" (")[0],what)]))       
        elif deloption == "Only From Main Storage" :
            if (who.split(" (")[0],what) not in lastDQuery :  
                lastDQuery[(who.split(" (")[0],what)] = "HasAfter" + "(" + who.split(" (")[0] + "," + what + "," + "time(" + dstringcontent1[0] + "))"
                queryHasAfter.add(DataOrFact(lastDQuery[(who.split(" (")[0],what)]))
            elif (who.split(" (")[0],what) in lastDQuery :
                queryHasAfter = removeterm(queryHasAfter,DataOrFact(lastDQuery[(who.split(" (")[0],what)]))
                lastDQuery[(who.split(" (")[0],what)] = "HasAfter" + "(" + who.split(" (")[0] + "," + what + "," + "time(" + dstringcontent1[0] + "))"
                queryHasAfter.add(DataOrFact(lastDQuery[(who.split(" (")[0],what)]))      
       
        
    if dcontent2 == "Service Provider (Only Main Storage)" : 
        if (who.split(" (")[0],what) not in lastDQuery : 
            lastDQuery[(who.split(" (")[0],what)] = "HasAfter" + "(" + who.split(" (")[0] + "," + what + "," + "time(" + dstringcontent1[0] + "))"
            queryHasAfter.add(DataOrFact(lastDQuery[(who.split(" (")[0],what)]))
        elif (who.split(" (")[0],what) in lastDQuery :
            queryHasAfter = removeterm(queryHasAfter,DataOrFact(lastDQuery[(who.split(" (")[0],what)])) 
            lastDQuery[(who.split(" (")[0],what)] = "HasAfter" + "(" + who.split(" (")[0] + "," + what + "," + "time(" + dstringcontent1[0] + "))"
            queryHasAfter.add(DataOrFact(lastDQuery[(who.split(" (")[0],what)]))
            
    
            
    if dcontent2 == "Decentralised (Not Service Provider)" : 
        if (deloption.split(" (")[0],what) not in lastDQuery : 
            lastDQuery[(deloption.split(" (")[0],what)] = "HasAfter" + "(" + deloption.split(" (")[0] + "," + what + "," + "time(" + dstringcontent1[0] + "))"
            queryHasAfter.add(DataOrFact(lastDQuery[(deloption.split(" (")[0],what)]))
        elif (deloption.split(" (")[0],what) in lastDQuery :
            queryHasAfter = removeterm(queryHasAfter,DataOrFact(lastDQuery[(deloption.split(" (")[0],what)])) 
            lastDQuery[(deloption.split(" (")[0],what)] = "HasAfter" + "(" + deloption.split(" (")[0] + "," + what + "," + "time(" + dstringcontent1[0] + "))"
            queryHasAfter.add(DataOrFact(lastDQuery[(deloption.split(" (")[0],what)]))         
   
    
    deleteframe.destroy()



def save_transferpolicy(transferframe,tcontent1,tcontent2, who1, what1) :
    global queryFWConsent
    global lastTQuery
    global transferThirdRec
    
    who=who1.lower()
    what=what1.lower()
    
    fwpolconsent[what] = tcontent1[0]       
    
    transferpolicytosave[(who1, what1)] = [tcontent1,tcontent2]
    
    if tcontent1[0] == "Y": 
        rowsofthird = tcontent2.splitlines()    
        
        if len(rowsofthird) > 0 :
            for third in rowsofthird : 
                if len(third) != 0:
                    if what not in transferThirdRec :
                        transferThirdRec[what] = {third}
                    else : 
                        transferThirdRec[what].add(third)
        else : 
            del transferThirdRec[what]
        
        if (who.split(" (")[0],what) not in lastTQuery :       
            for third in rowsofthird : 
                if len(third) != 0: 
                    if third == rowsofthird[0] :
                        lastTQuery[(who.split(" (")[0],what)] = {"fwconsentcollected" + "(" + who.split(" (")[0] + "," + what + "," + third + ")"} 
                        queryFWConsent.add("fwconsentcollected" + "(" + who.split(" (")[0] + "," + what + "," + third + ")")
                    else :
                        lastTQuery[(who.split(" (")[0],what)].add("fwconsentcollected" + "(" + who.split(" (")[0] + "," + what + "," + third + ")")    
                        queryFWConsent.add("fwconsentcollected" + "(" + who.split(" (")[0] + "," + what + "," + third + ")")
                        
        elif (who.split(" (")[0],what) in lastTQuery : 
            for fwquery in lastTQuery[(who.split(" (")[0],what)] : 
                queryFWConsent.discard(fwquery)  
            lastTQuery[(who.split(" (")[0],what)] = set()
            for third in rowsofthird : 
                if len(third) != 0: 
                    lastTQuery[(who.split(" (")[0],what)].add("fwconsentcollected" + "(" + who.split(" (")[0] + "," + what + "," + third + ")") 
                    queryFWConsent.add("fwconsentcollected" + "(" + who.split(" (")[0] + "," + what + "," + third + ")")  
            
    if tcontent1[0] == "N" or tcontent1[0] == "" :
        if (who.split(" (")[0],what) in lastTQuery : 
            for fwquery in lastTQuery[(who.split(" (")[0],what)] : 
                queryFWConsent.discard(fwquery)  
            del lastTQuery[(who.split(" (")[0],what)] 
    
   
                
    transferframe.destroy()




def insert_towhom(srolled,content) :
    srolled.insert(END,content.split(" (")[0] + "\n")   


    
def save_haspolicy(hasframe,hcontent, term11, term22):  
    global queryHas
    global queryHasAttEx
    global lastHQuery
    global lastHQueryAttEx
    global entityHasListRec
    global entityHasRec
    global listAttExHasData
  
    
    
    term1=term11.lower()
    term2=term22.lower()
    
    haspolicytosave[(term11, term22)] = [hcontent] 
    
    hstringcontent = hcontent.splitlines()
    
    if hcontent[0] == "Y":
    
        if term1.split(" (")[0] == "att" :  # An attacker entity
            if term2 not in lastHQueryAttEx :
                lastHQueryAttEx[term2] = "Has" + "(" + "att" + "," + term2 + ")"
                queryHasAttEx.append(DataOrFact(lastHQueryAttEx[term2]))
                listAttExHasData.append(term2)  
            
        else : # not an attacker entity  
            if (term1.split(" (")[0],term2) not in lastHQuery :    
                if term2 not in set(entityHasRec.keys()):   
                    lastHQuery[(term1.split(" (")[0],term2)] = "Has" + "(" + term1.split(" (")[0] + "," + term2 + ")"
                    queryHas.append(DataOrFact(lastHQuery[(term1.split(" (")[0],term2)]))
                    entitylist = [] 
                    entitylist.append(term1.split(" (")[0]) 
                    entityHasListRec[term2] = entitylist
                    entityHasRec[term2] = entityHasListRec[term2] 
                else :
                    lastHQuery[(term1.split(" (")[0],term2)] = "Has" + "(" + term1.split(" (")[0] + "," + term2 + ")"
                    queryHas.append(DataOrFact(lastHQuery[(term1.split(" (")[0],term2)]))
                    entitylist = entityHasListRec[term2]
                    entitylist.append(term1.split(" (")[0])
                    entityHasListRec[term2] = entitylist     
                    entityHasRec[term2] = entityHasListRec[term2]   
               
      
    elif  hcontent[0] == "N" or (lengthall(hstringcontent)==0) : 
        if term1.split(" (")[0] == "att" :  # An attacker entity 
            if term2 in lastHQueryAttEx :
                queryHasAttEx = list(removeterm(set(queryHasAttEx), DataOrFact(lastHQueryAttEx[term2])))
                lastHQueryAttEx.clear() 
                if term2 in listAttExHasData : 
                    listAttExHasData.remove(term2)
        else:  # not an attacker entity
            if (term1.split(" (")[0],term2) in lastHQuery :   
                queryHas=list(removeterm(set(queryHas), DataOrFact(lastHQuery[(term1.split(" (")[0],term2)])))
                lastHQuery.clear()
                if term2 in set(entityHasRec.keys()): 
                    del entityHasRec[term2] 
    
        
    hasframe.destroy()


def save_linkpermitpolicy(lframe, lcontent, who1, what1):   
    linkpermitpolicytosave[(who1, what1)] = [lcontent]
    lframe.destroy()
    

def save_linkforbidpolicy(lframe, lcontent, who1, what1):   
    linkforbidpolicytosave[(who1, what1)] = [lcontent]
    lframe.destroy()
    
    
def add_linkpolicy(linkframe,lentity1,ldata11,ldata22,isunique,srolled):
    
    global lastLinkPer  
    global queryLinkUnique
    global queryLink
    
    lentity=lentity1.lower()
    ldata1=ldata11.lower()
    ldata2=ldata22.lower()
    
   
    if isunique == "Yes" : 
        if (lentity.split(" (")[0],ldata1) not in lastLinkPer :
            lastLinkPer[(lentity.split(" (")[0],ldata1)] = {"LinkUnique" + "(" + lentity.split(" (")[0] + "," + ldata1 + "," + ldata2 + ")"}
        else: 
            lastLinkPer[(lentity.split(" (")[0],ldata1)].add("LinkUnique" + "(" + lentity.split(" (")[0] + "," + ldata1 + "," + ldata2 + ")")
        queryLinkUnique.append(DataOrFact("LinkUnique" + "(" + lentity.split(" (")[0] + "," + ldata1 + "," + ldata2 + ")"))
        srolled.insert(END,ldata1 + "-" + ldata2 + ":" + "Unique Link is Allowed" + "\n")
             
    
    if isunique == "No" :   
        if (lentity.split(" (")[0],ldata1) not in lastLinkPer :
            lastLinkPer[(lentity.split(" (")[0],ldata1)] = {"Link" + "(" + lentity.split(" (")[0] + "," + ldata1 + "," + ldata2 + ")"}
        else: 
            lastLinkPer[(lentity.split(" (")[0],ldata1)].add("Link" + "(" + lentity.split(" (")[0] + "," + ldata1 + "," + ldata2 + ")")
        lastLinkPer[(lentity.split(" (")[0],ldata1)] = {"Link" + "(" + lentity.split(" (")[0] + "," + ldata1 + "," + ldata2 + ")"}
        queryLink.append(DataOrFact("Link" + "(" + lentity.split(" (")[0] + "," + ldata1 + "," + ldata2 + ")"))
        srolled.insert(END,ldata1 + "-" + ldata2 + ":" + "Only Not Unique Link is Allowed" + "\n")


        
def add_linkforbidpolicy(linkframe,lentity1,ldata11,ldata22,isunique,srolled):
    global lastLinkFor
    global queryNotLinkUnique
    global queryNotLink
    
    lentity=lentity1.lower()
    ldata1=ldata11.lower()
    ldata2=ldata22.lower()
    
    
    
    if isunique == "Yes" : 
        if (lentity.split(" (")[0],ldata1) not in lastLinkFor :
            lastLinkFor[(lentity.split(" (")[0],ldata1)] = {"LinkUnique" + "(" + lentity.split(" (")[0] + "," + ldata1 + "," + ldata2 + ")"}
        else: 
            lastLinkFor[(lentity.split(" (")[0],ldata1)].add("LinkUnique" + "(" + lentity.split(" (")[0] + "," + ldata1 + "," + ldata2 + ")")
        queryNotLinkUnique.append(DataOrFact("LinkUnique" + "(" + lentity.split(" (")[0] + "," + ldata1 + "," + ldata2 + ")"))
        srolled.insert(END,ldata1 + "-" + ldata2 + ":" + "Unique Link is Forbidden" + "\n")
             
    
    if isunique == "No" :   
        if (lentity.split(" (")[0],ldata1) not in lastLinkFor :
            lastLinkFor[(lentity.split(" (")[0],ldata1)] = {"Link" + "(" + lentity.split(" (")[0] + "," + ldata1 + "," + ldata2 + ")"}
        else: 
            lastLinkFor[(lentity.split(" (")[0],ldata1)].add("Link" + "(" + lentity.split(" (")[0] + "," + ldata1 + "," + ldata2 + ")")
        lastLinkFor[(lentity.split(" (")[0],ldata1)] = {"Link" + "(" + lentity.split(" (")[0] + "," + ldata1 + "," + ldata2 + ")"}
        queryNotLink.append(DataOrFact("Link" + "(" + lentity.split(" (")[0] + "," + ldata1 + "," + ldata2 + ")"))
        srolled.insert(END,ldata1 + "-" + ldata2 + ":" + "Any Link is Forbidden" + "\n")
    
    
################################################ CLEAR LINK SUB-POLICIES #################################################################################################

def clear_linkpolicy(linkframe,lentity1,ldata11,ldata22,isunique,srolled): 
    global lastLinkPer  
    global queryLinkUnique
    global queryLink
    
    lentity=lentity1.lower()
    ldata1=ldata11.lower()
    
    if (lentity.split(" (")[0],ldata1) in lastLinkPer : 
       
        for linkquery in lastLinkPer[(lentity.split(" (")[0],ldata1)] : 
            
            queryLinkUnique = list(removeterm(set(queryLinkUnique), DataOrFact(linkquery)))  
            
            queryLink = list(removeterm(set(queryLink), DataOrFact(linkquery)))  
        del lastLinkPer[(lentity.split(" (")[0],ldata1)] 
    srolled.delete('1.0',END)     
        

def clear_linkforbidpolicy(linkframe,lentity1,ldata11,ldata22,isunique,srolled):
    global lastLinkFor
    global queryNotLinkUnique
    global queryNotLink
    
    lentity=lentity1.lower()
    ldata1=ldata11.lower()
    
    if (lentity.split(" (")[0],ldata1) in lastLinkFor : 
         for linkquery in lastLinkFor[(lentity.split(" (")[0],ldata1)] : 
            
                 queryNotLinkUnique = list(removeterm(set(queryNotLinkUnique), DataOrFact(linkquery)))   
            
                 queryNotLink = list(removeterm(set(queryNotLink), DataOrFact(linkquery)))  
         del lastLinkFor[(lentity.split(" (")[0],ldata1)] 
    srolled.delete('1.0',END)
    


def close_delpolicy(deleteframe) :
    deleteframe.destroy()

################################################ SUB-POLICIES GUI INPUT ##################################################################################################
    
def linkpol(loption1, loption2, loption3):
    if loption3 in ["-",""] : 
        linkFrame = Toplevel()
        linkFrame.geometry("700x550")
        linkFrame.title("DATA CONNECTION/LINKING POLICY - PERMIT POLICY")
        linkcanvas = Canvas(linkFrame, width = 700, height = 200, bg = "ivory2")
        ll1 = Label(linkcanvas, text="Choose a (data) group that " + loption1 + " is PERMITTED to be able to link with the data of type/group " + loption2,font=("Arial", 10), bg = "ivory2")
        ll1.pack(pady=25)
        
        OPTIONS3 = list(datatypesrec.keys()) 
        variable3 = StringVar(linkcanvas)
        
    
        variable3.set(OPTIONS3[-1])  
           
        
        wl = OptionMenu(linkcanvas, variable3, *OPTIONS3)
        wl.pack()
    
        ll2 = Label(linkcanvas, text="Do you PERMIT " + loption1  + " to uniquely link these two types of data ?",font=("Arial", 10), bg = "ivory2")
        ll2.pack(pady=25)
       
        OPTIONS4 = ["Yes","No"] 
        variable4 = StringVar(linkcanvas)
        
        
        variable4.set(OPTIONS4[-1])  
             
        wl2 = OptionMenu(linkcanvas, variable4, *OPTIONS4)
        wl2.pack()
        linkcanvas.pack(fill=BOTH) 
    
       
        middlecanvas = Canvas(linkFrame, width = 700, height = 200, bg = "ivory2")
        ll3 = Label(middlecanvas, text="     ",font=("Arial", 11),bg = "ivory2")
        ll3.pack()
        tl1 = scrolledtext.ScrolledText(middlecanvas, width=100, heigh=10, bd=1) 
        
        if (loption1, loption2) in linkpermitpolicytosave : 
            tl1.insert(END,linkpermitpolicytosave[(loption1, loption2)][0]) 
        else : 
            tl1.insert(END,"")
        tl1.pack()
        
        ll4 = Label(middlecanvas, text="     ",font=("Arial", 11),bg = "ivory2")
        ll4.pack()
        middlecanvas.pack(fill=BOTH)  
    
        
        bottomcanvas = Canvas(linkFrame, width = 700, height = 200)
        ll5 = Label(bottomcanvas, text="                                      ",font=("Arial", 11))
        ll5.pack() 
        ll6 = Label(bottomcanvas, text="                                      ",font=("Arial", 11))
        ll6.pack() 
        addlinkbutton = Button(bottomcanvas,text="ADD DATA CONNECTION POLICY", command=lambda:add_linkpolicy(linkFrame,loption1,loption2,variable3.get(),variable4.get(),tl1))    
        addlinkbutton.pack() 
        addlinkdelbutton = Button(bottomcanvas,text="DELETE CONNECTION POLICY", command=lambda:clear_linkpolicy(linkFrame,loption1,loption2,variable3.get(),variable4.get(),tl1))    
        addlinkdelbutton.pack() 
        closebutton = Button(bottomcanvas,text="CLOSE & SAVE", command=lambda:save_linkpermitpolicy(linkFrame,tl1.get("1.0", END),loption1,loption2))    
        closebutton.pack() 
        bottomcanvas.pack(expand=True,fill=BOTH) 
    else: 
        linkFrame = Toplevel()
        linkFrame.geometry("700x550")
        linkFrame.title("DATA CONNECTION/LINKING POLICY - PERMIT POLICY")
        linkcanvas = Canvas(linkFrame, width = 700, height = 200, bg = "ivory2")
        ll1 = Label(linkcanvas, text="Choose a (data) group that " + loption1 + " is PERMITTED to be able to link with the data of type " + loption3,font=("Arial", 10), bg = "ivory2")
        ll1.pack(pady=25)
       
        OPTIONS3 = list(datatypesrec[datagroupoftypes[loption3]]) 
        variable3 = StringVar(linkcanvas)
        
        variable3.set(OPTIONS3[-1]) 
        
        wl = OptionMenu(linkcanvas, variable3, *OPTIONS3)
        wl.pack()
    
        ll2 = Label(linkcanvas, text="Do you PERMIT " + loption1  + " to uniquely link these two types of data ?",font=("Arial", 10), bg = "ivory2")
        ll2.pack(pady=25)
        
        OPTIONS4 = ["Yes","No"] 
        variable4 = StringVar(linkcanvas)
        
       
        variable4.set(OPTIONS4[-1]) 
        
        wl2 = OptionMenu(linkcanvas, variable4, *OPTIONS4)
        wl2.pack()
        linkcanvas.pack(fill=BOTH) 
    
      
        middlecanvas = Canvas(linkFrame, width = 700, height = 200, bg = "ivory2")
        ll3 = Label(middlecanvas, text="     ",font=("Arial", 11),bg = "ivory2")
        ll3.pack()
        tl1 = scrolledtext.ScrolledText(middlecanvas, width=100, heigh=10, bd=1) 
        
        if (loption1, loption2) in linkpermitpolicytosave : 
            tl1.insert(END,linkpermitpolicytosave[(loption1, loption2)][0]) 
        else : 
            tl1.insert(END,"") 
        tl1.pack()
        
        ll4 = Label(middlecanvas, text="     ",font=("Arial", 11),bg = "ivory2")
        ll4.pack()
        middlecanvas.pack(fill=BOTH)   
    
        
        bottomcanvas = Canvas(linkFrame, width = 700, height = 200)
        ll5 = Label(bottomcanvas, text="                                      ",font=("Arial", 11))
        ll5.pack() 
        ll6 = Label(bottomcanvas, text="                                      ",font=("Arial", 11))
        ll6.pack() 
        addlinkbutton = Button(bottomcanvas,text="ADD DATA CONNECTION POLICY", command=lambda:add_linkpolicy(linkFrame,loption1,loption3,variable3.get(),variable4.get(),tl1))    
        addlinkbutton.pack() 
        addlinkdelbutton = Button(bottomcanvas,text="DELETE CONNECTION POLICY", command=lambda:clear_linkpolicy(linkFrame,loption1,loption3,variable3.get(),variable4.get(),tl1))    
        addlinkdelbutton.pack() 
        closebutton = Button(bottomcanvas,text="CLOSE & SAVE", command=lambda:save_linkpermitpolicy(linkFrame,tl1.get("1.0", END),loption1,loption2))    
        closebutton.pack() 
        bottomcanvas.pack(expand=True,fill=BOTH) 


def linkforbidpol(loption1, loption2, loption3):
    if loption3 in ["-",""] : 
        linkFrame = Toplevel()
        linkFrame.geometry("700x550")
        linkFrame.title("DATA CONNECTION/LINKING POLICY - FORBID POLICY")
        linkcanvas = Canvas(linkFrame, width = 700, height = 200, bg = "alice blue")
        ll1 = Label(linkcanvas, text="Choose a (data) group that " + loption1 + " is FORBIDDEN to be able to link with the data of type " + loption2,font=("Arial", 10), bg = "alice blue")
        ll1.pack(pady=25)
      
        OPTIONS3 = list(datatypesrec.keys()) 
        variable3 = StringVar(linkcanvas)
        
       
        variable3.set(OPTIONS3[-1]) 
        
        wl = OptionMenu(linkcanvas, variable3, *OPTIONS3)
        wl.pack()
    
        ll2 = Label(linkcanvas, text="Do you FORBID " + loption1  + " only to uniquely link these two types of data ?",font=("Arial", 10), bg = "alice blue")
        ll2.pack(pady=25)
        
        OPTIONS4 = ["Yes","No"] 
        variable4 = StringVar(linkcanvas)
        
        
        variable4.set(OPTIONS4[-1]) 
        
        wl2 = OptionMenu(linkcanvas, variable4, *OPTIONS4)
        wl2.pack()
        linkcanvas.pack(fill=BOTH) 
    
       
        middlecanvas = Canvas(linkFrame, width = 700, height = 200, bg = "alice blue")
        ll3 = Label(middlecanvas, text="     ",font=("Arial", 11),bg = "alice blue")
        ll3.pack()
        tl1 = scrolledtext.ScrolledText(middlecanvas, width=100, heigh=10, bd=1) 
        
        if (loption1, loption2) in linkforbidpolicytosave : 
            tl1.insert(END,linkforbidpolicytosave[(loption1, loption2)][0]) 
        else : 
            tl1.insert(END,"") 
        tl1.pack()
        
        ll4 = Label(middlecanvas, text="     ",font=("Arial", 11),bg = "alice blue")
        ll4.pack()
        middlecanvas.pack(fill=BOTH)   
    
        
        bottomcanvas = Canvas(linkFrame, width = 700, height = 200)
        ll5 = Label(bottomcanvas, text="                                      ",font=("Arial", 11))
        ll5.pack() 
        ll6 = Label(bottomcanvas, text="                                      ",font=("Arial", 11))
        ll6.pack() 
        addlinkbutton = Button(bottomcanvas,text="ADD DATA CONNECTION POLICY", command=lambda:add_linkforbidpolicy(linkFrame,loption1,loption2,variable3.get(),variable4.get(),tl1))    
        addlinkbutton.pack() 
        addlinkdelbutton = Button(bottomcanvas,text="DELETE CONNECTION POLICY", command=lambda:clear_linkforbidpolicy(linkFrame,loption1,loption2,variable3.get(),variable4.get(),tl1))    
        addlinkdelbutton.pack() 
        closebutton = Button(bottomcanvas,text="CLOSE & SAVE", command=lambda:save_linkforbidpolicy(linkFrame,tl1.get("1.0", END),loption1,loption2))    
        closebutton.pack() 
        bottomcanvas.pack(expand=True,fill=BOTH) 
    else:
        linkFrame = Toplevel()
        linkFrame.geometry("700x550")
        linkFrame.title("DATA CONNECTION/LINKING POLICY - FORBID POLICY")
        linkcanvas = Canvas(linkFrame, width = 700, height = 200, bg = "alice blue")
        ll1 = Label(linkcanvas, text="Choose a (data) group that " + loption1 + " is FORBIDDEN to be able to link with the data of type " + loption3,font=("Arial", 10), bg = "alice blue")
        ll1.pack(pady=25)
        
        OPTIONS3 = list(datatypesrec[datagroupoftypes[loption3]]) 
        variable3 = StringVar(linkcanvas)
        
        
        variable3.set(OPTIONS3[-1])
        
        wl = OptionMenu(linkcanvas, variable3, *OPTIONS3)
        wl.pack()
    
        ll2 = Label(linkcanvas, text="Do you FORBID " + loption1  + " to uniquely link these two types of data ?",font=("Arial", 10), bg = "alice blue")
        ll2.pack(pady=25)
       
        OPTIONS4 = ["Yes","No"] 
        variable4 = StringVar(linkcanvas)
        
        variable4.set(OPTIONS4[-1])  
        
        wl2 = OptionMenu(linkcanvas, variable4, *OPTIONS4)
        wl2.pack()
        linkcanvas.pack(fill=BOTH) 
    
        
        middlecanvas = Canvas(linkFrame, width = 700, height = 200, bg = "alice blue")
        ll3 = Label(middlecanvas, text="     ",font=("Arial", 11),bg = "alice blue")
        ll3.pack()
        tl1 = scrolledtext.ScrolledText(middlecanvas, width=100, heigh=10, bd=1) 
        
        if (loption1, loption2) in linkforbidpolicytosave : 
            tl1.insert(END,linkforbidpolicytosave[(loption1, loption2)][0]) 
        else : 
            tl1.insert(END,"") 
        tl1.pack()
        
        tl1.pack()
        ll4 = Label(middlecanvas, text="     ",font=("Arial", 11),bg = "alice blue")
        ll4.pack()
        middlecanvas.pack(fill=BOTH)  
    
       
        bottomcanvas = Canvas(linkFrame, width = 700, height = 200)
        ll5 = Label(bottomcanvas, text="                                      ",font=("Arial", 11))
        ll5.pack() 
        ll6 = Label(bottomcanvas, text="                                      ",font=("Arial", 11))
        ll6.pack() 
        addlinkbutton = Button(bottomcanvas,text="ADD DATA CONNECTION POLICY", command=lambda:add_linkforbidpolicy(linkFrame,loption1,loption3,variable3.get(),variable4.get(),tl1))    
        addlinkbutton.pack() 
        addlinkdelbutton = Button(bottomcanvas,text="DELETE CONNECTION POLICY", command=lambda:clear_linkforbidpolicy(linkFrame,loption1,loption3,variable3.get(),variable4.get(),tl1))    
        addlinkdelbutton.pack() 
        closebutton = Button(bottomcanvas,text="CLOSE & SAVE", command=lambda:save_linkforbidpolicy(linkFrame,tl1.get("1.0", END),loption1,loption2))    
        closebutton.pack() 
        bottomcanvas.pack(expand=True,fill=BOTH) 
        

        
def haspol(option1, option2, option3):
    if option3 not in ["-",""] : 
        hasFrame = Toplevel()
        hasFrame.geometry("700x400")
        hasFrame.title("DATA POSSESSION POLICY")
        hascanvas = Canvas(hasFrame, width = 650, height = 400)
        lh1 = Label(hasFrame, text="THE DATA POSSESSION POLICY CAN ONLY BE DEFINED FOR A DATA GROUP\n DATA TYPES CAN ONLY BE DEFINED IN THE DATA CONNECTIONS POLICIES \n (THE LAST TWO SUB-POLICIES)",font=("Arial", 10))
        lh1.pack(pady=25) 
    else: 
        hasFrame = Toplevel()
        hasFrame.geometry("650x400")
        hasFrame.title("DATA POSSESSION POLICY")
        hascanvas = Canvas(hasFrame, width = 650, height = 400)
        lh1 = Label(hasFrame, text="Is " + option1 + " allowed to have/possess the data group " + option2 + " ? (Y if Yes/Leave empty or N if NO)",font=("Arial", 10))
        lh1.pack(pady=25)
        h1 = scrolledtext.ScrolledText(hasFrame, width=55, heigh=1, bd=1) 
        
        if (option1, option2) in haspolicytosave : 
            h1.insert(END,haspolicytosave[(option1, option2)][0]) 
        else : 
            h1.insert(END,"") 
        h1.pack()
        
       
        savehasbutton = Button(hascanvas,text="SAVE DATA POSSESSION POLICY & CLOSE", command=lambda:save_haspolicy(hasFrame,h1.get("1.0", END),option1,option2))  #,h2.get("1.0", END)   
        savehasbutton.pack()
        hascanvas.pack(expand=True,fill=BOTH)



def transferpol(option1, option2, option3): 
    if option3 not in ["-",""] : 
        transferFrame = Toplevel()
        transferFrame.geometry("700x400")
        transferFrame.title("DATA TRANSFER POLICY")
        transfercanvas = Canvas(transferFrame, width = 700, height = 400)
        lt1 = Label(transferFrame, text="THE TRANSFER POLICY CAN ONLY BE DEFINED FOR A DATA GROUP\n DATA TYPES CAN ONLY BE DEFINED IN THE DATA CONNECTIONS POLICIES \n (THE LAST TWO SUB-POLICIES)",font=("Arial", 11))
        lt1.pack(pady=25)    
    else:
        transferFrame = Toplevel()
        transferFrame.geometry("760x600")
        transferFrame.title("DATA TRANSFER POLICY")
        transfercanvas = Canvas(transferFrame, width = 760, height = 300)
        lt1 = Label(transferFrame, text="Does " + option1 + " need to collect consent before transfering the data (of type) " + option2 + " ? (give Y or N)",font=("Arial", 11))
        lt1.pack(pady=25)
        t1 = scrolledtext.ScrolledText(transferFrame, width=55, heigh=1, bd=1) 
        
        if (option1, option2) in transferpolicytosave : 
            t1.insert(END,transferpolicytosave[(option1, option2)][0]) 
        else : 
            t1.insert(END,"") 
        t1.pack()
   
        
        transfermiddlecanvas = Canvas(transferFrame, width = 760, height = 300)
        transfermiddlecanvas.pack(expand=True,fill=BOTH)
    
        lt2 = Label(transfermiddlecanvas, text="    ",font=("Arial", 12))
        lt2.pack()
    
        TOPTIONS = convertdicttolist(entityrec) 
        tvariable = StringVar(transfermiddlecanvas)
        tvariable.set(TOPTIONS[-1]) 
        te = Label(transfermiddlecanvas, text="Choose to whom << " + option1 + " >> can transfer the data (of type) << " + option2 + " >>", font=("Arial", 11))
        te.pack()
        wte = OptionMenu(transfermiddlecanvas, tvariable, *TOPTIONS)
        wte.pack()
    
    
        lt3 = Label(transfermiddlecanvas, text="     ",font=("Arial", 12))
        lt3.pack()
    
        t2 = scrolledtext.ScrolledText(transfermiddlecanvas, width=40, heigh=10, bd=1) 
        
        if (option1, option2) in transferpolicytosave : 
            t2.insert(END,transferpolicytosave[(option1, option2)][1]) 
        else : 
            t2.insert(END,"") 
        t2.pack()
    
    
        lt4 = Label(transfermiddlecanvas, text="     ",font=("Arial", 12))
        lt4.pack()
    
        addtowhombutton = Button(transfermiddlecanvas,text="ADD TO WHOM \n (the selected entity will appear in the textbox above)", command=lambda:insert_towhom(t2,tvariable.get()))    
        addtowhombutton.pack()
    
        lt5 = Label(transfermiddlecanvas, text="     ",font=("Arial", 12))
        lt5.pack()
    
        savetransferbutton = Button(transfermiddlecanvas,text="SAVE TRANSFER POLICY & CLOSE", command=lambda:save_transferpolicy(transferFrame,t1.get("1.0", END),t2.get("1.0", END), option1, option2))    
        savetransferbutton.pack()
    


def deletepol(option1,option2,option3): 
    global entityrec
    
    if option3 not in ["-",""] :   
        deleteFrame = Toplevel()
        deleteFrame.geometry("800x500")
        deleteFrame.title("DATA RETENTION POLICY")
        deletecanvas = Canvas(deleteFrame, width = 800, height = 500)
        ld1 = Label(deleteFrame, text="THE DELETION POLICY CAN ONLY BE DEFINED FOR A DATA GROUP\n DATA TYPES CAN ONLY BE DEFINED IN THE DATA CONNECTIONS POLICIES \n (THE LAST TWO SUB-POLICIES)",font=("Arial", 11))
        ld1.pack(pady=25)
    else:
        deleteFrame = Toplevel()
        deleteFrame.geometry("880x500")
        deleteFrame.title("DATA RETENTION POLICY")
        deletecanvas = Canvas(deleteFrame, width = 800, height = 500)
    
        if (option1, option2) not in storeoptionrec :   # deletionpolicytosave[(option1, option2)][4] is storeopt  
            ld1 = Label(deleteFrame, text="The Storage Sub-Policy Needs To Be Specfied Before The Deletion Sub-Policy \n (Please Define the Storage Policy First)",font=("Arial", 11))
            ld1.pack(pady=25)
            closebutton = Button(deletecanvas,text="CLOSE", command=lambda:close_delpolicy(deleteFrame))    
            closebutton.pack()
            deletecanvas.pack(expand=True,fill=BOTH)
        
        elif storeoptionrec[(option1, option2)] == "Service Provider (Main & Backup Storage)" :    
            topcanvas = Canvas(deleteFrame, width = 880, height = 250)
            topcanvas.pack(expand=True,fill=BOTH)
    
            ls2 = Label(topcanvas, text="    ",font=("Arial", 12))
            ls2.pack()
    
            TOPTIONS = ["From Main & Backup Storage", "Only From Main Storage"] 
            tvariable = StringVar(topcanvas)
            
            if (option1, option2) in deletionpolicytosave : 
                tvariable.set(TOPTIONS[TOPTIONS.index(deletionpolicytosave[(option1, option2)][0])]) 
            else : 
                tvariable.set(TOPTIONS[0])  
            
            te = Label(topcanvas, text="CHOOSE A DELETION OPTION BELOW (FROM WHERE THE DATA << " + option2 + " >> WILL BE DELETED BY << " + option1 + " >>", font=("Arial", 11))
            te.pack()
        
            wte = OptionMenu(topcanvas, tvariable, *TOPTIONS) 
            wte.pack()
        
            middlecanvas = Canvas(deleteFrame, width = 880, height = 250)
            middlecanvas.pack(expand=True,fill=BOTH)
            
            ld2 = Label(middlecanvas, text="THE RETENTION DELAY OF THE DATA << " + option2 + " >> IN THE MAIN STORAGE OF << " + option1 + " >>" + "\n (e.g., 2y, 2mo, 2w, 2d, 2h, 2m, 2y+2mo - for 2 years,  2 months, 2 weeks, 2 days, 2 hours, 2 mins)",font=("Arial", 10))
            ld2.pack(pady=25)
            d2 = scrolledtext.ScrolledText(middlecanvas, width=55, heigh=1, bd=1) #, relief="raised" e1 = scrolledtext.ScrolledText(canvas, width=40, heigh=1, bd=5)
            
            if (option1, option2) in deletionpolicytosave : 
                d2.insert(END,deletionpolicytosave[(option1, option2)][1]) 
            else : 
                d2.insert(END,"") 
            
            d2.pack()
            
            ld3 = Label(middlecanvas, text="THE RETENTION DELAY OF THE DATA << " + option2 + " >> IN THE BACKUP STORAGE OF << " + option1 + " >>" + "\n (e.g., 2y, 2mo, 2w, 2d, 2h, 2m, 2y+2mo - for 2 years,  2 months, 2 weeks, 2 days, 2 hours, 2 mins)",font=("Arial", 10))
            ld3.pack(pady=25)
            d3 = scrolledtext.ScrolledText(middlecanvas, width=55, heigh=1, bd=1) #, relief="raised" e1 = scrolledtext.ScrolledText(canvas, width=40, heigh=1, bd=5)
            
            if (option1, option2) in deletionpolicytosave : 
                d3.insert(END,deletionpolicytosave[(option1, option2)][2])
            else : 
                d3.insert(END,"")
            
            d3.pack()
        
            ls3 = Label(middlecanvas, text="    ",font=("Arial", 12))
            ls3.pack()
            ls4 = Label(middlecanvas, text="    ",font=("Arial", 12))
            ls4.pack()
            
            savedeletebutton = Button(middlecanvas,text="SAVE DELETION POLICY & CLOSE", command=lambda:save_deletepolicy(deleteFrame,d2.get("1.0", END),d3.get("1.0", END),  tvariable.get(), option1,option2))    
            savedeletebutton.pack()
       
        elif storeoptionrec[(option1, option2)] == "Service Provider (Only Main Storage)" : 
            topcanvas = Canvas(deleteFrame, width = 800, height = 400)
            topcanvas.pack(expand=True,fill=BOTH)
    
            ls2 = Label(topcanvas, text="    ",font=("Arial", 12))
            ls2.pack()
    
            TOPTIONS = ["Only From Main Storage"] 
            tvariable = StringVar(topcanvas)
            tvariable.set(TOPTIONS[0])
        
            wte = OptionMenu(topcanvas, tvariable, *TOPTIONS) 
            wte.pack()
        
            middlecanvas = Canvas(deleteFrame, width = 800, height = 200)
            middlecanvas.pack(expand=True,fill=BOTH)
            
            ld2 = Label(middlecanvas, text="THE RETENTION DELAY OF THE DATA << " + option2 + " >> IN THE MAIN STORAGE OF << " + option1 + " >>" + "\n (e.g., 2y, 2mo, 2w, 2d, 2h, 2m, 2y+2mo - for 2 years,  2 months, 2 weeks, 2 days, 2 hours, 2 mins)",font=("Arial", 10))
            ld2.pack(pady=25)
            d2 = scrolledtext.ScrolledText(middlecanvas, width=55, heigh=1, bd=1) 
            
            if (option1, option2) in deletionpolicytosave : 
                d2.insert(END,deletionpolicytosave[(option1, option2)][1]) 
            else : 
                d2.insert(END,"") 
            
            d2.pack()   
        
            ls3 = Label(middlecanvas, text="    ",font=("Arial", 12))
            ls3.pack()
            ls4 = Label(middlecanvas, text="    ",font=("Arial", 12))
            ls4.pack()
        
            savedeletebutton = Button(middlecanvas,text="SAVE DELETION POLICY & CLOSE", command=lambda:save_deletepolicy(deleteFrame,d2.get("1.0", END), "Service Provider (Only Main Storage)", tvariable.get(), option1,option2))    
            savedeletebutton.pack()
        
        
        elif storeoptionrec[(option1, option2)] == "Not Service Provider (e.g., Decentralised or Client-side)" : 
            topcanvas = Canvas(deleteFrame, width = 800, height = 400)
            topcanvas.pack(expand=True,fill=BOTH)
    
            ls2 = Label(topcanvas, text="    ",font=("Arial", 12))
            ls2.pack()
    
            TOPTIONS = convertdicttolist(entityrec)[1:]
            tvariable = StringVar(topcanvas)
            tvariable.set(TOPTIONS[0])
        
            wte = OptionMenu(topcanvas, tvariable, *TOPTIONS) 
            wte.pack()
        
            middlecanvas = Canvas(deleteFrame, width = 800, height = 200)
            middlecanvas.pack(expand=True,fill=BOTH)
            
            ld2 = Label(middlecanvas, text="THE RETENTION DELAY OF THE DATA << " + option2 + " >> IN << " + tvariable.get() + " >>" + "\n (e.g., 2y, 2mo, 2w, 2d, 2h, 2m, 2y+2mo - for 2 years,  2 months, 2 weeks, 2 days, 2 hours, 2 mins)",font=("Arial", 10))
            ld2.pack(pady=25)
            d2 = scrolledtext.ScrolledText(middlecanvas, width=55, heigh=1, bd=1) 
            
            if (option1, option2) in deletionpolicytosave : 
                d2.insert(END,deletionpolicytosave[(option1, option2)][1]) 
            else : 
                d2.insert(END,"") 
            
            d2.pack()   
        
            ls3 = Label(middlecanvas, text="    ",font=("Arial", 12))
            ls3.pack()
            ls4 = Label(middlecanvas, text="    ",font=("Arial", 12))
            ls4.pack()
        
            savedeletebutton = Button(middlecanvas,text="SAVE DELETION POLICY & CLOSE", command=lambda:save_deletepolicy(deleteFrame,d2.get("1.0", END), "Decentralised (Not Service Provider)", tvariable.get(), option1,option2))    
            savedeletebutton.pack()
            
            
        
            
def storepol(option1, option2, option3):
    
    if option3 not in ["-",""] :
        storeFrame = Toplevel()
        storeFrame.geometry("700x400")
        storeFrame.title("DATA STORAGE POLICY")
        storecanvas = Canvas(storeFrame, width = 600, height = 700)
        ls1 = Label(storeFrame, text="THE STORAGE POLICY CAN ONLY BE DEFINED FOR A DATA GROUP\n DATA TYPES CAN ONLY BE DEFINED IN THE DATA CONNECTIONS POLICIES \n (THE LAST TWO SUB-POLICIES)",font=("Arial", 11))
        ls1.pack(pady=25)
    else:     
        storeFrame = Toplevel()
        storeFrame.geometry("800x400")
        storeFrame.title("DATA STORAGE POLICY")
        storecanvas = Canvas(storeFrame, width = 600, height = 700)
        ls1 = Label(storeFrame, text="Does " + option1 + " need to collect consent before the data (of type) " + option2 + " is stored ? (give Y or N)",font=("Arial", 12))
        ls1.pack(pady=25)
        s1 = scrolledtext.ScrolledText(storeFrame, width=55, heigh=1, bd=1) 
        if (option1, option2) in storagepolicytosave : 
            s1.insert(END,storagepolicytosave[(option1, option2)][0])
        else : 
            s1.insert(END,"") 
        
        s1.pack()
       
        storemiddlecanvas = Canvas(storeFrame, width = 600, height = 700)
        storemiddlecanvas.pack(expand=True,fill=BOTH)
    
        ls2 = Label(storemiddlecanvas, text="    ",font=("Arial", 12))
        ls2.pack()
        
        
        TOPTIONS = ["Service Provider (Main & Backup Storage)", "Service Provider (Only Main Storage)",  "Not Service Provider (e.g., Decentralised or Client-side)"]  
        tvariable = StringVar(storemiddlecanvas)
        
        if (option1, option2) in storagepolicytosave : 
            tvariable.set(TOPTIONS[TOPTIONS.index(storagepolicytosave[(option1, option2)][1])]) 
        else : 
           tvariable.set(TOPTIONS[0]) 
        
        
        te = Label(storemiddlecanvas, text="Choose a Storage Option (How the Data (of Type) " + option2 + " Will Be Stored By the Entity " + option1 + " )", font=("Arial", 11))
        te.pack()
        wte = OptionMenu(storemiddlecanvas, tvariable, *TOPTIONS)
        wte.pack()
    
        savestorebutton = Button(storecanvas,text="SAVE STORAGE POLICY & CLOSE", command=lambda:save_storepolicy(storeFrame,s1.get("1.0", END),tvariable.get(), option1, option2))    
        savestorebutton.pack()
        storecanvas.pack(expand=True,fill=BOTH)



def usagepol(option1, option2, option3):
    if option3 not in ["-",""] : 
        usageFrame = Toplevel()
        usageFrame.geometry("700x400")
        usageFrame.title("DATA USAGE POLICY")
        usagecanvas = Canvas(usageFrame, width = 700, height = 400)
        lu1 = Label(usageFrame, text="THE USAGE POLICY CAN ONLY BE DEFINED FOR A DATA GROUP\n DATA TYPES CAN ONLY BE DEFINED IN THE DATA CONNECTIONS POLICIES \n (THE LAST TWO SUB-POLICIES)",font=("Arial", 11))
        lu1.pack(pady=25)
    else:
        usageFrame = Toplevel()
        usageFrame.geometry("700x400")
        usageFrame.title("DATA USAGE POLICY")
        usagecanvas = Canvas(usageFrame, width = 700, height = 400)
        lu1 = Label(usageFrame, text="Does " + option1 + " collect consent before the data (of type) " + option2 + " is used ? (give Y or N)",font=("Arial", 11))
        lu1.pack(pady=25)
        u1 = scrolledtext.ScrolledText(usageFrame, width=55, heigh=1, bd=1) 
       
        if (option1, option2) in usagepolicytosave : 
            u1.insert(END,usagepolicytosave[(option1, option2)][0]) 
        else : 
            u1.insert(END,"") 
        
        u1.pack()
        
        lu2 = Label(usageFrame, text="Usage purposes, it can overlap with the collection purposes \n (1 per row in the followig format: action:data1,data2,..., e.g., create:account)",font=("Arial", 12))
        lu2.pack(pady=25)
        u2 = scrolledtext.ScrolledText(usageFrame, width=55, heigh=1, bd=1) 
        
        if (option1, option2) in usagepolicytosave : 
            u2.insert(END,usagepolicytosave[(option1, option2)][1]) 
        else : 
            u2.insert(END,"") 
        
        u2.pack()
        saveusebutton = Button(usagecanvas,text="SAVE USAGE POLICY & CLOSE", command=lambda:save_usepolicy(usageFrame,u1.get("1.0", END),u2.get("1.0", END), option1, option2))    
        saveusebutton.pack()
        usagecanvas.pack(expand=True,fill=BOTH) 



def collectionpol(option1, option2, option3):   
    if option3 not in ["-",""] : 
        collectionFrame = Toplevel()
        collectionFrame.geometry("700x400")
        collectionFrame.title("DATA COLLECTION POLICY")
        collectioncanvas = Canvas(collectionFrame, width = 700, height = 400)
        lc1 = Label(collectionFrame, text="THE COLLECTION POLICY CAN ONLY BE DEFINED FOR A DATA GROUP\n DATA TYPES CAN ONLY BE DEFINED IN THE DATA CONNECTIONS POLICIES\n (THE LAST TWO SUB-POLICIES)",font=("Arial", 11))
        lc1.pack(pady=25)
    else:    
        collectionFrame = Toplevel()
        collectionFrame.geometry("700x400")
        collectionFrame.title("DATA COLLECTION POLICY")
        collectioncanvas = Canvas(collectionFrame, width = 700, height = 400)
        lc1 = Label(collectionFrame, text="Does " + option1 + " collect consent before collecting the data (of type) " + option2 + " ? (give Y or N)",font=("Arial", 11))
        lc1.pack(pady=25)
        c1 = scrolledtext.ScrolledText(collectionFrame, width=55, heigh=1, bd=1) 
        if (option1, option2) in collectionpolicytosave : 
            c1.insert(END,collectionpolicytosave[(option1, option2)][0]) 
        else : 
            c1.insert(END,"") 
        c1.pack()
       
        lc2 = Label(collectionFrame, text="Collection Purposes (1 per row in the followig format: \n action:data1,data2,..., e.g., create:account)",font=("Arial", 12))
        lc2.pack(pady=25)
        c2 = scrolledtext.ScrolledText(collectionFrame, width=55, heigh=1, bd=1) 
        if (option1, option2) in collectionpolicytosave :
            c2.insert(END,collectionpolicytosave[(option1, option2)][1]) 
        else : 
            c2.insert(END,"") 
        c2.pack()
        savecolbutton = Button(collectioncanvas,text="SAVE COLLECTION POLICY & CLOSE", command=lambda:save_colpolicy(collectionFrame,c1.get("1.0", END),c2.get("1.0", END), option1, option2))    
        savecolbutton.pack()
        collectioncanvas.pack(expand=True,fill=BOTH)     


##########################################################################################################################################################
##########################################################################################################################################################
############################################################## THE ARCHITECTURE LEVEL ####################################################################
##########################################################################################################################################################
##########################################################################################################################################################        

############################# present the HOW TO texts in each mode ################################    
def HowToGui(): 
    howtoFrame = Toplevel()
    howtoFrame.geometry("800x500")
    howtoFrame.title("GUI FEATURES AND COMMANDS FOR THE ARCHITECTURE SPECIFICATION")
    howtocanvas = Canvas(howtoFrame, width = 800, height = 500)
    ld1 = Label(howtoFrame, text="The GUI mode facilitate a graphical specification of an architecture.\n\n 1. To add a component or textbox, choose ADD A COMPONENT.\n\n 2. To move a main-component (rectangle) or a sub-component (circle): \n  Option1: drag the component with the mouse.\n  Option2: click once on it, then move it with the keyboard arrow keys. \n\n\n 3. To move a textbox: drag it with the mouse either at its right-bottom corner or drag its text area.\n\n\n 4. To draw a line:  click on the right (mouse) button once at the starting point and then once at the end point of the line.\n\n\n 5. The components and the lines will turn red when the mouse curser goes over them with the mouse.\n\n\n 6. To change the color of a component or line: double click on the left mouse button.\n\n\n 7. To delete a component or a line: 1st click on it once with the left mouse button, then, press the spacebar on the keyboard.\n\n\n 8. To specify which main component has access to which sub component\n choose  SPECIFY THE RELATIONSHIP BETWEEN MAIN AND SUB-COMPONENTS.",font=("Arial", 10))
    ld1.pack(pady=25)
    howtocanvas.pack(expand=True,fill=BOTH)
    

def HowToText(): 
    howtoFrame = Toplevel()
    howtoFrame.geometry("800x300")
    howtoFrame.title("THE ARCHITECTURE SPECIFICATION IN TEXT MODE")
    howtocanvas = Canvas(howtoFrame, width = 800, height = 300)
    ld1 = Label(howtoFrame, text="The TEXT mode allows the user to specify an architecture in textual format by providing the architectural action\n (this mode can be useful when the architecture is very large or the user does not want to draw the architecture).\n\n\n 1. To specify an architecture, provide the architectural actions in the text box, each per row (no comma or point at the end).\n\n\n 2. Before running the conformance verification the user must click on SAVE CONTENT.\n\n\n 3. To specify which main component has access to which sub component\n choose  SPECIFY THE RELATIONSHIP BETWEEN MAIN AND SUB-COMPONENTS.",font=("Arial", 10))
    ld1.pack(pady=25)
    howtocanvas.pack(expand=True,fill=BOTH)
    
def Manual(): 
    manFrame = Toplevel()
    manFrame.geometry("800x500")
    manFrame.title("SUPPORTED FEATURES (Arch. Actions and Attacker Models)")
    mancanvas = Canvas(manFrame, width = 800, height = 300)
    ld1 = Label(manFrame, text="1. THE FOLLOWING ARCH. ACTIONS ARE SUPPORTED IN THIS VERSION:\n\n RECEIVE(E,Datatype) and RECEIVEAT(E,Datatype,Time(ti)): E can receive Datatype (at some non-specs time ti)\n (the above actions assume that the external attacker can eavesdrop and analyse Datatype.)\n\n CALCULATE(E,Datatype) and CALCULATEAT(E,Datatype,Time(ti)): E can calculate Datatype (at some non-specs time ti)\n\n CREATE(E,Datatype) and CREATEAT(E,Datatype,Time(ti)): E can create Datatype (at some non-specs time ti)\n\n CALCULATEFROM(E,Datatype1,Datatype2) and CALCULATEFROMAT(E,Datatype1,Datatype2,Time(ti)):\n E can calculate Datatype1 from Datatype2 (at some non-specs time ti)\n\n STORE(E,Datatype) and STOREAT(E,Datatype,Time(ti)): Datatype can be stored at place E (at some non-specs time ti)\n\n DELETEWITHIN(E,Datatype,Time(tvalue)) : Datatype can be deleted from place E within tvalue delay \n\n OWN(E,Datatype) : E can own Datatype (and aware of its nature, origin and properties)\n---------------------------------------------------------------------------------------------------------\n 2. ATTACKER MODEL:\n Verification against EXTERNAL ATTACKERS, INTERNAL ATTACKERS and HYBRID ATTACKERS.\n 2.1. The external attackers are not part of the system.They can eavesdrop and analyse the communications between entities.\n 2.2. The insider attackers are part of the system. they are compromised entities and have full access to those.\n 2.3. The hybrid attackers case specifies the collusion between insider and external attackers.\n---------------------------------------------------------------------------------------------------------\n 3. CRYPTOGRAPHY:\n The tool supports symmetric and asymmetric encryption, Hash, MAC functions (and simple hommomorphic encryption). \n It supports any number of layers of nested cryptographic function inside a datatype.",font=("Arial", 10))
    ld1.pack(pady=25)
    mancanvas.pack(expand=True,fill=BOTH)    
    
"""    
def HowToArch(): 
    howtoFrame = Toplevel()
    howtoFrame.geometry("800x400")
    howtoFrame.title("GUI FEATURES AND COMMANDS FOR THE ARCHITECTURE SPECIFICATION")
    howtocanvas = Canvas(howtoFrame, width = 800, height = 500)
    ld1 = Label(howtoFrame, text="An architecture can be defined either by ()",font=("Arial", 10))
    ld1.pack(pady=25)
    howtocanvas.pack(expand=True,fill=BOTH)    
"""    

######################################### MOVING THE ARCHITECTURE COMPONENTS AND GUI ELEMENTS #################################

def moveup(event):      
    #x = 0 
    #y = 0
    canvas.move(shapeonfocus, 0, -10)
   
    

def moveleft(event):
    #x = 0 
    #y = 0
    canvas.move(shapeonfocus, -10, 0)
   


def moveright(event):
    #x = 0 
    #y = 0
    canvas.move(shapeonfocus, 10, 0)
      

    
def movedown(event):
    #x = 0 
    #y = 0
    canvas.move(shapeonfocus, 0, 10)
    

    
def getshapeonfocus(event):
    global shapeonfocus
    if len(event.widget.find_withtag('current')) > 0 :
        shapeonfocus =  event.widget.find_withtag('current')[0]        
        

     
def deletefocuson(event) :            
    canvas.delete(shapeonfocus)
    


def getsetColor(event):
    if len(event.widget.find_withtag('current')) > 0 :
        tag = event.widget.find_withtag('current')[0]    
        canvas.itemconfig(tag,fill=askcolor()[1])
        

      
def clear_all(event):
    if len(event.widget.find_withtag('current')) > 0 :
        canvas.delete(event.widget.find_withtag('current')[0]) 
   

    
def create_circle(x, y, r, color, color2):
    global all_sub_comp
    
    try:
        radius = int(r)
        if len(r) > 0 :
            nextsub = canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                outline=color,
                fill=color,
                activefill = color2, 
                tags ="token"
      
            )   
            all_sub_comp.append(nextsub)
        else: 
            pass 
    except ValueError: 
        pass



def create_rectangle(x1, y1, x2, y2, color, color2):
    
    global all_main_comp
    
    try: 
        #intx2 = int(x2)
        #inty2 = int(y2)
        if len(str(x2)) > 0 and len(str(y2)) > 0: 
            nextmain = canvas.create_rectangle(
                x1, 
                y1, 
                x2, 
                y2, 
                outline=color, 
                fill=color,
                activefill = color2,
                tags ="token"
        
            )
            all_main_comp.append(nextmain)    
        else: 
            pass 
    except ValueError: 
        pass



def draw_line(event) : 
    global clicknum
    global xx1
    global yy1
    if clicknum == 0 : 
        xx1 = event.x
        yy1 = event.y 
        clicknum = 1
    else : 
       xx2 = event.x
       yy2 = event.y  
       nextline = canvas.create_line(xx1,yy1,xx2,yy2,fill="black", activefill="red",width=1,arrow=LAST, tags ="token")
       clicknum = 0
       all_lines.append(nextline)
       

    
def create_textbox(event,text):
    global all_entries
    otherFrame = Toplevel()
    otherFrame.geometry("700x400")
    otherFrame.title("THE CONTENT OF " + text)
  
    othercanvas = Canvas(otherFrame, width = 700, height = 400)
    
    if text in nameboxcontent.keys(): 
        e1 = scrolledtext.ScrolledText(othercanvas, width=100, heigh=20, bd=1) 
        e1.insert(END,nameboxcontent[text])
        e1.pack()
   
        othercanvas.pack(expand=True,fill=BOTH)
        all_entries.append( e1 )
    
        savebutton = Button(othercanvas,text="SAVE CONTENT & CLOSE", command=lambda:save_content(otherFrame, text, e1.get("1.0", END)))    
        savebutton.pack()
    else: 
        ld1 = Label(otherFrame, text="THERE IS NO CONTENT FOR <<"+ text + ">> \n (<<" + text + ">> IS DIFFERENT FROM THE ORIGINALLY GIVEN TEXT)",font=("Arial", 11))
        ld1.pack(pady=25)
        closebutton = Button(othercanvas,text="CLOSE", command=lambda:close_delpolicy(otherFrame))    
        closebutton.pack()
        
    othercanvas.pack(expand=True,fill=BOTH)



def create_namebox_open(wide,named,xc,yc): 
    global all_textboxes
    name = Entry(width=wide,justify=CENTER,bd=5)
    name.insert(END, named)
    
    newbox = canvas.create_window(xc,yc, window=name, tags="token")
    all_textboxes.append([newbox,name.get(),wide])
    
    name.bind("<Double-1>", lambda event : create_textbox(event, name.get()))
    name.bind("<ButtonPress-1>", drag_start)
    name.bind("<ButtonRelease-1>", drag_stop)
    name.bind("<B1-Motion>", drag)



def create_namebox(length,content): 
    global all_textboxes
    
    if len(length) >0 and len(content) >0:  
        name = Entry(width=length,justify=CENTER,bd=8)
        name.insert(END, content)
        nameboxcontent[name.get()] = ""  
    
        newbox = canvas.create_window(100,100, window=name, tags="token")
        all_textboxes.append([newbox,name.get(),length])
    
        name.bind("<Double-1>", lambda event : create_textbox(event, name.get()))
        name.bind("<ButtonPress-1>", drag_start)
        name.bind("<ButtonRelease-1>", drag_stop)
        name.bind("<B1-Motion>", drag)  
    else: 
        pass  



def opentexteditor(): 
    global all_entries
    global globalidoftexteditor 
    global globalidofbuttontxted
    global globalidoflabeltxted
    global globalidoflabeltxted2
    global Arch
    global ArchPseudo
    global ArchMeta
    global ArchTime
    global SetlistofbasicsHAS
    global SetlistofbasicsLink
    global storeArchRec
    global setRecvdOwnArgRec
    global recvdOwnArgRec
    global recvdStoreArgRec
    global setRecvdStoreArgRec
    global setcpurposesRecArch
    global cpurposesRecArch
    global setupurposesRecArch
    global upurposesRecArch
    global texteditorcontent
    global nameboxcontent
    global all_main_comp
    global all_sub_comp
    global all_lines
    global all_textboxes
    
    
    if globalidoftexteditor == -1 and globalidofbuttontxted == -1 and globalidoflabeltxted == -1 and globalidoflabeltxted2 == -1: 
        Arch.clear()
        ArchPseudo.clear() 
        ArchMeta.clear()
        ArchTime.clear()
        SetlistofbasicsHAS.clear() 
        SetlistofbasicsLink.clear()
        storeArchRec = {"mainstorage":set(), "backupstorage":set()}
        setRecvdOwnArgRec.clear()
        recvdOwnArgRec.clear()
        recvdStoreArgRec.clear()
        setRecvdStoreArgRec.clear()
        setcpurposesRecArch.clear()
        cpurposesRecArch.clear()
        setupurposesRecArch.clear()
        upurposesRecArch.clear()
        
    
        canvas.delete("all")  
        all_main_comp  = []
        all_sub_comp = []
        all_lines = []
        all_textboxes = []
        nameboxcontent = {}
        texteditorcontent = ""    
    
        globalidoflabeltxted = Label(canvas, text="TEXT EDITOR FOR ARCHITECTURE SPECS. (PROVIDE ONE ACTION PER ROW, NO PUNCTUATION AT THE END)\n Before a conformance verification, click on SAVE CONTENT.\n The same needs to be done before saving an architecture (to save the most up-to-date version).",font=("Arial", 11))
        globalidoflabeltxted.pack(pady=20)
    
        globalidoftexteditor = Text(canvas, width=100, height=35, bd=1) 
        
        globalidoftexteditor.pack(pady=5)
        

        globalidofbuttontxted = Button(canvas,text="SAVE CONTENT", command=lambda:save_texteditorcontent(globalidoftexteditor.get("1.0", END)))    
        globalidofbuttontxted.pack(pady=5)
        
        globalidoflabeltxted2 = Label(canvas, text="")
        globalidoflabeltxted2.pack()
        
    else: 
        pass 
    
    
def opentexteditorfile(): 
    global all_entries
    global globalidoftexteditor 
    global globalidofbuttontxted
    global globalidoflabeltxted
    global globalidoflabeltxted2
    global Arch
    global ArchPseudo
    global ArchMeta
    global ArchTime
    global SetlistofbasicsHAS
    global SetlistofbasicsLink
    global storeArchRec
    global setRecvdOwnArgRec
    global recvdOwnArgRec
    global recvdStoreArgRec
    global setRecvdStoreArgRec
    global setcpurposesRecArch
    global cpurposesRecArch
    global setupurposesRecArch
    global upurposesRecArch
    global texteditorcontent
    global nameboxcontent
    global all_main_comp
    global all_sub_comp
    global all_lines
    global all_textboxes
    
    
    if globalidoftexteditor == -1 and globalidofbuttontxted == -1 and globalidoflabeltxted == -1 and globalidoflabeltxted2 == -1: #if not called texteditor before
        Arch.clear()
        ArchPseudo.clear() 
        ArchMeta.clear()
        ArchTime.clear()
        SetlistofbasicsHAS.clear() 
        SetlistofbasicsLink.clear()
        storeArchRec = {"mainstorage":set(), "backupstorage":set()}
        setRecvdOwnArgRec.clear()
        recvdOwnArgRec.clear()
        recvdStoreArgRec.clear()
        setRecvdStoreArgRec.clear()
        setcpurposesRecArch.clear()
        cpurposesRecArch.clear()
        setupurposesRecArch.clear()
        upurposesRecArch.clear()
        
        canvas.delete("all")  
        all_main_comp  = []
        all_sub_comp = []
        all_lines = []
        all_textboxes = []
        nameboxcontent = {}
        
        globalidoflabeltxted = Label(canvas, text="TEXT EDITOR FOR ARCHITECTURE SPECS. (PROVIDE ONE ACTION PER ROW, NO PUNCTUATION AT THE END)\n Before a conformance verification, click on SAVE CONTENT.\n The same needs to be done before saving an architecture (to save the most up-to-date version).",font=("Arial", 11))
        globalidoflabeltxted.pack(pady=20)
    
        globalidoftexteditor = Text(canvas, width=100, height=35, bd=1) 
        globalidoftexteditor.insert(END,texteditorcontent)
        globalidoftexteditor.pack(pady=5)
        
        globalidofbuttontxted = Button(canvas,text="SAVE CONTENT", command=lambda:save_texteditorcontent(globalidoftexteditor.get("1.0", END)))    
        globalidofbuttontxted.pack(pady=5)
        
        globalidoflabeltxted2 = Label(canvas, text="")
        globalidoflabeltxted2.pack()
        
    else: 
        pass 
    

    
def drag_start(event):
    
    _drag_data["item"] = canvas.find_closest(event.x, event.y)[0]
    _drag_data["x"] = event.x
    _drag_data["y"] = event.y


def drag_stop(event):
     
    _drag_data["item"] = None
    _drag_data["x"] = 0
    _drag_data["y"] = 0


def drag(event):
       
    delta_x = event.x - _drag_data["x"]
    delta_y = event.y - _drag_data["y"]
    
    canvas.move(_drag_data["item"], delta_x, delta_y)
    
    _drag_data["x"] = event.x
    _drag_data["y"] = event.y
        

    
def move_start(event):
        canvas.scan_mark(event.x, event.y)
    
def move_move(event):
        canvas.scan_dragto(event.x, event.y, gain=1)


def zoomer(event):
    if (event.delta > 0):
        canvas.scale("all", event.x, event.y, 1.1, 1.1)
    elif (event.delta < 0):
        canvas.scale("all", event.x, event.y, 0.9, 0.9)
    canvas.configure(scrollregion = canvas.bbox("all"))



def addcomp():
    compFrame = Toplevel()
    compFrame.geometry("600x150")
    compFrame.title("ADD A NEW COMPONENT OR TEXT BOX")
    
    compcanvas = Canvas(compFrame, width = 600, height = 30)
    compcanvas.pack(expand=True,fill=BOTH)
    cl1 = Label(compcanvas, text="Width",font=("Arial", 10))
    cl1.pack(padx=5, pady=5, side=LEFT)
    sizeinputx = Entry(compcanvas, width=10)
    sizeinputx.pack(padx=5, pady=5, side=LEFT)
    cl2 = Label(compcanvas, text="Height",font=("Arial", 10))
    cl2.pack(padx=5, pady=5, side=LEFT)
    sizeinputy = Entry(compcanvas, width=10)
    sizeinputy.pack(padx=10, pady=5, side=LEFT)
    button_rectangle = Button(compcanvas, text="ADD MAIN-COMPONENT", command=lambda:create_rectangle(30, 10, sizeinputx.get(), sizeinputy.get(), 'grey', 'red')).pack(side=LEFT)
    
    compcanvas2 = Canvas(compFrame, width = 600, height = 30)
    compcanvas2.pack(expand=True,fill=BOTH)
    cl3 = Label(compcanvas2, text="Radius",font=("Arial", 10))
    cl3.pack(padx=5, pady=5, side=LEFT)
    sizeinputsubr = Entry(compcanvas2, width=10)
    sizeinputsubr.pack(padx=5, pady=5, side=LEFT)
    button_circle = Button(compcanvas2, text="ADD SUB-COMPONENT", command=lambda:create_circle(30, 10, sizeinputsubr.get(), "green", "red")).pack(side=LEFT)
    
    compcanvas3 = Canvas(compFrame, width = 600, height = 30)
    compcanvas3.pack(expand=True,fill=BOTH)
    cl4 = Label(compcanvas3, text="Init. Content",font=("Arial", 10))
    cl4.pack(padx=5, pady=5, side=LEFT)
    boxtext = Entry(compcanvas3, width=40)
    boxtext.pack(padx=5, pady=5, side=LEFT)
    cl5 = Label(compcanvas3, text="Box Length",font=("Arial", 10))
    cl5.pack(padx=5, pady=5, side=LEFT)
    boxlength = Entry(compcanvas3, width=10)
    boxlength.pack(padx=5, pady=5, side=LEFT)
    namebox = Button(compcanvas3, 
                   text="ADD TEXT BOX", 
                   fg="black",command=lambda:create_namebox(boxlength.get(),boxtext.get())
                   )
    namebox.pack(side=LEFT) 


def relation_mainsubtext():
    relationFrame = Toplevel()
    relationFrame.geometry("600x400")
    relationFrame.title("SPECIFY THE RELATION BETWEEN THE MAIN COMPONENTS AND THE SUB-COMPONENTS")
    
    relationcanvas = Canvas(relationFrame, width = 600, height = 400)
    lr1 = Label(relationFrame, text="SPECIFY WHICH MAIN COMPONENTS HAVE ACCESS TO WHICH SUB-COMPONENTS \n (1 row per entry, e.g., sp:panel or sp:webserver,storage (without space))\n (Provide att:E1,...,En to specify that the insider attacker compromised the entities E1,...,En)",font=("Arial", 10))
    lr1.pack(pady=25)
    er = scrolledtext.ScrolledText(relationcanvas, width=55, heigh=15, bd=1) #, relief="raised" e1 = scrolledtext.ScrolledText(canvas, width=40, heigh=1, bd=5)
    er.insert(END,relationbox[0])
    er.pack()
    
    savebutton = Button(relationcanvas,text="SAVE RELATIONS & CLOSE", command=lambda:save_relationtext(relationFrame, er.get("1.0", END)))    
    savebutton.pack()
    relationcanvas.pack(expand=True,fill=BOTH)    
    

def relation_mainsub():
    relationFrame = Toplevel()
    relationFrame.geometry("600x400")
    relationFrame.title("SPECIFY THE RELATION BETWEEN THE MAIN COMPONENTS AND THE SUB-COMPONENTS")
    
    relationcanvas = Canvas(relationFrame, width = 600, height = 400)
    lr1 = Label(relationFrame, text="SPECIFY WHICH MAIN COMPONENTS HAVE ACCESS TO WHICH SUB-COMPONENTS \n (1 row per entry, e.g., sp:panel or sp:webserver,storage (without space))\n (Provide att:E1,...,En to specify that the insider attacker compromised the entities E1,...,En)",font=("Arial", 10))
    lr1.pack(pady=25)
    er = scrolledtext.ScrolledText(relationcanvas, width=55, heigh=15, bd=1) #, relief="raised" e1 = scrolledtext.ScrolledText(canvas, width=40, heigh=1, bd=5)
    er.insert(END,relationbox[0])
    er.pack()
    
    savebutton = Button(relationcanvas,text="SAVE RELATIONS & CLOSE", command=lambda:save_relation(relationFrame, er.get("1.0", END)))    
    savebutton.pack()
    relationcanvas.pack(expand=True,fill=BOTH)
    
    
def save_content(oframe, namebox, content):
    nameboxcontent[namebox] = content
    add_to_arch() 
    oframe.destroy()


def save_texteditorcontent(content):
    global texteditorcontent
    
    texteditorcontent = content
    add_to_arch_text() 



def clear_archpane():
    global all_main_comp
    global all_sub_comp
    global all_lines
    global all_textboxes
    global nameboxcontent
    global texteditorcontent
    global globalidofbuttontxted
    global globalidoftexteditor
    global globalidoflabeltxted
    global globalidoflabeltxted2
    global Arch
    global ArchPseudo
    global ArchMeta
    global ArchTime
    global SetlistofbasicsHAS
    global SetlistofbasicsLink
    global storeArchRec
    global setRecvdOwnArgRec
    global recvdOwnArgRec
    global recvdStoreArgRec
    global setRecvdStoreArgRec
    global setcpurposesRecArch
    global cpurposesRecArch
    global setupurposesRecArch
    global upurposesRecArch
    
    
    Arch.clear()
    ArchPseudo.clear() 
    ArchMeta.clear()
    ArchTime.clear()
    SetlistofbasicsHAS.clear() 
    SetlistofbasicsLink.clear()
    storeArchRec = {"mainstorage":set(), "backupstorage":set()}
    setRecvdOwnArgRec.clear()
    recvdOwnArgRec.clear()
    recvdStoreArgRec.clear()
    setRecvdStoreArgRec.clear()
    setcpurposesRecArch.clear()
    cpurposesRecArch.clear()
    setupurposesRecArch.clear()
    upurposesRecArch.clear()
    
    
    canvas.delete("all")  
    all_main_comp  = []
    all_sub_comp = []
    all_lines = []
    all_textboxes = []
    nameboxcontent = {}
    texteditorcontent = ""
    
    if globalidofbuttontxted !=-1 and globalidoftexteditor !=-1 and globalidoflabeltxted !=-1 and globalidoflabeltxted2 !=-1: 
         globalidofbuttontxted.destroy()
         globalidoftexteditor.destroy()
         globalidoflabeltxted.destroy() 
         globalidoflabeltxted2.destroy()
         globalidofbuttontxted = -1
         globalidoftexteditor = -1
         globalidoflabeltxted = -1
         globalidoflabeltxted2 = -1
    else:
        pass

    

def save_relation_noframetext(rcontent):
    global HasAccessTo
    global entityRelationRec
    global entityRelationListRec
    global relationboxcontent 
    
    HasAccessTo = {}
    entityRelationRec = {}
    entityRelationListRec = {}
    
    rstringofrow = rcontent.splitlines()   
   
    if lengthall(rstringofrow) != 0: 
        for rstring in rstringofrow :
            if len(rstring) != 0:
                separation1 = rstring.split(":")  
                separation2 = separation1[1].split(",")  
                if separation1[0] in separation2 : 
                    separation2.remove(separation1[0])
                HasAccessTo[separation1[0]] = set(separation2)
                
                for element in separation2 : 
                    if element not in set(entityRelationRec.keys()):
                        templist = set()
                        templist.add(separation1[0])
                        entityRelationListRec[element] = templist
                        entityRelationRec[element] = entityRelationListRec[element]
                    else : 
                        templist = entityRelationListRec[element]
                        templist.add(separation1[0])
                        entityRelationListRec[element] = templist
                        entityRelationRec[element] = entityRelationListRec[element]  
            
        updatearchitecture_noframetext()
        
    else: 
        HasAccessTo = {}
        entityRelationRec = {}
        updatearchitecture_noframetext()                 
        
    parent_cpurposesrec()
    components_cpurposesrecpol()
    
    parent_upurposesrec()
    components_upurposesrecpol()
    
    relationbox[0] = rcontent
    relationboxcontent = "Relationship:\n" + rcontent 
    


def save_relationtext(rframe, rcontent):
    global HasAccessTo
    global entityRelationRec
    global entityRelationListRec
    global relationboxcontent 
    
    HasAccessTo = {}
    entityRelationRec = {}
    entityRelationListRec = {}
    
    rstringofrow = rcontent.splitlines()   
   
    if lengthall(rstringofrow) != 0: 
        for rstring in rstringofrow :
            if len(rstring) != 0:
                separation1 = rstring.split(":")  
                separation2 = separation1[1].split(",")  
                if separation1[0] in separation2 : 
                    separation2.remove(separation1[0])
                HasAccessTo[separation1[0]] = set(separation2)
                
                for element in separation2 : 
                    if element not in set(entityRelationRec.keys()):
                        templist = set()
                        templist.add(separation1[0])
                        entityRelationListRec[element] = templist
                        entityRelationRec[element] = entityRelationListRec[element]
                    else : 
                        templist = entityRelationListRec[element]
                        templist.add(separation1[0])
                        entityRelationListRec[element] = templist
                        entityRelationRec[element] = entityRelationListRec[element]  
                
        updatearchitecturetext()    
    else: 
        HasAccessTo = {}
        entityRelationRec = {}
        updatearchitecturetext()                 
    
    parent_cpurposesrec()
    components_cpurposesrecpol()
    
    parent_upurposesrec()
    components_upurposesrecpol()
    
    relationbox[0] = rcontent
    relationboxcontent = "Relationship:\n" + rcontent 
    rframe.destroy()    
    


def save_relation(rframe, rcontent):
    global HasAccessTo
    global entityRelationRec
    global entityRelationListRec
    global relationboxcontent 
    
    HasAccessTo = {}
    entityRelationRec = {}
    entityRelationListRec = {}
    
    
    
    rstringofrow = rcontent.splitlines()   
   
    if lengthall(rstringofrow) != 0: 
        for rstring in rstringofrow :
            if len(rstring) != 0:
                separation1 = rstring.split(":")  
                separation2 = separation1[1].split(",")  
                if separation1[0] in separation2 : 
                    separation2.remove(separation1[0])
                HasAccessTo[separation1[0]] = set(separation2)
                
                for element in separation2 : 
                    if element not in set(entityRelationRec.keys()):
                        templist = set()
                        templist.add(separation1[0])
                        entityRelationListRec[element] = templist
                        entityRelationRec[element] = entityRelationListRec[element]
                    else : 
                        templist = entityRelationListRec[element]
                        templist.add(separation1[0])
                        entityRelationListRec[element] = templist
                        entityRelationRec[element] = entityRelationListRec[element]  
                
        updatearchitecture()    
    else: 
        HasAccessTo = {}
        entityRelationRec = {}
        updatearchitecture()                 
    
    parent_cpurposesrec()
    components_cpurposesrecpol()
    
    parent_upurposesrec()
    components_upurposesrecpol()
    
    relationbox[0] = rcontent
    relationboxcontent = "Relationship:\n" + rcontent
    rframe.destroy()    

    
    
def replacedatatypetogroup(term) : 
    if str(term.predicate) in datagroupoftypes : 
        term.predicate = datagroupoftypes[str(term.predicate)] 
    for i in range(len(term.arguments)) :
        replacedatatypetogroup(term.arguments[i])
    return term


def checkarchsyntaxerror(inputlowered) : 
    verror = ""
    vlabel = "" 
    global atleastoneerror
    atleastoneerror = 0
    
    for strarchelement in inputlowered : 
        if len(strarchelement) != 0:   
            if str(DataOrFact(strarchelement).predicate) not in predefinedarchpred : 
                atleastoneerror = 1
                verror = verror + "THE ACTION << " + strarchelement + " >> IS NOT ALLOWED" + "\n" 
    if  atleastoneerror == 1 : 
        vlabel = "SYNTAX ERROR IN THE ARCHITECTURE (SEE DETAILS BELOW)"
        printarcherror(verror,vlabel)
        return 0
    else : 
        return 1


def printarcherror(error,label) : 
    errorFrame = Toplevel()
    errorFrame.geometry("600x400")
    errorFrame.title("ARCHITECTURE SYNTAX ERROR")
    errorcanvas = Canvas(errorFrame, width = 600, height = 400, background="LightSalmon")
    lre = Label(errorFrame, text=label,font=("Arial", 12),bg="LightSalmon")
    lre.pack(pady=25)
    tre = scrolledtext.ScrolledText(errorFrame, width=500, heigh=50, bd=1,bg="LightSalmon") 
    tre.insert(END,error)
    tre.pack()


def updatearchitecture_noframetext():  
    
    global basicEncRec
    global basicEncRecAttEx
    global basicEncRecAttIn
    global basicEncRecAttHyb
    
    global SetlistofbasicsHAS
    global SetlistofbasicsLink
    global SetlistofbasicsHASATTEX
    global SetlistofbasicsLinkATTEX
    global SetlistofbasicsHASATTIN
    global SetlistofbasicsLinkATTIN
    global SetlistofbasicsHASATTHYB
    global SetlistofbasicsLinkATTHYB
    global ReclistofbasicsLinkUnique
    global ReclistofbasicsLinkAttExUnique
    global SetlistofbasicsLinkATTHYBUnique
    global SetlistofbasicsLinkATTINUnique
    
    global RecofUnionArch
    global Recofactions
    
    global ReclistofbasicsHAS
    global ReclistofbasicsLink
   
    global ReclistofbasicsHASAttEx
    global ReclistofbasicsLinkAttEx
   
    
    global storeArchRec
    global setRecvdOwnArgRec
    global recvdOwnArgRec
    global recvdStoreArgRec
    global setRecvdStoreArgRec
   
    global nameboxcontent
    global cPurposeArch 
    global uPurposeArch 
   
    SetlistofbasicsHASATTEX.clear()
    SetlistofbasicsLinkATTEX.clear()
    SetlistofbasicsHASATTIN.clear()
    SetlistofbasicsLinkATTIN.clear()
    SetlistofbasicsHASATTHYB.clear()
    SetlistofbasicsLinkATTHYB.clear()
    SetlistofbasicsLinkATTHYBUnique.clear()
    SetlistofbasicsLinkATTINUnique.clear()
    
    RecofUnionArch.clear()
    Recofactions.clear()
    
    ReclistofbasicsHAS.clear()
    ReclistofbasicsLink.clear()
    
    ReclistofbasicsHASAttEx.clear()
    ReclistofbasicsLinkAttEx.clear()
    ReclistofbasicsLinkUnique.clear()
    ReclistofbasicsLinkAttExUnique.clear()
    
    basicEncRecAttEx.clear()
    basicEncRecAttIn.clear()
    basicEncRec.clear()
    basicEncRecAttHyb.clear()
    
    SetlistofbasicsHAS.clear() 
    SetlistofbasicsLink.clear()
    
    storeArchRec = {"mainstorage":set(), "backupstorage":set()}
    setRecvdOwnArgRec.clear()
    recvdOwnArgRec.clear()
    recvdStoreArgRec.clear()
    setRecvdStoreArgRec.clear()
    
    cPurposeArch.clear() 
    uPurposeArch.clear() 
    
    
    userinput = globalidoftexteditor.get("1.0", END)
    stringofrow2 = userinput.splitlines()    
    
    if lengthall(stringofrow2) > 0: 
        stringofrow = set(map(lambda e:e.lower(),stringofrow2)) 

        if checkarchsyntaxerror(stringofrow) == 1 :
            
            extractDataEFromArch(stringofrow) 
        
            update_cPurposeArch(userinput) 
        
            update_uPurposeArch(userinput) 
            
            
            add_recvdowned_args(userinput)
        
          
            add_storage_options(userinput)

           
            add_stored_args(userinput)
            
            for string in stringofrow : 
                if len(string) != 0: 
                    addtoArchRec(DataOrFact(string))
                    
                    if len(string.split("p(")) == 2 : 
                        ArchPseudo.add(string)#  
                        ArchPseudo.add(str(replacedatatypetogroup(DataOrFact(string)))) 
                    elif len(string.split("meta(")) == 2 : 
                        ArchMeta.add(string)
                        ArchMeta.add(str(replacedatatypetogroup(DataOrFact(string)))) 
                    elif len(string.split("time(")) == 2 : 
                        ArchTime.add(string) 
                        ArchTime.add(str(replacedatatypetogroup(DataOrFact(string)))) 
                    else : 
                        Arch.add(string) 
                        Arch.add(str(replacedatatypetogroup(DataOrFact(string))))  
    
                  
            UnionArchAccessTo()
            
            for ent in Recofactions.keys() : 
              if len(RecofUnionArch) > 0 and (ent in RecofUnionArch.keys()) :  
                  for arch in RecofUnionArch[ent] : 
                      generatebasics(arch)
                      generatebasicsEnc(arch)
                      generatebasicsEncAttEx(arch)
              else :  
                  for arch in Recofactions[ent] : 
                      generatebasics(arch)
                     
                      generatebasicsEnc(arch)
                     
                      generatebasicsEncAttEx(arch)
                     
                   
            if len(basicEncRec) > 0 :
                cleanbasicsEncRec()
            
            if len(basicEncRecAttEx) > 0 :
                cleanbasicsEncRecAttEx()    
            
            
            if len(RecofUnionArch) > 0 and ("att" in RecofUnionArch.keys()) :
                for arch in RecofUnionArch["att"] : 
                    generatebasicsAttIn(arch)
                    generatebasicsEncAttIn(arch)
                
            if len(basicEncRecAttIn) > 0 :
                cleanbasicsEncRecAttIn()          
  
            

def updatearchitecture_noframe():  
    
    global basicEncRec
    global basicEncRecAttEx
    global basicEncRecAttIn
    global basicEncRecAttHyb
    
    global SetlistofbasicsHAS
    global SetlistofbasicsLink
    global SetlistofbasicsHASATTEX
    global SetlistofbasicsLinkATTEX
    global SetlistofbasicsHASATTIN
    global SetlistofbasicsLinkATTIN
    global SetlistofbasicsHASATTHYB
    global SetlistofbasicsLinkATTHYB
    global ReclistofbasicsLinkUnique
    global ReclistofbasicsLinkAttExUnique
    global SetlistofbasicsLinkATTHYBUnique
    global SetlistofbasicsLinkATTINUnique
    
    global RecofUnionArch
    global Recofactions
    
    global ReclistofbasicsHAS
    global ReclistofbasicsLink
    
    global ReclistofbasicsHASAttEx
    global ReclistofbasicsLinkAttEx
   
    global storeArchRec
    global setRecvdOwnArgRec
    global recvdOwnArgRec
    global recvdStoreArgRec
    global setRecvdStoreArgRec
    
    global nameboxcontent
    global cPurposeArch 
    global uPurposeArch 
   
    SetlistofbasicsHASATTEX.clear()
    SetlistofbasicsLinkATTEX.clear()
    SetlistofbasicsHASATTIN.clear()
    SetlistofbasicsLinkATTIN.clear()
    SetlistofbasicsHASATTHYB.clear()
    SetlistofbasicsLinkATTHYB.clear()
    SetlistofbasicsLinkATTHYBUnique.clear()
    SetlistofbasicsLinkATTINUnique.clear()
    
    RecofUnionArch.clear()
    Recofactions.clear()
    
    ReclistofbasicsHAS.clear()
    ReclistofbasicsLink.clear()
    
    ReclistofbasicsHASAttEx.clear()
    ReclistofbasicsLinkAttEx.clear()
    ReclistofbasicsLinkUnique.clear()
    ReclistofbasicsLinkAttExUnique.clear()
    
    basicEncRecAttEx.clear()
    basicEncRecAttIn.clear()
    basicEncRec.clear()
    basicEncRecAttHyb.clear()
    
    SetlistofbasicsHAS.clear() 
    SetlistofbasicsLink.clear()
    
    
    storeArchRec = {"mainstorage":set(), "backupstorage":set()}
    setRecvdOwnArgRec.clear()
    recvdOwnArgRec.clear()
    recvdStoreArgRec.clear()
    setRecvdStoreArgRec.clear()
    cPurposeArch.clear() 
    uPurposeArch.clear() 
    
    
    
    for e in nameboxcontent.keys():
        userinput = nameboxcontent[e]
        stringofrow2 = userinput.splitlines()    
        
        if lengthall(stringofrow2) > 0: 
            stringofrow = set(map(lambda e:e.lower(),stringofrow2)) 
    
            if checkarchsyntaxerror(stringofrow) == 1 :
                
                extractDataEFromArch(stringofrow) 
            
                update_cPurposeArch(userinput) 
            
                update_uPurposeArch(userinput) 
                
                
                add_recvdowned_args(userinput)
            
              
                add_storage_options(userinput)
    
               
                add_stored_args(userinput)     
                
                for string in stringofrow : 
                    if len(string) != 0: 
                        addtoArchRec(DataOrFact(string))
                        
                        if len(string.split("p(")) == 2 : 
                            ArchPseudo.add(string)#  
                            ArchPseudo.add(str(replacedatatypetogroup(DataOrFact(string)))) 
                        elif len(string.split("meta(")) == 2 : 
                            ArchMeta.add(string)
                            ArchMeta.add(str(replacedatatypetogroup(DataOrFact(string)))) 
                        elif len(string.split("time(")) == 2 : 
                            ArchTime.add(string) 
                            ArchTime.add(str(replacedatatypetogroup(DataOrFact(string)))) 
                        else : 
                            Arch.add(string) 
                            Arch.add(str(replacedatatypetogroup(DataOrFact(string))))  
                           
                
    UnionArchAccessTo() 
    
    for ent in Recofactions.keys() : 
       if len(RecofUnionArch) > 0 and (ent in RecofUnionArch.keys()) :  
           for arch in RecofUnionArch[ent] : 
               generatebasics(arch)
               generatebasicsEnc(arch)
               generatebasicsEncAttEx(arch)
       else :  
           for arch in Recofactions[ent] : 
               generatebasics(arch)
               generatebasicsEnc(arch)
               generatebasicsEncAttEx(arch)
               
           
    if len(basicEncRec) > 0 :
        cleanbasicsEncRec()
    
    if len(basicEncRecAttEx) > 0 :
        cleanbasicsEncRecAttEx()    
    
    
    if len(RecofUnionArch) > 0 and ("att" in RecofUnionArch.keys()) :
        for arch in RecofUnionArch["att"] : 
            generatebasicsAttIn(arch)
            generatebasicsEncAttIn(arch)
        
    if len(basicEncRecAttIn) > 0 :
        cleanbasicsEncRecAttIn()         
  


def updatearchitecturetext():  
    
    global basicEncRec
    global basicEncRecAttEx
    global basicEncRecAttIn
    global basicEncRecAttHyb
    
    global SetlistofbasicsHAS
    global SetlistofbasicsLink
    global SetlistofbasicsHASATTEX
    global SetlistofbasicsLinkATTEX
    global SetlistofbasicsHASATTIN
    global SetlistofbasicsLinkATTIN
    global SetlistofbasicsHASATTHYB
    global SetlistofbasicsLinkATTHYB
    global ReclistofbasicsLinkUnique
    global ReclistofbasicsLinkAttExUnique
    global SetlistofbasicsLinkATTHYBUnique
    global SetlistofbasicsLinkATTINUnique
    
    global RecofUnionArch
    
    global ReclistofbasicsHAS
    global ReclistofbasicsLink
    
    global storeArchRec
    global setRecvdOwnArgRec
    global recvdOwnArgRec
    global recvdStoreArgRec
    global setRecvdStoreArgRec
    
    global nameboxcontent
    global cPurposeArch 
    global uPurposeArch 
   
    SetlistofbasicsHASATTEX.clear()
    SetlistofbasicsLinkATTEX.clear()
    SetlistofbasicsHASATTIN.clear()
    SetlistofbasicsLinkATTIN.clear()
    SetlistofbasicsHASATTHYB.clear()
    SetlistofbasicsLinkATTHYB.clear()
    SetlistofbasicsLinkATTHYBUnique.clear()
    SetlistofbasicsLinkATTINUnique.clear()
    
    RecofUnionArch.clear()
    
    ReclistofbasicsHAS.clear()
    ReclistofbasicsLink.clear()
    
    ReclistofbasicsHASAttEx.clear()
    ReclistofbasicsLinkAttEx.clear()
    ReclistofbasicsLinkUnique.clear()
    ReclistofbasicsLinkAttExUnique.clear()
    
    basicEncRecAttEx.clear()
    basicEncRecAttIn.clear()
    basicEncRec.clear()
    basicEncRecAttHyb.clear()
    
    SetlistofbasicsHAS.clear() 
    SetlistofbasicsLink.clear()
    
                  
    UnionArchAccessTo()
    
    for ent in Recofactions.keys() : 
      if len(RecofUnionArch) > 0 and (ent in RecofUnionArch.keys()) :  
          for arch in RecofUnionArch[ent] : 
              generatebasics(arch)
              generatebasicsEnc(arch)
              generatebasicsEncAttEx(arch)
      else :  
          for arch in Recofactions[ent] : 
              generatebasics(arch)
              
              generatebasicsEnc(arch)
             
              generatebasicsEncAttEx(arch)
             
           
    if len(basicEncRec) > 0 :
        cleanbasicsEncRec()
    
    if len(basicEncRecAttEx) > 0 :
        cleanbasicsEncRecAttEx()    
    
    
    if len(RecofUnionArch) > 0 and ("att" in RecofUnionArch.keys()) :
        for arch in RecofUnionArch["att"] : 
            generatebasicsAttIn(arch)
            generatebasicsEncAttIn(arch)
        
    if len(basicEncRecAttIn) > 0 :
        cleanbasicsEncRecAttIn()        
    

    
def updatearchitecture():  
    
    global basicEncRec
    global basicEncRecAttEx
    global basicEncRecAttIn
    global basicEncRecAttHyb
    
    global SetlistofbasicsHAS
    global SetlistofbasicsLink
    global SetlistofbasicsHASATTEX
    global SetlistofbasicsLinkATTEX
    global SetlistofbasicsHASATTIN
    global SetlistofbasicsLinkATTIN
    global SetlistofbasicsHASATTHYB
    global SetlistofbasicsLinkATTHYB
    global ReclistofbasicsLinkUnique
    global ReclistofbasicsLinkAttExUnique
    global SetlistofbasicsLinkATTHYBUnique
    global SetlistofbasicsLinkATTINUnique
    
    global RecofUnionArch
    
    global ReclistofbasicsHAS
    global ReclistofbasicsLink
    
    global ReclistofbasicsHASAttEx
    global ReclistofbasicsLinkAttEx
   
    
    global storeArchRec
    global setRecvdOwnArgRec
    global recvdOwnArgRec
    global recvdStoreArgRec
    global setRecvdStoreArgRec
   
    global nameboxcontent
    global cPurposeArch 
    global uPurposeArch 
   
    SetlistofbasicsHASATTEX.clear()
    SetlistofbasicsLinkATTEX.clear()
    SetlistofbasicsHASATTIN.clear()
    SetlistofbasicsLinkATTIN.clear()
    SetlistofbasicsHASATTHYB.clear()
    SetlistofbasicsLinkATTHYB.clear()
    SetlistofbasicsLinkATTHYBUnique.clear()
    SetlistofbasicsLinkATTINUnique.clear()
    
    RecofUnionArch.clear()
    
    ReclistofbasicsHAS.clear()
    ReclistofbasicsLink.clear()
    
    ReclistofbasicsHASAttEx.clear()
    ReclistofbasicsLinkAttEx.clear()
    ReclistofbasicsLinkUnique.clear()
    ReclistofbasicsLinkAttExUnique.clear()
    
    basicEncRecAttEx.clear()
    basicEncRecAttIn.clear()
    basicEncRec.clear()
    basicEncRecAttHyb.clear()
    
    SetlistofbasicsHAS.clear() 
    SetlistofbasicsLink.clear()
    
    UnionArchAccessTo() 
    
    for ent in Recofactions.keys() : 
       if len(RecofUnionArch) > 0 and (ent in RecofUnionArch.keys()) : 
           for arch in RecofUnionArch[ent] : 
               generatebasics(arch)
               generatebasicsEnc(arch)
               generatebasicsEncAttEx(arch)
       else : 
           for arch in Recofactions[ent] : 
               generatebasics(arch)
              
               generatebasicsEnc(arch)
              
               generatebasicsEncAttEx(arch)
              
           
    if len(basicEncRec) > 0 :
        cleanbasicsEncRec()
    
    if len(basicEncRecAttEx) > 0 :
        cleanbasicsEncRecAttEx()    
    
    
    if len(RecofUnionArch) > 0 and ("att" in RecofUnionArch.keys()) :
        for arch in RecofUnionArch["att"] : 
            generatebasicsAttIn(arch)
            generatebasicsEncAttIn(arch)
        
    if len(basicEncRecAttIn) > 0 :
        cleanbasicsEncRecAttIn()         
  


    
def add_to_arch_text(): 
    
    global Arch
    global ArchPseudo
    global ArchMeta
    global ArchTime
    global SetlistofbasicsHAS
    global SetlistofbasicsLink
    
    global SetlistofbasicsHASATTEX
    global SetlistofbasicsLinkATTEX
    global SetlistofbasicsHASATTIN
    global SetlistofbasicsLinkATTIN
    global SetlistofbasicsHASATTHYB
    global SetlistofbasicsLinkATTHYB
    global ReclistofbasicsLinkUnique
    global ReclistofbasicsLinkAttExUnique
    global SetlistofbasicsLinkATTHYBUnique
    global SetlistofbasicsLinkATTINUnique
    
    global RecofUnionArch
    
    global ReclistofbasicsHAS
    global ReclistofbasicsLink
    
    global ReclistofbasicsHASAttEx
    global ReclistofbasicsLinkAttEx
    
    
    global basicEncRecAttEx
    global basicEncRec
    global Recofactions
    global basicEncRecAttIn
    global basicEncRecAttHyb
    
    global storeArchRec
    global setRecvdOwnArgRec
    global recvdOwnArgRec
    global recvdStoreArgRec
    global setRecvdStoreArgRec
    global nameboxcontent
    global cPurposeArch 
    global uPurposeArch 
    
    
    Arch.clear()
    ArchPseudo.clear() 
    ArchMeta.clear()
    ArchTime.clear()
    SetlistofbasicsHAS.clear() 
    SetlistofbasicsLink.clear()
    
    SetlistofbasicsHASATTEX.clear()
    SetlistofbasicsLinkATTEX.clear()
    SetlistofbasicsHASATTIN.clear()
    SetlistofbasicsLinkATTIN.clear()
    SetlistofbasicsHASATTHYB.clear()
    SetlistofbasicsLinkATTHYB.clear()
    SetlistofbasicsLinkATTHYBUnique.clear()
    SetlistofbasicsLinkATTINUnique.clear()
    
    RecofUnionArch.clear()
    
    ReclistofbasicsHAS.clear()
    ReclistofbasicsLink.clear()
    
    ReclistofbasicsHASAttEx.clear()
    ReclistofbasicsLinkAttEx.clear()
    ReclistofbasicsLinkUnique.clear()
    ReclistofbasicsLinkAttExUnique.clear()

    basicEncRecAttEx.clear()
    basicEncRec.clear()
    Recofactions.clear()
    basicEncRecAttIn.clear()
    basicEncRecAttHyb.clear()
    
    storeArchRec = {"mainstorage":set(), "backupstorage":set()}
    setRecvdOwnArgRec.clear()
    recvdOwnArgRec.clear()
    recvdStoreArgRec.clear()
    setRecvdStoreArgRec.clear()
    cPurposeArch.clear() 
    uPurposeArch.clear() 
    
    userinput = texteditorcontent  
    stringofrow2 = userinput.splitlines()    
        
    if lengthall(stringofrow2) > 0: 
        stringofrow = set(map(lambda e:e.lower(),stringofrow2))  
    
        if checkarchsyntaxerror(stringofrow) == 1 :  
            
            extractDataEFromArch(stringofrow) 
            
            update_cPurposeArch(userinput) 
            
            update_uPurposeArch(userinput) 
            
            add_recvdowned_args(userinput)
            
            add_storage_options(userinput)
    
            add_stored_args(userinput)
         
            for string in stringofrow : 
                if len(string) != 0: 
                    addtoArchRec(DataOrFact(string))
                    
                    if len(string.split("p(")) == 2 : 
                        ArchPseudo.add(string)#  
                        ArchPseudo.add(str(replacedatatypetogroup(DataOrFact(string)))) 
                    elif len(string.split("meta(")) == 2 : 
                        ArchMeta.add(string)
                        ArchMeta.add(str(replacedatatypetogroup(DataOrFact(string)))) 
                    elif len(string.split("time(")) == 2 : 
                        ArchTime.add(string) 
                        ArchTime.add(str(replacedatatypetogroup(DataOrFact(string)))) 
                    else : 
                        Arch.add(string) 
                        Arch.add(str(replacedatatypetogroup(DataOrFact(string))))         
                
            UnionArchAccessTo()
            
            for ent in Recofactions.keys() : 
                if len(RecofUnionArch) > 0 and (ent in RecofUnionArch.keys()) :  
                    for arch in RecofUnionArch[ent] : 
                        generatebasics(arch)
                        generatebasicsEnc(arch)
                        generatebasicsEncAttEx(arch)
                else : 
                    for arch in Recofactions[ent] : 
                        generatebasics(arch)
                        
                        generatebasicsEnc(arch)
                       
                        generatebasicsEncAttEx(arch)
                        
           
            if len(basicEncRec) > 0 :
                cleanbasicsEncRec()
               
                
            if len(basicEncRecAttEx) > 0 :
                cleanbasicsEncRecAttEx()     
    
            if len(RecofUnionArch) > 0 and ("att" in RecofUnionArch.keys()) :
                for arch in RecofUnionArch["att"] : 
                    generatebasicsAttIn(arch)
                    generatebasicsEncAttIn(arch)
                
            if len(basicEncRecAttIn) > 0 :
                cleanbasicsEncRecAttIn()  
            
            



def add_to_arch(): 
    
    global Arch
    global ArchPseudo
    global ArchMeta
    global ArchTime
    global SetlistofbasicsHAS
    global SetlistofbasicsLink
    
    global SetlistofbasicsHASATTEX
    global SetlistofbasicsLinkATTEX
    global SetlistofbasicsHASATTIN
    global SetlistofbasicsLinkATTIN
    global SetlistofbasicsHASATTHYB
    global SetlistofbasicsLinkATTHYB
    
    global ReclistofbasicsLinkUnique
    global ReclistofbasicsLinkAttExUnique
    global SetlistofbasicsLinkATTHYBUnique
    global SetlistofbasicsLinkATTINUnique
    
    global RecofUnionArch
    
    global ReclistofbasicsHAS
    global ReclistofbasicsLink
    
    global basicEncRec
    global Recofactions
    global basicEncRecAttIn
    global basicEncRecAttHyb
    
    global storeArchRec
    global setRecvdOwnArgRec
    global recvdOwnArgRec
    global recvdStoreArgRec
    global setRecvdStoreArgRec
    
    global nameboxcontent
    global cPurposeArch 
    global uPurposeArch 
    
    
    Arch.clear()
    ArchPseudo.clear() 
    ArchMeta.clear()
    ArchTime.clear()
    
    SetlistofbasicsHAS.clear() 
    SetlistofbasicsLink.clear()
    SetlistofbasicsHASATTEX.clear()
    SetlistofbasicsLinkATTEX.clear()
    SetlistofbasicsHASATTIN.clear()
    SetlistofbasicsLinkATTIN.clear()
    SetlistofbasicsHASATTHYB.clear()
    SetlistofbasicsLinkATTHYB.clear()
    SetlistofbasicsLinkATTHYBUnique.clear()
    SetlistofbasicsLinkATTINUnique.clear()
    
    RecofUnionArch.clear()
    
    ReclistofbasicsHAS.clear()
    ReclistofbasicsLink.clear()
    
    ReclistofbasicsHASAttEx.clear()
    ReclistofbasicsLinkAttEx.clear()
    ReclistofbasicsLinkUnique.clear()
    ReclistofbasicsLinkAttExUnique.clear()
    
    basicEncRecAttEx.clear()
    basicEncRec.clear()
    Recofactions.clear()
    basicEncRecAttIn.clear()
    basicEncRecAttHyb.clear()
    
    
    storeArchRec = {"mainstorage":set(), "backupstorage":set()}
    setRecvdOwnArgRec.clear()
    recvdOwnArgRec.clear()
    recvdStoreArgRec.clear()
    setRecvdStoreArgRec.clear()
   
    cPurposeArch.clear() 
    uPurposeArch.clear() 
    
    for e in nameboxcontent.keys():
        userinput = nameboxcontent[e]
        stringofrow2 = userinput.splitlines()    
        
        if lengthall(stringofrow2) > 0: 
            stringofrow = set(map(lambda e:e.lower(),stringofrow2)) 
    
            if checkarchsyntaxerror(stringofrow) == 1 :  
                
                extractDataEFromArch(stringofrow) 
            
                update_cPurposeArch(userinput) 
            
                update_uPurposeArch(userinput) 
               
                add_recvdowned_args(userinput)
            
              
                add_storage_options(userinput)
    
              
                add_stored_args(userinput)
         
                for string in stringofrow : 
                    if len(string) != 0:   
                        addtoArchRec(DataOrFact(string)) 
                        
                        if len(string.split("p(")) == 2 : 
                            ArchPseudo.add(string)#  
                            ArchPseudo.add(str(replacedatatypetogroup(DataOrFact(string)))) 
                        elif len(string.split("meta(")) == 2 : 
                            ArchMeta.add(string)
                            ArchMeta.add(str(replacedatatypetogroup(DataOrFact(string)))) 
                        elif len(string.split("time(")) == 2 : 
                            ArchTime.add(string) 
                            ArchTime.add(str(replacedatatypetogroup(DataOrFact(string)))) 
                        else : 
                            Arch.add(string) 
                            Arch.add(str(replacedatatypetogroup(DataOrFact(string)))) 
                    
                
                UnionArchAccessTo()     
                
                for ent in Recofactions.keys() : 
                    if len(RecofUnionArch) > 0 and (ent in RecofUnionArch.keys()) :  
                        for arch in RecofUnionArch[ent] : 
                            generatebasics(arch)
                            generatebasicsEnc(arch)
                            generatebasicsEncAttEx(arch)
                    else :  
                        for arch in Recofactions[ent] : 
                            generatebasics(arch)
                           
                            generatebasicsEnc(arch)
                           
                            generatebasicsEncAttEx(arch)
                           
           
                if len(basicEncRec) > 0 :
                    cleanbasicsEncRec()   
                
                if len(basicEncRecAttEx) > 0 :
                    cleanbasicsEncRecAttEx()     
                
                if len(RecofUnionArch) > 0 and ("att" in RecofUnionArch.keys()) :
                    for arch in RecofUnionArch["att"] : 
                        generatebasicsAttIn(arch)
                        generatebasicsEncAttIn(arch)
                    
                if len(basicEncRecAttIn) > 0 :
                    cleanbasicsEncRecAttIn()   
               



def add_storage_options(userinput) : 
    ustringofrow2 = userinput.splitlines()   
    ustringofrow = set(map(lambda e:e.lower(),ustringofrow2))
    for ustring in ustringofrow : 
        if len(ustring) != 0 : 
           if (DataOrFact(ustring).predicate == "store") or (DataOrFact(ustring).predicate == "storeat") : 
               if len(DataOrFact(ustring).arguments) > 1 :
                   for data in DataOrFact(ustring).arguments[1:] :
                       if str(DataOrFact(ustring).arguments[0]) == "mainstorage" : 
                           storeArchRec["mainstorage"].add(str(data))   
                       elif str(DataOrFact(ustring).arguments[0]) == "backupstorage" : 
                           storeArchRec["backupstorage"].add(str(data)) 
                       if len(data.arguments) > 0 :   
                           if (str(data.predicate) not in ["time","meta","p"]) : 
                               for simpledata in data.arguments :  
                                   if str(DataOrFact(ustring).arguments[0]) == "mainstorage" : 
                                       storeArchRec["mainstorage"].add(str(simpledata))
                                   elif str(DataOrFact(ustring).arguments[0]) == "backupstorage" : 
                                       storeArchRec["backupstorage"].add(str(simpledata))



def add_recvdowned_args(userinput) : 
    ustringofrow2 = userinput.splitlines()   
    ustringofrow = set(map(lambda e:e.lower(),ustringofrow2)) 
    for ustring in ustringofrow :
        if len(ustring) != 0: 
            if (DataOrFact(ustring).predicate == "receive") or (DataOrFact(ustring).predicate == "receiveat") or (DataOrFact(ustring).predicate == "own") : 
                if len(DataOrFact(ustring).arguments) > 1 :  
                    for data in DataOrFact(ustring).arguments[1:] : 
                        if (str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate)) not in setRecvdOwnArgRec : 
                            setRecvdOwnArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))] = {str(data)}
                            recvdOwnArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))] = setRecvdOwnArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))]
                        else :
                            setRecvdOwnArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))].add(str(data))
                            recvdOwnArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))] = setRecvdOwnArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))]
                        if len(data.arguments) > 0 : 
                            if (str(data.predicate) not in CryptoPred) and (str(data.predicate) not in ["time","meta","p", "a"]) :
                                for simpledata in data.arguments : 
                                     if (str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate)) not in setRecvdOwnArgRec : 
                                         setRecvdOwnArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))] = {str(simpledata)}
                                         recvdOwnArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))] = setRecvdOwnArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))]
                                     else :
                                        setRecvdOwnArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))].add(str(simpledata))
                                        recvdOwnArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))] = setRecvdOwnArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))]
                        


def add_stored_args(userinput) : 
    ustringofrow2 = userinput.splitlines()    
    ustringofrow = set(map(lambda e:e.lower(),ustringofrow2)) 
    for ustring in ustringofrow :
        if len(ustring) != 0: 
            if (DataOrFact(ustring).predicate == "store") or (DataOrFact(ustring).predicate == "storeat") : 
                if len(DataOrFact(ustring).arguments) > 1 : 
                    for data in DataOrFact(ustring).arguments[1:] :
                        if (str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate)) not in setRecvdStoreArgRec : 
                            setRecvdStoreArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))] = {str(data)}   
                            recvdStoreArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))] = setRecvdStoreArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))]
                        else :
                            setRecvdStoreArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))].add(str(data))
                            recvdStoreArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))] = setRecvdStoreArgRec[(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate))]
                        



def cpurposenextnestdata(strentity,straction,strmostcomplexdata,strnextdata) : 
    
    if len(DataOrFact(strnextdata).arguments) == 0  and (straction not in ["receive","receiveat","own"]) : 
        if ((strentity,strnextdata) not in setcpurposesRecArch) :  
            setcpurposesRecArch[(strentity,strnextdata)] = {(straction,strmostcomplexdata)}
            cpurposesRecArch[(strentity,strnextdata)] = setcpurposesRecArch[(strentity,strnextdata)]
        
        else:  
            setcpurposesRecArch[(strentity,strnextdata)].add((straction,strmostcomplexdata))
            cpurposesRecArch[(strentity,strnextdata)] = setcpurposesRecArch[(strentity,strnextdata)]
                
    elif len(DataOrFact(strnextdata).arguments) > 0 and (strmostcomplexdata not in ["meta","time","p", "a"]) and (straction not in ["receive","receiveat","own"]) :
        if str(DataOrFact(strnextdata).predicate) in ["p", "a"] : 
            if ((strentity,strnextdata) not in setcpurposesRecArch) : 
                setcpurposesRecArch[(strentity,strnextdata)] = {(straction,strmostcomplexdata)}  
                cpurposesRecArch[(strentity,strnextdata)] = setcpurposesRecArch[(strentity,strnextdata)]
            else:  
                setcpurposesRecArch[(strentity,strnextdata)].add((straction,strmostcomplexdata))   
                cpurposesRecArch[(strentity,strnextdata)] = setcpurposesRecArch[(strentity,strnextdata)]
            
            for data in DataOrFact(strnextdata).arguments : 
                cpurposenextnestdata(strentity,straction,strmostcomplexdata,str(data))
        else: 
            if str(DataOrFact(strnextdata).predicate) not in ["meta", "time"] : 
                if (strentity,str(DataOrFact(strnextdata))) not in setcpurposesRecArch : 
                    setcpurposesRecArch[(strentity,str(DataOrFact(strnextdata)))] = {(straction,strmostcomplexdata)} 
                    cpurposesRecArch[(strentity,str(DataOrFact(strnextdata)))] = setcpurposesRecArch[(strentity,str(DataOrFact(strnextdata)))]
                else:  
                    setcpurposesRecArch[(strentity,str(DataOrFact(strnextdata)))].add((straction,strmostcomplexdata))   
                    cpurposesRecArch[(strentity,str(DataOrFact(strnextdata)))] = setcpurposesRecArch[(strentity,str(DataOrFact(strnextdata)))]
                for data in DataOrFact(strnextdata).arguments : 
                    cpurposenextnestdata(strentity,straction,strmostcomplexdata,str(data))




def extractDataEFromArch(stringofrow) : 
    global ReceiveDataE
    global CreateDataE
    global CalculateDataE
    global CConsDataE
    global UConsDataE
    global SConsDataE
    global FwConsDataE
   
    
    ReceiveDataE.clear()
    CreateDataE.clear()
    CalculateDataE.clear()
    CConsDataE.clear()
    UConsDataE.clear()
    SConsDataE.clear()
    FwConsDataE.clear()
   

    for ustring in stringofrow :
        if len(ustring) != 0: 
            if len(DataOrFact(ustring).arguments) > 1 : 
                if str(DataOrFact(ustring).predicate) in ["receive", "receiveat"] : 
                    if str(DataOrFact(ustring).arguments[1].predicate) in ["cconsent", "uconsent", "sconsent", "fwconsent"] : 
                        extractparamConsent(DataOrFact(ustring).arguments[1])
                    else :   
                        ReceiveDataE.add((str(DataOrFact(ustring).arguments[1]), str(DataOrFact(ustring).arguments[0])))  
                elif str(DataOrFact(ustring).predicate) in ["create", "createat"] : 
                   CreateDataE.add((str(DataOrFact(ustring).arguments[1]), str(DataOrFact(ustring).arguments[0]))) 
                elif str(DataOrFact(ustring).predicate) in ["calculate", "calculateat", "calculatefrom", "calculatefromat"] : 
                   CalculateDataE.add((str(DataOrFact(ustring).arguments[1]), str(DataOrFact(ustring).arguments[0])))   
                elif str(DataOrFact(ustring).predicate) in ["store", "storeat"] : 
                   StoreDataE.add((str(DataOrFact(ustring).arguments[1]), str(DataOrFact(ustring).arguments[0])))   
    


def update_cPurposeArch(userinput) : 
    global cPurposeArch
    
    ustringofrow2 = userinput.splitlines() 
    ustringofrow = set(map(lambda e:e.lower(),ustringofrow2)) 
    for ustring in ustringofrow :
        if len(ustring) != 0: 
            if len(DataOrFact(ustring).arguments) > 1 and (str(DataOrFact(ustring).arguments[1].predicate) not in ["cconsent", "uconsent", "sconsent", "fwconsent"]) : 
                
                if str(DataOrFact(ustring).predicate) in ["createat", "calculateat", "calculatefromat", "receiveat"] : 
                    if  len(DataOrFact(ustring).arguments[1].arguments) > 0 : 
                        for simpledata in DataOrFact(ustring).arguments[1].arguments: 
                            cPurposeArch.add("CPURPOSE(" + str(DataOrFact(ustring).arguments[1].predicate) + "," + str(DataOrFact(ustring).predicate)[:-2] + "," + str(simpledata)  + ")")  
                            cPurposeArch.add("CPURPOSE(" + str(DataOrFact(ustring).arguments[1].predicate) + "," + str(DataOrFact(ustring).predicate)[:-2] + ")") 
                    else: 
                        cPurposeArch.add("CPURPOSE(" + str(DataOrFact(ustring).arguments[1].predicate) + "," + str(DataOrFact(ustring).predicate)[:-2] + ")")
                elif str(DataOrFact(ustring).predicate) in ["create", "calculate", "calculatefrom","receive"]:   
                    if  len(DataOrFact(ustring).arguments[1].arguments) > 0 :
                        for simpledata in DataOrFact(ustring).arguments[1].arguments: 
                            cPurposeArch.add("CPURPOSE(" + str(DataOrFact(ustring).arguments[1].predicate) + "," + str(DataOrFact(ustring).predicate) + "," + str(simpledata) + ")")  
                            cPurposeArch.add("CPURPOSE(" + str(DataOrFact(ustring).arguments[1].predicate) + "," + str(DataOrFact(ustring).predicate) + ")") 
                    else :
                        cPurposeArch.add("CPURPOSE(" + str(DataOrFact(ustring).arguments[1].predicate) + "," + str(DataOrFact(ustring).predicate) + ")")
                        

                        
def update_uPurposeArch(userinput) : 
    global uPurposeArch
    
    ustringofrow2 = userinput.splitlines() 
    ustringofrow = set(map(lambda e:e.lower(),ustringofrow2)) 
    for ustring in ustringofrow :
        if len(ustring) != 0: 
            if len(DataOrFact(ustring).arguments) > 1 and (str(DataOrFact(ustring).arguments[1].predicate) not in ["cconsent", "uconsent", "sconsent", "fwconsent"]) : 
                
                if str(DataOrFact(ustring).predicate) in ["createat", "calculateat", "calculatefromat"] :  
                    if  len(DataOrFact(ustring).arguments[1].arguments) > 0 : 
                        for simpledata in DataOrFact(ustring).arguments[1].arguments: 
                            uPurposeArch.add("UPURPOSE(" + str(DataOrFact(ustring).arguments[1].predicate) + "," + str(DataOrFact(ustring).predicate)[:-2] + "," + str(simpledata)  + ")")  
                            uPurposeArch.add("UPURPOSE(" + str(DataOrFact(ustring).arguments[1].predicate) + "," + str(DataOrFact(ustring).predicate)[:-2] + ")") 
                    else:    
                        uPurposeArch.add("UPURPOSE(" + str(DataOrFact(ustring).arguments[1].predicate) + "," + str(DataOrFact(ustring).predicate)[:-2] + ")")
                elif str(DataOrFact(ustring).predicate) in ["create", "calculate", "calculatefrom"]:   
                    if  len(DataOrFact(ustring).arguments[1].arguments) > 0 :  
                        for simpledata in DataOrFact(ustring).arguments[1].arguments: 
                            uPurposeArch.add("UPURPOSE(" + str(DataOrFact(ustring).arguments[1].predicate) + "," + str(DataOrFact(ustring).predicate) + "," + str(simpledata) + ")")  
                            uPurposeArch.add("UPURPOSE(" + str(DataOrFact(ustring).arguments[1].predicate) + "," + str(DataOrFact(ustring).predicate) + ")") 
                    else :    
                        uPurposeArch.add("UPURPOSE(" + str(DataOrFact(ustring).arguments[1].predicate) + "," + str(DataOrFact(ustring).predicate) + ")")
                    
                    
        
                                 
def update_cpurposesrec(userinput) : 
    ustringofrow2 = userinput.splitlines()  
    ustringofrow = set(map(lambda e:e.lower(),ustringofrow2)) 
    for ustring in ustringofrow :
        if len(ustring) != 0: 
            if len(DataOrFact(ustring).arguments) > 1 : 
                for mostcomplexdata in DataOrFact(ustring).arguments[1:] : 
                        if len(mostcomplexdata.arguments) > 0 and (str(mostcomplexdata.predicate) not in ["meta","time","p", "a"]) and (str(DataOrFact(ustring).predicate) not in ["receive","receiveat","own"]) : 
                            for nextdata in mostcomplexdata.arguments : 
                                cpurposenextnestdata(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate),str(mostcomplexdata.predicate),str(nextdata))
                        
                        elif len(mostcomplexdata.arguments) > 0 and (str(mostcomplexdata.predicate) in ["p", "a"]) and (str(DataOrFact(ustring).predicate) not in ["receive","receiveat","own"]) :       
                            for nextdata in mostcomplexdata.arguments : 
                                cpurposenextnestdata(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate),str(mostcomplexdata.predicate),str(nextdata))
                            
                        elif len(mostcomplexdata.arguments) == 0 and (str(DataOrFact(ustring).predicate) not in ["receive","receiveat","own"]) : 
                            if ((str(DataOrFact(ustring).arguments[0]),str(mostcomplexdata)) not in setcpurposesRecArch) :  
                                setcpurposesRecArch[(str(DataOrFact(ustring).arguments[0]),str(mostcomplexdata))] = {(str(DataOrFact(ustring).predicate),str(mostcomplexdata))}
                                cpurposesRecArch[(str(DataOrFact(ustring).arguments[0]),str(mostcomplexdata))] = setcpurposesRecArch[(str(DataOrFact(ustring).arguments[0]),str(mostcomplexdata))]
                            else: 
                                setcpurposesRecArch[(str(DataOrFact(ustring).arguments[0]),str(mostcomplexdata))].add((str(DataOrFact(ustring).predicate),str(mostcomplexdata)))
                                cpurposesRecArch[(str(DataOrFact(ustring).arguments[0]),str(mostcomplexdata))] = setcpurposesRecArch[(str(DataOrFact(ustring).arguments[0]),str(mostcomplexdata))]



def parent_cpurposesrec() : 
    tempRec = cpurposesRecArch.copy()  
    for (entity,simpledata) in tempRec.keys() : 
         if (entity in entityRelationRec) and  len(entityRelationRec[entity]) > 0 :  
            for parent in entityRelationRec[entity] : 
               if (parent,simpledata) not in setcpurposesRecArch :
                   setcpurposesRecArch[(parent,simpledata)] = cpurposesRecArch[(entity,simpledata)]  
                   cpurposesRecArch[(parent,simpledata)] = setcpurposesRecArch[(parent,simpledata)]
               else : 
                setcpurposesRecArch[(parent,simpledata)].union(cpurposesRecArch[(entity,simpledata)])  
                cpurposesRecArch[(parent,simpledata)] = setcpurposesRecArch[(parent,simpledata)]



def upurposenextnestdata(strentity,straction,strmostcomplexdata,strnextdata) : 
    if len(DataOrFact(strnextdata).arguments) == 0  and (straction not in ["receive","receiveat","own"]) : 
        if ((strentity,strnextdata) not in setupurposesRecArch) :
            setupurposesRecArch[(strentity,strnextdata)] = {(straction,strmostcomplexdata)} 
            upurposesRecArch[(strentity,strnextdata)] = setupurposesRecArch[(strentity,strnextdata)]
        
        else:  
            setupurposesRecArch[(strentity,strnextdata)].add((straction,strmostcomplexdata))
            upurposesRecArch[(strentity,strnextdata)] = setupurposesRecArch[(strentity,strnextdata)]
                
    elif len(DataOrFact(strnextdata).arguments) > 0 and (strmostcomplexdata not in ["meta","time","p", "a"]) and (straction not in ["receive","receiveat","own"]) :  
        if str(DataOrFact(strnextdata).predicate) in ["p", "a"] : 
            if ((strentity,strnextdata) not in setupurposesRecArch) : 
                setupurposesRecArch[(strentity,strnextdata)] = {(straction,strmostcomplexdata)}  
                upurposesRecArch[(strentity,strnextdata)] = setupurposesRecArch[(strentity,strnextdata)]
            else:  
                setupurposesRecArch[(strentity,strnextdata)].add((straction,strmostcomplexdata))  
                upurposesRecArch[(strentity,strnextdata)] = setupurposesRecArch[(strentity,strnextdata)]
            
            for data in DataOrFact(strnextdata).arguments : 
                upurposenextnestdata(strentity,straction,strmostcomplexdata,str(data))
        else: 
            if str(DataOrFact(strnextdata).predicate) not in ["meta", "time"] : 
                if (strentity,str(DataOrFact(strnextdata))) not in setupurposesRecArch :
                    setupurposesRecArch[(strentity,str(DataOrFact(strnextdata)))] = {(straction,strmostcomplexdata)}  
                    upurposesRecArch[(strentity,str(DataOrFact(strnextdata)))] = setupurposesRecArch[(strentity,str(DataOrFact(strnextdata)))]
                else: 
                    setupurposesRecArch[(strentity,str(DataOrFact(strnextdata)))].add((straction,strmostcomplexdata))   
                    upurposesRecArch[(strentity,str(DataOrFact(strnextdata)))] = setupurposesRecArch[(strentity,str(DataOrFact(strnextdata)))]
                for data in DataOrFact(strnextdata).arguments : 
                    upurposenextnestdata(strentity,straction,strmostcomplexdata,str(data))
    
     
        


                             
def update_upurposesrec(userinput) : 
    ustringofrow2 = userinput.splitlines()   
    ustringofrow = set(map(lambda e:e.lower(),ustringofrow2)) 
    for ustring in ustringofrow :
        if len(ustring) != 0: 
            if len(DataOrFact(ustring).arguments) > 1 : 
                for mostcomplexdata in DataOrFact(ustring).arguments[1:] : 
                        if len(mostcomplexdata.arguments) > 0 and (str(mostcomplexdata.predicate) not in ["meta","time","p", "a"]) and (str(DataOrFact(ustring).predicate) not in ["receive","receiveat","own"]) : 
                                for nextdata in mostcomplexdata.arguments : 
                                    upurposenextnestdata(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate),str(mostcomplexdata.predicate),str(nextdata))
                        
                         
                        elif len(mostcomplexdata.arguments) > 0 and (str(mostcomplexdata.predicate) in ["p", "a"]) and (str(DataOrFact(ustring).predicate) not in ["receive","receiveat","own"]) :       
                            for nextdata in mostcomplexdata.arguments : 
                                upurposenextnestdata(str(DataOrFact(ustring).arguments[0]),str(DataOrFact(ustring).predicate),str(mostcomplexdata.predicate),str(nextdata))
                    
                        elif len(mostcomplexdata.arguments) == 0 and (str(DataOrFact(ustring).predicate) not in ["receive","receiveat","own"]) : 
                            if ((str(DataOrFact(ustring).arguments[0]),str(mostcomplexdata)) not in setupurposesRecArch) : 
                                setupurposesRecArch[(str(DataOrFact(ustring).arguments[0]),str(mostcomplexdata))] = {(str(DataOrFact(ustring).predicate),str(mostcomplexdata))}
                                upurposesRecArch[(str(DataOrFact(ustring).arguments[0]),str(mostcomplexdata))] = setupurposesRecArch[(str(DataOrFact(ustring).arguments[0]),str(mostcomplexdata))]
                            else: 
                                setupurposesRecArch[(str(DataOrFact(ustring).arguments[0]),str(mostcomplexdata))].add((str(DataOrFact(ustring).predicate),str(mostcomplexdata)))
                                upurposesRecArch[(str(DataOrFact(ustring).arguments[0]),str(mostcomplexdata))] = setupurposesRecArch[(str(DataOrFact(ustring).arguments[0]),str(mostcomplexdata))]



def parent_upurposesrec() : 
    tempRec = upurposesRecArch.copy()  
    for (entity,simpledata) in tempRec.keys() : 
         if (entity in entityRelationRec) and  len(entityRelationRec[entity]) > 0 :  
            for parent in entityRelationRec[entity] : 
               if (parent,simpledata) not in setupurposesRecArch :
                   setupurposesRecArch[(parent,simpledata)] = upurposesRecArch[(entity,simpledata)]  
                   upurposesRecArch[(parent,simpledata)] = setupurposesRecArch[(parent,simpledata)]
               else : 
                setupurposesRecArch[(parent,simpledata)].union(upurposesRecArch[(entity,simpledata)]) 
                upurposesRecArch[(parent,simpledata)] = setupurposesRecArch[(parent,simpledata)]
                            
        

def strtoterm(string): 
    return DataOrFact(string)
    


def add_to_query(q,q1):
    q.append(convertHasAfter(DataOrFact(q1)))
    



def saveactionsfileas(text): 
    files = [('Actions Text File', '*.txt')]  
    file = asksaveasfile(mode='w', filetypes = files, defaultextension = files) 
    if file:
        file.write(text)
        file.close()
    else: 
      
        return 0



def show_arch():
    if len(Arch) > 0:
        actions = "ACTIONS:\n"
        for act in Arch :
            actions = actions + act + "\n"
    else: 
        actions = ""
    
    if len(ArchPseudo) > 0:    
        actionspseudo = "\nACTIONS WITH PSEUDONYMISED DATA: \n"
        for act in ArchPseudo : 
            actionspseudo = actionspseudo + act + "\n"
    else: 
        actionspseudo = ""
    
    if len(ArchMeta) > 0:
        actionsmeta = "\nACTIONS WITH METADATA: \n"
        for act in ArchMeta :
            actionsmeta = actionsmeta + act + "\n"
    else: 
        actionsmeta = ""
    
    if len(ArchTime) > 0:    
        actionstime = "\nACTIONS WITH TIME CONSTRUCT: \n"
        for act in ArchTime :    
            actionstime = actionstime + act + "\n"
    else: 
        actionstime = ""
    
    allactions = actions + actionspseudo + actionsmeta + actionstime
    
    saveactionsfileas(allactions)  



def save_datagroupoftypes(datagroup, datatypes):  
    for rstring in datatypes :
        if len(rstring) != 0: 
                if rstring not in set(datagroupoftypes.keys()):
                    datagroupoftypes[rstring] = datagroup.lower() 
                else :
                    datagroupoftypes[rstring].add(datagroup.lower())



def addtypes(pframe,group1,typelist,isunique): 
    stringofrow2 = typelist.splitlines()
    stringofrow = set(map(lambda e:e.lower(),stringofrow2)) 
    group = group1.lower() 
    datatypesrec[group] = set(stringofrow)
    datatypesrec1[group1] = set(stringofrow) 
    save_datagroupoftypes(group, stringofrow)
    if isunique == "Yes" : 
        if len(group) != 0:   
            UniqueData.add("Unique(" + group  + ")") 
    show_policy_window()
    pframe.destroy()



def addentity(pframe,ent,desc):
    entityrec[ent.lower()] = desc 
    show_policy_window()
    pframe.destroy()     

    
def convertdicttolist(dictionary): 
    dlist =[]
    for key, value in dictionary.items():
        if key == "": 
            dlist.append("")
        else: dlist.append(key + " (" + value +")")
    return dlist   




def show_policy_window(): 
    policyframe=Toplevel()
    policyframe.state("zoomed") 
    policyframe.title("                                                                                                                                                         DataProVe Tool (THIS IS THE DATA PROTECTION POLICY SPECIFICATION PAGE)")
    
  
    policycanvas1 = Canvas(policyframe, width = 900, height = 50, background="LightSkyBlue3")
    policycanvas1.pack(expand=True,fill=BOTH)
    le1 = Label(policycanvas1, text="PROVIDE A NEW ENTITY: ",font=("Arial", 11), bg = "LightSkyBlue3")
    le1.pack(side=LEFT)
    entity = Entry(policycanvas1, width=40,justify=CENTER,bd=5)
    entity.pack(side=LEFT)
    le2 = Label(policycanvas1, text="PROVIDE A DESCRIPTION: ",font=("Arial", 11), bg = "LightSkyBlue3")
    le2.pack(side=LEFT)
    description = Entry(policycanvas1, width=40,justify=CENTER,bd=5)
    description.pack(side=LEFT)
    le3 = Label(policycanvas1, text="       ",font=("Arial", 11), bg = "LightSkyBlue3")
    le3.pack(side=LEFT)
    addentitybutton = Button(policycanvas1,text="ADD NEW ENTITY", command=lambda:addentity(policyframe,entity.get(),description.get()))    
    addentitybutton.pack(side=LEFT)
    
   
    policycanvas0 = Canvas(policyframe, width = 900, height = 50, background="LightSkyBlue2")
    policycanvas0.pack(expand=True,fill=BOTH)
    ld1 = Label(policycanvas0, text="PROVIDE A GROUP\n OF DATA TYPES: ",font=("Arial", 11), bg = "LightSkyBlue2")
    ld1.pack(side=LEFT)
    datagroup = Entry(policycanvas0, width=40,justify=CENTER,bd=5)
    datagroup.pack(side=LEFT)
    
    ld5 = Label(policycanvas0, text="   ",font=("Arial", 11), bg = "LightSkyBlue2")
    ld5.pack(side=LEFT)
    
    OPTIONS3 = ["Yes","No"] 
    variable3 = StringVar(policycanvas0)
    variable3.set(OPTIONS3[-1]) 
    lu = Label(policycanvas0, text="IS THIS\n UNIQUE?",font=("Arial", 11), bg = "LightSkyBlue2")   
    lu.pack(side=LEFT)
    wu = OptionMenu(policycanvas0, variable3, *OPTIONS3)
    wu.pack(side=LEFT)
    
    ld4 = Label(policycanvas0, text="   ",font=("Arial", 11), bg = "LightSkyBlue2")
    ld4.pack(side=LEFT)
    
    
    ld2 = Label(policycanvas0, text="THE DATA TYPES\n IN THIS GROUP: ",font=("Arial", 11), bg = "LightSkyBlue2")
    ld2.pack(side=LEFT)
    datatypes = scrolledtext.ScrolledText(policycanvas0, width=40, heigh=10, bd=1) 
    datatypes.pack(side=LEFT)
    
    ld3 = Label(policycanvas0, text="      ",font=("Arial", 11), bg = "LightSkyBlue2")
    ld3.pack(side=LEFT)
     
    adddatatypesbutton = Button(policycanvas0,text="ADD DATA\n GROUP & TYPES", command=lambda:addtypes(policyframe,datagroup.get(),datatypes.get("1.0", END),variable3.get())) 
    adddatatypesbutton.pack(side=LEFT)
    
   
    policycanvas = Canvas(policyframe, width = 900, height = 50, background="LightSkyBlue1")
    policycanvas.pack(expand=True,fill=BOTH)
    
    OPTIONS2 = convertdicttolist(entityrec)
    variable2 = StringVar(policycanvas)
    variable2.set(OPTIONS2[-1]) 
    le = Label(policycanvas, text="Choose\n an entity ",font=("Arial", 11), bg = "LightSkyBlue1")
    le.pack(side=LEFT)
    we = OptionMenu(policycanvas, variable2, *OPTIONS2)
    we.pack(side=LEFT)
    ld7 = Label(policycanvas, text="      ",font=("Arial", 11), bg = "LightSkyBlue1")
    ld7.pack(side=LEFT)
    
    OPTIONS = list(datatypesrec1.keys()) 
    variable = StringVar(policycanvas)
    variable.set(OPTIONS[-1])
    lo = Label(policycanvas, text="Choose\n a data group ",font=("Arial", 11), bg = "LightSkyBlue1")
    lo.pack(side=LEFT)
    w = OptionMenu(policycanvas, variable, *OPTIONS)
    w.pack(side=LEFT)
    ld6 = Label(policycanvas, text="      ",font=("Arial", 11), bg = "LightSkyBlue1")
    ld6.pack(side=LEFT)
    
    unionvalues = set()
    for v in datatypesrec.values() :
        for e in v: 
            if e != "-": 
                unionvalues.add(e)
    
    OPTIONS1 = ["-"] + list(unionvalues) 
    variable1 = StringVar(policycanvas)
    variable1.set(OPTIONS1[-1]) 
    lo1 = Label(policycanvas, text="Choose\n a data type ",font=("Arial", 11), bg = "LightSkyBlue1")
    lo1.pack(side=LEFT)
    wt = OptionMenu(policycanvas, variable1, *OPTIONS1)
    wt.pack(side=LEFT)
    ld8 = Label(policycanvas, text="      ",font=("Arial", 11), bg = "LightSkyBlue1")
    ld8.pack(side=LEFT)
    
    lp = Label(policycanvas, text="SUB-\n POLICIES : ",font=("Arial", 11), bg = "LightSkyBlue1")
    lp.pack(side=LEFT)
   
    collectionbutton = Button(policycanvas,text="Data\n Collection\n ", command=lambda:collectionpol("sp (service provider)",variable.get(),variable1.get()))    
    collectionbutton.pack(side=LEFT)
    
    usagebutton = Button(policycanvas,text="Data\n Usage\n ", command=lambda:usagepol("sp (service provider)",variable.get(),variable1.get()))
    usagebutton.pack(side=LEFT)
   
    storebutton = Button(policycanvas,text="Data\n Storage\n ", command=lambda:storepol("sp (service provider)",variable.get(),variable1.get()))
    storebutton.pack(side=LEFT)
    
    deletebutton = Button(policycanvas,text="Data\n Retention\n ", command=lambda:deletepol("sp (service provider)",variable.get(),variable1.get()))
    deletebutton.pack(side=LEFT)
   
    transferbutton = Button(policycanvas,text="Data\n Transfer\n ", command=lambda:transferpol("sp (service provider)",variable.get(),variable1.get()))
    transferbutton.pack(side=LEFT)
    hasbutton = Button(policycanvas,text="Data\n Possession\n ", command=lambda:haspol(variable2.get(),variable.get(),variable1.get()))    
    hasbutton.pack(side=LEFT)
    linkbutton = Button(policycanvas,text="Data\n Connection\n (Permit)", command=lambda:linkpol(variable2.get(),variable.get(),variable1.get()))    
    linkbutton.pack(side=LEFT)
    linkforbidbutton = Button(policycanvas,text="Data\n Connection\n (Forbid)", command=lambda:linkforbidpol(variable2.get(),variable.get(),variable1.get()))    
    linkforbidbutton.pack(side=LEFT)



def show_policy_window_reset(): 
    global entityrec
    global datagroupoftypes
    global datatypesrec
    global datatypesrec1
    
    global collectionpolicytosave
    global usagepolicytosave
    global storagepolicytosave
    global deletionpolicytosave 
    global transferpolicytosave 
    global haspolicytosave 
    global linkpermitpolicytosave 
    global linkforbidpolicytosave
    global storagemodepol    
    global storeoptionrec
    
    global storePolRec
    global entityHasRec
    global cpurposesRecPol 
    global upurposesRecPol
    
    global queryHasAfter 
    global queryFWConsent 
    global queryHas 
    global queryLinkUnique 
    global queryLink 
    global queryNotLinkUnique  
    global queryNotLink
    global queryCConsent
    global queryUConsent
    global querySConsent
    
    global UniqueData
    
    global entityHasListRec
    global setcpurposesRecPol
    global setupurposesRecPol
    
    entityrec = {"att":"attacker","sp":"service provider"}  
    datagroupoftypes = {"":""} 
    datatypesrec = {"":"-"}  
    datatypesrec1 = {"":"-"}
    
    collectionpolicytosave = {}
    usagepolicytosave = {}
    storagepolicytosave = {}
    deletionpolicytosave = {}
    transferpolicytosave = {}
    haspolicytosave = {}
    linkpermitpolicytosave = {} 
    linkforbidpolicytosave = {}
    
    storeoptionrec = {}
    
    storePolRec = {"mainstorage":set(), "backupstorage":set()}
   
    queryHas.clear()
    entityHasListRec.clear()
    entityHasRec.clear()
    queryCConsent.clear()
    cpurposesRecPol.clear()
    setcpurposesRecPol.clear()
    queryUConsent.clear()
    upurposesRecPol.clear()
    setupurposesRecPol.clear()
    querySConsent.clear()
    storagemodepol.clear()    
    
    queryHasAfter.clear()
    queryFWConsent.clear()
     
    queryLinkUnique.clear()  
    queryLink.clear() 
    queryNotLinkUnique.clear()  
    queryNotLink.clear()
    UniqueData.clear()
    
    
    policyframe=Toplevel()
    
    policyframe.state("zoomed")  
    policyframe.title("                                                                                                                                                         DataProVe Tool (THIS IS THE DATA PROTECTION POLICY SPECIFICATION PAGE)")
    
  
    policycanvas1 = Canvas(policyframe, width = 900, height = 50, background="LightSkyBlue3")
    policycanvas1.pack(expand=True,fill=BOTH)
    le1 = Label(policycanvas1, text="PROVIDE A NEW ENTITY: ",font=("Arial", 11), bg = "LightSkyBlue3")
    le1.pack(side=LEFT)
    entity = Entry(policycanvas1, width=40,justify=CENTER,bd=5)
    entity.pack(side=LEFT)
    le2 = Label(policycanvas1, text="PROVIDE A DESCRIPTION: ",font=("Arial", 11), bg = "LightSkyBlue3")
    le2.pack(side=LEFT)
    description = Entry(policycanvas1, width=40,justify=CENTER,bd=5)
    description.pack(side=LEFT)
    le3 = Label(policycanvas1, text="       ",font=("Arial", 11), bg = "LightSkyBlue3")
    le3.pack(side=LEFT)
    addentitybutton = Button(policycanvas1,text="ADD NEW ENTITY", command=lambda:addentity(policyframe,entity.get(),description.get()))    
    addentitybutton.pack(side=LEFT)
    
  
    policycanvas0 = Canvas(policyframe, width = 900, height = 50, background="LightSkyBlue2")
    policycanvas0.pack(expand=True,fill=BOTH)
    ld1 = Label(policycanvas0, text="PROVIDE A GROUP\n OF DATA TYPES: ",font=("Arial", 11), bg = "LightSkyBlue2")
    ld1.pack(side=LEFT)
    datagroup = Entry(policycanvas0, width=40,justify=CENTER,bd=5)
    datagroup.pack(side=LEFT)
    
    ld5 = Label(policycanvas0, text="   ",font=("Arial", 11), bg = "LightSkyBlue2")
    ld5.pack(side=LEFT)
    
    OPTIONS3 = ["Yes","No"] 
    variable3 = StringVar(policycanvas0)
    variable3.set(OPTIONS3[-1]) 
    lu = Label(policycanvas0, text="IS THIS\n UNIQUE?",font=("Arial", 11), bg = "LightSkyBlue2")   
    lu.pack(side=LEFT)
    wu = OptionMenu(policycanvas0, variable3, *OPTIONS3)
    wu.pack(side=LEFT)
    
    ld4 = Label(policycanvas0, text="   ",font=("Arial", 11), bg = "LightSkyBlue2")
    ld4.pack(side=LEFT)
    
   
    ld2 = Label(policycanvas0, text="THE DATA TYPES\n IN THIS GROUP: ",font=("Arial", 11), bg = "LightSkyBlue2")
    ld2.pack(side=LEFT)
    datatypes = scrolledtext.ScrolledText(policycanvas0, width=40, heigh=10, bd=1) 
    datatypes.pack(side=LEFT)
    
    ld3 = Label(policycanvas0, text="      ",font=("Arial", 11), bg = "LightSkyBlue2")
    ld3.pack(side=LEFT)
   
    adddatatypesbutton = Button(policycanvas0,text="ADD DATA\n GROUP & TYPES", command=lambda:addtypes(policyframe,datagroup.get(),datatypes.get("1.0", END),variable3.get())) 
    adddatatypesbutton.pack(side=LEFT)
    
  
    policycanvas = Canvas(policyframe, width = 900, height = 50, background="LightSkyBlue1")
    policycanvas.pack(expand=True,fill=BOTH)
    
    OPTIONS2 = convertdicttolist(entityrec) 
    variable2 = StringVar(policycanvas)
    variable2.set(OPTIONS2[-1]) 
    le = Label(policycanvas, text="Choose\n an entity ",font=("Arial", 11), bg = "LightSkyBlue1")
    le.pack(side=LEFT)
    we = OptionMenu(policycanvas, variable2, *OPTIONS2)
    we.pack(side=LEFT)
    ld7 = Label(policycanvas, text="      ",font=("Arial", 11), bg = "LightSkyBlue1")
    ld7.pack(side=LEFT)
   
    OPTIONS = list(datatypesrec1.keys())
    variable = StringVar(policycanvas)
    variable.set(OPTIONS[-1]) 
    lo = Label(policycanvas, text="Choose\n a data group ",font=("Arial", 11), bg = "LightSkyBlue1")
    lo.pack(side=LEFT)
    w = OptionMenu(policycanvas, variable, *OPTIONS)
    w.pack(side=LEFT)
    ld6 = Label(policycanvas, text="      ",font=("Arial", 11), bg = "LightSkyBlue1")
    ld6.pack(side=LEFT)
  
    unionvalues = set()
    for v in datatypesrec.values() :
        for e in v: 
            if e != "-": 
                unionvalues.add(e)
    
    OPTIONS1 = ["-"] + list(unionvalues) 
    variable1 = StringVar(policycanvas)
    variable1.set(OPTIONS1[-1]) 
    lo1 = Label(policycanvas, text="Choose\n a data type ",font=("Arial", 11), bg = "LightSkyBlue1")
    lo1.pack(side=LEFT)
    wt = OptionMenu(policycanvas, variable1, *OPTIONS1)
    wt.pack(side=LEFT)
    ld8 = Label(policycanvas, text="      ",font=("Arial", 11), bg = "LightSkyBlue1")
    ld8.pack(side=LEFT)
    
    lp = Label(policycanvas, text="SUB-\n POLICIES : ",font=("Arial", 11), bg = "LightSkyBlue1")
    lp.pack(side=LEFT)
    
    collectionbutton = Button(policycanvas,text="Data\n Collection\n ", command=lambda:collectionpol("sp (service provider)",variable.get(),variable1.get()))    
    collectionbutton.pack(side=LEFT)
     
    usagebutton = Button(policycanvas,text="Data\n Usage\n ", command=lambda:usagepol("sp (service provider)",variable.get(),variable1.get()))
    usagebutton.pack(side=LEFT)
    
    storebutton = Button(policycanvas,text="Data\n Storage\n ", command=lambda:storepol("sp (service provider)",variable.get(),variable1.get()))
    storebutton.pack(side=LEFT)
       
    deletebutton = Button(policycanvas,text="Data\n Retention\n ", command=lambda:deletepol("sp (service provider)",variable.get(),variable1.get()))
    deletebutton.pack(side=LEFT)
   
    transferbutton = Button(policycanvas,text="Data\n Transfer\n ", command=lambda:transferpol("sp (service provider)",variable.get(),variable1.get()))
    transferbutton.pack(side=LEFT)
    hasbutton = Button(policycanvas,text="Data\n Possession\n ", command=lambda:haspol(variable2.get(),variable.get(),variable1.get()))    
    hasbutton.pack(side=LEFT)
    linkbutton = Button(policycanvas,text="Data\n Connection\n (Permit)", command=lambda:linkpol(variable2.get(),variable.get(),variable1.get()))    
    linkbutton.pack(side=LEFT)
    linkforbidbutton = Button(policycanvas,text="Data\n Connection\n (Forbid)", command=lambda:linkforbidpol(variable2.get(),variable.get(),variable1.get()))    
    linkforbidbutton.pack(side=LEFT)




def visitweb(url): 
    webbrowser.open(url)


########################################################################################################################################
########################## MAIN CANVAS - ARCHITECTURE SPECIFICATION PANE ###############################################################
########################################################################################################################################
  
root = Tk()
root.state("zoomed")
root.title("                                                                                                                                                         DataProVe Tool (THIS IS THE SYSTEM ARCHITECTURE SPECIFICATION PAGE)")  # we added space to center the window title

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="SPECIFY A NEW DATA PROTECTION POLICY", command=show_policy_window_reset)  
filemenu.add_command(label="SAVE THE POLICY", command=savepolicyfileas)  
filemenu.add_command(label="OPEN A POLICY", command=open_policyfile)  
menubar.add_cascade(label="POLICY", menu=filemenu)  

file1menu = Menu(menubar, tearoff=0)
file1menu.add_command(label="?? HOWTO/HELP/README (GUI MODE) ??", command=lambda:HowToGui())
file1menu.add_command(label="CLEAR THE ARCHITECTURE PANE", command=clear_archpane)  
file1menu.add_command(label="SAVE THE ARCHITECTURE (GUI)", command=savearchitecturefileas)  
file1menu.add_command(label="OPEN AN ARCHITECTURE (GUI)", command=open_architecturefile) 
file1menu.add_command(label="ADD A COMPONENT", command=addcomp)  
file1menu.add_command(label="SPECIFY THE RELATIONSHIP BETWEEN THE MAIN AND SUB-COMPONENTS (GUI)", command=relation_mainsub)  
file1menu.add_command(label="WRITE ARCH. ACTIONS TO FILE", command=show_arch) 
menubar.add_cascade(label="ARCHITECTURE-GUI", menu=file1menu) 

file2menu = Menu(menubar, tearoff=0)
file2menu.add_command(label="?? HOWTO/HELP/README (TEXT MODE) ??", command=lambda:HowToText())
file2menu.add_command(label="LAUNCH TEXT EDITOR TO SPECIFY AN ARCHITECTURE", command=opentexteditor)
file2menu.add_command(label="SAVE THE ARCHITECTURE (TEXT)", command=savetextarchitecturefileas)  
file2menu.add_command(label="OPEN AN ARCHITECTURE (TEXT)", command=open_textarchitecturefile) 
file2menu.add_command(label="SPECIFY THE RELATIONSHIP BETWEEN THE MAIN AND SUB-COMPONENTS (TEXT)", command=relation_mainsubtext)  
menubar.add_cascade(label="ARCHITECTURE-TEXTMODE", menu=file2menu) 

verifymenu = Menu(menubar, tearoff=0)
verifymenu.add_command(label="VERIFY THE CONFORMANCE BETWEEN THE ARCH. AND THE POL. (NO ATTACKER)", command=lambda:VerifyPolicy(set(map(strtoterm,queryFWConsent)), set(map(strtoterm,queryCConsent)), set(map(strtoterm,queryUConsent)), queryHas, createNotHasTerms(entityHasRec), queryHasAfter, queryLink, queryNotLink , queryLinkUnique, queryNotLinkUnique, set(map(strtoterm,querySConsent)), set(map(strtoterm,UniqueData)), set(map(strtoterm,ArchMeta)), set(map(strtoterm,Arch)), set(map(strtoterm,ArchPseudo)), set(map(strtoterm,ArchTime)), 0, CryptoPred, NestEnc))  
verifymenu.add_command(label="VERIFY THE CONFORMANCE BETWEEN THE ARCH. AND THE POL. (EXTERNAL ATTACKERS)", command=lambda:VerifyPolicyEXATT(set(map(strtoterm,queryFWConsent)), set(map(strtoterm,queryCConsent)), set(map(strtoterm,queryUConsent)), queryHas, createNotHasTermsAttEx(listAttExHasData), queryHasAfter, queryLink, queryNotLink , queryLinkUnique, queryNotLinkUnique, set(map(strtoterm,querySConsent)), set(map(strtoterm,UniqueData)), set(map(strtoterm,ArchMeta)), set(map(strtoterm,Arch)), set(map(strtoterm,ArchPseudo)), set(map(strtoterm,ArchTime)), 0, CryptoPred, NestEnc))
verifymenu.add_command(label="VERIFY THE CONFORMANCE BETWEEN THE ARCH. AND THE POL. (INSIDER ATTACKERS)", command=lambda:VerifyPolicyINATT(set(map(strtoterm,queryFWConsent)), set(map(strtoterm,queryCConsent)), set(map(strtoterm,queryUConsent)), queryHas, createNotHasTermsAttEx(listAttExHasData), queryHasAfter, queryLink, queryNotLink , queryLinkUnique, queryNotLinkUnique, set(map(strtoterm,querySConsent)), set(map(strtoterm,UniqueData)), set(map(strtoterm,ArchMeta)), set(map(strtoterm,Arch)), set(map(strtoterm,ArchPseudo)), set(map(strtoterm,ArchTime)), 0, CryptoPred, NestEnc))
verifymenu.add_command(label="VERIFY THE CONFORMANCE BETWEEN THE ARCH. AND THE POL. (HYBRID ATTACKERS)", command=lambda:VerifyPolicyHYBATT(set(map(strtoterm,queryFWConsent)), set(map(strtoterm,queryCConsent)), set(map(strtoterm,queryUConsent)), queryHas, createNotHasTermsAttEx(listAttExHasData), queryHasAfter, queryLink, queryNotLink , queryLinkUnique, queryNotLinkUnique, set(map(strtoterm,querySConsent)), set(map(strtoterm,UniqueData)), set(map(strtoterm,ArchMeta)), set(map(strtoterm,Arch)), set(map(strtoterm,ArchPseudo)), set(map(strtoterm,ArchTime)), 0, CryptoPred, NestEnc))
menubar.add_cascade(label="[[ VERIFY ]]", menu=verifymenu)  

authormenu = Menu(menubar, tearoff=0)
authormenu.add_command(label="Short Manual (Version June 2021).", command=lambda:Manual())
authormenu.add_command(label="DataProVe Version June 2021.")
authormenu.add_command(label="GitHub Page", command=lambda:visitweb("https://github.com/Dataprove/Dataprovetool/"))
menubar.add_cascade(label="ABOUT", menu=authormenu)


root.config(menu=menubar)


frame=Frame(root,width=900,height=800)
frame.pack(expand=True, fill=BOTH) 
canvas=Canvas(frame,width=900, height=800, background="MistyRose") 
hbar=Scrollbar(frame,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas.xview)
vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)
canvas.config(width=900,height=800)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side=LEFT,expand=True,fill=BOTH) 


_drag_data = {"x": 0, "y": 0, "xx":0,"yy":0, "xx2":0, "yy2":0, "item": None}


canvas.bind("<Double-1>", getsetColor)
canvas.tag_bind("token", "<ButtonPress-1>", drag_start)
canvas.tag_bind("token", "<ButtonRelease-1>", drag_stop)
canvas.tag_bind("token", "<B1-Motion>", drag)

canvas.bind("<Button-3>", draw_line) 

canvas.bind("<Button-1>", getshapeonfocus)

root.bind("<space>", deletefocuson)
root.bind("<Up>", moveup)
root.bind("<Left>", moveleft)
root.bind("<Right>", moveright)
root.bind("<Down>", movedown)
canvas.bind("<MouseWheel>",zoomer)

root.bind_all("<MouseWheel>", zoomer)


########################################################################################################################################
########################################################################################################################################
##################################  (GLOBAL) VARIABLES DECLARATION #######################################################################
########################################################################################################################################
########################################################################################################################################

globalidoftexteditor = -1
globalidofbuttontxted = -1
globalidoflabeltxted = -1
globalidoflabeltxted2 = -1

texteditorcontent = ""
relationboxcontent = ""
nameboxcontent = {}  
relationbox = [""]
cpurposesRecArch = {}
setcpurposesRecArch = {} 
upurposesRecArch = {}
setupurposesRecArch = {} 
storeArchRec = {"mainstorage":set(), "backupstorage":set()}  
recvdOwnArgRec = {}          
setRecvdOwnArgRec = {}
recvdStoreArgRec = {}    
setRecvdStoreArgRec = {}
entityRelationRec = {} 
entityRelationListRec = {}

atleastonenotwellformed = 0 
atleastoneerror = 0

 
entityrec = {"att":"attacker","sp":"service provider"}
datagroupoftypes = {"":""}
datatypesrec = {"":"-"}  
datatypesrec1 = {"":"-"} 

entityHasRec = {}
entityHasListRec = {}


cpurposesRecPol = {}
upurposesRecPol = {}
setcpurposesRecPol = {} 
setupurposesRecPol = {} 


collectionpolconsent = {}
usagepolconsent = {}
storepolconsent = {}
fwpolconsent = {}

collectionpolicytosave = {} 
usagepolicytosave = {}
storagepolicytosave = {}
deletionpolicytosave = {}
transferpolicytosave = {}
haspolicytosave = {}
linkpermitpolicytosave = {}
linkforbidpolicytosave = {}

storeoptionrec ={}

storePolRec = {"mainstorage":set(), "backupstorage":set()} 
  
storagemodepol = {}

lastCQuery = {}
lastUQuery = {}
lastSQuery = {}
lastDQuery = {}
lastTQuery = {}
lastHQuery = {}
lastHQueryAttEx ={}
lastLinkPer = {}
lastLinkFor = {}


shapeonfocus = -1  


clicknum = 0 
all_main_comp = []    
all_sub_comp = []
all_lines = []
all_entries = []
all_textboxes = []

info_list_main = []
info_list_sub = []
info_list_lines = []
info_list_box = []

capital= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

VARMAPRECORD = {}   # Variable -> Value mappings set/Unifiers set
VARMAPRECORDCrypto = {}

y = 525600 
w = 10080 
mo = 43200  
d = 1440 
h = 60  
m = 1  

UniqueData = set()
Arch = set()
ArchPseudo = set()
ArchMeta = set()
ArchTime = set()
SetlistofbasicsLink = set()
SetlistofnewLink = set()
SetlistofbasicsHAS = set()
SetlistofbasicsLinkUnique = set()

basicEncRec ={} 
basicEncRecAttEx = {} 
basicEncRecAttIn = {}
basicEncRecAttHyb = {} 

RecofUnionArch = {}
SetlistofbasicsHASATTEX = set() 
SetlistofbasicsLinkATTEX = set() 
SetlistofbasicsHASATTIN = set() 
SetlistofbasicsLinkATTIN = set() 
SetlistofbasicsHASATTHYB = set() 
SetlistofbasicsLinkATTHYB = set() 
SetlistofbasicsLinkATTHYBUnique = set()
SetlistofbasicsLinkATTINUnique = set()
SetlistofbasicsLinkATTEXUnique = set()

Recofactions = {} 

ReclistofbasicsHASAttEx = {}
ReclistofbasicsLinkAttEx = {}
ReclistofbasicsHAS = {}
ReclistofbasicsLink = {} 
ReclistofbasicsLinkUnique = {}
ReclistofbasicsLinkAttExUnique = {}

SetlistofnewHAS = set()
queryCConsent = set()
queryUConsent = set()
querySConsent = set()
queryFWConsent = set()
queryHasAfter = set()

cPurposePolAll = set()
cPurposePol = {}  
cPurposeArch = set()  

uPurposePolAll = set()
uPurposePol = {}  
uPurposeArch = set()  

ReceiveDataE = set()  
CreateDataE = set()  
CalculateDataE = set()  
StoreDataE = set() 

CConsDataE = {}  
UConsDataE = {}  
FwConsDataE = {}  
SConsDataE = {} 

transferThirdRec = {}

msginsidecrypto = set()

query = []  

queryHas = []
queryNotHas = []

queryHasAttEx = []  
queryNotHasAttEx = [] 
listAttExHasData = [] 

queryLink = []
queryLinkUnique = []
queryNotLink = []
queryNotLinkUnique = []


crypthasnotneeded = 1 

NestEnc = 3  #Nested level of crypto functions to be checked.
HasAccessTo = {}  

# Predicates that denotes crypto functions
CryptoPred = ["senc", "mac", "aenc", "hash", "homenc"]    

####################################################################################################################################################
########################################## INFERENCE RULESET USED IN THE VERIFICATION ##############################################################
####################################################################################################################################################

AbilitySetConsent = [InfRule("fwconsentcollected(EE,XX,Third):-receiveat(EE,fwconsent(XX,Third),time(TN)),receiveat(Third,XX,time(TN))"),
             InfRule("fwconsentcollected(EX,XE,Thi):-receiveat(EX,fwconsent(XE,Thi),time(TN)),receiveat(Thi,Anytypeinccrypto(XE),time(TN))"),
             InfRule("cconsentcollected(QQ,S):-receiveat(QQ,cconsent(S,QK),time(TM)),receiveat(QK,S,time(TM))"),  
             InfRule("cconsentcollected(QX,SX):-receiveat(QX,cconsent(SX,QZ),time(TM)),receiveat(QZ,Anytypeinccrypto(SX),time(TM))"),  
             InfRule("uconsentcollected(LX,UX):-receiveat(LX,uconsent(UX,LZ),time(TI)),createat(LZ,UX,time(TI))"),
             InfRule("uconsentcollected(LL,UU):-receiveat(LL,uconsent(UU,LK),time(TI)),createat(LK,Anytypeinccrypto(UU),time(TI))"), 
             InfRule("uconsentcollected(LB,UB):-receiveat(LB,uconsent(UB,BT),time(TA)),calculateat(BT,UB,time(TA))"), 
             InfRule("uconsentcollected(LA,UA):-receiveat(LA,uconsent(UA,LT),time(TA)),calculateat(LT,Anytypeinccrypto(UA),time(TA))"),
             InfRule("strconsentcollected(LS,US):-receiveat(LS,sconsent(US,UJ),time(TS)),storeat(UJ,US,time(TS))"), 
             InfRule("strconsentcollected(LP,UW):-receiveat(LP,sconsent(UW,UT),time(TW)),storeat(UT,Anytypeinccrypto(UW),time(TW))")]  
             
AbilitySetHasUpto = [InfRule("HasUpTo(RR,NN,time(TT)):-store(RR,NN),deletewithin(RR,NN,time(TT))"), 
             InfRule("HasUpTo(RL,NL,time(TL)):-storeat(RL,NL,time(AT)),deletewithin(RL,NL,time(TL))")]

AbilitySetHas = [InfRule("Has(trusted,_anypred(ds,M@)):-Has(trusted,_anypred(M@,p(ds)))"), 
             InfRule("Has(trusted,_anypred(M@,ds)):-Has(trusted,_anypred(M@,p(ds)))")]
             
             
AbilitySetLink = [InfRule("Link(OKN,BZN,JMN):-calculatefrom(OKN,BZN,FRN),calculatefrom(OKN,JMN,FRN)"),
             InfRule("Link(OKM,BZM,JMM):-calculatefromat(OKM,BZM,FRM,time(TLM)),calculatefromat(OKM,JMM,FRM,time(TLM))"),
             InfRule("Link(OKL,BZL,JML):-own(OKL,BZL),own(OKL,JML)"), 
             InfRule("Link(C,V,W):-Has(C,_anypredA(V,Q!,meta(K))),Has(C,_anypredB(W,P!,meta(K)))"),
             InfRule("Link(O,B,J):-Has(O,_anypredC(B,U)),Has(O,_anypredD(J,U))")
             #InfRule("Link(OP,BP,JP):-Has(OP,_anypredE(BP,UP)),Has(OP,_anypredF(JP,Anytypeinccrypto(UP)))"),
             #InfRule("Link(OA,BA,JA):-Has(OA,_anypredG(BA,UK)),Has(OA,_anypredH(Anytypeinccrypto(JA),UK))"),
             #InfRule("Link(OS,BS,JS):-Has(OS,_anypredI(BS,UL)),Has(OS,_anypredJ(Anytypeinccrypto1(JS),Anytypeinccrypto2(UL)))"),
             #InfRule("Link(OD,BD,JD):-Has(OD,_anypredK(BD,UD)),Has(OD,_anypredL(UD,JD))"), 
             #InfRule("Link(OE,BE,JE):-Has(OE,_anypredM(UE,BE)),Has(OE,_anypredN(JE,UE))"), 
             #InfRule("Link(OF,BF,JF):-Has(OF,_anypredQ(UF,BF)),Has(OF,_anypredP(UF,JF))")
             ]

AbilitySetLinkUnique = [InfRule("LinkUnique(OKE,BZE,JME):-calculatefrom(OKE,BZE,FRE),calculatefrom(OKE,JME,FRE)"),
             InfRule("LinkUnique(OKD,BZD,JMD):-calculatefromat(OKD,BZD,FRD,time(TLD)),calculatefromat(OKD,JMD,FRD,time(TLD))"),           
             InfRule("LinkUnique(OKC,BZC,JMC):-calculatefrom(OKC,BZC,FRC),calculatefrom(OKC,JMC,FRC)"), 
             InfRule("LinkUnique(OK,BZ,JM):-own(OK,BZ),own(OK,JM)"), 
             InfRule("LinkUnique(OOA,BOA,JOA):-Has(OOA,_anypreDA(BOA,UOA)),Has(OOA,_anypreDB(JOA,UOA)),Unique(UOA)"), 
             #InfRule("LinkUnique(OOB,BOB,JOB):-Has(OOB,_anypreDC(BOB,UOB)),Has(OOB,_anypreDD(JOB,Anytypeinccrypto(UOB))),Unique(UOB)"),      
             #InfRule("LinkUnique(OOC,BOC,JOC):-Has(OOC,_anypreDE(BOC,UOC)),Has(OOC,_anypreDF(Anytypeinccrypto(JOC),UOC)),Unique(UOC)"),      
             #InfRule("LinkUnique(OOD,BOD,JOD):-Has(OOD,_anypreDG(BOD,UOD)),Has(OOD,_anypreDH(Anytypeinccrypto1(JOD),Anytypeinccrypto2(UOD))),Unique(UOD)"),      
             InfRule("LinkUnique(OOE,BOE,JOE):-Has(OOE,_anypreDI(BOE,UOE)),Has(OOE,_anypreDJ(UOE,JOE)),Unique(UOE)"), 
             InfRule("LinkUnique(OOF,BOF,JOF):-Has(OOF,_anypreDK(UOF,BOF)),Has(OOF,_anypreDL(JOF,UOF)),Unique(UOF)"), 
             InfRule("LinkUnique(OOG,BOG,JOG):-Has(OOG,_anypreDM(UOG,BOG)),Has(OOG,_anypreDN(UOG,JOG)),Unique(UOG)"),
             InfRule("LinkUnique(KKA,BKA,JKA):-Link(KKA,BKA,JKA),Unique(BKA)"),
             InfRule("LinkUnique(KKB,BKB,JKB):-Link(KKB,BKB,JKB),Unique(JKB)")]
             

AbilitySetAttackerHas =  [InfRule("Has(att,GATT):-Has(att,senc(GATT,IATT)),Has(att,IATT)"),
                          InfRule("Has(att,QATT):-Has(att,aenc(QATT,TATT)),Has(att,sk(TATT))")] 

AbilitySetAttackerLink =  [InfRule("Link(att,VATT,WATT):-Has(att,_anypredA(VATT,QATT!,meta(KATT))),Has(att,_anypredB(WATT,PATT!,meta(KATT)))"),
             InfRule("Link(att,BATT,JATT):-Has(att,_anypredC(BATT,UATT)),Has(att,_anypredD(JATT,UATT))"),
             #InfRule("Link(att,BPATT,JPATT):-Has(att,_anypredE(BPATT,UPATT)),Has(att,_anypredF(JPATT,Anytypeinccrypto(UPATT)))"),
             #InfRule("Link(att,BAATT,JAATT):-Has(att,_anypredG(BAATT,UKATT)),Has(att,_anypredH(Anytypeinccrypto(JAATT),UKATT))"),
             #InfRule("Link(att,BSATT,JSATT):-Has(att,_anypredI(BSATT,ULATT)),Has(att,_anypredJ(Anytypeinccrypto1(JSATT),Anytypeinccrypto2(ULATT)))"),
             InfRule("Link(att,BDATT,JDATT):-Has(att,_anypredK(BDATT,UDATT)),Has(att,_anypredL(UDATT,JDATT))"), 
             InfRule("Link(att,BEATT,JEATT):-Has(att,_anypredM(UEATT,BEATT)),Has(att,_anypredN(JEATT,UEATT))"), 
             InfRule("Link(att,BFATT,JFATT):-Has(att,_anypredQ(UFATT,BFATT)),Has(att,_anypredP(UFATT,JFATT))")]

AbilitySetAttackerLinkUnique =  [InfRule("LinkUnique(att,BOAA,JOAA):-Has(att,_anypreDA(BOAA,UOAA)),Has(att,_anypreDB(JOAA,UOAA)),Unique(UOAA)"), 
             #InfRule("LinkUnique(att,BOBA,JOBA):-Has(att,_anypreDC(BOBA,UOBA)),Has(att,_anypreDD(JOBA,Anytypeinccrypto(UOBA))),Unique(UOBA)"),      
             #InfRule("LinkUnique(att,BOCA,JOCA):-Has(att,_anypreDE(BOCA,UOCA)),Has(att,_anypreDF(Anytypeinccrypto(JOCA),UOCA)),Unique(UOCA)"),      
             #InfRule("LinkUnique(att,BODA,JODA):-Has(att,_anypreDG(BODA,UODA)),Has(att,_anypreDH(Anytypeinccrypto1(JODA),Anytypeinccrypto2(UODA))),Unique(UODA)"),      
             InfRule("LinkUnique(att,BOEA,JOEA):-Has(att,_anypreDI(BOEA,UOEA)),Has(att,_anypreDJ(UOEA,JOEA)),Unique(UOEA)"), 
             InfRule("LinkUnique(att,BOFA,JOFA):-Has(att,_anypreDK(UOFA,BOFA)),Has(att,_anypreDL(JOFA,UOFA)),Unique(UOFA)"), 
             InfRule("LinkUnique(att,BOGA,JOGA):-Has(att,_anypreDM(UOGA,BOGA)),Has(att,_anypreDN(UOGA,JOGA)),Unique(UOGA)"),
             InfRule("LinkUnique(att,BKAA,JKAA):-Link(att,BKAA,JKAA),Unique(BKAA)"),
             InfRule("LinkUnique(att,BKBA,JKBA):-Link(att,BKBA,JKBA),Unique(JKBA)")]            


AbilitySetCrypto = [InfRule("Has(Z,Y):-Has(Z,senc(Y,X)),Has(Z,X)"), 
                    InfRule("Has(P,Q):-Has(P,aenc(Q,T)),Has(P,sk(T))")]  


# Predicates that denotes architecture actions
predefinedarchpred = {"store", "storeat", "own", "receive", "receiveat", "create", "createat", "delete", "deletewithin", "calculate", "calculateat", "calculatefrom", "calculatefromat"}



root.mainloop()