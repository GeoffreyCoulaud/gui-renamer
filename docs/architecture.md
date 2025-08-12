```mermaid
graph TD;

app["Application"]
window["Main Window"]
controller["Main Window Controller"]
empty["Empty View"]
rename["Renaming View"]
picker["File Picker"]
model["Model"]

controller -- Updates --> model
app -- Instanciates --> controller
app -- Instanciates ---> window
app -- Instanciates --> model
rename & empty -- Signals to --> window
controller -- Instanciates --> picker
picker -- Signals to --> controller
window -- Signals to --> controller
window -- Manages --> rename & empty
controller -- Updates --> window
```