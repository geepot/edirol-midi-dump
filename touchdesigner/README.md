## Usage

You need Touchdesigner to open this. You can download it over on the developer's website here: https://derivative.ca/

Just go to the Dialogs > MIDI Device Mapper menu and change the In/Out devices to your particular USB MIDI adapter, and enable MIDI Out on your video mixer and you should start getting some output in the Python terminal on the right when you move the t-bar. 

Clear the terminal and run the MIDI Bulk Dump on your mixer and it will output it all nicely in hex in the terminal. This can be pasted in some of the scripts in the scripts directory. 

This is here temporarily until I entirely automate this with Python. In the future this folder will be used for the project responsible for actually controlling all of the discovered parameters via MIDI.