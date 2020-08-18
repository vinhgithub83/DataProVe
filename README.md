# DataProVe
DataProVe: A Data Protection Policy and System Architecture Verification Tool

DataProVe is a tool with GUI written in Python that allows a user to specify a high-level data protection (or privacy) policy and a system architecture, then verify the conformance between the specified architecture and the high-level policy. The main goal of the tool is to help a system designer at the higher level (compared to the other tools that mainly focus on the protocol level.), such as policy and architecture design. This step can be important to spot any potential high-level design flaw before proceeding to the lower level system specification. 

The verification engine of DataProVe is based on logic (resolution based proofs), combining both the so-called backward and forward search strategies. 

The tool is available in two formats, .exe and .pyc. You just need to download and double click on them to run the program. 
- You may be asked in Windows if you really want to run/trust the .exe file, because by default, any .exe extension is suspicous for the Windows. It will offer an option if you want to proceed. 
- If you want to run the .pyc file, then you need ideally Python 3.8.5 (or above, from https://www.python.org/downloads/).  

The template policy (.pol) and architecture (.arch) files can be found in the zip called "Template files used in the manual", just open them in the app and try. 

To watch the demo videos, please visit the following site: https://sites.google.com/site/drvinhthongta/dataprove/dataprove-demo-videos
