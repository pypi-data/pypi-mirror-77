# flecsimo
Software components of the research/educational model of a cellular 
production site. This development is part of the flecsimo project (flexible 
cellular manufacturing simulation model), initiated at Frankfurt University 
of Applied Sciences and co-funded by DigLL 2020 (https://www.digll-hessen.de/).

## Release notes 0.1.3
This release is a development release. It does not implement all desired 
features and only promises to work, if the user does exactly the right things 
in the right way. With this, it should be considered as a "proof of concept", 
rather than a general usable software.

**THEREFORE**: this version is not intended to be used in real learning 
environments!

### Installation
Use ``pypi install flecsimo`` to install a testable version and all 
required python dependencies. It is recommended to install in a virtualenv.

Additional to the pypi installation, you have to install, configure 
and run a mqtt server to fully operate flecsimo (e.g. Eclipse mosquitto, 
see https://mosquitto.org).

### Testing
After installation (using a virtualenv) you will find the libraries in the 
site-packages directory and the executable python scripts in your script 
directory. Running the scripts requires to set PYTHONPATH or to call the 
scripts as arguments of the python interpreter, e.g. 
``python Scripts\site_control.py``

This version does *not* include the uni-test scripts (as they are not ready 
to use yet). Visit the documentation homepage 
https://confluence.frankfurt-university.de/display/FFP. Information how to run 
a test scenario will be published there soon.

### Closing Remarks:
If You are interested in the concept and want to support us in development, 
design of future use cases, or just providing feedback, please contact the 
maintainers. 

## Why flecsimo?
For detailed information on visit 
https://confluence.frankfurt-university.de/display/FFP

### Problem statement
The current developments in production logistics - generally discussed under 
the terms of digitisation or Industry 4.0 - will have a considerable impact on 
the working and living world of the future. Key elements of this change are 
so-called "cyber-physical systems", i.e. the integration of IT systems into 
physical devices.

The technical complexity of these systems, however, makes access difficult for 
non-technical, especially business management courses of study, although the 
topic is of great relevance to these in particular. Pure software simulations 
of such systems are very complex to realize, didactically difficult to use and 
demonstrate the cyber-physical character of digitization only very abstractly 
and thus often incomplete.

### Planned solution
The project comprises the design and implementation of a hardware simulation 
model with four autonomous workstations (e.g "drilling", "painting", ...) as 
cyber-physical production systems.

The workstations are based on Fischertechnik training models and can be 
positioned anywhere in the four fields of a carrier module . 
This results in the grid of a so-called "flexible cell production", as it is 
forced in practice for Industry 4.0 scenarios. An autonomous, self-propelled 
transportation system handles the material flows between the stations. In 
addition, a high-bay warehouse or existing Fischertechnik Training Model can 
be connected. The plant is equipped with cameras that allow the processes to be 
transmitted to other locations.

Along with the technical solution, the project will offer the required learning 
material.

### Intended users
The flecsimo project is licensed under GPLv3+. We hope that users at 
Universities and educational institutions benefit from our solution, but we 
would also be happy to get support from an open user community to keep on 
development.

## Roadmap
The system will be used first at Frankfurt University in winter term 2020/21. 
It will comprise
* the workstations communication backbone
* the first physical models
* the first version of learning material

Based on the evaluation of winter term, we plan to implement the following 
features on mid- to longterm base:
* improve stability
* improve management of the site (including improved GUIs and a simulation 
cockpit) 
* importer for ERP data (e.g. SAP IDocs)
* collecting readings in time series databases (like kafka)
* gradually implement automatic transportation between workstations and 
warehouse (e. g. an AGV model).
* implement logistics planning algorithms and data analysis  
* ... and everything which we like to do :) 