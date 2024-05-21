(: 
 Detect suspicious powershell execution
 Author: Antonio Blescia @ CYS4
:)

let $files_path := "./workbench/dataset/HW_ADD_sys.evtx-20231004.ndjson"
for $event in json-file($files_path)
let $args :=["-NoP", "-NonI","-W","-Exec","bypass","iwr"]
where $event.event.code = "1" and contains($event.winlog.event_data.Image, "powershell") and (some $val in $args[] satisfies contains(upper-case($event.winlog.event_data.CommandLine),upper-case($val)))
return {
  "timestamp":$event."@timestamp",
  "p_process_pid": $event.winlog.event_data.ParentProcessId,
  "p_process_name": $event.winlog.event_data.ParentImage,
  "process_pid": $event.winlog.event_data.ProcessId,
  "process_cmdline": $event.winlog.event_data.CommandLine
}