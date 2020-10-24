# DataProVe
DataProVe: A Data Protection Policy and System Architecture Verification Tool (https://sites.google.com/view/dataprove/)

DataProVe is a tool with GUI written in Python that allows a user to specify a high-level data protection (or privacy) policy and a system architecture, then verify the conformance between the specified architecture and the high-level policy in a fully automated way. 

The main goal of the tool is to help a system designer at the higher level (compared to the other tools that mainly focus on the protocol level.), such as policy and architecture design. This step can be important to spot any potential high-level design flaw before proceeding to the lower level system specification. It can be useful for education purposes as well, especially, where the subject is about personal data protection or privacy.  

The verification engine of DataProVe is based on logic (resolution based proofs), combining both the so-called backward and forward search strategies. 

<h2> Downloads: </h2>
The tool is available in two formats, .exe and .pyc. You just need to download and double click on them to run the program. 

- <b> DataProVe-v0.9.1.pyc (Recommended) </b>: If you want to run the .pyc file, then you need to install, <b> Python version 3.8.2 or 3.8.5 32bit/64bit or above </b> (from https://www.python.org/downloads/). If you have an older version of Python (e.g. Python 3.6), the .pyc file still runs, but some functionality might be missing.          
      * This file can be run by either double clicking on the DataProVe-v0.9.1.pyc file, or    
      * from command line, e.g., under Windows cmd using the command (assumed that you already added Python to path, see this guide https://geek-university.com/python/add-python-to-the-windows-path/): 

            python "<replace_with_path_to_file>\DataProVe-v0.9.1.pyc" 

Note: Virustotal found DataProVe-v0.9.1.pyc 100% clean by 59 scan engines: https://www.virustotal.com/gui/file/f711941a5e8177e4abbc380ae6f438bc780203ad4e90be67615aa2d89179a0ea/detection)

- <b> DataProVe-v0.9.1.exe </b>: Just double click on the file to run it. You might be asked in Windows if you really want to run/trust the .exe file (as it is not digitally signed and shown as unknown publisher). The app contains no malicious code, so it's safe to run (56 antivirus scan engines found it safe, including BitDefender, Kaspersky, Sophos AV, McAfee). 

- You can also download the .zip file called <b>DataProVe-v0.9.1-all-in-one.zip</b>  that contains both the .pyc and .exe versions, the user manual, and the example .pol and .arch files used in the manual. 

<h2> Policy and Architecture Files Used in the Manual: </h2>
The template policy (.pol) and architecture (.arch) files can be found in the zip called <i>“Pol and arch files used in the manual v0.9.1.zip”</i>, just open them in the app and try. 

<h2> Demo Videos: </h2>
To watch demo videos about DataProVe, please visit the following site: https://sites.google.com/view/dataprove/demo-videos

<h2> Versions: </h2>
The latest version is: DataProVe-v0.9.1.
- Fixed the save and open policy and architecture functionalities in version 0.9.

<h2> Updates: </h2> 

Manual v0.9.1:
- A pseudonym example added (example 13).

Manual v0.9.1-Oct:
- A new application example (contact tracing app, without crypto function) added between pages 33-38. 

"Template files used in the manual v0.9.1-Oct.zip": 
- Policy and architecture files added for the contact tracing app examples. 

Renamed "Template files used in the manual v0.9.1-Oct.zip" to “Pol and arch files used in the manual v0.9.1.zip”

“Pol and arch files used in the manual v0.9.1.zip”: 
 - Now contains the complete list of policy and architecture files used in the user manual. 
 - The examples got the names referred to in the user manual, so it is easier to find which files correspond to which example in the manual.  
