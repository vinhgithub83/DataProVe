# DataProVe
DataProVe: A Data Protection Policy and System Architecture Verification Tool (https://sites.google.com/view/dataprove/)

DataProVe is a tool with GUI written in Python that allows a user to specify a high-level data protection (or privacy) policy and a system architecture, then verify the conformance between the specified architecture and the high-level policy in a fully automated way. 

The main goal of the tool is to help a system designer at the higher level (compared to the other tools that mainly focus on the protocol level.), such as policy and architecture design. This step can be important to spot any potential high-level design flaw before proceeding to the lower level system specification. It can be useful for education purposes as well, especially, where the subject is about personal data protection or privacy.  

The verification engine of DataProVe is based on logic (resolution based proofs), combining both the so-called backward and forward search strategies. 

The tool is available in two formats, .exe and .pyc. You just need to download and double click on them to run the program. 
- .Pyc: If you want to run the .pyc file, then you need to install, ideally, Python version 3.8.2 or 3.8.5 32bit (or above, from https://www.python.org/downloads/). This file can be run by either double click or from command line, e.g., under Windows cmd using the command (assumed that you already added Python to path, see this guide https://geek-university.com/python/add-python-to-the-windows-path/): 

      python "<replace_with_path_to_file>\DataProVe-v0.9.1.pyc" 

Note: Virustotal found DataProVe-v0.9.1.pyc 100% clean by 59 scan engines: https://www.virustotal.com/gui/file/f711941a5e8177e4abbc380ae6f438bc780203ad4e90be67615aa2d89179a0ea/detection)

- .Exe: Just double click on the file to run it. You might be asked in Windows if you really want to run/trust the .exe file (as it is not digitally signed and shown as unknown publisher). The app contains no malicious code, so it's safe to run (56 AV scan engines found it safe, including BitDefender, Kaspersky). 

The template policy (.pol) and architecture (.arch) files can be found in the zip called "Template files used in the manual", just open them in the app and try. 

To watch demo videos about DataProVe, please visit the following site: https://sites.google.com/site/drvinhthongta/dataprove/dataprove-demo-videos

Latest version: DataProVe-v0.9.1.
- Fixed the save and open policy and architecture functionalities in version 0.9.

Manual v0.9.1:
- A pseudonym example added (example 13).

Manual v0.9.1-Oct:
- A new application example (without crypto function) added between pages 33-38. 
