(: 
 Detect suspicious PowerShell execution using Script Block Logging
 Author: Antonio Blescia @ NoCommentLab
:)


let $files_path := "./workbench/dataset/PowerShell_Operational.ndjson"
for $event in json-file($files_path)
where $event.Event.System.EventID = 4104
return {
  "EventDateTime": $event.Event.System.TimeCreated."#attributes".SystemTime,
  "EventId": $event.Event.System.EventID,
  "ScriptBlockText": $event.Event.EventData.ScriptBlockText
}

