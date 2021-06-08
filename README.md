# DataProVe
DataProVe: A Data Protection Policy and System Architecture Verification Tool (https://sites.google.com/view/dataprove/)

DataProVe is a tool with GUI written in Python that allows a user to specify a high-level data protection (or privacy) policy and a system architecture, then verify the conformance between the specified architecture and the high-level policy in a fully automated way. 

The main goal of the tool is to help a system designer at the higher level (compared to the other tools that mainly focus on the protocol level.), such as policy and architecture design. This step can be important to spot any potential high-level design flaw before proceeding to the lower level system specification. It can be useful for education purposes as well, especially, where the subject is about personal data protection or privacy.  

The verification engine of DataProVe is based on logic (resolution based proofs), combining both the so-called backward and forward search strategies. 

<h2> Versions: </h2>
The <b>latest version</b> is: <b>DataProVe-v0.9.8</b>.

<h2> Downloads: </h2>
The tool is available in .pcy format. You just need to download and double click on them to run the program. 

- <b> DataProVe-v0.9.8.pyc  </b>: To run the .pyc file you need to install, <b> Python version 3.8.2 or 3.8.5 32bit/64bit or above </b> (from https://www.python.org/downloads/). If you have an older version of Python (e.g. Python 3.6), the .pyc file still runs, but some functionality might be missing.          
      * This file can be run by either double clicking on the DataProVe-v0.9.8.pyc file, or    
      * from command line, e.g., under Windows cmd using the command (assumed that you already added Python to path, see this guide https://geek-university.com/python/add-python-to-the-windows-path/): 

            python "<replace_with_path_to_file>\DataProVe-v0.9.8.pyc" 

MD5 (DataProVe-v0.9.8.pyc) : fcf25e08ce8ff2409edbe217a9552fc4    
(Virustotal found DataProVe-v0.9.8.pyc clean by 58 scan engines: https://www.virustotal.com/gui/file/e232d5cea5540dcdb82928abf89b5ee935a770815fa1ff594f30b00355e6903f/detection)


<h2> Policy and Architecture Files Used in the Manual: </h2>
The template policy (.pol) and architecture (.arch) files can be found in the zip called <i>“Pol and arch files used in the manual v0.9.8.zip”</i>, just open them in the app and try. 

<h2> Demo Videos: </h2>
To watch demo videos about DataProVe, please visit the following site: https://sites.google.com/view/dataprove/demo-videos

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

Version 0.9.2 uploaded: 
 - Fixed the "open a policy" issue (completely delete the previous opened policy when open a new policy) 
 - Improved the verification for the Linkability property (increased the layer of allowed compound datatype)
 
Version 0.9.3 uploaded: 
 - Changed menu items.
 - Added the TEXT MODE specification for architectures. 
 - Changed the GUI features/commands (e.g. 
     - (1) to change color of a component: double click on the left mouse button, 
     - (2) to delete a component, line or textbox use the spacebar on the keyboard, 
     - (3) moving objects with both mouse and keyboard arrows, 
     - (4) textbox can be also dragged with its text area not only at the border.).
 - Exception handling fixed.
 - Updated the template files (“Pol and arch files used in the manual v0.9.3.zip”), with examples for the TEXT MODE. 
 - User Manual v0.9.3 with examples of the TEXT MODE at the end of the document. 
 - “Pol and arch files used in the manual v0.9.3.zip” contains some examples of the TEXT MODE (Examples-TEXTMODE). 
 
 Version 0.9.4 uploaded:
 - Improved verification engine
 - Minor changes in the menubar
 - Minor changes with the content of the warning messages in the verification results window.
 - Tested on real-life contact tracing approaches (a version of DP3T https://github.com/DP-3T/documents, and an example implementation of PEPP-PT https://github.com/pepp-pt/pepp-pt-documentation.) 
   - Video link to the verification: https://www.youtube.com/watch?v=JxI-OzoFuR8 
 - The template .zip contains extra examples in the folder called "Example-TEXTMODE-Link-Enc" with encryption for the TEXT MODE.
 
 Version 0.9.5 uploaded:
 - Improved verification speed using intermediary storage techniques. 
 - Extended the description for purposes in the verification results window. 

Version 0.9.6 uploaded:
 - Actions CALCULATEFROM(component,Datatype1,Datatype2) and CALCULATEFROMAT(component,Datatype1,Datatype2,Time(t)) are added to specify a piece of data can be calculated from another piece of data. 
 - Improve notification text for the verification results.  
 - The TEXTMODE saving also includes the list of relationships between main and sub-components, which will be then loaded in the program when the arch .txt file is opened. 
 - Added more TEXTMODE examples in the "Pol and Arch files used in the manual" (including the example with CALCULATEFROMAT)
 - Improved the user manual, make it more related to the version 0.9.6.

Version 0.9.7 uploaded:
 - Improved and fixed linkability verification for compound data types.  

Version 0.9.8 uploaded:
- The tool now supports any number of layers of nested cryptographic functions/encryption inside a datatype. 
- Added three attacker models: External attackers, insider attackers, hybrid attackers. 
- Improved verification speed. 
